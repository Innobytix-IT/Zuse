# FILE: tests/test_zpkg.py
# Tests für den Zuse Paket-Manager zpkg (Phase 5.4)

import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from zpkg_core import (
    erstelle_manifest, validiere_manifest, lade_manifest, speichere_manifest,
    initialisiere_paket, installiere_paket, liste_pakete, entferne_paket,
    finde_paket_pfad, ZpkgError, MANIFEST_NAME, PAKETE_DIR
)

ZUSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_DIR = os.path.join(ZUSE_DIR, "zpkg_registry")


# ─── Hilfsfunktionen ────────────────────────────────────────────────────

def _erstelle_test_paket(tmp_path, name, version="1.0.0", deps=None, code=None):
    """Erstellt ein Test-Paket in einem temporären Verzeichnis."""
    paket_dir = tmp_path / name
    paket_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": name,
        "version": version,
        "autor": "Test",
        "beschreibung": f"Test-Paket {name}",
        "abhaengigkeiten": deps or {},
        "sprache": "deutsch",
        "hauptdatei": f"{name}.zuse",
    }
    (paket_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=4), encoding="utf-8")
    zuse_code = code or f'DEFINIERE hallo():\n    AUSGABE "{name} funktioniert!"\nENDE FUNKTION\n'
    (paket_dir / f"{name}.zuse").write_text(zuse_code, encoding="utf-8")
    return str(paket_dir)


# ─── Manifest ────────────────────────────────────────────────────────────

class TestManifest:
    def test_erstelle_manifest(self):
        m = erstelle_manifest("test_paket")
        assert m["name"] == "test_paket"
        assert m["version"] == "0.1.0"
        assert m["hauptdatei"] == "test_paket.zuse"
        assert m["abhaengigkeiten"] == {}

    def test_erstelle_manifest_custom(self):
        m = erstelle_manifest("mein_tool", version="2.0.0", autor="Max", beschreibung="Ein Tool")
        assert m["version"] == "2.0.0"
        assert m["autor"] == "Max"
        assert m["beschreibung"] == "Ein Tool"

    def test_validiere_manifest_gueltig(self):
        m = erstelle_manifest("test")
        fehler = validiere_manifest(m)
        assert fehler == []

    def test_validiere_manifest_name_fehlt(self):
        fehler = validiere_manifest({"version": "1.0.0"})
        assert any("name" in f for f in fehler)

    def test_validiere_manifest_version_fehlt(self):
        fehler = validiere_manifest({"name": "test"})
        assert any("version" in f for f in fehler)

    def test_validiere_manifest_kein_dict(self):
        fehler = validiere_manifest("nicht ein dict")
        assert len(fehler) > 0

    def test_validiere_manifest_ungueltiger_name(self):
        fehler = validiere_manifest({"name": "test paket!", "version": "1.0.0"})
        assert any("Paketname" in f for f in fehler)

    def test_lade_manifest(self, tmp_path):
        _erstelle_test_paket(tmp_path, "mein_paket")
        m = lade_manifest(str(tmp_path / "mein_paket"))
        assert m["name"] == "mein_paket"
        assert m["version"] == "1.0.0"

    def test_lade_manifest_nicht_gefunden(self, tmp_path):
        with pytest.raises(ZpkgError, match="Keine zpkg.json"):
            lade_manifest(str(tmp_path / "gibts_nicht"))

    def test_speichere_und_lade(self, tmp_path):
        m = erstelle_manifest("round_trip")
        speichere_manifest(str(tmp_path), m)
        geladen = lade_manifest(str(tmp_path))
        assert geladen["name"] == "round_trip"


# ─── Initialisierung ────────────────────────────────────────────────────

class TestInitialisierung:
    def test_init_erstellt_manifest(self, tmp_path):
        ziel = str(tmp_path / "neues_projekt")
        m = initialisiere_paket(ziel, "mein_projekt")
        assert m["name"] == "mein_projekt"
        assert os.path.isfile(os.path.join(ziel, MANIFEST_NAME))

    def test_init_ohne_name(self, tmp_path):
        ziel = str(tmp_path / "auto_name")
        os.makedirs(ziel)
        m = initialisiere_paket(ziel)
        assert m["name"] == "auto_name"

    def test_init_existiert_bereits(self, tmp_path):
        ziel = str(tmp_path / "doppelt")
        initialisiere_paket(ziel, "test")
        with pytest.raises(ZpkgError, match="existiert bereits"):
            initialisiere_paket(ziel, "test")


# ─── Installation ────────────────────────────────────────────────────────

