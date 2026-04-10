# FILE: zpkg_core.py
# Zuse Paket-Manager — Kernlogik (Phase 5.4)
# Verwaltet Pakete für die Zuse-Programmiersprache.

import os
import json
import shutil

# ─── Konstanten ──────────────────────────────────────────────────────────

MANIFEST_NAME = "zpkg.json"
PAKETE_DIR = "zpkg_pakete"
REGISTRY_ENV_VAR = "ZPKG_REGISTRY"

PFLICHTFELDER = {"name", "version"}
ALLE_FELDER = {"name", "version", "autor", "beschreibung",
               "abhaengigkeiten", "sprache", "hauptdatei"}


# ─── SemVer ──────────────────────────────────────────────────────────────

import re as _re

def _parse_semver(version_str):
    """Parst eine SemVer-Version in (major, minor, patch) Tupel."""
    m = _re.match(r'^(\d+)\.(\d+)\.(\d+)', str(version_str))
    if not m:
        return (0, 0, 0)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def pruefe_version(version_str, constraint):
    """Prüft ob eine Version einen Constraint erfüllt.

    Unterstützte Constraints:
        ">=1.0.0"    — mindestens 1.0.0
        "<2.0.0"     — kleiner als 2.0.0
        ">=1.0.0,<2.0.0" — Bereich
        "1.0.0"      — exakt 1.0.0
        "*"          — beliebig
    """
    if not constraint or constraint == "*":
        return True
    version = _parse_semver(version_str)
    for teil in constraint.split(","):
        teil = teil.strip()
        if teil.startswith(">="):
            if version < _parse_semver(teil[2:]):
                return False
        elif teil.startswith("<="):
            if version > _parse_semver(teil[2:]):
                return False
        elif teil.startswith(">"):
            if version <= _parse_semver(teil[1:]):
                return False
        elif teil.startswith("<"):
            if version >= _parse_semver(teil[1:]):
                return False
        else:
            if version != _parse_semver(teil):
                return False
    return True


# ─── Fehler ──────────────────────────────────────────────────────────────

class ZpkgError(Exception):
    """Fehler im Zuse-Paketmanager."""
    pass


# ─── Manifest ────────────────────────────────────────────────────────────

def erstelle_manifest(name, version="0.1.0", autor="", beschreibung=""):
    """Erzeugt ein neues Manifest-Dict mit Standardwerten."""
    return {
        "name": name,
        "version": version,
        "autor": autor,
        "beschreibung": beschreibung,
        "abhaengigkeiten": {},
        "sprache": "deutsch",
        "hauptdatei": f"{name}.zuse",
    }


def validiere_manifest(manifest):
    """Prüft ein Manifest auf Vollständigkeit. Gibt Liste von Fehlern zurück."""
    fehler = []
    if not isinstance(manifest, dict):
        return ["Manifest muss ein JSON-Objekt sein."]
    for feld in PFLICHTFELDER:
        if feld not in manifest or not manifest[feld]:
            fehler.append(f"Pflichtfeld '{feld}' fehlt oder ist leer.")
    if "name" in manifest:
        name = manifest["name"]
        if not isinstance(name, str) or not name.replace("_", "").isalnum():
            fehler.append("Paketname darf nur Buchstaben, Zahlen und Unterstriche enthalten.")
    if "version" in manifest:
        v = manifest["version"]
        if not isinstance(v, str):
            fehler.append("Version muss ein String sein (z.B. '1.0.0').")
    if "abhaengigkeiten" in manifest:
        deps = manifest["abhaengigkeiten"]
        if not isinstance(deps, dict):
            fehler.append("'abhaengigkeiten' muss ein Objekt sein.")
    return fehler


def lade_manifest(verzeichnis):
    """Liest zpkg.json aus einem Verzeichnis."""
    pfad = os.path.join(verzeichnis, MANIFEST_NAME)
    if not os.path.exists(pfad):
        raise ZpkgError(f"Keine {MANIFEST_NAME} gefunden in: {verzeichnis}")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        raise ZpkgError(f"Ungültiges JSON in {pfad}: {e}")
    fehler = validiere_manifest(manifest)
    if fehler:
        raise ZpkgError(f"Ungültiges Manifest in {verzeichnis}: {'; '.join(fehler)}")
    return manifest


