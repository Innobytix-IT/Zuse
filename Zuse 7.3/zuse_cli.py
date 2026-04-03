# FILE: zuse_cli.py
# Zuse CLI — Einheitlicher Einstiegspunkt für alle Zuse-Werkzeuge
# Benutzung: zuse <befehl> [optionen]

import sys
import os
import io
import argparse

# Zuse-Verzeichnis zum Pfad hinzufügen
ZUSE_DIR = os.path.dirname(os.path.abspath(__file__))
if ZUSE_DIR not in sys.path:
    sys.path.insert(0, ZUSE_DIR)

# Windows-Konsole auf UTF-8
if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


VERSION = "7.1.0"

BANNER = f"""
  ╔═══════════════════════════════════════╗
  ║   ZUSE v{VERSION}                       ║
  ║   Die mehrsprachige Programmiersprache ║
  ╚═══════════════════════════════════════╝
"""


# ─── Befehle ─────────────────────────────────────────────────────────────

def cmd_run(args):
    """Zuse-Programm ausführen."""
    from language_loader import lade_sprache
    from lexer import tokenize
    from parser import Parser
    from interpreter import Interpreter
    from error_i18n import set_language

    datei = args.datei
    sprache = args.sprache
    set_language(sprache)

    if not os.path.exists(datei):
        print(f"Fehler: Datei '{datei}' nicht gefunden.")
        sys.exit(1)

    with open(datei, 'r', encoding='utf-8') as f:
        user_code = f.read()

    # Bibliothek laden
    final_code = user_code
    lib_path = os.path.join(ZUSE_DIR, "bibliothek", f"{sprache}.zuse")
    if os.path.exists(lib_path):
        try:
            with open(lib_path, 'r', encoding='utf-8') as f:
                lib_code = f.read()
            final_code = lib_code + "\n\n" + user_code
        except Exception as e:
            print(f"Warnung: Bibliothek konnte nicht geladen werden: {e}")

    try:
        config = lade_sprache(sprache)
        tokens = tokenize(final_code, config)
        ast = Parser(tokens).parse()
        interp = Interpreter(output_callback=print, sprache=sprache)
        interp.working_dir = os.path.dirname(os.path.abspath(datei))
        interp.interpretiere(ast)
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)


def cmd_studio(args):
    """Zuse Studio (grafische IDE) starten."""
    try:
        import zuse_studio
        zuse_studio.main() if hasattr(zuse_studio, 'main') else zuse_studio.ZuseStudio()
    except ImportError:
        print("Fehler: tkinter ist nicht installiert.")
        sys.exit(1)
    except Exception as e:
        print(f"Fehler beim Start des Studios: {e}")
        sys.exit(1)


def cmd_transpile(args):
    """Zuse-Code in eine andere Sprache transpilieren."""
    from transpiler import transpile_file, BACKENDS

    datei = args.datei
    ziel = args.ziel
    output = args.output

    if ziel not in BACKENDS:
        print(f"Fehler: Unbekanntes Ziel '{ziel}'.")
        print(f"Verfuegbar: {', '.join(BACKENDS.keys())}")
        sys.exit(1)

    try:
        out = transpile_file(datei, target_backend=ziel,
                            source_lang=args.sprache, output_path=output)
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)


def cmd_debug(args):
    """Zuse-Programm im Debugger starten."""
    from zuse_debug import ZuseDebugCLI

    datei = args.datei
    sprache = args.sprache

    cli = ZuseDebugCLI(datei, sprache)
    cli.run()


def cmd_zpkg(args):
    """Paket-Manager aufrufen."""
    # Argumente an zpkg.py weiterleiten
    import zpkg
    sys.argv = ['zpkg'] + args.zpkg_args
    zpkg.main()


