@echo off
chcp 65001 >nul
REM =================================================================
REM ==        ZZZ Profiler Build Script v6.0 (PyQt5)             ==
REM =================================================================
title Building ZZZ Profiler...

echo ⚡ ZZZ Profiler - Build Script (PyQt5)
echo ========================================
echo.

echo [1/5] Очистка старых сборок...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo ✓ Готово
echo.

echo [2/5] Проверка зависимостей...
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
echo ✓ Зависимости готовы
echo.

echo [3/5] Обновление .spec файла...
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
echo     excludes=['customtkinter', 'tkinter'],
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
echo ✓ Spec файл обновлен
echo.

echo [4/5] Сборка приложения...
echo Это может занять несколько минут...
echo.
pyinstaller --clean --noconfirm ZZZ_Profiler.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ ОШИБКА: Сборка завершилась с ошибкой
    echo.
    pause
    goto :EOF
)

echo.
echo [5/5] Очистка временных файлов...
if exist build rmdir /s /q build
echo ✓ Готово
echo.

echo ========================================
echo ✓ Сборка успешно завершена!
echo.
echo 📦 Файл: dist\ZZZ_Profiler.exe
echo 📁 Размер: 
dir dist\ZZZ_Profiler.exe | find "ZZZ_Profiler.exe"
echo.
echo 🎨 Версия: PyQt5 (оптимизированная)
echo 🚀 Готово к использованию!
echo ========================================
pause