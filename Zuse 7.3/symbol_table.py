# FILE: symbol_table.py
# Symbol Table für Zuse — ersetzt die einfache Environment Dict-Chain.
# Trackt Scope-Typen, Variablen-Metadaten und bietet bessere Fehlerdiagnose.


class Symbol:
    """Metadaten zu einer Variable oder Funktion."""
    __slots__ = ('name', 'value', 'defined_line', 'scope_type', 'mutable')

    def __init__(self, name, value, defined_line=0, scope_type='local', mutable=True):
        self.name = name
        self.value = value
        self.defined_line = defined_line
        self.scope_type = scope_type    # 'local', 'parameter', 'global', 'builtin'
        self.mutable = mutable

    def __repr__(self):
        return f"Symbol({self.name!r}, type={self.scope_type}, line={self.defined_line})"


class SymbolTable:
    """
    Scope-bewusste Symbol-Tabelle mit Parent-Chain.

    Scope-Typen: 'global', 'function', 'class', 'method', 'loop', 'block'
    """

    # Gültige Scope-Typen
    SCOPE_TYPES = ('global', 'function', 'class', 'method', 'loop', 'block')

    def __init__(self, parent=None, scope_type='global', scope_name='global', variables=None):
        self.parent = parent
        self.scope_type = scope_type
        self.scope_name = scope_name
        self._symbols = {}
        # Rückwärtskompatibilität: 'vars' Property für direkten Zugriff
        self.vars = self._symbols

        if variables:
            for name, value in variables.items():
                self._symbols[name] = Symbol(name, value, scope_type='builtin')

    # ─── Kernoperationen ─────────────────────────────────────────────────

    def define(self, name, value, line=0, symbol_type='local'):
        """Definiert eine neue Variable im aktuellen Scope."""
        self._symbols[name] = Symbol(name, value, defined_line=line, scope_type=symbol_type)

    def get(self, name):
        """Sucht eine Variable in der Scope-Kette (aktuell → parent → ... → global)."""
        sym = self._symbols.get(name)
        if sym is not None:
            return sym.value
        if self.parent:
            return self.parent.get(name)
        from interpreter import ZuseError
        raise ZuseError(f"Variable '{name}' nicht definiert.")

    def set(self, name, value):
        """Setzt eine existierende Variable (sucht in der Scope-Kette)."""
        if name in self._symbols:
            self._symbols[name].value = value
        elif self.parent and self.parent.has_recursive(name):
            self.parent.set(name, value)
        else:
            # Neue Variable im aktuellen Scope
            self._symbols[name] = Symbol(name, value, scope_type='local')

    def has(self, name):
        """Prüft ob die Variable im aktuellen Scope existiert (nicht rekursiv)."""
        return name in self._symbols

    def has_recursive(self, name):
        """Prüft ob die Variable irgendwo in der Scope-Kette existiert."""
        if name in self._symbols:
            return True
        if self.parent:
            return self.parent.has_recursive(name)
        return False

    def delete(self, name):
        """Entfernt eine Variable aus dem aktuellen Scope."""
        if name in self._symbols:
            del self._symbols[name]

    # ─── Erweiterte Operationen ──────────────────────────────────────────

    def get_symbol(self, name):
        """Gibt das vollständige Symbol-Objekt zurück (nicht nur den Wert)."""
        sym = self._symbols.get(name)
        if sym is not None:
            return sym
        if self.parent:
            return self.parent.get_symbol(name)
        return None

    def find_scope(self, scope_type):
        """Findet den nächsten übergeordneten Scope eines bestimmten Typs."""
        if self.scope_type == scope_type:
            return self
        if self.parent:
            return self.parent.find_scope(scope_type)
        return None

    def is_in_scope(self, scope_type):
        """Prüft ob wir uns innerhalb eines bestimmten Scope-Typs befinden."""
        return self.find_scope(scope_type) is not None

    def all_symbols(self, local_only=False):
        """Gibt alle sichtbaren Symbole zurück."""
        result = dict(self._symbols)
        if not local_only and self.parent:
            parent_symbols = self.parent.all_symbols()
            # Lokale Symbole haben Vorrang
            parent_symbols.update(result)
            result = parent_symbols
        return result

    def local_names(self):
        """Gibt alle Variablennamen im aktuellen Scope zurück."""
        return set(self._symbols.keys())

    def scope_chain(self):
        """Gibt die Scope-Kette als Liste zurück (aktuell zuerst)."""
        chain = [self]
        current = self.parent
        while current:
            chain.append(current)
            current = current.parent
        return chain

    def depth(self):
        """Gibt die Verschachtelungstiefe zurück."""
        return len(self.scope_chain()) - 1

    def copy(self):
        """Erstellt einen neuen Kind-Scope (Rückwärtskompatibilität)."""
        return SymbolTable(parent=self, scope_type='block', scope_name='copy')

    def __repr__(self):
        names = list(self._symbols.keys())
        return f"SymbolTable({self.scope_name}, type={self.scope_type}, vars={names})"

    def __contains__(self, name):
        return name in self._symbols
