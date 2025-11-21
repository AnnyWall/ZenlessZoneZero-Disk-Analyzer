# ⚡ ZZZ Profiler

Красивое desktop-приложение для анализа профилей игроков Zenless Zone Zero с неоновым дизайном на PyQt5.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)

---

## 🇷🇺 Русская версия

### 🎮 Возможности

- **Детальный анализ агентов**: характеристики, навыки, W-Engine и диски
- **Система рейтингов**: автоматическая оценка дисков (SSS, SS, S, A, B, C, D)
- **Визуализация прогресса**: Mindscape (созвездия) и Core Skills (пассивки)
- **Неоновый дизайн**: современный киберпанк интерфейс
- **Интерактивные элементы**: эффекты свечения при наведении
- **Оптимизированная производительность**: плавная работа без лагов

### 📥 Для обычных пользователей

#### Установка через релизы (рекомендуется)

1. Перейдите на страницу [Releases](https://github.com/AnnyWall/ZenlessZoneZero-Disk-Analyzer/releases)
2. Скачайте последнюю версию `ZZZ_Profiler.exe`
3. Запустите файл - приложение готово к использованию!

**Примечание**: При первом запуске Windows может показать предупреждение SmartScreen. Нажмите "Подробнее" → "Выполнить в любом случае"

#### Использование

1. Введите UID игрока в поле ввода
2. Нажмите кнопку поиска 🔍
3. Выберите агента из списка слева
4. Просматривайте детальную информацию справа

### 🛠️ Для разработчиков

#### Требования

- Python 3.10 или выше
- Windows / Linux / macOS

#### Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/AnnyWall/ZenlessZoneZero-Disk-Analyzer.git
cd zzz-profiler

# Установите PyQt5 (автоматически)
install_pyqt5.bat

# Или вручную
pip install -r requirements.txt
```

#### Запуск из исходников

**Windows (батник):**
```bash
start_qt.bat
```

**PowerShell:**
```bash
.\start_qt.ps1
```

**Или напрямую:**
```bash
python -m zzz_profiler
```

#### Сборка .exe

```bash
# Запустите автоматическую сборку
build.bat
```

Готовый .exe будет в папке `dist/`


### 🎨 Особенности интерфейса

#### Цветовая индикация рангов

- **SSS** 🔥 (Красный) - Супер крутая сборка!
- **SS** (Оранжевый) - Отличное качество
- **S** (Фиолетовый) - Очень хорошее качество
- **A** (Голубой) - Хорошее качество
- **B** (Зеленый) - Среднее качество
- **C** (Желтый) - Ниже среднего
- **D** (Серый) - Низкое качество

#### Визуализация навыков

- 👊 Базовая атака
- ✨ Особая атака
- 💫 Ульта
- 🌀 Уклонение
- �️  Парирование

### 🔧 Технологии

- **PyQt5** - современный GUI фреймворк
- **Flask** - backend API сервер
- **enka.py** - библиотека для работы с Enka Network API
- **Pillow** - обработка изображений
- **Requests** - HTTP запросы с connection pooling

---

## 🇬🇧 English Version

### 🎮 Features

- **Detailed agent analysis**: stats, skills, W-Engine and disks
- **Rating system**: automatic disk quality assessment (SSS, SS, S, A, B, C, D)
- **Progress visualization**: Mindscape (constellations) and Core Skills (passives)
- **Neon design**: modern cyberpunk interface
- **Interactive elements**: glow effects on hover
- **Optimized performance**: smooth operation without lags

### 📥 For Regular Users

#### Installation via Releases (recommended)

1. Go to [Releases](https://github.com/AnnyWall/ZenlessZoneZero-Disk-Analyzer/releases) page
2. Download the latest `ZZZ_Profiler.exe`
3. Run the file - the app is ready to use!

**Note**: On first launch, Windows may show SmartScreen warning. Click "More info" → "Run anyway"

#### Usage

1. Enter player UID in the input field
2. Click the search button 🔍
3. Select an agent from the list on the left
4. View detailed information on the right

### 🛠️ For Developers

#### Requirements

- Python 3.10 or higher
- Windows / Linux / macOS

#### Installation

```bash
# Clone the repository
git clone https://github.com/AnnyWall/ZenlessZoneZero-Disk-Analyzer.git
cd zzz-profiler

# Install PyQt5 (automatically)
install_pyqt5.bat

# Or manually
pip install -r requirements.txt
```

#### Running from source

**Windows (batch):**
```bash
start_qt.bat
```

**PowerShell:**
```bash
.\start_qt.ps1
```

**Or directly:**
```bash
python -m zzz_profiler
```

#### Building .exe

```bash
# Run automatic build
build.bat
```

The ready .exe will be in the `dist/` folder


### 🎨 Interface Features

#### Rank Color Coding

- **SSS** 🔥 (Red) - Super awesome build!
- **SS** (Orange) - Excellent quality
- **S** (Purple) - Very good quality
- **A** (Blue) - Good quality
- **B** (Green) - Average quality
- **C** (Yellow) - Below average
- **D** (Gray) - Low quality

#### Skill Visualization

- 👊 Basic Attack
- ✨ Special Attack
- 💫 Ultimate
- 🌀 Dodge
- 🛡️ Parry

### 🔧 Technologies

- **PyQt5** - modern GUI framework
- **Flask** - backend API server
- **enka.py** - library for Enka Network API
- **Pillow** - image processing
- **Requests** - HTTP requests with connection pooling

---

## 📦 Project Structure

```
zzz-profiler/
├── zzz_profiler/          # Main application package
│   ├── assets/            # Resources (fonts, icons)
│   ├── services/          # Services (rating calculation)
│   ├── api.py            # API for data retrieval
│   ├── qt_app.py         # Main PyQt5 GUI application
│   ├── config.py         # Configuration and metadata
│   └── __main__.py       # Entry point
├── requirements.txt       # Python dependencies
├── build.bat             # Build script
├── README.md             # Documentation
└── LICENSE               # License
```

## 🤝 Contributing

Contributions are welcome! Feel free to create Issues and Pull Requests.

## 📄 License

GPL-3.0 License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- [Enka Network](https://enka.network/) for providing the API
- Zenless Zone Zero community for support

## ⚠️ Disclaimer

This is an unofficial application, not affiliated with HoYoverse. Use at your own risk.

---

If you want support me, there is my uid:1307801758(Asia)
