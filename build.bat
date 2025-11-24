@echo off
chcp 65001 >nul
title Building ZZZ Profiler...

echo ZZZ Profiler - Build Script (PyQt5)
echo ========================================
echo.

echo [1/5] Cleaning old builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo Done
echo.

echo [2/5] Checking dependencies...
pip show pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)
pip show PyQt5 >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyQt5...
    pip install PyQt5
)
echo Dependencies ready
echo.

echo [3/5] Updating .spec file...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis^(
echo     ['zzz_profiler/__main__.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[^('zzz_profiler/assets', 'assets'^)],
echo     hiddenimports=[
echo         'enka', 'flask', 'PIL', 'PyQt5', 'PyQt5.QtCore', 
echo         'PyQt5.QtGui', 'PyQt5.QtWidgets', 'requests'
echo     ],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[
echo         'customtkinter', 'tkinter', 'matplotlib', 'numpy', 
echo         'pandas', 'scipy', 'IPython', 'jupyter'
echo     ],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo ^)
echo.
echo pyz = PYZ^(a.pure, a.zipped_data, cipher=block_cipher^)
echo.
echo exe = EXE^(
echo     pyz,
echo     a.scripts,
echo     [],
echo     exclude_binaries=True,
echo     name='ZZZ_Profiler',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     icon=None,
echo ^)
echo.
echo coll = COLLECT^(
echo     exe,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     name='ZZZ_Profiler',
echo ^)
) > ZZZ_Profiler.spec
echo Spec file updated
echo.

echo [4/5] Building application...
echo This may take several minutes...
echo.
pyinstaller --clean --noconfirm ZZZ_Profiler.spec

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed
    echo.
    pause
    goto :EOF
)

echo.
echo [5/5] Cleaning temporary files...
if exist build rmdir /s /q build
echo Done
echo.

echo ========================================
echo Build completed successfully!
echo.
echo Folder: dist\ZZZ_Profiler\
echo Executable: dist\ZZZ_Profiler\ZZZ_Profiler.exe
echo.
echo Version: PyQt5 (optimized - fast startup)
echo Ready to use!
echo.
echo Note: Distribute the entire ZZZ_Profiler folder
echo ========================================
pause