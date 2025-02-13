# -*- mode: python ; coding: utf-8 -*-

import os
import glob

block_cipher = None

# Находим все .dylib файлы для pypdfium2
pypdfium2_binaries = []
if os.path.exists('venv/lib/python3.11/site-packages/pypdfium2'):
    for f in glob.glob('venv/lib/python3.11/site-packages/pypdfium2/*.dylib'):
        pypdfium2_binaries.append((f, 'pypdfium2'))

# Собираем все ресурсы
resources = [
    ('src/logo/logo_rgb_black.png', 'src/logo'),  # Лого
    ('src/fonts/*.ttf', 'src/fonts'),  # Все шрифты
]

a = Analysis(
    ['pdf_to_txt_converter.py'],
    pathex=[],
    binaries=pypdfium2_binaries,
    datas=resources,
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'pypdfium2',
        '_tkinter',
        'pdfplumber',
        'pdfminer',
        'pdfminer.pdftypes',
        'pdfminer.psparser',
        'pdfminer.utils',
        'charset_normalizer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='PDF to TXT Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,  # Оставляем консоль для отладки
    disable_windowed_traceback=False,
    argv_emulation=True,
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
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'PDF Document',
                'CFBundleTypeRole': 'Viewer',
                'LSHandlerRank': 'Alternate',
                'LSItemContentTypes': ['com.adobe.pdf'],
            },
        ],
    },
) 