def cmd_check(args):
    """Zuse-Code prüfen (Syntax + Semantik)."""
    from language_loader import lade_sprache
    from lexer import tokenize
    from parser import Parser
    from semantic_analyzer import SemanticAnalyzer
    from error_i18n import set_language

    datei = args.datei
    sprache = args.sprache
    set_language(sprache)

    if not os.path.exists(datei):
        print(f"Fehler: Datei '{datei}' nicht gefunden.")
        sys.exit(1)

    with open(datei, 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        config = lade_sprache(sprache)
        tokens = tokenize(code, config)
        ast = Parser(tokens).parse()
        print(f"Syntax OK: {datei}")
    except Exception as e:
        print(f"Syntaxfehler: {e}")
        sys.exit(1)

    try:
        analyzer = SemanticAnalyzer()
        errors, warnings = analyzer.analyze(ast)
        for w in warnings:
            print(f"  Warnung (Zeile {w.zeile}): {w.nachricht}")
        for e in errors:
            print(f"  Fehler (Zeile {e.zeile}): {e.nachricht}")
        if not errors and not warnings:
            print("Semantik OK: Keine Probleme gefunden.")
        elif errors:
            sys.exit(1)
    except Exception as e:
        print(f"Analyse-Fehler: {e}")
        sys.exit(1)


def cmd_version(args):
    """Versionsinformation anzeigen."""
    print(f"Zuse v{VERSION}")
    print(f"Python {sys.version}")
    print(f"Plattform: {sys.platform}")


# ─── Hauptprogramm ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="zuse",
        description="Zuse — Die mehrsprachige Programmiersprache",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  zuse run mein_programm.zuse              Programm ausfuehren
  zuse run mein_programm.zuse --sprache english
  zuse transpile mein_programm.zuse --ziel javascript
  zuse debug mein_programm.zuse            Im Debugger starten
  zuse check mein_programm.zuse            Syntax + Semantik pruefen
  zuse studio                              Grafische IDE starten
  zuse zpkg install mathe_extra            Paket installieren
        """,
    )
    subparsers = parser.add_subparsers(dest="befehl", help="Verfuegbare Befehle")

    # run
    p_run = subparsers.add_parser("run", help="Zuse-Programm ausfuehren")
    p_run.add_argument("datei", help="Pfad zur .zuse Datei")
    p_run.add_argument("--sprache", "-s", default="deutsch",
                       help="Quellsprache (default: deutsch)")

    # studio
    subparsers.add_parser("studio", help="Grafische IDE starten")

    # transpile
    p_trans = subparsers.add_parser("transpile", help="Code transpilieren")
    p_trans.add_argument("datei", help="Pfad zur .zuse Datei")
    p_trans.add_argument("--ziel", "-z", default="python",
                        help="Zielsprache: python, javascript, java, csharp, wasm")
    p_trans.add_argument("--sprache", "-s", default="deutsch",
                        help="Quellsprache (default: deutsch)")
    p_trans.add_argument("--output", "-o", default=None,
                        help="Ausgabedatei (optional)")

    # debug
    p_debug = subparsers.add_parser("debug", help="Im Debugger starten")
    p_debug.add_argument("datei", help="Pfad zur .zuse Datei")
    p_debug.add_argument("--sprache", "-s", default="deutsch",
                        help="Quellsprache (default: deutsch)")

    # check
    p_check = subparsers.add_parser("check", help="Syntax + Semantik pruefen")
    p_check.add_argument("datei", help="Pfad zur .zuse Datei")
    p_check.add_argument("--sprache", "-s", default="deutsch",
                        help="Quellsprache (default: deutsch)")

    # zpkg
    p_zpkg = subparsers.add_parser("zpkg", help="Paket-Manager")
    p_zpkg.add_argument("zpkg_args", nargs=argparse.REMAINDER,
                       help="Argumente fuer zpkg")

    # version
    subparsers.add_parser("version", help="Version anzeigen")

    args = parser.parse_args()

    if not args.befehl:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    befehle = {
        "run": cmd_run,
        "studio": cmd_studio,
        "transpile": cmd_transpile,
        "debug": cmd_debug,
        "check": cmd_check,
        "zpkg": cmd_zpkg,
        "version": cmd_version,
    }
    befehle[args.befehl](args)


if __name__ == "__main__":
    main()
