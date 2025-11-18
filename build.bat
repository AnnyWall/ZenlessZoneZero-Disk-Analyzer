@echo off
REM =================================================================
REM ==        ZZZ Showcase Profiler Build Script v4              ==
REM =================================================================
title Building ZZZ Showcase Profiler...

echo [1/3] Ochistka starykh sborok...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist ZZZ_Profiler.spec del ZZZ_Profiler.spec
echo       gotovo.
echo.

echo [2/3] Ustanovka/proverka PyInstaller...
pip show pyinstaller >nul 2>nul
if %errorlevel% neq 0 (pip install pyinstaller)
echo      PyInstaller na meste.
echo.

echo [3/3] Zapusk sborki prilozheniya... Eto mozhet zanyat' neskol'ko minut.

REM --- ИЗМЕНЕНИЕ: Самая простая и надежная команда ---
pyinstaller --noconsole --add-data "zzz_profiler/assets;assets" --name "ZZZ_Profiler" zzz_profiler/__main__.py

if %errorlevel% neq 0 (
    echo [!] OSHIBKA: Protsess sborki zavershilsya s oshibkoy.
    pause
    goto :EOF
)
echo      Sborka uspeshno zavershena!
echo.
echo Vash prilozheniye gotovo v papke: dist\ZZZ_Profiler
pause