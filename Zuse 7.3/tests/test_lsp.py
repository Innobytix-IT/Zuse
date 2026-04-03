# FILE: tests/test_lsp.py
# Tests für den Zuse Language Server (Phase 5.2)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json

LSP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lsp")
VSCODE_DIR = os.path.join(LSP_DIR, "vscode-zuse")


# ─── Datei-Struktur ───────────────────────────────────────────────────────

class TestDateiStruktur:
    def test_server_existiert(self):
        assert os.path.exists(os.path.join(LSP_DIR, "zuse_server.py"))

    def test_init_existiert(self):
        assert os.path.exists(os.path.join(LSP_DIR, "__init__.py"))

    def test_main_existiert(self):
        assert os.path.exists(os.path.join(LSP_DIR, "__main__.py"))

    def test_vscode_package_json(self):
        assert os.path.exists(os.path.join(VSCODE_DIR, "package.json"))

    def test_vscode_extension_js(self):
        assert os.path.exists(os.path.join(VSCODE_DIR, "extension.js"))

    def test_vscode_language_config(self):
        assert os.path.exists(os.path.join(VSCODE_DIR, "language-configuration.json"))

    def test_vscode_grammar(self):
        assert os.path.exists(os.path.join(VSCODE_DIR, "syntaxes", "zuse.tmLanguage.json"))


# ─── Server-Import ────────────────────────────────────────────────────────

class TestServerImport:
    def test_server_importierbar(self):
        from lsp.zuse_server import server, main
        assert server is not None
        assert main is not None

    def test_analyze_function(self):
        from lsp.zuse_server import _analyze_document
        assert callable(_analyze_document)

    def test_word_at_function(self):
        from lsp.zuse_server import _word_at
        assert _word_at("AUSGABE x", 0) == "AUSGABE"
        assert _word_at("AUSGABE x", 8) == "x"

    def test_detect_language(self):
        from lsp.zuse_server import _detect_language
        assert _detect_language("AUSGABE 42") == "deutsch"
        assert _detect_language("PRINT 42") == "english"


# ─── Diagnosen ────────────────────────────────────────────────────────────

class TestDiagnosen:
    def test_korrekter_code_keine_fehler(self):
        from lsp.zuse_server import _analyze_document
        diags = _analyze_document('x = 5\nAUSGABE x')
        errors = [d for d in diags if d.severity == 1]  # 1 = Error
        assert len(errors) == 0

    def test_syntax_fehler(self):
        from lsp.zuse_server import _analyze_document
        diags = _analyze_document('WENN DANN DANN')
        assert len(diags) > 0

    def test_semantik_warnung_undefinierte_variable(self):
        from lsp.zuse_server import _analyze_document
        diags = _analyze_document('AUSGABE undefiniert_xyz')
        warnings = [d for d in diags if d.severity == 2]  # 2 = Warning
        assert len(warnings) > 0

    def test_semantik_fehler_break_ausserhalb(self):
        from lsp.zuse_server import _analyze_document
        diags = _analyze_document('ABBRUCH')
        errors = [d for d in diags if d.severity == 1]
        assert len(errors) > 0


# ─── Autovervollständigung ───────────────────────────────────────────────

class TestCompletion:
    def test_hat_keywords(self):
        from lsp.zuse_server import _KEYWORDS
        assert 'AUSGABE' in _KEYWORDS
        assert 'DEFINIERE' in _KEYWORDS
        assert 'WENN' in _KEYWORDS

    def test_hat_builtin_docs(self):
        from lsp.zuse_server import _BUILTIN_DOCS
        assert 'WURZEL' in _BUILTIN_DOCS
        assert 'GROSSBUCHSTABEN' in _BUILTIN_DOCS
        assert 'SORTIEREN' in _BUILTIN_DOCS
        assert 'LESE_DATEI' in _BUILTIN_DOCS
        assert 'PI' in _BUILTIN_DOCS
        assert 'Spielfeld' in _BUILTIN_DOCS

    def test_builtin_docs_format(self):
        from lsp.zuse_server import _BUILTIN_DOCS
        for name, (typ, doc) in _BUILTIN_DOCS.items():
            assert typ in ('Funktion', 'Konstante', 'Klasse'), f"{name}: ungültiger Typ '{typ}'"
            assert len(doc) > 0, f"{name}: leere Dokumentation"


# ─── VS Code Extension ──────────────────────────────────────────────────

class TestVSCodeExtension:
    def test_package_json_gueltig(self):
        with open(os.path.join(VSCODE_DIR, "package.json"), encoding="utf-8") as f:
            pkg = json.load(f)
        assert pkg["name"] == "zuse-language"
        assert "zuse" in str(pkg["contributes"]["languages"])
        assert ".zuse" in str(pkg["contributes"]["languages"])

    def test_grammar_gueltig(self):
        path = os.path.join(VSCODE_DIR, "syntaxes", "zuse.tmLanguage.json")
        with open(path, encoding="utf-8") as f:
            grammar = json.load(f)
        assert grammar["scopeName"] == "source.zuse"
        assert "keywords" in grammar["repository"]
        assert "builtins" in grammar["repository"]
        assert "strings" in grammar["repository"]
        assert "comments" in grammar["repository"]

    def test_language_config_gueltig(self):
        path = os.path.join(VSCODE_DIR, "language-configuration.json")
        with open(path, encoding="utf-8") as f:
            config = json.load(f)
        assert config["comments"]["lineComment"] == "#"
        assert len(config["brackets"]) >= 3

    def test_extension_hat_activate(self):
        path = os.path.join(VSCODE_DIR, "extension.js")
        with open(path, encoding="utf-8") as f:
            code = f.read()
        assert "activate" in code
        assert "deactivate" in code
        assert "LanguageClient" in code
