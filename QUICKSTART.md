# ⚡ Быстрый старт

## Для пользователей

### Windows

1. Скачайте `ZZZ_Profiler.exe` из [Releases](https://github.com/YOUR_USERNAME/zzz-profiler/releases)
2. Запустите файл
3. Введите UID игрока
4. Наслаждайтесь!

### Из исходного кода

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/YOUR_USERNAME/zzz-profiler.git
cd zzz-profiler

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Запустите
python -m zzz_profiler
```

## Для разработчиков

### Настройка окружения

```bash
# Создайте виртуальное окружение
python -m venv .venv

# Активируйте
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Установите зависимости
pip install -r requirements.txt
```

### Структура проекта

```
zzz_profiler/
├── beautiful_app.py    # Главное GUI
├── api.py             # Backend API
├── config.py          # Конфигурация
├── performance_config.py  # Настройки производительности
└── services/
    └── rating_calculator.py  # Расчет рейтингов
```

### Запуск в режиме разработки

```bash
python -m zzz_profiler
```

### Сборка .exe

```bash
pyinstaller ZZZ_Profiler.spec
```

## Получение UID

1. Откройте Zenless Zone Zero
2. Перейдите в настройки
3. Найдите свой UID (обычно в правом нижнем углу)
4. Убедитесь, что профиль открыт для просмотра

## Поддержка

- 🐛 [Сообщить об ошибке](https://github.com/YOUR_USERNAME/zzz-profiler/issues)
- 💡 [Предложить функцию](https://github.com/YOUR_USERNAME/zzz-profiler/issues)
- 📖 [Документация](README.md)

---

Приятного использования! 🎮
