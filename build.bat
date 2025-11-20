@echo off
chcp 65001 >nul
REM =================================================================
REM ==        ZZZ Profiler Build Script v5.0                     ==
REM =================================================================
title Building ZZZ Profiler...

echo ⚡ ZZZ Profiler - Build Script
echo ================================
echo.

echo [1/4] Очистка старых сборок...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist ZZZ_Profiler.spec del ZZZ_Profiler.spec
echo ✓ Готово
echo.

echo [2/4] Проверка PyInstaller...
pip show pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)
echo ✓ PyInstaller готов
echo.

echo [3/4] Создание .spec файла...
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
echo     hiddenimports=['enka', 'flask', 'PIL', 'customtkinter'],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
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
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='ZZZ_Profiler',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo ^)
) > ZZZ_Profiler.spec
echo ✓ Spec файл создан
echo.

echo [4/4] Сборка приложения...
echo Это может занять несколько минут...
echo.
pyinstaller --clean ZZZ_Profiler.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ ОШИБКА: Сборка завершилась с ошибкой
    echo.
    pause
    goto :EOF
)

echo.
echo ================================
echo ✓ Сборка успешно завершена!
echo.
echo 📦 Файл: dist\ZZZ_Profiler.exe
echo 📁 Размер: 
dir dist\ZZZ_Profiler.exe | find "ZZZ_Profiler.exe"
echo.
echo Готово к использованию! 🎉
echo ================================
pause