def speichere_manifest(verzeichnis, manifest):
    """Schreibt ein Manifest als zpkg.json."""
    pfad = os.path.join(verzeichnis, MANIFEST_NAME)
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)


# ─── Initialisierung ────────────────────────────────────────────────────

def initialisiere_paket(verzeichnis, name=None):
    """Erstellt ein neues zpkg.json im angegebenen Verzeichnis."""
    if name is None:
        name = os.path.basename(os.path.abspath(verzeichnis))
        # Sicherstellen, dass der Name gültig ist
        name = name.lower().replace(" ", "_").replace("-", "_")
    pfad = os.path.join(verzeichnis, MANIFEST_NAME)
    if os.path.exists(pfad):
        raise ZpkgError(f"{MANIFEST_NAME} existiert bereits in: {verzeichnis}")
    manifest = erstelle_manifest(name)
    os.makedirs(verzeichnis, exist_ok=True)
    speichere_manifest(verzeichnis, manifest)
    return manifest


# ─── Installation ────────────────────────────────────────────────────────

def _standard_registry():
    """Gibt den Standard-Registry-Pfad zurück."""
    env = os.environ.get(REGISTRY_ENV_VAR)
    if env and os.path.isdir(env):
        return env
    # Fallback: zpkg_registry/ neben diesem Skript
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "zpkg_registry")


def _validiere_paketname(paket_name):
    """Prüft ob ein Paketname sicher ist (keine Pfad-Traversal)."""
    if not isinstance(paket_name, str) or not paket_name:
        raise ZpkgError("Paketname darf nicht leer sein.")
    if '..' in paket_name or '/' in paket_name or '\\' in paket_name:
        raise ZpkgError(f"Ungültiger Paketname: '{paket_name}' (Pfad-Traversal nicht erlaubt)")
    if not paket_name.replace('_', '').replace('-', '').isalnum():
        raise ZpkgError(f"Ungültiger Paketname: '{paket_name}' (nur Buchstaben, Zahlen, _ und - erlaubt)")


def installiere_paket(paket_name, registry_pfad=None, ziel_verzeichnis=".", _kette=None):
    """
    Installiert ein Paket aus der Registry in zpkg_pakete/.

    Returns:
        dict mit Infos über installierte Pakete
    """
    _validiere_paketname(paket_name)

    # Zirkuläre Abhängigkeiten erkennen
    if _kette is None:
        _kette = set()
    if paket_name in _kette:
        raise ZpkgError(
            f"Zirkuläre Abhängigkeit erkannt: {' → '.join(_kette)} → {paket_name}"
        )
    _kette = _kette | {paket_name}

    if registry_pfad is None:
        registry_pfad = _standard_registry()
    if not os.path.isdir(registry_pfad):
        raise ZpkgError(f"Registry-Verzeichnis nicht gefunden: {registry_pfad}")

    quell_pfad = os.path.join(registry_pfad, paket_name)
    if not os.path.isdir(quell_pfad):
        raise ZpkgError(
            f"Paket '{paket_name}' nicht in der Registry gefunden.\n"
            f"  Registry: {registry_pfad}\n"
            f"  Verfügbare Pakete: {_liste_registry(registry_pfad)}"
        )

    manifest = lade_manifest(quell_pfad)
    ziel_pakete = os.path.join(ziel_verzeichnis, PAKETE_DIR)
    ziel_paket = os.path.join(ziel_pakete, paket_name)

    # Kopieren (überschreibt vorhandenes)
    if os.path.exists(ziel_paket):
        shutil.rmtree(ziel_paket)
    os.makedirs(ziel_pakete, exist_ok=True)
    shutil.copytree(quell_pfad, ziel_paket)

    installiert = [{"name": paket_name, "version": manifest.get("version", "?")}]

    # Abhängigkeiten mit Versions-Prüfung installieren
    deps = manifest.get("abhaengigkeiten", {})
    for dep_name, dep_constraint in deps.items():
        dep_ziel = os.path.join(ziel_pakete, dep_name)
        if not os.path.exists(dep_ziel):
            sub = installiere_paket(dep_name, registry_pfad, ziel_verzeichnis, _kette)
            installiert.extend(sub["installiert"])
        else:
            # Version prüfen wenn bereits installiert
            try:
                dep_manifest = lade_manifest(dep_ziel)
                dep_version = dep_manifest.get("version", "0.0.0")
                if dep_constraint and not pruefe_version(dep_version, dep_constraint):
                    raise ZpkgError(
                        f"Version {dep_version} von '{dep_name}' erfüllt nicht "
                        f"Constraint '{dep_constraint}' (benötigt von '{paket_name}')"
                    )
            except ZpkgError as e:
                raise ZpkgError(f"Abhängigkeitsfehler: {e}")

    return {"installiert": installiert}


