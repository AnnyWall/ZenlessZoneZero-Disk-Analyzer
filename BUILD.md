# 🔨 Инструкция по сборке

## Сборка .exe файла

### Требования

- Python 3.10+
- PyInstaller
- Все зависимости из `requirements.txt`

### Автоматическая сборка (Windows)

Просто запустите:

```bash
build.bat
```

Скрипт автоматически:
1. Очистит старые сборки
2. Проверит/установит PyInstaller
3. Создаст .spec файл
4. Соберет приложение

### Ручная сборка

```bash
# 1. Установите PyInstaller
pip install pyinstaller

# 2. Соберите приложение
pyinstaller --clean ZZZ_Profiler.spec
```

### Результат

После успешной сборки:
- Исполняемый файл: `dist/ZZZ_Profiler.exe`
- Размер: ~50-80 MB (включает Python и все библиотеки)

## Структура .spec файла

Файл `ZZZ_Profiler.spec` содержит:

- **datas**: Включает папку `assets` с шрифтами и иконками
- **hiddenimports**: Явно указанные зависимости (enka, flask, PIL, customtkinter)
- **console=False**: Запуск без консоли
- **upx=True**: Сжатие для уменьшения размера
- **onefile**: Один .exe файл со всем необходимым

## Оптимизация размера

Для уменьшения размера .exe:

1. **Используйте виртуальное окружение** с минимальными зависимостями
2. **Исключите ненужные модули** в .spec файле
3. **Включите UPX сжатие** (уже включено)

## Тестирование

После сборки протестируйте:

```bash
# Запустите .exe
dist\ZZZ_Profiler.exe

# Проверьте:
# - Запуск без ошибок
# - Загрузка шрифтов и иконок
# - Работа API
# - Загрузка профилей
```

## Распространение

### Вариант 1: Один .exe файл

Текущая конфигурация создает один файл `ZZZ_Profiler.exe` со всем необходимым.

**Плюсы:**
- Легко распространять
- Не нужна установка

**Минусы:**
- Больший размер
- Медленнее запуск (распаковка)

### Вариант 2: Папка с файлами

Измените в .spec:
```python
exe = EXE(
    ...
    exclude_binaries=True,  # Добавьте эту строку
    ...
)

coll = COLLECT(  # Добавьте этот блок
    exe,
    a.binaries,
    a.datas,
    ...
)
```

**Плюсы:**
- Быстрее запуск
- Меньше размер каждого файла

**Минусы:**
- Нужно распространять всю папку

## Решение проблем

### Ошибка: "Failed to execute script"

- Проверьте, что все зависимости установлены
- Добавьте недостающие модули в `hiddenimports`
- Запустите с `console=True` для просмотра ошибок

### Ошибка: "No module named 'enka'"

Добавьте в .spec:
```python
hiddenimports=['enka', 'enka.zzz'],
```

### Ошибка: Assets не найдены

Проверьте путь в .spec:
```python
datas=[('zzz_profiler/assets', 'assets')],
```

### Большой размер .exe

1. Используйте чистое виртуальное окружение
2. Исключите ненужные библиотеки
3. Включите UPX сжатие

## CI/CD (GitHub Actions)

Для автоматической сборки при каждом релизе создайте `.github/workflows/build.yml`:

```yaml
name: Build

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: pyinstaller --clean ZZZ_Profiler.spec
      - uses: actions/upload-artifact@v2
        with:
          name: ZZZ_Profiler
          path: dist/ZZZ_Profiler.exe
```

---

Удачной сборки! 🚀
