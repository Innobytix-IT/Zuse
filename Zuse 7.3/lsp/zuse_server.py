# FILE: lsp/zuse_server.py
# Zuse Language Server (LSP) — Phase 5.2
# Bietet: Diagnosen, Autovervollständigung, Hover-Info
# Starten: python -m lsp.zuse_server [--port PORT]

import sys
import os
import re

# Zuse-Module importierbar machen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lsprotocol import types as lsp
from pygls.lsp.server import LanguageServer

from lexer import tokenize
from parser import Parser
from language_loader import lade_sprache
from semantic_analyzer import SemanticAnalyzer, BUILTINS

# ─── Server-Instanz ──────────────────────────────────────────────────────

server = LanguageServer("zuse-language-server", "v1.0.0")

# ─── Sprach-Erkennung ────────────────────────────────────────────────────

def _detect_language(text):
    """Erkennt die Sprache anhand von Keywords im Code."""
    markers = {
        'deutsch':   ['AUSGABE', 'DEFINIERE', 'WENN', 'SOLANGE', 'FUR', 'ENDE'],
        'english':   ['PRINT', 'DEFINE', 'IF', 'WHILE', 'FOR', 'END'],
        'espaniol':  ['MOSTRAR', 'DEFINIR', 'SI', 'MIENTRAS', 'PARA', 'FIN'],
        'francais':  ['AFFICHER', 'DEFINIR', 'SI', 'TANT_QUE', 'POUR', 'FIN'],
        'italiano':  ['MOSTRA', 'DEFINISCI', 'SE', 'MENTRE', 'PER', 'FINE'],
        'portugues': ['MOSTRAR', 'DEFINIR', 'SE', 'ENQUANTO', 'PARA', 'FIM'],
    }
    scores = {lang: 0 for lang in markers}
    words = set(re.findall(r'[A-Z_]{2,}', text))
    for lang, kws in markers.items():
        for kw in kws:
            if kw in words:
                scores[lang] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'deutsch'


# ─── Diagnosen ───────────────────────────────────────────────────────────

def _analyze_document(text):
    """Lexer + Parser + Semantik ausfuehren, Diagnosen sammeln."""
    diagnostics = []
    lang = _detect_language(text)

    try:
        config = lade_sprache(lang)
        tokens = tokenize(text, config)
    except RuntimeError as e:
        msg = str(e)
        line = _extract_line(msg)
        diagnostics.append(lsp.Diagnostic(
            range=lsp.Range(
                start=lsp.Position(line=max(0, line - 1), character=0),
                end=lsp.Position(line=max(0, line - 1), character=100),
            ),
            message=msg,
            severity=lsp.DiagnosticSeverity.Error,
            source="zuse-lexer",
        ))
        return diagnostics

    try:
        ast = Parser(tokens).parse()
    except RuntimeError as e:
        msg = str(e)
        line = _extract_line(msg)
        diagnostics.append(lsp.Diagnostic(
            range=lsp.Range(
                start=lsp.Position(line=max(0, line - 1), character=0),
                end=lsp.Position(line=max(0, line - 1), character=100),
            ),
            message=msg,
            severity=lsp.DiagnosticSeverity.Error,
            source="zuse-parser",
        ))
        return diagnostics

    # Semantische Analyse
    try:
        analyzer = SemanticAnalyzer()
        errors, warnings = analyzer.analyze(ast)

        for err in errors:
            line = err.zeile if isinstance(err.zeile, int) else 1
            diagnostics.append(lsp.Diagnostic(
                range=lsp.Range(
                    start=lsp.Position(line=max(0, line - 1), character=0),
                    end=lsp.Position(line=max(0, line - 1), character=100),
                ),
                message=err.nachricht,
                severity=lsp.DiagnosticSeverity.Error,
                source="zuse-semantik",
            ))

        for warn in warnings:
            line = warn.zeile if isinstance(warn.zeile, int) else 1
            diagnostics.append(lsp.Diagnostic(
                range=lsp.Range(
                    start=lsp.Position(line=max(0, line - 1), character=0),
                    end=lsp.Position(line=max(0, line - 1), character=100),
                ),
                message=warn.nachricht,
                severity=lsp.DiagnosticSeverity.Warning,
                source="zuse-semantik",
            ))
    except Exception:
        pass  # Semantik-Fehler nicht kritisch

    return diagnostics


def _extract_line(msg):
    """Extrahiert die Zeilennummer aus einer Fehlermeldung."""
    m = re.search(r'[Zz]eile\s+(\d+)', msg)
    if m:
        return int(m.group(1))
    m = re.search(r'[Ll]ine\s+(\d+)', msg)
    if m:
        return int(m.group(1))
    return 1


