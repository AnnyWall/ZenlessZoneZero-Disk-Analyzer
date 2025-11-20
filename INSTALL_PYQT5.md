# Установка PyQt5

## Быстрая установка

### Вариант 1: Автоматически (рекомендуется)

Просто запустите:
```bash
start_qt.bat
```

Скрипт автоматически установит PyQt5 если его нет.

### Вариант 2: Вручную

```bash
# Активируйте виртуальное окружение (если используете)
.venv\Scripts\activate

# Установите PyQt5
pip install PyQt5

# Запустите приложение
python -m zzz_profiler.qt_app
```

### Вариант 3: Через PowerShell

```powershell
.\start_qt.ps1
```

## Проверка установки

```bash
# Проверьте, что PyQt5 установлен
python -c "import PyQt5; print('PyQt5 установлен!')"

# Проверьте версию
pip show PyQt5
```

## Решение проблем

### Ошибка: "No module named 'PyQt5'"

**Решение 1:** Установите вручную
```bash
pip install PyQt5
```

**Решение 2:** Обновите pip
```bash
python -m pip install --upgrade pip
pip install PyQt5
```

**Решение 3:** Используйте виртуальное окружение
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Ошибка: "pip is not recognized"

Убедитесь, что Python добавлен в PATH:
1. Откройте "Изменение системных переменных среды"
2. Нажмите "Переменные среды"
3. Добавьте путь к Python в PATH

### Ошибка при установке на Windows

Попробуйте установить Visual C++ Redistributable:
https://aka.ms/vs/17/release/vc_redist.x64.exe

### Долгая установка

PyQt5 большая библиотека (~50 MB). Установка может занять 1-3 минуты.

## Альтернатива: PySide6

Если PyQt5 не устанавливается, можно использовать PySide6:

```bash
pip install PySide6
```

Затем в `qt_app.py` замените:
```python
from PyQt5.QtWidgets import ...
```

на:
```python
from PySide6.QtWidgets import ...
```

## Системные требования

- Python 3.7+
- Windows 7+ / Linux / macOS
- ~100 MB свободного места
- Интернет для установки

## Проверка работы

После установки запустите:
```bash
python -m zzz_profiler.qt_app
```

Должно открыться окно приложения с неоновым дизайном.

---

Если проблемы остались, создайте Issue на GitHub! 🚀