class TestInstallation:
    def test_installiere_einfaches_paket(self, tmp_path):
        # Registry erstellen
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, "hallo_welt")
        # Ziel-Verzeichnis
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        ergebnis = installiere_paket("hallo_welt", str(registry), str(projekt))
        assert len(ergebnis["installiert"]) == 1
        assert ergebnis["installiert"][0]["name"] == "hallo_welt"
        # Paket wurde kopiert
        assert os.path.isdir(str(projekt / PAKETE_DIR / "hallo_welt"))

    def test_installiere_mit_abhaengigkeiten(self, tmp_path):
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, "basis")
        _erstelle_test_paket(registry, "erweitert", deps={"basis": "1.0.0"})
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        ergebnis = installiere_paket("erweitert", str(registry), str(projekt))
        namen = [p["name"] for p in ergebnis["installiert"]]
        assert "erweitert" in namen
        assert "basis" in namen

    def test_installiere_paket_nicht_gefunden(self, tmp_path):
        registry = tmp_path / "registry"
        registry.mkdir()
        with pytest.raises(ZpkgError, match="nicht in der Registry"):
            installiere_paket("gibts_nicht", str(registry), str(tmp_path))

    def test_installiere_ungueltige_registry(self, tmp_path):
        with pytest.raises(ZpkgError, match="Registry-Verzeichnis nicht gefunden"):
            installiere_paket("test", str(tmp_path / "nope"), str(tmp_path))

    def test_installiere_ueberschreibt(self, tmp_path):
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, "paket_a", version="1.0.0")
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        installiere_paket("paket_a", str(registry), str(projekt))
        # Version ändern und neu installieren
        _erstelle_test_paket(registry, "paket_a", version="2.0.0")
        installiere_paket("paket_a", str(registry), str(projekt))
        m = lade_manifest(str(projekt / PAKETE_DIR / "paket_a"))
        assert m["version"] == "2.0.0"


# ─── Paket-Liste ─────────────────────────────────────────────────────────

class TestListe:
    def test_liste_leer(self, tmp_path):
        pakete = liste_pakete(str(tmp_path))
        assert pakete == []

    def test_liste_mit_paketen(self, tmp_path):
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, "paket_a")
        _erstelle_test_paket(registry, "paket_b")
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        installiere_paket("paket_a", str(registry), str(projekt))
        installiere_paket("paket_b", str(registry), str(projekt))
        pakete = liste_pakete(str(projekt))
        namen = [p["name"] for p in pakete]
        assert "paket_a" in namen
        assert "paket_b" in namen


# ─── Entfernen ───────────────────────────────────────────────────────────

class TestEntfernen:
    def test_entferne_paket(self, tmp_path):
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, "weg_damit")
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        installiere_paket("weg_damit", str(registry), str(projekt))
        assert entferne_paket("weg_damit", str(projekt)) is True
        assert not os.path.exists(str(projekt / PAKETE_DIR / "weg_damit"))

    def test_entferne_nicht_installiert(self, tmp_path):
        with pytest.raises(ZpkgError, match="nicht installiert"):
            entferne_paket("gibts_nicht", str(tmp_path))


# ─── Paket-Auflösung ────────────────────────────────────────────────────

class TestPaketAufloesung:
    def test_finde_installiertes_paket(self, tmp_path):
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, "finder_test")
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        installiere_paket("finder_test", str(registry), str(projekt))
        pfad = finde_paket_pfad("finder_test", str(projekt))
        assert pfad is not None
        assert pfad.endswith("finder_test.zuse")

    def test_finde_nicht_vorhandenes_paket(self, tmp_path):
        pfad = finde_paket_pfad("gibts_nicht", str(tmp_path))
        assert pfad is None

    def test_finde_aus_standard_registry(self):
        """Prüft, ob Pakete aus der mitgelieferten Registry gefunden werden."""
        # Installiere mathe_extra ins zpkg_pakete neben dem Skript
        import zpkg_core
        script_dir = os.path.dirname(os.path.abspath(zpkg_core.__file__))
        pakete_dir = os.path.join(script_dir, PAKETE_DIR, "mathe_extra")
        try:
            installiere_paket("mathe_extra", REGISTRY_DIR, script_dir)
            pfad = finde_paket_pfad("mathe_extra")
            assert pfad is not None
            assert "mathe_extra.zuse" in pfad
        finally:
            # Aufräumen
            if os.path.exists(pakete_dir):
                shutil.rmtree(pakete_dir)
            # Leeres zpkg_pakete entfernen falls leer
            parent = os.path.dirname(pakete_dir)
            if os.path.isdir(parent) and not os.listdir(parent):
                os.rmdir(parent)


# ─── CLI ─────────────────────────────────────────────────────────────────

