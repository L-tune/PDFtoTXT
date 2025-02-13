from setuptools import setup

APP = ['pdf_to_txt_converter.py']
DATA_FILES = [
    ('src/fonts', [
        'src/fonts/Inter_24pt-Regular.ttf',
        'src/fonts/Inter_28pt-Black.ttf',
        'src/fonts/SpaceGrotesk-Bold.ttf',
        'src/fonts/SpaceGrotesk-Light.ttf',
        'src/fonts/SpaceGrotesk-Regular.ttf'
    ]),
    ('src/logo', ['src/logo/logo_rgb_black.png'])
]
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'customtkinter',
        'pdfplumber',
        'PIL',
        'tkinter',
        'darkdetect'
    ],
    'includes': [
        'tkinter',
        'tkinter.ttk',
        '_tkinter',
        'Tcl',
        'Tk'
    ],
    'excludes': [
        'PyQt6',
        'PyQt5',
        'PySide6',
        'PySide2',
        'sip',
        'numpy',
        'matplotlib'
    ],
    'frameworks': ['Python'],
    'strip': True,
    'optimize': 2,
    'plist': {
        'CFBundleName': 'PDF to TXT Converter',
        'CFBundleDisplayName': 'PDF to TXT Converter',
        'CFBundleGetInfoString': "Converting PDF files to TXT",
        'CFBundleIdentifier': "com.ltuneously.pdftotxt",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.12',
        'NSHumanReadableCopyright': "© 2025 Alexey Evdokimov"
    }
}

setup(
    name='PDF to TXT Converter',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
) 