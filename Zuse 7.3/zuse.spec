# -*- mode: python ; coding: utf-8 -*-
# PyInstaller Spec für Zuse Studio — Windows EXE
# Erstellt mit: pyinstaller zuse.spec --clean

import os
from pathlib import Path

ROOT = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

a = Analysis(
    [os.path.join(ROOT, 'zuse_studio.py')],
    pathex=[ROOT],
    binaries=[],
    datas=[
        # Icon (für tkinter-Laufzeit-Icon im Fenster)
        (os.path.join(ROOT, 'zuse_icon.ico'),        '.'),
        # Sprachdateien (JSON)
        (os.path.join(ROOT, 'sprachen', '*.json'),   'sprachen'),
        # Standardbibliothek (.zuse)
        (os.path.join(ROOT, 'bibliothek', '*.zuse'), 'bibliothek'),
        # Paketmanager-Registry
        (os.path.join(ROOT, 'zpkg_registry'),        'zpkg_registry'),
        # Beispielprogramme
        (os.path.join(ROOT, 'Zuse Programme'),       'Zuse Programme'),
    ],
    hiddenimports=[
        # tkinter (wird manchmal nicht automatisch erkannt)
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'tkinter.font',
        'tkinter.scrolledtext',
        '_tkinter',
        # Zuse-interne Module
        'language_loader',
        'lexer',
        'parser',
        'interpreter',
        'transpiler',
        'debugger',
        'ir',
        'optimizer',
        'semantic_analyzer',
        'symbol_table',
        'visitor',
        'builtin_i18n',
        'studio_i18n',
        'error_messages',
        'error_hints',
        'error_i18n',
        'spielfeld',
        'zpkg_core',
        'zpkg',
        'backends.python_backend',
        'backends.javascript_backend',
        'backends.java_backend',
        'backends.csharp_backend',
        'backends.wasm_backend',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # LSP wird in der Studio-EXE nicht benötigt
    excludes=['pygls', 'lsprotocol', 'pytest', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Zuse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # Kein Konsolenfenster — reine GUI-App
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(ROOT, 'zuse_icon.ico'),
)
