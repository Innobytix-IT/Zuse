# FILE: visitor.py
# Visitor-Pattern Basisklasse für AST-Traversierung.
# Wird von Interpreter und Transpiler-Backends verwendet.


class NodeVisitor:
    """
    Basisklasse für das Visitor-Pattern auf Zuse-AST-Knoten.

    Dispatcht automatisch anhand von node['type']:
      visit(node) → visit_ZUWEISUNG(node), visit_WENN_ANWEISUNG(node), etc.

    Subklassen überschreiben die visit_XXX-Methoden.
    """

    def visit(self, node, *args, **kwargs):
        """Dispatcht zum passenden visit_TYPE-Handler."""
        if node is None:
            return None
        typ = node.get('type')
        method_name = f'visit_{typ}'
        handler = getattr(self, method_name, None)
        if handler:
            return handler(node, *args, **kwargs)
        return self.generic_visit(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        """Fallback wenn kein spezifischer Handler existiert."""
        raise NotImplementedError(
            f"{self.__class__.__name__} hat keinen Handler für '{node.get('type')}'"
        )