# ─── Autovervollständigung ──────────────────────────────────────────────

# Deutsche Keywords und Builtins
_KEYWORDS = [
    'AUSGABE', 'DEFINIERE', 'ENDE FUNKTION', 'ERGEBNIS IST',
    'WENN', 'DANN', 'SONST', 'SONST WENN', 'ENDE WENN',
    'SOLANGE', 'MACHE', 'ENDE SOLANGE',
    'FUR', 'IN', 'ENDE FUR',
    'KLASSE', 'ENDE KLASSE', 'MEIN',
    'VERSUCHE', 'FANGE', 'ENDE VERSUCHE',
    'ABBRUCH', 'WEITER',
    'BENUTZE', 'ALS',
    'AKTION',
    'wahr', 'falsch',
]

_BUILTIN_DOCS = {
    # Mathe
    'PI': ('Konstante', 'Die Kreiszahl Pi (3.14159...)'),
    'E': ('Konstante', 'Die Eulersche Zahl e (2.71828...)'),
    'WURZEL': ('Funktion', 'WURZEL(x) — Quadratwurzel von x'),
    'SINUS': ('Funktion', 'SINUS(x) — Sinus von x (Bogenmass)'),
    'COSINUS': ('Funktion', 'COSINUS(x) — Cosinus von x (Bogenmass)'),
    'TANGENS': ('Funktion', 'TANGENS(x) — Tangens von x (Bogenmass)'),
    'RUNDEN': ('Funktion', 'RUNDEN(x, stellen=0) — Rundet x auf n Stellen'),
    'ABSOLUT': ('Funktion', 'ABSOLUT(x) — Absolutwert von x'),
    'POTENZ': ('Funktion', 'POTENZ(x, y) — x hoch y'),
    'LOGARITHMUS': ('Funktion', 'LOGARITHMUS(x, basis=e) — Logarithmus von x'),
    'MINIMUM': ('Funktion', 'MINIMUM(a, b, ...) — Kleinster Wert'),
    'MAXIMUM': ('Funktion', 'MAXIMUM(a, b, ...) — Groesster Wert'),
    'SUMME': ('Funktion', 'SUMME(liste) — Summe aller Elemente'),
    'BODEN': ('Funktion', 'BODEN(x) — Abrunden auf Ganzzahl'),
    'DECKE': ('Funktion', 'DECKE(x) — Aufrunden auf Ganzzahl'),
    'ZUFALL': ('Funktion', 'ZUFALL() — Zufallszahl zwischen 0 und 1'),
    'ZUFALL_BEREICH': ('Funktion', 'ZUFALL_BEREICH(min, max) — Ganzzahl zwischen min und max'),
    # Text
    'GROSSBUCHSTABEN': ('Funktion', 'GROSSBUCHSTABEN(text) — Text in Grossbuchstaben'),
    'KLEINBUCHSTABEN': ('Funktion', 'KLEINBUCHSTABEN(text) — Text in Kleinbuchstaben'),
    'ERSETZE': ('Funktion', 'ERSETZE(text, alt, neu) — Ersetzt alt durch neu'),
    'TEILE': ('Funktion', 'TEILE(text, trenner) — Teilt Text an Trenner'),
    'TRIMME': ('Funktion', 'TRIMME(text) — Entfernt Leerzeichen am Rand'),
    'ENTHAELT': ('Funktion', 'ENTHAELT(text, teil) — Prueft ob teil in text'),
    'LAENGE': ('Funktion', 'LAENGE(x) — Laenge von String oder Liste'),
    'FINDE': ('Funktion', 'FINDE(text, teil) — Position von teil in text (-1 wenn nicht gefunden)'),
    'BEGINNT_MIT': ('Funktion', 'BEGINNT_MIT(text, praefix) — Prueft Anfang'),
    'ENDET_MIT': ('Funktion', 'ENDET_MIT(text, suffix) — Prueft Ende'),
    'VERBINDE': ('Funktion', 'VERBINDE(liste, trenner="") — Verbindet Liste zu String'),
    # Listen
    'SORTIEREN': ('Funktion', 'SORTIEREN(liste) — Sortierte Kopie der Liste'),
    'FILTERN': ('Funktion', 'FILTERN(liste, funktion) — Filtert Elemente'),
    'UMWANDELN': ('Funktion', 'UMWANDELN(liste, funktion) — Wandelt jedes Element um'),
    'UMKEHREN': ('Funktion', 'UMKEHREN(liste) — Umgekehrte Kopie der Liste'),
    'FLACH': ('Funktion', 'FLACH(liste) — Verschachtelte Liste flach machen'),
    'EINDEUTIG': ('Funktion', 'EINDEUTIG(liste) — Nur einzigartige Elemente'),
    'AUFZAEHLEN': ('Funktion', 'AUFZAEHLEN(liste) — Liste mit (Index, Wert) Paaren'),
    'ANHAENGEN': ('Funktion', 'ANHAENGEN(liste, element, ...) — Neue Liste mit angehaengten Elementen'),
    # Datei
    'LESE_DATEI': ('Funktion', 'LESE_DATEI(pfad) — Liest eine Datei als Text'),
    'SCHREIBE_DATEI': ('Funktion', 'SCHREIBE_DATEI(pfad, inhalt) — Schreibt Text in Datei'),
    'EXISTIERT': ('Funktion', 'EXISTIERT(pfad) — Prueft ob Datei existiert'),
    'LESE_ZEILEN': ('Funktion', 'LESE_ZEILEN(pfad) — Liest Datei als Liste von Zeilen'),
    # Standard
    'BEREICH': ('Funktion', 'BEREICH(ende) / BEREICH(start, ende, schritt) — Zahlenbereich'),
    'FORMAT': ('Funktion', 'FORMAT(vorlage, wert1, ...) — String-Formatierung mit {}'),
    'str': ('Funktion', 'str(x) — Konvertiert x zu Text'),
    'int': ('Funktion', 'int(x) — Konvertiert x zu Ganzzahl'),
    'float': ('Funktion', 'float(x) — Konvertiert x zu Dezimalzahl'),
    'len': ('Funktion', 'len(x) — Laenge von x'),
    'typ': ('Funktion', 'typ(x) — Typ von x als Text'),
    'Spielfeld': ('Klasse', 'Spielfeld(titel, breite, hoehe, farbe) — Spielfeld fuer Spiele'),
    # Typ-Prüfung
    'IST_ZAHL': ('Funktion', 'IST_ZAHL(x) — Prueft ob x eine Zahl ist'),
    'IST_TEXT': ('Funktion', 'IST_TEXT(x) — Prueft ob x ein Text ist'),
    'IST_LISTE': ('Funktion', 'IST_LISTE(x) — Prueft ob x eine Liste ist'),
    'IST_DICT': ('Funktion', 'IST_DICT(x) — Prueft ob x ein Woerterbuch ist'),
    'IST_BOOL': ('Funktion', 'IST_BOOL(x) — Prueft ob x ein Wahrheitswert ist'),
    'IST_NICHTS': ('Funktion', 'IST_NICHTS(x) — Prueft ob x Nichts ist'),
    'ALS_ZAHL': ('Funktion', 'ALS_ZAHL(x) — Konvertiert x zu einer Zahl'),
    'ALS_TEXT': ('Funktion', 'ALS_TEXT(x) — Konvertiert x zu Text'),
    'ALLE': ('Funktion', 'ALLE(liste) — Prueft ob alle Elemente wahr sind'),
    'IRGENDEIN': ('Funktion', 'IRGENDEIN(liste) — Prueft ob mindestens ein Element wahr ist'),
    'ZEICHENCODE': ('Funktion', 'ZEICHENCODE(zeichen) — Unicode-Codepunkt eines Zeichens'),
    'ZEICHEN': ('Funktion', 'ZEICHEN(code) — Zeichen aus Unicode-Codepunkt'),
    'HEX': ('Funktion', 'HEX(zahl) — Hexadezimale Darstellung'),
    'BIN': ('Funktion', 'BIN(zahl) — Binaere Darstellung'),
    'OKT': ('Funktion', 'OKT(zahl) — Oktale Darstellung'),
    'KOMBINIEREN': ('Funktion', 'KOMBINIEREN(liste1, liste2, ...) — Kombiniert Listen zu Paaren'),
    'BEREICH_LISTE': ('Funktion', 'BEREICH_LISTE(n) — Liste von 0 bis n-1'),
    'ERGAENZE_DATEI': ('Funktion', 'ERGAENZE_DATEI(pfad, inhalt) — Haengt Text an Datei an'),
    'LOESCHE_DATEI': ('Funktion', 'LOESCHE_DATEI(pfad) — Loescht eine Datei'),
}


