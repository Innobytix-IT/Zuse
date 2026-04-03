#!/usr/bin/env python3
# FILE: add_language.py
# Hilfsskript zum Hinzufuegen einer neuen Sprache zu Zuse
#
# Benutzung:
#   python add_language.py <sprach_name> <iso_code>
#
# Beispiel:
#   python add_language.py tuerkisch tr
#
# Was es tut:
# 1. Erstellt sprachen/<name>.json mit allen Keywords (als Vorlage)
# 2. Fuegt den ISO-Code zu error_messages.py hinzu (als Vorlage)
# 3. Fuegt den ISO-Code zu error_hints.py hinzu (als Vorlage)
# 4. Registriert die Sprache in error_i18n.py
# 5. Erstellt eine Checkliste was noch uebersetzt werden muss

import os
import sys
import json

ZUSE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ZUSE_DIR)


def main():
    if len(sys.argv) < 3:
        print("Benutzung: python add_language.py <sprach_name> <iso_code>")
        print("Beispiel:  python add_language.py tuerkisch tr")
        print()
        print("Existierende Sprachen:")
        lang_dir = os.path.join(ZUSE_DIR, "sprachen")
        for f in sorted(os.listdir(lang_dir)):
            if f.endswith(".json"):
                print(f"  - {f[:-5]}")
        sys.exit(1)

    name = sys.argv[1].lower()
    iso = sys.argv[2].lower()

    print(f"\n{'='*50}")
    print(f"  Neue Sprache: {name} ({iso})")
    print(f"{'='*50}\n")

    # ─── Schritt 1: Keywords-Datei ────────────────────────────────────
    keywords_path = os.path.join(ZUSE_DIR, "sprachen", f"{name}.json")
    if os.path.exists(keywords_path):
        print(f"[OK] {keywords_path} existiert bereits.")
    else:
        # Deutsch als Vorlage laden
        with open(os.path.join(ZUSE_DIR, "sprachen", "deutsch.json"), "r", encoding="utf-8") as f:
            deutsch = json.load(f)
        # Alle Werte als TODO markieren
        vorlage = {}
        for key, value in deutsch.items():
            vorlage[key] = f"TODO_{value}"
        with open(keywords_path, "w", encoding="utf-8") as f:
            json.dump(vorlage, f, indent=4, ensure_ascii=False)
        print(f"[ERSTELLT] {keywords_path}")
        print(f"           -> {len(vorlage)} Keywords muessen uebersetzt werden")
        print(f"           -> Ersetze alle TODO_* Eintraege mit den {name}-Uebersetzungen")

    # ─── Schritt 2: error_messages.py ─────────────────────────────────
    err_msg_path = os.path.join(ZUSE_DIR, "error_messages.py")
    with open(err_msg_path, "r", encoding="utf-8") as f:
        content = f.read()

    if f'"{iso}"' in content:
        print(f"[OK] error_messages.py enthaelt bereits '{iso}'.")
    else:
        # Fuege nach jeder "pt": Zeile eine neue Zeile ein
        import re
        count = 0
        lines = content.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line)
            # Nach jeder "pt": ... Zeile die neue Sprache einfuegen
            match = re.match(r'^(\s+)"pt":\s*"(.+)",$', line)
            if match:
                indent = match.group(1)
                # Verwende den deutschen Text als Platzhalter
                new_lines.append(f'{indent}"{iso}": "TODO",')
                count += 1
        with open(err_msg_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        print(f"[AKTUALISIERT] error_messages.py")
        print(f"               -> {count} Eintraege mit TODO hinzugefuegt")
        print(f"               -> Ersetze alle \"{iso}\": \"TODO\" mit Uebersetzungen")

    # ─── Schritt 3: error_hints.py ────────────────────────────────────
    hints_path = os.path.join(ZUSE_DIR, "error_hints.py")
    with open(hints_path, "r", encoding="utf-8") as f:
        hints_content = f.read()

    if f'"{iso}"' in hints_content:
        print(f"[OK] error_hints.py enthaelt bereits '{iso}'.")
    else:
        import re
        count = 0
        lines = hints_content.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line)
            match = re.match(r'^(\s+)"pt":\s*"(.+)",$', line)
            if match:
                indent = match.group(1)
                new_lines.append(f'{indent}"{iso}": "TODO",')
                count += 1
        with open(hints_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        print(f"[AKTUALISIERT] error_hints.py")
        print(f"               -> {count} Hint-Eintraege mit TODO hinzugefuegt")

    # ─── Schritt 4: error_i18n.py LANG_MAP ────────────────────────────
    i18n_path = os.path.join(ZUSE_DIR, "error_i18n.py")
    with open(i18n_path, "r", encoding="utf-8") as f:
        i18n_content = f.read()

    if f'"{name}"' in i18n_content:
        print(f"[OK] error_i18n.py enthaelt bereits '{name}'.")
    else:
        # Fuege vor dem schliessenden } von LANG_MAP ein
        i18n_content = i18n_content.replace(
            f'"portugues": "pt",\n}}',
            f'"portugues": "pt",\n    "{name}":   "{iso}",\n}}'
        )
        with open(i18n_path, "w", encoding="utf-8") as f:
            f.write(i18n_content)
        print(f"[AKTUALISIERT] error_i18n.py")
        print(f"               -> '{name}' -> '{iso}' registriert")

    # ─── Schritt 5: builtin_i18n.py LANG_TO_ISO ───────────────────────
    bi18n_path = os.path.join(ZUSE_DIR, "builtin_i18n.py")
    with open(bi18n_path, "r", encoding="utf-8") as f:
        bi18n_content = f.read()

    if f"'{name}'" in bi18n_content:
        print(f"[OK] builtin_i18n.py enthaelt bereits '{name}'.")
    else:
        bi18n_content = bi18n_content.replace(
            f"'portugues': 'pt',\n}}",
            f"'portugues': 'pt',\n    '{name}': '{iso}',\n}}"
        )
        with open(bi18n_path, "w", encoding="utf-8") as f:
            f.write(bi18n_content)
        print(f"[AKTUALISIERT] builtin_i18n.py")
        print(f"               -> '{name}' -> '{iso}' in LANG_TO_ISO registriert")

    # Zaehle wie viele Builtin-Uebersetzungen noch fehlen
    from builtin_i18n import BUILTIN_TRANSLATIONS, METHODEN_TRANSLATIONS
    builtin_todo = sum(1 for b in BUILTIN_TRANSLATIONS.values() if iso not in b)
    methoden_todo = sum(1 for m in METHODEN_TRANSLATIONS.values() if iso not in m)

    # ─── Zusammenfassung ──────────────────────────────────────────────
    from error_messages import MESSAGES
    from error_hints import KEY_HINTS

    print(f"\n{'='*50}")
    print(f"  Checkliste fuer {name} ({iso})")
    print(f"{'='*50}")
    print(f"""
  [ ] sprachen/{name}.json
      -> {len(json.load(open(os.path.join(ZUSE_DIR, 'sprachen', 'deutsch.json'))))} Keywords uebersetzen
      -> Ersetze alle TODO_* Eintraege

  [ ] error_messages.py
      -> {len(MESSAGES)} Fehlermeldungen uebersetzen
      -> Suche nach: "{iso}": "TODO"

  [ ] error_hints.py
      -> {len(KEY_HINTS)} Tipps uebersetzen
      -> Suche nach: "{iso}": "TODO"

  [ ] builtin_i18n.py
      -> {builtin_todo} Builtin-Funktionen uebersetzen (BUILTIN_TRANSLATIONS)
      -> {methoden_todo} Methoden-Aliase uebersetzen (METHODEN_TRANSLATIONS)
      -> Fuer jedes Dict: '{iso}': 'UEBERSETZUNG' hinzufuegen

  [ ] Testen:
      python -c "
      from error_i18n import set_language, t
      set_language('{name}')
      print(t('ERR_VAR_NOT_DEFINED', line=1, name='x'))
      "

  Tipp: Nutze 'Suchen & Ersetzen' in deinem Editor
        um alle TODO-Eintraege zu finden!
""")


if __name__ == "__main__":
    main()
