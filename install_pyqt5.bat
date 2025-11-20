@echo off
chcp 65001 >nul
title Установка зависимостей для ZZZ Profiler

echo ⚡ Установка зависимостей для ZZZ Profiler
echo ==========================================
echo.

REM Проверяем/создаем виртуальное окружение
if not exist .venv (
    echo [1/3] Создание виртуального окружения...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ Ошибка создания виртуального окружения
        echo Убедитесь, что Python установлен правильно
        pause
        exit /b 1
    )
    echo ✓ Виртуальное окружение создано
    echo.
) else (
    echo [1/3] Виртуальное окружение уже существует
    echo.
)

REM Активируем виртуальное окружение
echo [2/3] Активация виртуального окружения...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Ошибка активации виртуального окружения
    pause
    exit /b 1
)
echo ✓ Виртуальное окружение активировано
echo.

REM Устанавливаем зависимости
echo [3/3] Установка зависимостей...
echo Это может занять 2-5 минут...
echo.

REM Обновляем pip
echo Обновление pip...
python -m pip install --upgrade pip --quiet

REM Устанавливаем все зависимости из requirements.txt
echo Установка библиотек из requirements.txt...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✓ Все зависимости успешно установлены!
    echo ========================================
    echo.
    echo Установлено:
    pip list | findstr /i "PyQt5 Flask enka requests Pillow"
    echo.
    echo Теперь можете запустить: start_qt.bat
) else (
    echo.
    echo ❌ Ошибка установки зависимостей
    echo.
    echo Попробуйте:
    echo 1. Проверить интернет-соединение
    echo 2. Запустить от имени администратора
    echo 3. Установить вручную:
    echo    .venv\Scripts\activate
    echo    pip install -r requirements.txt
)

echo.
pause