def _liste_registry(registry_pfad):
    """Listet alle Pakete in einer Registry."""
    if not os.path.isdir(registry_pfad):
        return []
    pakete = []
    for name in sorted(os.listdir(registry_pfad)):
        manifest_pfad = os.path.join(registry_pfad, name, MANIFEST_NAME)
        if os.path.isfile(manifest_pfad):
            pakete.append(name)
    return pakete


# ─── Paket-Liste ─────────────────────────────────────────────────────────

def liste_pakete(verzeichnis="."):
    """Listet alle installierten Pakete in zpkg_pakete/."""
    pakete_dir = os.path.join(verzeichnis, PAKETE_DIR)
    if not os.path.isdir(pakete_dir):
        return []
    ergebnis = []
    for name in sorted(os.listdir(pakete_dir)):
        paket_pfad = os.path.join(pakete_dir, name)
        manifest_pfad = os.path.join(paket_pfad, MANIFEST_NAME)
        if os.path.isfile(manifest_pfad):
            try:
                manifest = lade_manifest(paket_pfad)
                ergebnis.append(manifest)
            except ZpkgError:
                ergebnis.append({"name": name, "version": "?", "beschreibung": "(ungültiges Manifest)"})
    return ergebnis


# ─── Entfernen ───────────────────────────────────────────────────────────

def entferne_paket(paket_name, verzeichnis="."):
    """Entfernt ein installiertes Paket."""
    _validiere_paketname(paket_name)
    paket_pfad = os.path.join(verzeichnis, PAKETE_DIR, paket_name)
    if not os.path.isdir(paket_pfad):
        raise ZpkgError(f"Paket '{paket_name}' ist nicht installiert.")
    shutil.rmtree(paket_pfad)
    return True


# ─── Paket-Auflösung (für Interpreter) ──────────────────────────────────

def finde_paket_pfad(paket_name, start_verzeichnis=None):
    """
    Sucht ein zpkg-Paket und gibt den Pfad zur Hauptdatei zurück.

    Suchreihenfolge:
    1. {start_verzeichnis}/zpkg_pakete/{paket_name}/
    2. {script_dir}/zpkg_pakete/{paket_name}/
    3. None (nicht gefunden)
    """
    such_pfade = []
    if start_verzeichnis:
        such_pfade.append(os.path.join(start_verzeichnis, PAKETE_DIR, paket_name))
    # Auch neben diesem Skript suchen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    such_pfade.append(os.path.join(script_dir, PAKETE_DIR, paket_name))

    for paket_pfad in such_pfade:
        manifest_pfad = os.path.join(paket_pfad, MANIFEST_NAME)
        if os.path.isfile(manifest_pfad):
            try:
                manifest = lade_manifest(paket_pfad)
                hauptdatei = manifest.get("hauptdatei", f"{paket_name}.zuse")
                datei_pfad = os.path.join(paket_pfad, hauptdatei)
                if os.path.isfile(datei_pfad):
                    return datei_pfad
            except ZpkgError:
                pass
    return None
