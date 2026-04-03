# FILE: transpiler.py
# Zuse Transpiler - Haupt-Orchestrator
# Nutzt den bestehenden Lexer/Parser und leitet den AST an das gewählte Backend.

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from language_loader import lade_sprache
from lexer import tokenize
from parser import Parser

from backends.python_backend     import PythonBackend
from backends.javascript_backend import JavaScriptBackend
from backends.java_backend       import JavaBackend
from backends.csharp_backend     import CSharpBackend
from backends.wasm_backend       import WasmBackend

# Registry aller verfügbaren Backends
BACKENDS = {
    "python":     PythonBackend,
    "javascript": JavaScriptBackend,
    "java":       JavaBackend,
    "csharp":     CSharpBackend,
    "wasm":       WasmBackend,
}

BACKEND_DISPLAY_NAMES = {
    "python":     "Python 3",
    "javascript": "JavaScript (ES6+)",
    "java":       "Java 11+",
    "csharp":     "C# 10+",
    "wasm":       "WebAssembly (WAT)",
}


def transpile(zuse_code, source_lang="deutsch", target_backend="python",
              include_stdlib=True, base_dir=None):
    """
    Transpiliert Zuse-Quellcode in die Zielsprache.

    Args:
        zuse_code (str):       Der Zuse-Quellcode
        source_lang (str):     Sprache des Zuse-Codes (z.B. 'deutsch', 'english')
        target_backend (str):  Ziel-Backend ('python', 'javascript', 'java', 'csharp')
        include_stdlib (bool): Standardbibliothek einbinden (für Maler, etc.)
        base_dir (str):        Basisverzeichnis für Bibliotheks-Lookup

    Returns:
        dict: {
            'code':      str  - Der generierte Quellcode,
            'backend':   str  - Name des Backends,
            'extension': str  - Dateiendung (.py, .js, ...),
            'warnings':  list - Warnungen
        }
    """
    if target_backend not in BACKENDS:
        raise ValueError(f"Unbekanntes Backend: '{target_backend}'. "
                         f"Verfügbar: {list(BACKENDS.keys())}")

    warnings = []

    # 1. Bibliothek laden (optional)
    final_code = zuse_code
    if include_stdlib and base_dir:
        lib_path = os.path.join(base_dir, "bibliothek", f"{source_lang}.zuse")
        if os.path.exists(lib_path):
            try:
                with open(lib_path, "r", encoding="utf-8") as f:
                    lib_code = f.read()
                    final_code = lib_code + "\n\n" + zuse_code
            except Exception as e:
                warnings.append(f"Bibliothek konnte nicht geladen werden: {e}")
        else:
            warnings.append(f"Keine Bibliothek für '{source_lang}' gefunden.")

    # 2. Lexen & Parsen
    try:
        config = lade_sprache(source_lang)
        tokens = tokenize(final_code, config)
        ast = Parser(tokens).parse()
    except RuntimeError as e:
        raise SyntaxError(f"Zuse-Syntaxfehler: {e}")

    # 3. Code generieren
    backend_cls = BACKENDS[target_backend]
    backend = backend_cls()

    try:
        generated_code = backend.generate(ast)
    except Exception as e:
        raise RuntimeError(f"Transpiler-Fehler ({target_backend}): {e}")

    return {
        'code':      generated_code,
        'backend':   backend.LANGUAGE_NAME,
        'extension': backend.FILE_EXTENSION,
        'warnings':  warnings,
    }


def transpile_file(input_path, target_backend="python", source_lang=None, output_path=None):
    """
    Liest eine .zuse-Datei und schreibt den transpilierten Code in eine neue Datei.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Datei nicht gefunden: {input_path}")

    # Sprache aus Datei-Extension ableiten, oder Standard nutzen
    if source_lang is None:
        source_lang = "deutsch"

    with open(input_path, "r", encoding="utf-8") as f:
        zuse_code = f.read()

    base_dir = os.path.dirname(os.path.abspath(input_path))
    result = transpile(zuse_code, source_lang, target_backend,
                       include_stdlib=True, base_dir=base_dir)

    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = base + result['extension']

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result['code'])

    print(f"✅ Transpiliert: {input_path} → {output_path}")
    print(f"   Ziel: {result['backend']}")
    if result['warnings']:
        for w in result['warnings']:
            print(f"   ⚠️  {w}")

    return output_path


# ─── CLI-Interface ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Zuse Transpiler - Konvertiert .zuse Dateien in andere Sprachen"
    )
    parser.add_argument("input",   help="Eingabe-Datei (.zuse)")
    parser.add_argument("--target", default="python",
                        choices=list(BACKENDS.keys()),
                        help="Ziel-Sprache (default: python)")
    parser.add_argument("--lang",   default="deutsch",
                        help="Quell-Sprache des Zuse-Codes (default: deutsch)")
    parser.add_argument("--output", default=None,
                        help="Ausgabe-Datei (optional, wird automatisch benannt)")

    args = parser.parse_args()

    try:
        out = transpile_file(args.input, args.target, args.lang, args.output)
        print(f"\nInhalt der generierten Datei ({out}):")
        print("─" * 50)
        with open(out) as f:
            print(f.read())
    except Exception as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)
