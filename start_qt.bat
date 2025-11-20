@echo off
chcp 65001 >nul
title ZZZ Profiler (PyQt5)

echo ⚡ ZZZ Profiler - PyQt5 Version
echo ================================
echo.

REM Проверяем/создаем виртуальное окружение
if not exist .venv (
    echo Создание виртуального окружения...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ Ошибка создания виртуального окружения
        pause
        exit /b 1
    )
    echo ✓ Виртуальное окружение создано
    echo.
)

REM Активируем виртуальное окружение
echo Активация виртуального окружения...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Ошибка активации виртуального окружения
    pause
    exit /b 1
)
echo ✓ Виртуальное окружение активировано
echo.

REM Проверяем PyQt5
echo Проверка зависимостей...
python -c "import PyQt5" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo PyQt5 не установлен. Устанавливаю зависимости...
    echo Это может занять 1-3 минуты...
    echo.
    
    REM Обновляем pip
    python -m pip install --upgrade pip --quiet
    
    REM Устанавливаем все зависимости
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Ошибка установки зависимостей
        echo Попробуйте вручную:
        echo   .venv\Scripts\activate
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
    echo ✓ Все зависимости установлены
)

echo ✓ Все готово к запуску
echo.
echo Запуск приложения...
echo.

REM Запускаем приложение
python -m zzz_profiler.qt_app

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка запуска приложения
    echo.
)

pause
