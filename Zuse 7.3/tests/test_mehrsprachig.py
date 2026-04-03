# FILE: tests/test_mehrsprachig.py
# Gleiches Programm in 6 Sprachen → gleiches Ergebnis
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from conftest import zuse_ausfuehren

# ─── Alle 6 Sprachen mit ihren Keywords ──────────────────────

SPRACHEN = {
    "deutsch": {
        "AUSGABE": "AUSGABE", "WENN": "WENN", "DANN": "DANN", "SONST": "SONST",
        "ENDE_WENN": "ENDE WENN", "SCHLEIFE_FUER": "SCHLEIFE FÜR",
        "IN": "IN", "MACHE": "MACHE", "ENDE_SCHLEIFE": "ENDE SCHLEIFE",
        "SCHLEIFE_SOLANGE": "SCHLEIFE SOLANGE",
        "DEFINIERE": "DEFINIERE", "ENDE_FUNKTION": "ENDE FUNKTION",
        "ERGEBNIS": "ERGEBNIS IST", "KLASSE": "KLASSE", "ENDE_KLASSE": "ENDE KLASSE",
        "ERSTELLE": "ERSTELLE", "SELBST": "MEIN",
        "WAHR": "wahr", "FALSCH": "falsch",
        "VERSUCHE": "VERSUCHE", "FANGE": "FANGE", "ENDE_VERSUCHE": "ENDE VERSUCHE",
    },
    "english": {
        "AUSGABE": "PRINT", "WENN": "IF", "DANN": "THEN", "SONST": "ELSE",
        "ENDE_WENN": "END IF", "SCHLEIFE_FUER": "LOOP FOR",
        "IN": "IN", "MACHE": "DO", "ENDE_SCHLEIFE": "END LOOP",
        "SCHLEIFE_SOLANGE": "LOOP WHILE",
        "DEFINIERE": "DEFINE", "ENDE_FUNKTION": "END FUNCTION",
        "ERGEBNIS": "RETURN", "KLASSE": "CLASS", "ENDE_KLASSE": "END CLASS",
        "ERSTELLE": "NEW", "SELBST": "SELF",
        "WAHR": "true", "FALSCH": "false",
        "VERSUCHE": "TRY", "FANGE": "CATCH", "ENDE_VERSUCHE": "END TRY",
    },
    "espaniol": {
        "AUSGABE": "IMPRIMIR", "WENN": "SI", "DANN": "ENTONCES", "SONST": "SINO",
        "ENDE_WENN": "FIN SI", "SCHLEIFE_FUER": "BUCLE PARA",
        "IN": "EN", "MACHE": "HACER", "ENDE_SCHLEIFE": "FIN BUCLE",
        "SCHLEIFE_SOLANGE": "BUCLE MIENTRAS",
        "DEFINIERE": "DEFINIR", "ENDE_FUNKTION": "FIN FUNCION",
        "ERGEBNIS": "RETORNO", "KLASSE": "CLASE", "ENDE_KLASSE": "FIN CLASE",
        "ERSTELLE": "CREAR", "SELBST": "MIO",
        "WAHR": "verdadero", "FALSCH": "falso",
        "VERSUCHE": "INTENTAR", "FANGE": "CAPTURAR", "ENDE_VERSUCHE": "FIN INTENTAR",
    },
    "francais": {
        "AUSGABE": "IMPRIMER", "WENN": "SI", "DANN": "ALORS", "SONST": "SINON",
        "ENDE_WENN": "FIN SI", "SCHLEIFE_FUER": "BOUCLE POUR",
        "IN": "DANS", "MACHE": "FAIRE", "ENDE_SCHLEIFE": "FIN BOUCLE",
        "SCHLEIFE_SOLANGE": "BOUCLE TANTQUE",
        "DEFINIERE": "DEFINIR", "ENDE_FUNKTION": "FIN FONCTION",
        "ERGEBNIS": "RETOURNER", "KLASSE": "CLASSE", "ENDE_KLASSE": "FIN CLASSE",
        "ERSTELLE": "CREER", "SELBST": "MOI",
        "WAHR": "vrai", "FALSCH": "faux",
        "VERSUCHE": "ESSAYER", "FANGE": "ATTRAPER", "ENDE_VERSUCHE": "FIN ESSAYER",
    },
    "italiano": {
        "AUSGABE": "STAMPA", "WENN": "SE", "DANN": "ALLORA", "SONST": "ALTRIMENTI",
        "ENDE_WENN": "FINE SE", "SCHLEIFE_FUER": "CICLO PER",
        "IN": "IN", "MACHE": "FARE", "ENDE_SCHLEIFE": "FINE CICLO",
        "SCHLEIFE_SOLANGE": "CICLO MENTRE",
        "DEFINIERE": "DEFINIRE", "ENDE_FUNKTION": "FINE FUNZIONE",
        "ERGEBNIS": "RITORNA", "KLASSE": "CLASSE", "ENDE_KLASSE": "FINE CLASSE",
        "ERSTELLE": "CREARE", "SELBST": "MIO",
        "WAHR": "vero", "FALSCH": "falso",
        "VERSUCHE": "PROVA", "FANGE": "CATTURA", "ENDE_VERSUCHE": "FINE PROVA",
    },
    "portugues": {
        "AUSGABE": "IMPRIMIR", "WENN": "SE", "DANN": "ENTAO", "SONST": "SENAO",
        "ENDE_WENN": "FIM SE", "SCHLEIFE_FUER": "CICLO PARA",
        "IN": "EM", "MACHE": "FACA", "ENDE_SCHLEIFE": "FIM CICLO",
        "SCHLEIFE_SOLANGE": "CICLO ENQUANTO",
        "DEFINIERE": "DEFINIR", "ENDE_FUNKTION": "FIM FUNCAO",
        "ERGEBNIS": "RETORNO", "KLASSE": "CLASSE", "ENDE_KLASSE": "FIM CLASSE",
        "ERSTELLE": "CRIAR", "SELBST": "MEU",
        "WAHR": "verdadeiro", "FALSCH": "falso",
        "VERSUCHE": "TENTAR", "FANGE": "PEGAR", "ENDE_VERSUCHE": "FIM TENTAR",
    },
}


