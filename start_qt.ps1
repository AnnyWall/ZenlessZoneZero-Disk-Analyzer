# ZZZ Profiler - PyQt5 Version
Write-Host "⚡ ZZZ Profiler - PyQt5 Version" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Проверяем/создаем виртуальное окружение
if (-not (Test-Path ".venv")) {
    Write-Host "Создание виртуального окружения..." -ForegroundColor Yellow
    python -m venv .venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка создания виртуального окружения" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
    Write-Host "✓ Виртуальное окружение создано" -ForegroundColor Green
    Write-Host ""
}

# Активируем виртуальное окружение
Write-Host "Активация виртуального окружения..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка активации виртуального окружения" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}
Write-Host "✓ Виртуальное окружение активировано" -ForegroundColor Green
Write-Host ""

# Проверяем PyQt5
Write-Host "Проверка зависимостей..." -ForegroundColor Yellow
$pyqt5Installed = python -c "import PyQt5" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "PyQt5 не установлен. Устанавливаю зависимости..." -ForegroundColor Yellow
    Write-Host "Это может занять 1-3 минуты..." -ForegroundColor Yellow
    Write-Host ""
    
    # Обновляем pip
    python -m pip install --upgrade pip --quiet
    
    # Устанавливаем все зависимости
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Ошибка установки зависимостей" -ForegroundColor Red
        Write-Host "Попробуйте вручную:" -ForegroundColor Yellow
        Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
        Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
    Write-Host ""
    Write-Host "✓ Все зависимости установлены" -ForegroundColor Green
}

Write-Host "✓ Все готово к запуску" -ForegroundColor Green
Write-Host ""
Write-Host "Запуск приложения..." -ForegroundColor Cyan
Write-Host ""

# Запускаем приложение
python -m zzz_profiler.qt_app

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Ошибка запуска приложения" -ForegroundColor Red
    Write-Host ""
}

Read-Host "Нажмите Enter для выхода"