# ─── LSP-Handler ─────────────────────────────────────────────────────────

@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: lsp.DidOpenTextDocumentParams):
    text = params.text_document.text
    uri = params.text_document.uri
    diagnostics = _analyze_document(text)
    server.publish_diagnostics(uri, diagnostics)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: lsp.DidChangeTextDocumentParams):
    uri = params.text_document.uri
    doc = server.workspace.get_text_document(uri)
    diagnostics = _analyze_document(doc.source)
    server.publish_diagnostics(uri, diagnostics)


@server.feature(lsp.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: lsp.DidSaveTextDocumentParams):
    uri = params.text_document.uri
    doc = server.workspace.get_text_document(uri)
    diagnostics = _analyze_document(doc.source)
    server.publish_diagnostics(uri, diagnostics)


@server.feature(lsp.TEXT_DOCUMENT_COMPLETION)
def completions(params: lsp.CompletionParams):
    items = []

    # Keywords
    for kw in _KEYWORDS:
        items.append(lsp.CompletionItem(
            label=kw,
            kind=lsp.CompletionItemKind.Keyword,
            detail="Schluesselwort",
        ))

    # Builtins mit Dokumentation
    for name, (typ, doc) in _BUILTIN_DOCS.items():
        kind = (lsp.CompletionItemKind.Constant if typ == 'Konstante'
                else lsp.CompletionItemKind.Class if typ == 'Klasse'
                else lsp.CompletionItemKind.Function)
        items.append(lsp.CompletionItem(
            label=name,
            kind=kind,
            detail=typ,
            documentation=doc,
        ))

    return lsp.CompletionList(is_incomplete=False, items=items)