def code(sprache, template):
    """Ersetzt Platzhalter im Template durch die Keywords der Sprache."""
    kw = SPRACHEN[sprache]
    result = template
    # Laengere Keys zuerst ersetzen, damit z.B. ENDE_WENN vor WENN ersetzt wird
    for key in sorted(kw.keys(), key=len, reverse=True):
        result = result.replace(f"{{{key}}}", kw[key])
    return result


def ausfuehren_alle_sprachen(template, erwartete_ausgabe):
    """Fuehrt das Template in allen 6 Sprachen aus und prueft Ergebnis."""
    for sprache in SPRACHEN:
        programm = code(sprache, template)
        ergebnis = zuse_ausfuehren(programm, sprache=sprache)
        assert ergebnis == erwartete_ausgabe, (
            f"Sprache '{sprache}' liefert {ergebnis}, erwartet {erwartete_ausgabe}\n"
            f"Code: {programm}"
        )


# ─── Tests ────────────────────────────────────────────────────

class TestMehrsprachigAusgabe:
    """Einfache Ausgaben in allen 6 Sprachen."""

    def test_hallo_welt(self):
        template = '{AUSGABE} "Hallo"'
        ausfuehren_alle_sprachen(template, ["Hallo"])

    def test_zahl_ausgabe(self):
        template = "{AUSGABE} 42"
        ausfuehren_alle_sprachen(template, ["42"])

    def test_rechnung(self):
        template = "{AUSGABE} 10 + 5"
        ausfuehren_alle_sprachen(template, ["15"])

    def test_string_verkettung(self):
        template = '{AUSGABE} "A" + "B"'
        ausfuehren_alle_sprachen(template, ["AB"])


class TestMehrsprachigVariablen:
    """Variablen und Zuweisungen in allen 6 Sprachen."""

    def test_variable_zahl(self):
        template = 'x = 99\n{AUSGABE} x'
        ausfuehren_alle_sprachen(template, ["99"])

    def test_variable_string(self):
        template = 'name = "Zuse"\n{AUSGABE} name'
        ausfuehren_alle_sprachen(template, ["Zuse"])

    def test_variable_rechnung(self):
        template = 'a = 10\nb = 20\n{AUSGABE} a + b'
        ausfuehren_alle_sprachen(template, ["30"])


class TestMehrsprachigBedingungen:
    """WENN/DANN/SONST in allen 6 Sprachen."""

    def test_wenn_wahr(self):
        template = (
            "x = 10\n"
            "{WENN} x > 5 {DANN}\n"
            '    {AUSGABE} "ja"\n'
            "{ENDE_WENN}"
        )
        ausfuehren_alle_sprachen(template, ["ja"])

    def test_wenn_falsch_mit_sonst(self):
        template = (
            "x = 3\n"
            "{WENN} x > 5 {DANN}\n"
            '    {AUSGABE} "gross"\n'
            "{SONST}\n"
            '    {AUSGABE} "klein"\n'
            "{ENDE_WENN}"
        )
        ausfuehren_alle_sprachen(template, ["klein"])


class TestMehrsprachigSchleifen:
    """Schleifen in allen 6 Sprachen."""

    def test_fuer_schleife(self):
        template = (
            "{SCHLEIFE_FUER} i {IN} [1, 2, 3] {MACHE}\n"
            "    {AUSGABE} i\n"
            "{ENDE_SCHLEIFE}"
        )
        ausfuehren_alle_sprachen(template, ["1", "2", "3"])

    def test_solange_schleife(self):
        template = (
            "x = 0\n"
            "{SCHLEIFE_SOLANGE} x < 3 {MACHE}\n"
            "    x = x + 1\n"
            "{ENDE_SCHLEIFE}\n"
            "{AUSGABE} x"
        )
        ausfuehren_alle_sprachen(template, ["3"])


