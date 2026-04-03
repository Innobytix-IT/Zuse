# FILE: tests/test_logische_operatoren.py
# Tests fuer UND, ODER, NICHT in allen 6 Sprachen + Transpiler
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from conftest import zuse_ausfuehren
from transpiler import transpile

# ─── Sprach-Keywords ──────────────────────────────────────────

SPRACHEN = {
    "deutsch":   {"UND": "UND",  "ODER": "ODER", "NICHT": "NICHT", "WENN": "WENN", "DANN": "DANN", "SONST": "SONST", "ENDE_WENN": "ENDE WENN", "AUSGABE": "AUSGABE", "WAHR": "wahr", "FALSCH": "falsch"},
    "english":   {"UND": "AND",  "ODER": "OR",   "NICHT": "NOT",   "WENN": "IF",   "DANN": "THEN", "SONST": "ELSE",  "ENDE_WENN": "END IF",    "AUSGABE": "PRINT",   "WAHR": "true", "FALSCH": "false"},
    "espaniol":  {"UND": "Y",    "ODER": "O",    "NICHT": "NO",    "WENN": "SI",   "DANN": "ENTONCES", "SONST": "SINO", "ENDE_WENN": "FIN SI",  "AUSGABE": "IMPRIMIR","WAHR": "verdadero", "FALSCH": "falso"},
    "francais":  {"UND": "ET",   "ODER": "OU",   "NICHT": "PAS",   "WENN": "SI",   "DANN": "ALORS", "SONST": "SINON", "ENDE_WENN": "FIN SI",   "AUSGABE": "IMPRIMER","WAHR": "vrai", "FALSCH": "faux"},
    "italiano":  {"UND": "E",    "ODER": "O",    "NICHT": "NON",   "WENN": "SE",   "DANN": "ALLORA", "SONST": "ALTRIMENTI", "ENDE_WENN": "FINE SE", "AUSGABE": "STAMPA", "WAHR": "vero", "FALSCH": "falso"},
    "portugues": {"UND": "E",    "ODER": "OU",   "NICHT": "NAO",   "WENN": "SE",   "DANN": "ENTAO", "SONST": "SENAO", "ENDE_WENN": "FIM SE",   "AUSGABE": "IMPRIMIR","WAHR": "verdadeiro", "FALSCH": "falso"},
}

def code(sprache, template):
    kw = SPRACHEN[sprache]
    result = template
    for key in sorted(kw.keys(), key=len, reverse=True):
        result = result.replace(f"{{{key}}}", kw[key])
    return result


# ─── 1. Interpreter: Deutsch ─────────────────────────────────

class TestLogischDeutsch:

    def test_und_wahr_wahr(self):
        out = zuse_ausfuehren('AUSGABE wahr UND wahr')
        assert out == ["True"]

    def test_und_wahr_falsch(self):
        out = zuse_ausfuehren('AUSGABE wahr UND falsch')
        assert out == ["False"]

    def test_und_falsch_wahr(self):
        out = zuse_ausfuehren('AUSGABE falsch UND wahr')
        assert out == ["False"]

    def test_oder_wahr_falsch(self):
        out = zuse_ausfuehren('AUSGABE wahr ODER falsch')
        assert out == ["True"]

    def test_oder_falsch_falsch(self):
        out = zuse_ausfuehren('AUSGABE falsch ODER falsch')
        assert out == ["False"]

    def test_nicht_wahr(self):
        out = zuse_ausfuehren('AUSGABE NICHT wahr')
        assert out == ["False"]

    def test_nicht_falsch(self):
        out = zuse_ausfuehren('AUSGABE NICHT falsch')
        assert out == ["True"]

    def test_und_mit_vergleich(self):
        out = zuse_ausfuehren('x = 10\nWENN x > 5 UND x < 20 DANN\n    AUSGABE "ja"\nENDE WENN')
        assert out == ["ja"]

    def test_oder_mit_vergleich(self):
        out = zuse_ausfuehren('x = 3\nWENN x > 10 ODER x < 5 DANN\n    AUSGABE "ja"\nENDE WENN')
        assert out == ["ja"]

    def test_nicht_mit_vergleich(self):
        out = zuse_ausfuehren('x = 3\nWENN NICHT x > 10 DANN\n    AUSGABE "ja"\nENDE WENN')
        assert out == ["ja"]

    def test_kombiniert_und_oder(self):
        """ODER hat niedrigere Prioritaet als UND."""
        out = zuse_ausfuehren('AUSGABE falsch UND wahr ODER wahr')
        assert out == ["True"]  # (falsch UND wahr) ODER wahr = False OR True = True

    def test_kombiniert_und_oder_2(self):
        out = zuse_ausfuehren('AUSGABE wahr ODER falsch UND falsch')
        assert out == ["True"]  # wahr ODER (falsch UND falsch) = True OR False = True

    def test_nicht_hat_hoechste_prioritaet(self):
        out = zuse_ausfuehren('AUSGABE NICHT falsch UND wahr')
        assert out == ["True"]  # (NICHT falsch) UND wahr = True AND True = True

    def test_short_circuit_und(self):
        """UND wertet rechte Seite nicht aus wenn links falsch."""
        out = zuse_ausfuehren('x = falsch\nAUSGABE x UND y')
        # y ist nicht definiert, aber durch short-circuit wird es nicht ausgewertet
        assert out == ["False"]

    def test_short_circuit_oder(self):
        """ODER wertet rechte Seite nicht aus wenn links wahr."""
        out = zuse_ausfuehren('x = wahr\nAUSGABE x ODER y')
        assert out == ["True"]


