# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['zzz_profiler/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('zzz_profiler/assets', 'assets')],
    hiddenimports=[
        'enka', 'flask', 'PIL', 'PyQt5', 'PyQt5.QtCore', 
        'PyQt5.QtGui', 'PyQt5.QtWidgets', 'requests'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['customtkinter', 'tkinter'],
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
    name='ZZZ_Profiler',
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
)