class TestMehrsprachigFunktionen:
    """Funktionen in allen 6 Sprachen."""

    def test_funktion_ohne_return(self):
        template = (
            "{DEFINIERE} hallo():\n"
            '    {AUSGABE} "hi"\n'
            "{ENDE_FUNKTION}\n"
            "hallo()"
        )
        ausfuehren_alle_sprachen(template, ["hi"])

    def test_funktion_mit_return(self):
        template = (
            "{DEFINIERE} doppelt(x):\n"
            "    {ERGEBNIS} x * 2\n"
            "{ENDE_FUNKTION}\n"
            "{AUSGABE} doppelt(21)"
        )
        ausfuehren_alle_sprachen(template, ["42"])

    def test_funktion_mit_parameter(self):
        template = (
            "{DEFINIERE} addiere(a, b):\n"
            "    {ERGEBNIS} a + b\n"
            "{ENDE_FUNKTION}\n"
            "{AUSGABE} addiere(3, 7)"
        )
        ausfuehren_alle_sprachen(template, ["10"])


class TestMehrsprachigKlassen:
    """Klassen und OOP in allen 6 Sprachen."""

    def test_klasse_mit_konstruktor(self):
        template = (
            "{KLASSE} Tier:\n"
            "    {DEFINIERE} {ERSTELLE}(name):\n"
            "        {SELBST}.name = name\n"
            "    {ENDE_FUNKTION}\n"
            "    {DEFINIERE} ruf():\n"
            "        {AUSGABE} {SELBST}.name\n"
            "    {ENDE_FUNKTION}\n"
            "{ENDE_KLASSE}\n"
            "t = Tier(\"Rex\")\n"
            "t.ruf()"
        )
        ausfuehren_alle_sprachen(template, ["Rex"])


class TestMehrsprachigBooleans:
    """Boolesche Werte in allen 6 Sprachen."""

    def test_wahr(self):
        template = (
            "x = {WAHR}\n"
            "{WENN} x {DANN}\n"
            '    {AUSGABE} "ok"\n'
            "{ENDE_WENN}"
        )
        ausfuehren_alle_sprachen(template, ["ok"])

    def test_falsch(self):
        template = (
            "x = {FALSCH}\n"
            "{WENN} x {DANN}\n"
            '    {AUSGABE} "ja"\n'
            "{SONST}\n"
            '    {AUSGABE} "nein"\n'
            "{ENDE_WENN}"
        )
        ausfuehren_alle_sprachen(template, ["nein"])


class TestMehrsprachigFehlerbehandlung:
    """Try/Catch in allen 6 Sprachen."""

    def test_versuche_fange(self):
        template = (
            "{VERSUCHE}\n"
            "    x = 10 / 0\n"
            "{FANGE}\n"
            '    {AUSGABE} "fehler"\n'
            "{ENDE_VERSUCHE}"
        )
        ausfuehren_alle_sprachen(template, ["fehler"])


class TestMehrsprachigKomplex:
    """Komplexere Programme die mehrere Features kombinieren."""

    def test_fibonacci_schleife(self):
        """Fibonacci-Berechnung mit Schleife - alle Sprachen."""
        template = (
            "a = 0\n"
            "b = 1\n"
            "{SCHLEIFE_FUER} i {IN} [1, 2, 3, 4, 5] {MACHE}\n"
            "    temp = b\n"
            "    b = a + b\n"
            "    a = temp\n"
            "{ENDE_SCHLEIFE}\n"
            "{AUSGABE} b"
        )
        ausfuehren_alle_sprachen(template, ["8"])

    def test_funktion_in_schleife(self):
        """Funktion wird in Schleife aufgerufen."""
        template = (
            "{DEFINIERE} quadrat(x):\n"
            "    {ERGEBNIS} x * x\n"
            "{ENDE_FUNKTION}\n"
            "{SCHLEIFE_FUER} i {IN} [2, 3, 4] {MACHE}\n"
            "    {AUSGABE} quadrat(i)\n"
            "{ENDE_SCHLEIFE}"
        )
        ausfuehren_alle_sprachen(template, ["4", "9", "16"])

    def test_verschachtelte_bedingungen(self):
        """Verschachtelte WENN-Bloecke."""
        template = (
            "x = 15\n"
            "{WENN} x > 10 {DANN}\n"
            "    {WENN} x > 20 {DANN}\n"
            '        {AUSGABE} "sehr gross"\n'
            "    {SONST}\n"
            '        {AUSGABE} "mittel"\n'
            "    {ENDE_WENN}\n"
            "{SONST}\n"
            '    {AUSGABE} "klein"\n'
            "{ENDE_WENN}"
        )
        ausfuehren_alle_sprachen(template, ["mittel"])