@server.feature(lsp.TEXT_DOCUMENT_HOVER)
def hover(params: lsp.HoverParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    lines = doc.source.split('\n')
    if params.position.line >= len(lines):
        return None
    line = lines[params.position.line]
    col = params.position.character

    # Wort unter dem Cursor finden
    word = _word_at(line, col)
    if not word:
        return None

    # In Builtins nachschauen
    if word in _BUILTIN_DOCS:
        typ, doc = _BUILTIN_DOCS[word]
        return lsp.Hover(
            contents=lsp.MarkupContent(
                kind=lsp.MarkupKind.Markdown,
                value=f"**{word}** ({typ})\n\n{doc}",
            )
        )

    # Keywords
    if word in _KEYWORDS:
        return lsp.Hover(
            contents=lsp.MarkupContent(
                kind=lsp.MarkupKind.Markdown,
                value=f"**{word}** — Zuse Schluesselwort",
            )
        )

    return None


@server.feature(lsp.TEXT_DOCUMENT_DEFINITION)
def goto_definition(params: lsp.DefinitionParams):
    """Springt zur Definition einer Funktion oder Klasse."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    lines = doc.source.split('\n')
    if params.position.line >= len(lines):
        return None
    line = lines[params.position.line]
    col = params.position.character
    word = _word_at(line, col)
    if not word:
        return None

    # Suche DEFINIERE name( oder KLASSE name im Dokument
    patterns = [
        re.compile(rf'\bDEFINIERE\s+{re.escape(word)}\s*\('),
        re.compile(rf'\bDEFINE\s+{re.escape(word)}\s*\('),
        re.compile(rf'\bKLASSE\s+{re.escape(word)}\b'),
        re.compile(rf'\bCLASS\s+{re.escape(word)}\b'),
        re.compile(rf'^{re.escape(word)}\s*='),
    ]
    for i, l in enumerate(lines):
        for pat in patterns:
            if pat.search(l):
                return lsp.Location(
                    uri=params.text_document.uri,
                    range=lsp.Range(
                        start=lsp.Position(line=i, character=0),
                        end=lsp.Position(line=i, character=len(l)),
                    ),
                )
    return None


def _word_at(line, col):
    """Extrahiert das Wort an Position col in der Zeile."""
    if col >= len(line):
        col = max(0, len(line) - 1)
    if not line:
        return None

    # Wortgrenzen finden
    start = col
    while start > 0 and (line[start - 1].isalnum() or line[start - 1] == '_'):
        start -= 1
    end = col
    while end < len(line) and (line[end].isalnum() or line[end] == '_'):
        end += 1

    word = line[start:end]
    return word if word else None


# ─── Hauptprogramm ───────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Zuse Language Server")
    parser.add_argument("--tcp", action="store_true", help="TCP statt stdio")
    parser.add_argument("--port", type=int, default=2087, help="TCP-Port (default: 2087)")
    args = parser.parse_args()

    if args.tcp:
        server.start_tcp("127.0.0.1", args.port)
    else:
        server.start_io()


if __name__ == "__main__":
    main()
