@echo off
chcp 65001 >nul
title ZZZ Profiler (PyQt5)

echo ZZZ Profiler - PyQt5 Version
echo ================================
echo.

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
    echo.
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

echo Checking dependencies...
python -c "import PyQt5" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo PyQt5 not found. Installing dependencies...
    echo This may take 1-3 minutes...
    echo.
    
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo.
        echo Error: Failed to install dependencies
        echo Try manually:
        echo   .venv\Scripts\activate
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
    echo All dependencies installed
)

echo Ready to launch
echo.
echo Starting application...
echo.

python -m zzz_profiler.qt_app

if %errorlevel% neq 0 (
    echo.
    echo Error: Application failed to start
    echo.
)

pause
