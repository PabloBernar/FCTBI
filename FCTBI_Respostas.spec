# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('fctbi.ico', '.'), ('BLMelody-Regular.otf', '.'), ('special_effects.py', '.')],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.sip', 'typing_extensions', 'json', 'pathlib', 'datetime', 'shutil', 'sys', 'os', 'dataclasses', 'typing'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'tkinter', 'PIL', 'cv2', 'requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna', 'ssl', 'http', 'email', 'xml', 'html', 'xmlrpc', 'ftplib', 'smtplib', 'poplib', 'imaplib', 'nntplib', 'telnetlib', 'socketserver', 'multiprocessing'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FCTBI_Respostas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['fctbi.ico'],
)
