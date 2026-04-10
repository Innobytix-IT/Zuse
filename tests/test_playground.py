# FILE: tests/test_playground.py
# Tests für den Web-Playground (Phase 5.1)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PLAYGROUND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "playground")


# ─── Datei-Struktur ───────────────────────────────────────────────────────

class TestDateiStruktur:
    def test_index_html_existiert(self):
        assert os.path.exists(os.path.join(PLAYGROUND_DIR, "index.html"))

    def test_server_py_existiert(self):
        assert os.path.exists(os.path.join(PLAYGROUND_DIR, "server.py"))


# ─── HTML-Inhalt ──────────────────────────────────────────────────────────

class TestHTMLInhalt:
    def _read_html(self):
        with open(os.path.join(PLAYGROUND_DIR, "index.html"), "r", encoding="utf-8") as f:
            return f.read()

    def test_hat_titel(self):
        html = self._read_html()
        assert "<title>Zuse Playground</title>" in html

    def test_hat_editor(self):
        html = self._read_html()
        assert 'id="editor"' in html

    def test_hat_output(self):
        html = self._read_html()
        assert 'id="output"' in html

    def test_hat_run_button(self):
        html = self._read_html()
        assert 'id="btn-run"' in html

    def test_hat_pyodide(self):
        """Playground laedt Pyodide."""
        html = self._read_html()
        assert "pyodide" in html.lower()

    def test_hat_sprachauswahl(self):
        """Alle 6 Sprachen sind waehlbar."""
        html = self._read_html()
        for sprache in ["deutsch", "english", "espaniol", "francais", "italiano", "portugues"]:
            assert sprache in html, f"Sprache '{sprache}' fehlt in der Auswahl"

    def test_hat_beispiele(self):
        """Beispiel-Programme sind enthalten."""
        html = self._read_html()
        assert "EXAMPLES" in html
        assert "hallo" in html
        assert "fizzbuzz" in html

    def test_hat_keyboard_shortcut(self):
        """Ctrl+Enter Shortcut ist implementiert."""
        html = self._read_html()
        assert "Ctrl-Enter" in html or "ctrlKey" in html

    def test_hat_tab_support(self):
        """Tab-Einrueckung funktioniert."""
        html = self._read_html()
        assert "Tab" in html

    def test_laedt_zuse_dateien(self):
        """Playground laedt alle nötigen Zuse-Quelldateien."""
        html = self._read_html()
        assert "lexer.py" in html
        assert "parser.py" in html
        assert "interpreter.py" in html
        assert "deutsch.json" in html

    def test_hat_fehlerbehandlung(self):
        """Fehlerausgabe ist implementiert."""
        html = self._read_html()
        assert "output-error" in html
        assert "FEHLER" in html

    def test_hat_transpiler_button(self):
        """Transpiler-Button ist vorhanden."""
        html = self._read_html()
        assert 'id="btn-transpile"' in html

    def test_hat_transpiler_modal(self):
        """Transpiler-Modal mit Zielsprachen ist vorhanden."""
        html = self._read_html()
        assert 'id="transpile-modal"' in html
        assert 'data-backend="python"' in html
        assert 'data-backend="javascript"' in html
        assert 'data-backend="java"' in html
        assert 'data-backend="csharp"' in html
        assert 'data-backend="wasm"' in html

    def test_hat_transpiler_kopieren(self):
        """Transpiler hat Copy- und Download-Buttons."""
        html = self._read_html()
        assert 'id="btn-transpile-copy"' in html
        assert 'id="btn-transpile-download"' in html

    def test_laedt_transpiler_module(self):
        """Playground laedt Transpiler- und i18n-Module."""
        html = self._read_html()
        assert "transpiler.py" in html
        assert "builtin_i18n.py" in html
        assert "error_i18n.py" in html

    def test_interpreter_mit_sprache(self):
        """Interpreter wird mit sprache-Parameter aufgerufen."""
        html = self._read_html()
        assert "sprache=_lang" in html or "sprache=" in html

    def test_version_aktuell(self):
        """Footer zeigt aktuelle Version."""
        html = self._read_html()
        assert "7.3" in html

    def test_hat_canvas_element(self):
        """Playground hat ein HTML5 Canvas fuer Spielfeld."""
        html = self._read_html()
        assert 'id="game-canvas"' in html
        assert 'id="canvas-container"' in html

    def test_hat_canvas_engine(self):
        """JavaScript Canvas-Engine ist vorhanden."""
        html = self._read_html()
        assert '_zuseCanvas' in html
        assert 'addSprite' in html
        assert 'moveSprite' in html
        assert 'isKeyPressed' in html
        assert 'renderFrame' in html

    def test_hat_spielfeld_web(self):
        """spielfeld_web.py wird geladen."""
        html = self._read_html()
        assert 'spielfeld_web.py' in html

    def test_hat_snake_beispiel(self):
        """Snake-Beispiel ist vorhanden."""
        html = self._read_html()
        assert 'data-example="snake"' in html
        assert 'Snake' in html

    def test_erkennt_spielfeld_code(self):
        """Playground erkennt Spielfeld-Nutzung im Code."""
        html = self._read_html()
        assert 'usesSpielfeld' in html
        assert 'Spielfeld\\s*\\(' in html or 'Spielfeld' in html


# ─── Server-Skript ────────────────────────────────────────────────────────

class TestServer:
    def test_server_importierbar(self):
        """server.py hat eine main()-Funktion."""
        server_path = os.path.join(PLAYGROUND_DIR, "server.py")
        with open(server_path, "r", encoding="utf-8") as f:
            code = f.read()
        assert "def main():" in code
        assert "HTTPServer" in code or "http.server" in code

    def test_server_default_port(self):
        """Server nutzt Port 8080 als Default."""
        server_path = os.path.join(PLAYGROUND_DIR, "server.py")
        with open(server_path, "r", encoding="utf-8") as f:
            code = f.read()
        assert "8080" in code