# ─── 2. Alle 6 Sprachen ──────────────────────────────────────

class TestLogischMehrsprachig:

    @pytest.mark.parametrize("sprache", SPRACHEN.keys())
    def test_und(self, sprache):
        programm = code(sprache, "{AUSGABE} {WAHR} {UND} {WAHR}")
        out = zuse_ausfuehren(programm, sprache=sprache)
        assert out == ["True"]

    @pytest.mark.parametrize("sprache", SPRACHEN.keys())
    def test_oder(self, sprache):
        programm = code(sprache, "{AUSGABE} {FALSCH} {ODER} {WAHR}")
        out = zuse_ausfuehren(programm, sprache=sprache)
        assert out == ["True"]

    @pytest.mark.parametrize("sprache", SPRACHEN.keys())
    def test_nicht(self, sprache):
        programm = code(sprache, "{AUSGABE} {NICHT} {FALSCH}")
        out = zuse_ausfuehren(programm, sprache=sprache)
        assert out == ["True"]

    @pytest.mark.parametrize("sprache", SPRACHEN.keys())
    def test_kombination(self, sprache):
        programm = code(sprache,
            "x = 10\n"
            "{WENN} x > 5 {UND} x < 20 {DANN}\n"
            '    {AUSGABE} "ok"\n'
            "{ENDE_WENN}"
        )
        out = zuse_ausfuehren(programm, sprache=sprache)
        assert out == ["ok"]


# ─── 3. Transpiler-Backends ──────────────────────────────────

class TestLogischTranspiler:

    def _transpiliere(self, code_str, backend):
        return transpile(code_str, target_backend=backend, include_stdlib=False)["code"]

    # Python
    def test_python_und(self):
        code = self._transpiliere('AUSGABE wahr UND falsch', "python")
        assert "and" in code

    def test_python_oder(self):
        code = self._transpiliere('AUSGABE wahr ODER falsch', "python")
        assert "or" in code

    def test_python_nicht(self):
        code = self._transpiliere('AUSGABE NICHT wahr', "python")
        assert "not" in code

    # JavaScript
    def test_js_und(self):
        code = self._transpiliere('AUSGABE wahr UND falsch', "javascript")
        assert "&&" in code

    def test_js_oder(self):
        code = self._transpiliere('AUSGABE wahr ODER falsch', "javascript")
        assert "||" in code

    def test_js_nicht(self):
        code = self._transpiliere('AUSGABE NICHT wahr', "javascript")
        assert "!" in code

    # Java
    def test_java_und(self):
        code = self._transpiliere('AUSGABE wahr UND falsch', "java")
        assert "&&" in code

    def test_java_oder(self):
        code = self._transpiliere('AUSGABE wahr ODER falsch', "java")
        assert "||" in code

    def test_java_nicht(self):
        code = self._transpiliere('AUSGABE NICHT wahr', "java")
        assert "!_truthy(" in code

    # C#
    def test_csharp_und(self):
        code = self._transpiliere('AUSGABE wahr UND falsch', "csharp")
        assert "&&" in code

    def test_csharp_oder(self):
        code = self._transpiliere('AUSGABE wahr ODER falsch', "csharp")
        assert "||" in code

    def test_csharp_nicht(self):
        code = self._transpiliere('AUSGABE NICHT wahr', "csharp")
        assert "!" in code
