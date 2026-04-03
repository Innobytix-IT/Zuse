# FILE: tests/test_symbol_table.py
# Tests für die SymbolTable (Phase 3.5)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from symbol_table import SymbolTable, Symbol


# ─── Grundoperationen ────────────────────────────────────────────────────────

class TestGrundoperationen:
    def test_define_und_get(self):
        st = SymbolTable()
        st.define('x', 42)
        assert st.get('x') == 42

    def test_set_existierende_variable(self):
        st = SymbolTable()
        st.define('x', 1)
        st.set('x', 2)
        assert st.get('x') == 2

    def test_set_neue_variable(self):
        st = SymbolTable()
        st.set('y', 10)
        assert st.get('y') == 10

    def test_get_undefiniert_wirft_fehler(self):
        st = SymbolTable()
        try:
            st.get('nix')
            assert False, "Sollte Fehler werfen"
        except Exception as e:
            assert "nicht definiert" in str(e)

    def test_has(self):
        st = SymbolTable()
        st.define('x', 1)
        assert st.has('x')
        assert not st.has('y')

    def test_has_recursive(self):
        parent = SymbolTable()
        parent.define('x', 1)
        child = SymbolTable(parent=parent)
        assert child.has_recursive('x')
        assert not child.has('x')  # Nicht lokal

    def test_delete(self):
        st = SymbolTable()
        st.define('x', 1)
        st.delete('x')
        assert not st.has('x')


# ─── Scope-Kette ────────────────────────────────────────────────────────────

class TestScopeKette:
    def test_parent_lookup(self):
        parent = SymbolTable(scope_name='global')
        parent.define('x', 10)
        child = SymbolTable(parent=parent, scope_type='function', scope_name='foo')
        assert child.get('x') == 10

    def test_lokale_variable_verdeckt_parent(self):
        parent = SymbolTable()
        parent.define('x', 10)
        child = SymbolTable(parent=parent, scope_type='function')
        child.define('x', 20)
        assert child.get('x') == 20
        assert parent.get('x') == 10  # Unverändert

    def test_set_propagiert_zum_parent(self):
        parent = SymbolTable()
        parent.define('x', 10)
        child = SymbolTable(parent=parent, scope_type='function')
        child.set('x', 20)
        assert parent.get('x') == 20

    def test_dreifach_verschachtelt(self):
        g = SymbolTable(scope_type='global', scope_name='global')
        g.define('a', 1)
        f = SymbolTable(parent=g, scope_type='function', scope_name='foo')
        f.define('b', 2)
        b = SymbolTable(parent=f, scope_type='block', scope_name='if')
        b.define('c', 3)
        assert b.get('a') == 1
        assert b.get('b') == 2
        assert b.get('c') == 3


# ─── Scope-Typen ────────────────────────────────────────────────────────────

class TestScopeTypen:
    def test_scope_type(self):
        st = SymbolTable(scope_type='function', scope_name='foo')
        assert st.scope_type == 'function'
        assert st.scope_name == 'foo'

    def test_find_scope(self):
        g = SymbolTable(scope_type='global')
        f = SymbolTable(parent=g, scope_type='function', scope_name='foo')
        b = SymbolTable(parent=f, scope_type='block', scope_name='if')
        assert b.find_scope('function') is f
        assert b.find_scope('global') is g
        assert b.find_scope('class') is None

    def test_is_in_scope(self):
        g = SymbolTable(scope_type='global')
        f = SymbolTable(parent=g, scope_type='function')
        b = SymbolTable(parent=f, scope_type='loop')
        assert b.is_in_scope('function')
        assert b.is_in_scope('loop')
        assert b.is_in_scope('global')
        assert not b.is_in_scope('class')


# ─── Symbol-Metadaten ───────────────────────────────────────────────────────

