# 🚀 Инструкция по загрузке на GitHub

## Шаг 1: Инициализация Git репозитория

```bash
# Инициализируйте Git (если еще не сделано)
git init

# Добавьте все файлы
git add .

# Создайте первый коммит
git commit -m "Initial commit: ZZZ Profiler with neon design"
```

## Шаг 2: Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com)
2. Нажмите "New repository"
3. Введите название: `zzz-profiler`
4. Описание: `Beautiful desktop app for Zenless Zone Zero profile analysis`
5. Выберите Public или Private
6. **НЕ** создавайте README, .gitignore или LICENSE (они уже есть)
7. Нажмите "Create repository"

## Шаг 3: Подключение к GitHub

```bash
# Добавьте remote репозиторий (замените YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/zzz-profiler.git

# Проверьте remote
git remote -v

# Отправьте код на GitHub
git branch -M main
git push -u origin main
```

## Шаг 4: Настройка репозитория

### Добавьте Topics (теги)

В настройках репозитория добавьте topics:
- `zenless-zone-zero`
- `zzz`
- `python`
- `customtkinter`
- `gui`
- `desktop-app`
- `game-tools`

### Добавьте описание

```
⚡ Beautiful desktop app for Zenless Zone Zero profile analysis with neon design
```

### Включите Issues и Discussions

В Settings → Features включите:
- ✅ Issues
- ✅ Discussions (опционально)

## Шаг 5: Добавьте скриншоты

1. Создайте папку `screenshots/` в корне проекта
2. Добавьте скриншоты приложения
3. Обновите README.md, добавив ссылки на скриншоты:

```markdown
## 📸 Скриншоты

![Main Interface](screenshots/main.png)
![Agent Details](screenshots/agent.png)
![Disk Analysis](screenshots/disks.png)
```

4. Закоммитьте и запушьте:

```bash
git add screenshots/ README.md
git commit -m "Add screenshots"
git push
```

## Шаг 6: Создайте Release (опционально)

1. Перейдите в Releases → Create a new release
2. Tag version: `v1.0.0`
3. Release title: `ZZZ Profiler v1.0.0 - Initial Release`
4. Описание:
```markdown
## 🎉 First Release

### Features
- ⚡ Beautiful neon design
- 📊 Agent analysis with ratings
- 💎 Disk quality evaluation
- 🎮 Mindscape and Core Skills visualization
- 🚀 Optimized performance

### Installation
Download and run `ZZZ_Profiler.exe` (Windows)
Or install from source (see README.md)
```

5. Прикрепите .exe файл (если есть)
6. Publish release

## Полезные команды Git

```bash
# Проверить статус
git status

# Добавить изменения
git add .

# Создать коммит
git commit -m "Your message"

# Отправить на GitHub
git push

# Создать новую ветку
git checkout -b feature/new-feature

# Переключиться на main
git checkout main

# Слить ветку
git merge feature/new-feature
```

## Готово! 🎉

Ваш проект теперь на GitHub и готов к использованию сообществом!
