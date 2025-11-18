# =================================================================
# ==           ZZZ Showcase Profiler PowerShell Launcher         ==
# =================================================================
# Этот скрипт является основной точкой входа.

# Устанавливаем текущую директорию на местоположение скрипта, чтобы все пути работали
Set-Location -Path $PSScriptRoot

Write-Host "--- ZZZ Showcase Profiler ---" -ForegroundColor Cyan

# --- Шаг 1: Создание/Проверка виртуального окружения ---
if (-not (Test-Path -Path ".\.venv" -PathType Container)) {
    Write-Host "[1/4] Sozdaniye virtual'nogo okruzheniya..." -ForegroundColor Yellow
    python -m venv .venv
}

# --- Шаг 2: Установка зависимостей ---
Write-Host "[2/4] Ustanovka bibliotek..." -ForegroundColor Yellow
try {
    # Прямой вызов pip для максимальной надежности
    .\.venv\Scripts\pip.exe install -r requirements.txt
} catch {
    Write-Host "[!] OSHIBKA pri ustanovke bibliotek:" -ForegroundColor Red
    Write-Host $_
    Read-Host "Nazhmite Enter dlya vykhoda."
    exit
}

# --- Шаг 3: Запуск фонового API-сервера ---
Write-Host "[3/4] Zapusk API-servera v fone..." -ForegroundColor Yellow
$backend_process = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m zzz_profiler.run" -NoNewWindow -PassThru
Start-Sleep -Seconds 3 # Даем серверу время на запуск

# --- Шаг 4: Запуск GUI ---
Write-Host "[4/4] Zapusk prilozheniya..." -ForegroundColor Green
$gui_process = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m zzz_profiler" -Wait -PassThru

# --- Завершение работы ---
# Этот код выполнится ПОСЛЕ того, как вы закроете окно приложения
Write-Host "Prilozheniye zakryto. Zaversheniye raboty fonovogo servera..."
Stop-Process -Id $backend_process.Id -Force

Write-Host "Rabota zavershena."
Start-Sleep -Seconds 2