class TestCLI:
    def test_zpkg_help(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(ZUSE_DIR, "zpkg.py"), "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "zpkg" in result.stdout.lower() or "Paket" in result.stdout

    def test_zpkg_init(self, tmp_path):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(ZUSE_DIR, "zpkg.py"), "init", "testpaket"],
            capture_output=True, text=True, cwd=str(tmp_path)
        )
        assert result.returncode == 0
        assert os.path.isfile(str(tmp_path / MANIFEST_NAME))

    def test_zpkg_list_leer(self, tmp_path):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(ZUSE_DIR, "zpkg.py"), "list"],
            capture_output=True, text=True, cwd=str(tmp_path)
        )
        assert result.returncode == 0
        assert "Keine Pakete" in result.stdout

    def test_zpkg_registry(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(ZUSE_DIR, "zpkg.py"), "registry"],
            capture_output=True, text=True, cwd=ZUSE_DIR
        )
        assert result.returncode == 0
        assert "mathe_extra" in result.stdout
        assert "text_werkzeuge" in result.stdout


# ─── Interpreter-Integration ────────────────────────────────────────────

class TestInterpreterIntegration:
    def _setup_paket(self, tmp_path, name, code):
        """Installiert ein Test-Paket und gibt das Projektverzeichnis zurück."""
        registry = tmp_path / "registry"
        _erstelle_test_paket(registry, name, code=code)
        projekt = tmp_path / "projekt"
        projekt.mkdir()
        installiere_paket(name, str(registry), str(projekt))
        return str(projekt)

    def test_benutze_zpkg_paket(self, tmp_path):
        from conftest import zuse_ausfuehren
        from interpreter import Interpreter
        from language_loader import lade_sprache
        from lexer import tokenize
        from parser import Parser

        code_paket = 'DEFINIERE gruss():\n    AUSGABE "Hallo von Paket"\nENDE FUNKTION\n'
        projekt = self._setup_paket(tmp_path, "gruss_paket", code_paket)

        zuse_code = 'BENUTZE gruss_paket\ngruss_paket.gruss()'
        config = lade_sprache("deutsch")
        tokens = tokenize(zuse_code, config)
        ast = Parser(tokens).parse()

        ausgaben = []
        interp = Interpreter(output_callback=lambda t: ausgaben.append(str(t)))
        interp.working_dir = projekt
        interp.interpretiere(ast)
        assert "Hallo von Paket" in ausgaben

    def test_benutze_zpkg_mit_alias(self, tmp_path):
        from interpreter import Interpreter
        from language_loader import lade_sprache
        from lexer import tokenize
        from parser import Parser

        code_paket = 'DEFINIERE wert():\n    ERGEBNIS IST 42\nENDE FUNKTION\n'
        projekt = self._setup_paket(tmp_path, "antwort", code_paket)

        zuse_code = 'BENUTZE antwort ALS a\nAUSGABE a.wert()'
        config = lade_sprache("deutsch")
        tokens = tokenize(zuse_code, config)
        ast = Parser(tokens).parse()

        ausgaben = []
        interp = Interpreter(output_callback=lambda t: ausgaben.append(str(t)))
        interp.working_dir = projekt
        interp.interpretiere(ast)
        assert "42" in ausgaben

    def test_benutze_zpkg_funktion_mit_parameter(self, tmp_path):
        from interpreter import Interpreter
        from language_loader import lade_sprache
        from lexer import tokenize
        from parser import Parser

        code_paket = 'DEFINIERE verdopple(x):\n    ERGEBNIS IST x * 2\nENDE FUNKTION\n'
        projekt = self._setup_paket(tmp_path, "rechner", code_paket)

        zuse_code = 'BENUTZE rechner\nAUSGABE rechner.verdopple(21)'
        config = lade_sprache("deutsch")
        tokens = tokenize(zuse_code, config)
        ast = Parser(tokens).parse()

        ausgaben = []
        interp = Interpreter(output_callback=lambda t: ausgaben.append(str(t)))
        interp.working_dir = projekt
        interp.interpretiere(ast)
        assert "42" in ausgaben

    def test_benutze_example_registry_paket(self, tmp_path):
        """Testet Import des mitgelieferten mathe_extra Pakets."""
        from interpreter import Interpreter
        from language_loader import lade_sprache
        from lexer import tokenize
        from parser import Parser

        # mathe_extra aus der Registry installieren
        projekt = str(tmp_path / "projekt")
        os.makedirs(projekt)
        installiere_paket("mathe_extra", REGISTRY_DIR, projekt)

        zuse_code = 'BENUTZE mathe_extra\nAUSGABE mathe_extra.fibonacci(10)'
        config = lade_sprache("deutsch")
        tokens = tokenize(zuse_code, config)
        ast = Parser(tokens).parse()

        ausgaben = []
        interp = Interpreter(output_callback=lambda t: ausgaben.append(str(t)))
        interp.working_dir = projekt
        interp.interpretiere(ast)
        assert "55" in ausgaben