class TestSymbolMetadaten:
    def test_symbol_type(self):
        st = SymbolTable()
        st.define('x', 42, symbol_type='parameter')
        sym = st.get_symbol('x')
        assert sym is not None
        assert sym.scope_type == 'parameter'
        assert sym.value == 42

    def test_defined_line(self):
        st = SymbolTable()
        st.define('x', 42, line=5)
        sym = st.get_symbol('x')
        assert sym.defined_line == 5

    def test_get_symbol_rekursiv(self):
        parent = SymbolTable()
        parent.define('x', 10, symbol_type='global')
        child = SymbolTable(parent=parent, scope_type='function')
        sym = child.get_symbol('x')
        assert sym is not None
        assert sym.scope_type == 'global'

    def test_get_symbol_nicht_vorhanden(self):
        st = SymbolTable()
        assert st.get_symbol('nix') is None


# ─── Introspection ──────────────────────────────────────────────────────────

class TestIntrospection:
    def test_local_names(self):
        st = SymbolTable()
        st.define('a', 1)
        st.define('b', 2)
        assert st.local_names() == {'a', 'b'}

    def test_all_symbols_lokal(self):
        st = SymbolTable()
        st.define('x', 1)
        syms = st.all_symbols(local_only=True)
        assert 'x' in syms

    def test_all_symbols_mit_parent(self):
        parent = SymbolTable()
        parent.define('a', 1)
        child = SymbolTable(parent=parent)
        child.define('b', 2)
        syms = child.all_symbols()
        assert 'a' in syms
        assert 'b' in syms

    def test_scope_chain(self):
        g = SymbolTable(scope_type='global', scope_name='g')
        f = SymbolTable(parent=g, scope_type='function', scope_name='f')
        b = SymbolTable(parent=f, scope_type='block', scope_name='b')
        chain = b.scope_chain()
        assert len(chain) == 3
        assert chain[0] is b
        assert chain[1] is f
        assert chain[2] is g

    def test_depth(self):
        g = SymbolTable(scope_type='global')
        f = SymbolTable(parent=g, scope_type='function')
        assert g.depth() == 0
        assert f.depth() == 1

    def test_copy(self):
        st = SymbolTable()
        st.define('x', 1)
        child = st.copy()
        assert child.get('x') == 1
        assert child.parent is st

    def test_contains(self):
        st = SymbolTable()
        st.define('x', 1)
        assert 'x' in st
        assert 'y' not in st

    def test_repr(self):
        st = SymbolTable(scope_type='function', scope_name='foo')
        st.define('x', 1)
        r = repr(st)
        assert 'foo' in r
        assert 'function' in r


# ─── Integration mit Interpreter ────────────────────────────────────────────

class TestInterpreterIntegration:
    def test_einfaches_programm(self):
        """SymbolTable funktioniert nahtlos mit dem Interpreter."""
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests'))
        from conftest import zuse_ausfuehren
        result = zuse_ausfuehren("x = 42\nAUSGABE x")
        assert result == ['42']

    def test_funktion_scope(self):
        from conftest import zuse_ausfuehren
        code = "x = 10\nDEFINIERE foo()\nAUSGABE x\nENDE FUNKTION\nfoo()"
        result = zuse_ausfuehren(code)
        assert result == ['10']

    def test_verschachtelte_scopes(self):
        from conftest import zuse_ausfuehren
        code = """x = 1
DEFINIERE foo()
    y = 2
    DEFINIERE bar()
        z = 3
        ERGEBNIS IST x + y + z
    ENDE FUNKTION
    ERGEBNIS IST bar()
ENDE FUNKTION
AUSGABE foo()"""
        result = zuse_ausfuehren(code)
        assert result == ['6']

    def test_globale_variable(self):
        from conftest import zuse_ausfuehren
        code = """zaehler = 0
DEFINIERE erhoehe()
    GLOBAL zaehler
    zaehler = zaehler + 1
ENDE FUNKTION
erhoehe()
erhoehe()
AUSGABE zaehler"""
        result = zuse_ausfuehren(code)
        assert result == ['2']
