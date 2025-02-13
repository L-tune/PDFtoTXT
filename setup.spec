# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdf_to_txt_converter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'pypdfium2',
        '_tkinter',
        'pdfplumber',
        'pdfminer',
        'pdfminer.pdftypes',
        'pdfminer.psparser',
        'pdfminer.utils',
        'charset_normalizer',
        'charset_normalizer.md',
        'charset_normalizer.cd',
        'charset_normalizer.assets',
        'charset_normalizer.legacy',
        'charset_normalizer.models',
        'charset_normalizer.utils',
    ],
    hookspath=[],
    hooksconfig={
        'charset_normalizer': {
            'include_assets': True,
        },
    },
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Добавляем дополнительные данные для charset-normalizer
a.datas += Tree('venv/lib/python3.11/site-packages/charset_normalizer', prefix='charset_normalizer')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF to TXT Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='PDF to TXT Converter',
)

app = BUNDLE(
    coll,
    name='PDF to TXT Converter.app',
    icon=None,
    bundle_identifier=None,
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '11.0',
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,
        'NSAppleEventsUsageDescription': 'This app needs to access files for PDF conversion.',
        'NSRequiresAquaSystemAppearance': False,
    },
) 