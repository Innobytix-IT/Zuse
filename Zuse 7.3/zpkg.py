# FILE: zpkg.py
# Zuse Paket-Manager — CLI-Werkzeug (Phase 5.4)
# Benutzung: python zpkg.py <befehl> [optionen]

import sys
import os
import io
import argparse

# Windows-Konsole auf UTF-8 umstellen
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zpkg_core import (
    initialisiere_paket, installiere_paket, liste_pakete,
    entferne_paket, lade_manifest, _liste_registry, _standard_registry,
    ZpkgError, MANIFEST_NAME
)


def cmd_init(args):
    """Neues Paket initialisieren."""
    try:
        manifest = initialisiere_paket(".", args.name)
        print(f"✅ Paket '{manifest['name']}' initialisiert!")
        print(f"   {MANIFEST_NAME} erstellt.")
        print(f"   Erstelle jetzt eine Datei: {manifest['hauptdatei']}")
    except ZpkgError as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)


def cmd_install(args):
    """Paket installieren."""
    try:
        registry = args.registry or _standard_registry()
        print(f"📦 Installiere '{args.paketname}'...")
        ergebnis = installiere_paket(args.paketname, registry, ".")
        for pkg in ergebnis["installiert"]:
            print(f"   ✅ {pkg['name']} v{pkg['version']}")
        print(f"\n{len(ergebnis['installiert'])} Paket(e) installiert.")
    except ZpkgError as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)


def cmd_list(args):
    """Installierte Pakete anzeigen."""
    pakete = liste_pakete(".")
    if not pakete:
        print("Keine Pakete installiert.")
        print("Tipp: python zpkg.py install <paketname>")
        return
    print(f"{'Name':<20} {'Version':<10} {'Beschreibung'}")
    print("─" * 60)
    for p in pakete:
        name = p.get("name", "?")
        version = p.get("version", "?")
        beschr = p.get("beschreibung", "")
        print(f"{name:<20} {version:<10} {beschr}")
    print(f"\n{len(pakete)} Paket(e) installiert.")


def cmd_info(args):
    """Paket-Details anzeigen."""
    paket_pfad = os.path.join("zpkg_pakete", args.paketname)
    if not os.path.isdir(paket_pfad):
        print(f"❌ Paket '{args.paketname}' ist nicht installiert.")
        sys.exit(1)
    try:
        manifest = lade_manifest(paket_pfad)
        print(f"📦 {manifest['name']} v{manifest.get('version', '?')}")
        if manifest.get("autor"):
            print(f"   Autor: {manifest['autor']}")
        if manifest.get("beschreibung"):
            print(f"   {manifest['beschreibung']}")
        if manifest.get("sprache"):
            print(f"   Sprache: {manifest['sprache']}")
        if manifest.get("hauptdatei"):
            print(f"   Hauptdatei: {manifest['hauptdatei']}")
        deps = manifest.get("abhaengigkeiten", {})
        if deps:
            print(f"   Abhängigkeiten: {', '.join(deps.keys())}")
    except ZpkgError as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)


def cmd_entfernen(args):
    """Paket entfernen."""
    try:
        entferne_paket(args.paketname, ".")
        print(f"✅ Paket '{args.paketname}' entfernt.")
    except ZpkgError as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)


def cmd_registry(args):
    """Verfügbare Pakete in der Registry anzeigen."""
    registry = args.registry or _standard_registry()
    if not os.path.isdir(registry):
        print(f"❌ Registry nicht gefunden: {registry}")
        sys.exit(1)
    pakete = _liste_registry(registry)
    if not pakete:
        print("Keine Pakete in der Registry.")
        return
    print(f"Registry: {registry}")
    print(f"{'Name':<20} {'Version':<10} {'Beschreibung'}")
    print("─" * 60)
    for name in pakete:
        try:
            manifest = lade_manifest(os.path.join(registry, name))
            version = manifest.get("version", "?")
            beschr = manifest.get("beschreibung", "")
            print(f"{name:<20} {version:<10} {beschr}")
        except ZpkgError:
            print(f"{name:<20} {'?':<10} (ungültiges Manifest)")
    print(f"\n{len(pakete)} Paket(e) verfügbar.")


def main():
    parser = argparse.ArgumentParser(
        prog="zpkg",
        description="Zuse Paket-Manager — Pakete für die Zuse-Programmiersprache verwalten",
    )
    subparsers = parser.add_subparsers(dest="befehl", help="Verfügbare Befehle")

    # init
    p_init = subparsers.add_parser("init", help="Neues Paket initialisieren")
    p_init.add_argument("name", nargs="?", default=None, help="Paketname (optional)")

    # install
    p_install = subparsers.add_parser("install", help="Paket installieren")
    p_install.add_argument("paketname", help="Name des zu installierenden Pakets")
    p_install.add_argument("--registry", default=None, help="Pfad zur Registry")

    # list
    subparsers.add_parser("list", help="Installierte Pakete anzeigen")

    # info
    p_info = subparsers.add_parser("info", help="Paket-Details anzeigen")
    p_info.add_argument("paketname", help="Name des Pakets")

    # entfernen
    p_entf = subparsers.add_parser("entfernen", help="Paket entfernen")
    p_entf.add_argument("paketname", help="Name des zu entfernenden Pakets")

    # registry
    p_reg = subparsers.add_parser("registry", help="Verfügbare Pakete anzeigen")
    p_reg.add_argument("--registry", default=None, help="Pfad zur Registry")

    args = parser.parse_args()

    if not args.befehl:
        parser.print_help()
        sys.exit(0)

    befehle = {
        "init": cmd_init,
        "install": cmd_install,
        "list": cmd_list,
        "info": cmd_info,
        "entfernen": cmd_entfernen,
        "registry": cmd_registry,
    }
    befehle[args.befehl](args)


if __name__ == "__main__":
    main()
