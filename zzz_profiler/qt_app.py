"""
PyQt5 версия ZZZ Profiler - оптимизированная и быстрая
"""

import sys
import os
import requests
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QScrollArea,
    QFrame, QGridLayout, QSizePolicy, QDialog, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
from io import BytesIO

# Добавляем путь для импортов
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, os.path.abspath(os.path.join(application_path, '..')))
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from zzz_profiler.config import AGENT_METADATA, STAT_NORMALIZATION_VALUES, DISK_SET_NAMES
    from zzz_profiler.run import run_server
    from zzz_profiler.localization import Localization
    from zzz_profiler.settings_dialog import SettingsDialog
except ImportError:
    AGENT_METADATA, STAT_NORMALIZATION_VALUES, DISK_SET_NAMES = {}, {}, {}
    run_server = None
    Localization = None
    SettingsDialog = None

# Неоновая цветовая палитра
NEON_COLORS = {
    "background": "#0A0E1A",
    "panel_bg": "#1A1B1E",
    "card_bg": "#1E2433",
    "card_hover": "#252D3F",
    "border_neon": "#00E5FF",
    "text_main": "#EAEAEA",
    "text_secondary": "#8B92A8",
    "text_neon": "#00E5FF",
    "accent_purple": "#B388FF",
    "accent_pink": "#FF4081",
    "accent_green": "#69F0AE",
    "stat_highlight": "#FFB74D",
}

RANK_COLORS = {
    "SSS": "#FF1744",  # Ярко-красный для супер крутых сборок
    "SS": "#FFB74D",
    "S": "#BA68C8",
    "A": "#4FC3F7",
    "B": "#81C784",
    "C": "#FFF176",
    "D": "#8B92A8"
}

# Глобальные стили
GLOBAL_STYLE = f"""
QMainWindow {{
    background-color: {NEON_COLORS['background']};
}}

QWidget {{
    background-color: transparent;
    color: {NEON_COLORS['text_main']};
    font-family: 'Segoe UI', Arial;
    font-size: 14px;
}}

QLineEdit {{
    background-color: {NEON_COLORS['card_bg']};
    border: 2px solid {NEON_COLORS['border_neon']};
    border-radius: 8px;
    padding: 8px;
    color: {NEON_COLORS['text_main']};
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {NEON_COLORS['text_neon']};
}}

QPushButton {{
    background-color: {NEON_COLORS['border_neon']};
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    color: {NEON_COLORS['background']};
    font-weight: bold;
    font-size: 14px;
}}

QPushButton:hover {{
    background-color: {NEON_COLORS['text_neon']};
}}

QPushButton:pressed {{
    background-color: #00B8D4;
}}

QListWidget {{
    background-color: {NEON_COLORS['panel_bg']};
    border: none;
    border-radius: 8px;
    padding: 5px;
}}

QListWidget::item {{
    background-color: {NEON_COLORS['card_bg']};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 8px;
    margin: 2px;
    color: {NEON_COLORS['text_main']};
}}

QListWidget::item:selected {{
    background-color: {NEON_COLORS['card_hover']};
    border: 1px solid {NEON_COLORS['border_neon']};
}}

QListWidget::item:hover {{
    background-color: {NEON_COLORS['card_hover']};
}}

QScrollBar:vertical {{
    background-color: {NEON_COLORS['panel_bg']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {NEON_COLORS['border_neon']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {NEON_COLORS['text_neon']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QLabel {{
    background-color: transparent;
}}
"""


class FetchThread(QThread):
    """Поток для загрузки данных профиля"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
    
    def run(self):
        try:
            response = requests.get(f"http://127.0.0.1:5000/api/profile/{self.uid}", timeout=10)
            response.raise_for_status()
            data = response.json()
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class ImageManager:
    """Глобальный менеджер загрузки изображений"""
    CACHE_DIR = os.path.join(os.path.dirname(__file__), '.image_cache')
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.session = self._create_session()
        
        # Создаем директорию кеша
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)
    
    def _create_session(self):
        """Создать сессию с настройками"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        return session
    
    def get_cache_path(self, url):
        """Получить путь к кешированному файлу"""
        import hashlib
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.CACHE_DIR, f"{url_hash}.png")
    
    def load_image(self, url, size=(100, 100)):
        """Загрузить изображение (синхронно)"""
        cache_path = self.get_cache_path(url)
        
        # Проверяем кеш
        if os.path.exists(cache_path):
            pixmap = QPixmap(cache_path)
            if not pixmap.isNull():
                return pixmap.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Загружаем с сервера
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Сохраняем в кеш
            with open(cache_path, 'wb') as f:
                f.write(response.content)
            
            # Загружаем pixmap
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                return pixmap.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        except Exception as e:
            print(f"[ImageManager] Ошибка загрузки {url.split('/')[-1]}: {str(e)[:50]}")
        
        # Возвращаем placeholder
        return self._create_placeholder(size)
    
    def _create_placeholder(self, size):
        """Создать placeholder"""
        from PyQt5.QtGui import QPainter
        pixmap = QPixmap(size[0], size[1])
        pixmap.fill(QColor(NEON_COLORS['card_bg']))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor(NEON_COLORS['text_secondary']))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "?")
        painter.end()
        
        return pixmap


class ImageLoader(QThread):
    """Асинхронный загрузчик изображений"""
    finished = pyqtSignal(QPixmap)
    
    def __init__(self, url, size=(64, 64)):
        super().__init__()
        self.url = url
        self.size = size
        self.manager = ImageManager()
    
    def run(self):
        pixmap = self.manager.load_image(self.url, self.size)
        self.finished.emit(pixmap)


class CardFrame(QFrame):
    """Базовый класс для карточек с неоновым дизайном"""
    def __init__(self, border_color=None, parent=None):
        super().__init__(parent)
        if border_color is None:
            border_color = NEON_COLORS['border_neon']
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {NEON_COLORS['card_bg']};
                border: 2px solid {border_color};
                border-radius: 10px;
                padding: 10px;
            }}
        """)


class CoreSkillButton(QWidget):
    """Интерактивная кнопка Core Skill"""
    def __init__(self, letter, is_unlocked, parent=None):
        super().__init__(parent)
        self.letter = letter
        self.is_unlocked = is_unlocked
        self.is_hovered = False
        
        self.setFixedSize(38, 38)
        self.setMouseTracking(True)
    
    def enterEvent(self, event):
        """При наведении мыши"""
        self.is_hovered = True
        self.update()
    
    def leaveEvent(self, event):
        """При уходе мыши"""
        self.is_hovered = False
        self.update()
    
    def paintEvent(self, event):
        """Отрисовка с интерактивностью"""
        from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Размеры
        rect = self.rect()
        center_x = rect.width() / 2
        center_y = rect.height() / 2
        radius = min(rect.width(), rect.height()) / 2 - 2
        
        if self.is_unlocked:
            # Разблокированные - неоновый цвет
            if self.is_hovered:
                # При наведении - белое свечение
                pen = QPen(QColor("#FFFFFF"), 3)
                painter.setPen(pen)
                painter.setBrush(QBrush(QColor(NEON_COLORS['border_neon'])))
            else:
                pen = QPen(QColor(NEON_COLORS['border_neon']), 2)
                painter.setPen(pen)
                painter.setBrush(QBrush(QColor(NEON_COLORS['border_neon'])))
            
            painter.drawEllipse(int(center_x - radius), int(center_y - radius), 
                              int(radius * 2), int(radius * 2))
            
            # Текст
            painter.setPen(QColor(NEON_COLORS['background']))
            font = QFont('Segoe UI', 14, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self.letter)
            
        else:
            # Неразблокированные - серые
            pen = QPen(QColor(NEON_COLORS['text_secondary']), 2)
            painter.setPen(pen)
            
            if self.is_hovered:
                painter.setBrush(QBrush(QColor(NEON_COLORS['card_hover'])))
            else:
                painter.setBrush(QBrush(QColor(NEON_COLORS['card_bg'])))
            
            painter.drawEllipse(int(center_x - radius), int(center_y - radius), 
                              int(radius * 2), int(radius * 2))
            
            # Текст
            painter.setPen(QColor(NEON_COLORS['text_secondary']))
            font = QFont('Segoe UI', 13)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self.letter)


class ZZZProfilerQt(QMainWindow):
    def get_settings_path(self):
        """Получить путь к файлу настроек рядом с exe"""
        if getattr(sys, 'frozen', False):
            # Если запущен как exe (PyInstaller)
            application_path = os.path.dirname(sys.executable)
        else:
            # Если запущен как скрипт
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(application_path, 'settings.json')
    
    def load_language_setting(self):
        """Загрузить настройку языка"""
        try:
            import json
            config_path = self.get_settings_path()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return settings.get('language', 'en')
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
        return 'en'
    
    def __init__(self):
        super().__init__()
        
        # Инициализация локализации с загрузкой сохраненного языка
        saved_lang = self.load_language_setting()
        self.localization = Localization(saved_lang) if Localization else None
        
        self.setWindowTitle("⚡ ZZZ Profiler")
        self.setGeometry(100, 100, 1400, 900)
        
        self.current_agents_data = []
        self.current_agent_index = None
        self.image_cache = {}
        self.image_loaders = []  # Храним ссылки на загрузчики изображений
        
        self.init_ui()
        self.setStyleSheet(GLOBAL_STYLE)
    
    def init_ui(self):
        """Инициализация интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Левая панель
        self.create_left_panel(main_layout)
        
        # Правая панель
        self.create_right_panel(main_layout)
    
    def create_left_panel(self, parent_layout):
        """Создание левой панели"""
        left_panel = QWidget()
        left_panel.setFixedWidth(250)
        left_panel.setStyleSheet(f"background-color: {NEON_COLORS['panel_bg']};")
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок с кнопкой настроек
        title_container = QWidget()
        title_container.setStyleSheet(f"""
            background-color: {NEON_COLORS['card_bg']};
            border-radius: 10px;
        """)
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(15, 15, 15, 15)
        
        title_text = self.localization.get('app_title') if self.localization else "⚡ ZZZ PROFILER"
        title = QLabel(title_text)
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {NEON_COLORS['text_neon']};
        """)
        title_layout.addWidget(title)
        
        title_layout.addStretch()
        
        # Кнопка настроек
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(44, 44)
        settings_btn.setToolTip("Настройки")
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {NEON_COLORS['border_neon']}, 
                    stop:1 {NEON_COLORS['accent_purple']});
                border: none;
                border-radius: 22px;
                font-size: 20px;
                color: {NEON_COLORS['background']};
                padding: 0px;
                text-align: center;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {NEON_COLORS['text_neon']}, 
                    stop:1 {NEON_COLORS['accent_pink']});
            }}
            QPushButton:pressed {{
                background-color: {NEON_COLORS['accent_purple']};
            }}
        """)
        settings_btn.clicked.connect(self.open_settings)
        title_layout.addWidget(settings_btn)
        
        left_layout.addWidget(title_container)
        
        # Поле ввода UID
        input_layout = QHBoxLayout()
        self.uid_input = QLineEdit()
        placeholder = self.localization.get('search_placeholder') if self.localization else "Введите UID..."
        self.uid_input.setPlaceholderText(placeholder)
        self.uid_input.returnPressed.connect(self.fetch_profile)
        input_layout.addWidget(self.uid_input)
        
        search_btn_text = self.localization.get('search_button') if self.localization else "🔍"
        search_btn = QPushButton(search_btn_text)
        search_btn.setFixedWidth(45)
        search_btn.clicked.connect(self.fetch_profile)
        input_layout.addWidget(search_btn)
        
        left_layout.addLayout(input_layout)
        
        # Информация о игроке
        self.player_label = QLabel("")
        self.player_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {NEON_COLORS['text_neon']};
            padding: 5px;
        """)
        left_layout.addWidget(self.player_label)
        
        # Список агентов
        agents_text = self.localization.get('agents_title') if self.localization else "👥 АГЕНТЫ"
        agents_label = QLabel(agents_text)
        agents_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {NEON_COLORS['text_neon']};
            padding: 5px;
        """)
        left_layout.addWidget(agents_label)
        
        self.agent_list = QListWidget()
        self.agent_list.itemClicked.connect(self.on_agent_selected)
        left_layout.addWidget(self.agent_list)
        
        parent_layout.addWidget(left_panel)
    
    def create_right_panel(self, parent_layout):
        """Создание правой панели"""
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet(f"background-color: {NEON_COLORS['background']};")
        
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        
        # Приветственное сообщение
        welcome = CardFrame(NEON_COLORS['border_neon'])
        welcome_layout = QVBoxLayout(welcome)
        
        welcome_title_text = self.localization.get('welcome_title') if self.localization else "⚡ ZZZ PROFILER ⚡"
        welcome_title = QLabel(welcome_title_text)
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {NEON_COLORS['text_neon']};
        """)
        welcome_layout.addWidget(welcome_title)
        
        welcome_text_content = self.localization.get('welcome_text') if self.localization else "Введите UID и выберите агента\nдля просмотра детальной информации"
        welcome_text = QLabel(welcome_text_content)
        welcome_text.setAlignment(Qt.AlignCenter)
        welcome_text.setStyleSheet(f"color: {NEON_COLORS['text_secondary']}; font-size: 14px;")
        welcome_layout.addWidget(welcome_text)
        
        self.right_layout.addWidget(welcome, alignment=Qt.AlignCenter)
        self.right_layout.addStretch()
        
        parent_layout.addWidget(self.right_panel)
    
    def fetch_profile(self):
        """Загрузка профиля"""
        uid = self.uid_input.text().strip()
        if not uid:
            return
        
        loading_text = self.localization.get('loading') if self.localization else "Загрузка..."
        self.player_label.setText(loading_text)
        self.agent_list.clear()
        
        self.fetch_thread = FetchThread(uid)
        self.fetch_thread.finished.connect(self.on_profile_loaded)
        self.fetch_thread.error.connect(self.on_profile_error)
        self.fetch_thread.start()
    
    def on_profile_loaded(self, data):
        """Обработка загруженного профиля"""
        player_info = data.get('player', {})
        self.player_label.setText(f"{player_info.get('nickname', 'N/A')} (Ур. {player_info.get('level', 'N/A')})")
        
        self.current_agents_data = data.get('agents', [])
        
        # Заполняем список агентов
        self.agent_list.clear()
        for agent in self.current_agents_data:
            rank = agent.get('agent_rank', 'D')
            rank_indicator = {'SSS': '🔥', 'SS': '⭐⭐', 'S': '⭐', 'A': '▲', 'B': '●', 'C': '○', 'D': '·'}
            item_text = f"{rank_indicator.get(rank, '·')} {agent.get('name', 'N/A')}"
            self.agent_list.addItem(item_text)
        
        # Показываем первого агента
        if self.current_agents_data:
            self.agent_list.setCurrentRow(0)
            self.show_agent_details(0)
    
    def on_profile_error(self, error):
        """Обработка ошибки загрузки"""
        error_text = self.localization.get('error') if self.localization else "Ошибка"
        self.player_label.setText(f"{error_text}: {error}")
    
    def on_agent_selected(self, item):
        """Обработка выбора агента"""
        index = self.agent_list.row(item)
        self.show_agent_details(index)
    
    def open_settings(self):
        """Открыть диалог настроек"""
        if not SettingsDialog or not self.localization:
            return
        
        dialog = SettingsDialog(self.localization, self)
        dialog.language_changed.connect(self.change_language)
        dialog.exec_()
    
    def change_language(self, language):
        """Изменить язык интерфейса"""
        if self.localization:
            self.localization.set_language(language)
            # Сохраняем настройку
            self.save_language_setting(language)
            # Показываем сообщение о необходимости перезапуска
            self.show_restart_message(language)
    
    def save_language_setting(self, language):
        """Сохранить настройку языка"""
        try:
            import json
            config_path = self.get_settings_path()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({'language': language}, f, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def show_restart_message(self, language):
        """Показать сообщение о необходимости перезапуска"""
        from PyQt5.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Language Changed" if language == 'en' else "Язык изменен")
        
        if language == 'en':
            msg.setText("Language has been changed to English.\n\nPlease restart the application for changes to take effect.")
        else:
            msg.setText("Язык изменен на русский.\n\nПожалуйста, перезапустите приложение для применения изменений.")
        
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {NEON_COLORS['panel_bg']};
            }}
            QMessageBox QLabel {{
                color: {NEON_COLORS['text_main']};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {NEON_COLORS['border_neon']};
                color: {NEON_COLORS['background']};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {NEON_COLORS['text_neon']};
            }}
        """)
        msg.exec_()
    
    def show_agent_details(self, index):
        """Отображение деталей агента"""
        if index >= len(self.current_agents_data):
            return
        
        self.current_agent_index = index
        agent = self.current_agents_data[index]
        
        # Очищаем правую панель
        while self.right_layout.count():
            child = self.right_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Создаем scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(10)
        
        # Заголовок агента
        self.create_agent_header(content_layout, agent)
        
        # Характеристики, W-Engine, Навыки
        self.create_stats_section(content_layout, agent)
        
        # Диски
        self.create_disks_section(content_layout, agent)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        self.right_layout.addWidget(scroll)
    
    def _apply_circular_mask(self, label, pixmap, size):
        """Применить круглую маску к изображению"""
        if pixmap.isNull():
            return
        
        # Проверяем, что виджет еще существует
        try:
            if not label or label.isHidden():
                return
        except RuntimeError:
            # Виджет уже удален
            return
        
        from PyQt5.QtGui import QPainter, QPainterPath
        
        # Создаем круглое изображение
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Создаем круглую маску
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        
        # Рисуем изображение, масштабируя его до размера круга
        # Используем drawPixmap с целевым прямоугольником для заполнения
        painter.drawPixmap(0, 0, size, size, pixmap)
        painter.end()
        
        try:
            label.setPixmap(rounded)
        except RuntimeError:
            # Виджет был удален во время обработки
            pass
    
    def create_agent_header(self, layout, agent):
        """Создание заголовка агента"""
        header = CardFrame(NEON_COLORS['border_neon'])
        header_layout = QHBoxLayout(header)
        
        # Иконка агента (круглая)
        icon_container = QLabel()
        icon_container.setFixedSize(64, 64)
        icon_container.setAlignment(Qt.AlignCenter)
        icon_container.setStyleSheet("""
            QLabel {
                border: 3px solid #00E5FF;
                border-radius: 32px;
                background-color: #1E2433;
            }
        """)
        # Включаем маску для обрезки содержимого
        icon_container.setScaledContents(True)
        header_layout.addWidget(icon_container)
        
        # Пробуем разные варианты структуры данных для иконки
        icon_url = None
        icon_data = agent.get("icon")
        if isinstance(icon_data, dict):
            icon_url = icon_data.get("round") or icon_data.get("image") or icon_data.get("url")
        elif isinstance(icon_data, str):
            icon_url = icon_data
        
        if icon_url:
            # Загружаем через менеджер (большого размера для заполнения круга)
            manager = ImageManager()
            cache_path = manager.get_cache_path(icon_url)
            
            if os.path.exists(cache_path):
                # Из кеша - мгновенно
                pixmap = manager.load_image(icon_url, (150, 150))
                self._apply_circular_mask(icon_container, pixmap, 60)
            else:
                # Асинхронная загрузка
                loader = ImageLoader(icon_url, (150, 150))
                loader.finished.connect(lambda p: self._apply_circular_mask(icon_container, p, 60))
                self.image_loaders.append(loader)
                loader.start()
        
        # Информация
        info_layout = QVBoxLayout()
        
        # Имя и ранг
        name_layout = QHBoxLayout()
        agent_name = agent.get('name', 'N/A')
        # Переводим имя агента
        agent_name_translated = self.localization.get(agent_name, agent_name) if self.localization else agent_name
        name_label = QLabel(agent_name_translated)
        name_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {NEON_COLORS['text_neon']};
        """)
        name_layout.addWidget(name_label)
        
        rank = agent.get('agent_rank', 'D')
        rank_label = QLabel(f" {rank} ")
        rank_label.setStyleSheet(f"""
            background-color: {RANK_COLORS.get(rank)};
            color: {NEON_COLORS['background']};
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 6px;
        """)
        name_layout.addWidget(rank_label)
        name_layout.addStretch()
        
        info_layout.addLayout(name_layout)
        
        # Метаданные
        meta = AGENT_METADATA.get(agent.get('name'), {})
        specialty_icons = {
            'Attack': '⚔️', 'Anomaly': '⚡', 'Stun': '💥',
            'Defense': '🛡️', 'Support': '💚', 'Rupture': '🔨'
        }
        specialty = meta.get('specialty', 'N/A')
        specialty_icon = specialty_icons.get(specialty, '❓')
        # Переводим специальность
        specialty_translated = self.localization.get(specialty, specialty) if self.localization else specialty
        
        rarity = agent.get('rarity', 'S')
        rarity_display = f"[{rarity}]" if isinstance(rarity, str) else '⭐' * int(rarity)
        
        level_text = self.localization.get('level') if self.localization else "Ур."
        meta_label = QLabel(f"{level_text} {agent.get('level')} | {specialty_icon} {specialty_translated} | {rarity_display}")
        meta_label.setStyleSheet(f"color: {NEON_COLORS['text_secondary']};")
        info_layout.addWidget(meta_label)
        
        # Общий счет
        score_text = self.localization.get('total_score') if self.localization else "⭐ Общий счет"
        score_label = QLabel(f"{score_text}: {agent.get('total_score', 'N/A')}")
        score_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {RANK_COLORS.get(rank)};
        """)
        info_layout.addWidget(score_label)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addWidget(header)
    
    def create_stats_section(self, layout, agent):
        """Создание секции характеристик, W-Engine и навыков"""
        # Контейнер для трех колонок
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setSpacing(10)
        
        # Колонка 1: Характеристики
        stats_card = self.create_stats_card(agent)
        stats_layout.addWidget(stats_card, 3)
        
        # Колонка 2: W-Engine
        engine_card = self.create_engine_card(agent)
        stats_layout.addWidget(engine_card, 2)
        
        # Колонка 3: Навыки и прогресс
        skills_card = self.create_skills_card(agent)
        stats_layout.addWidget(skills_card, 2)
        
        layout.addWidget(stats_widget)
    
    def create_stats_card(self, agent):
        """Создание карточки характеристик (упрощенная)"""
        card = CardFrame(NEON_COLORS['border_neon'])
        card_layout = QVBoxLayout(card)
        
        # Заголовок
        title_text = self.localization.get('stats_title') if self.localization else "⚡ ХАРАКТЕРИСТИКИ"
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {NEON_COLORS['text_neon']};
            padding: 5px 0px 15px 0px;
        """)
        card_layout.addWidget(title)
        
        # Сетка статов (простой текст без рамок)
        stats_grid = QGridLayout()
        stats_grid.setSpacing(12)
        stats_grid.setContentsMargins(10, 0, 10, 0)
        
        stats_to_show = [
            "HP", "ATK", "DEF", 
            "CRIT Rate", "CRIT DMG", "Energy Regen",
            "Anomaly Mastery", "Sheer Force", "Impact"
        ]
        
        row = 0
        for stat_name in stats_to_show:
            stat_obj = next((s for s in agent.get('stats', {}).values() if s['name'] == stat_name), None)
            if stat_obj:
                # Название стата
                name_label = QLabel(stat_name)
                name_label.setStyleSheet(f"""
                    color: {NEON_COLORS['text_secondary']}; 
                    font-size: 13px; 
                    background: transparent;
                    border: none;
                    padding: 4px 0px;
                """)
                stats_grid.addWidget(name_label, row, 0)
                
                # Значение стата
                value_label = QLabel(stat_obj['formatted_value'])
                value_label.setAlignment(Qt.AlignRight)
                value_label.setStyleSheet(f"""
                    color: {NEON_COLORS['text_main']}; 
                    font-weight: bold; 
                    font-size: 14px; 
                    background: transparent;
                    border: none;
                    padding: 4px 0px;
                """)
                stats_grid.addWidget(value_label, row, 1)
                
                row += 1
        
        card_layout.addLayout(stats_grid)
        card_layout.addStretch()
        
        return card
    
    def create_engine_card(self, agent):
        """Создание карточки W-Engine"""
        card = CardFrame(NEON_COLORS['accent_purple'])
        card_layout = QVBoxLayout(card)
        
        # Заголовок
        title_text = self.localization.get('w_engine_title') if self.localization else "⚙️ W-ENGINE"
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {NEON_COLORS['accent_purple']};
            padding: 5px;
        """)
        card_layout.addWidget(title)
        
        w_engine = agent.get('w_engine')
        if w_engine:
            # Иконка - увеличиваем размер чтобы изображение не обрезалось
            icon_label = QLabel()
            icon_label.setFixedSize(120, 120)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setScaledContents(False)
            icon_label.setStyleSheet("border: none; background: transparent;")
            card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
            
            # Пробуем разные варианты структуры данных для иконки
            icon_url = None
            icon_data = w_engine.get('icon')
            if isinstance(icon_data, dict):
                icon_url = icon_data.get("url") or icon_data.get("round")
            elif isinstance(icon_data, str):
                icon_url = icon_data
            
            if icon_url:
                # Сначала проверяем кеш синхронно (быстро)
                import hashlib
                cache_dir = os.path.join(os.path.dirname(__file__), '.image_cache')
                url_hash = hashlib.md5(icon_url.encode()).hexdigest()
                cache_path = os.path.join(cache_dir, f"{url_hash}.png")
                
                if os.path.exists(cache_path):
                    # Из кеша - мгновенно
                    pixmap = QPixmap(cache_path)
                    if not pixmap.isNull():
                        # Масштабируем до 110x110 чтобы поместилось в контейнер 120x120
                        pixmap = pixmap.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        icon_label.setPixmap(pixmap)
                else:
                    # Нет в кеше - загружаем асинхронно
                    loader = ImageLoader(icon_url, (110, 110))
                    loader.finished.connect(icon_label.setPixmap)
                    self.image_loaders.append(loader)
                    loader.start()
            
            # Название
            name_label = QLabel(w_engine.get('name', 'N/A'))
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setWordWrap(True)
            name_label.setStyleSheet(f"""
                font-weight: bold;
                color: {NEON_COLORS['accent_purple']};
                font-size: 14px;
            """)
            card_layout.addWidget(name_label)
            
            # Уровень
            level_label = QLabel(f"Ур. {w_engine.get('level', 0)}")
            level_label.setAlignment(Qt.AlignCenter)
            level_label.setStyleSheet(f"color: {NEON_COLORS['text_secondary']}; font-size: 12px;")
            card_layout.addWidget(level_label)
            
            # Статы
            main_stat = w_engine.get('main_stat', {})
            if main_stat:
                stat_label = QLabel(f"▸ {main_stat.get('name')}: {main_stat.get('formatted_value')}")
                stat_label.setStyleSheet(f"color: {NEON_COLORS['text_main']}; font-size: 12px;")
                stat_label.setWordWrap(True)
                card_layout.addWidget(stat_label)
            
            sub_stat = w_engine.get('sub_stat', {})
            if sub_stat:
                stat_label = QLabel(f"▸ {sub_stat.get('name')}: {sub_stat.get('formatted_value')}")
                stat_label.setStyleSheet(f"color: {NEON_COLORS['text_main']}; font-size: 12px;")
                stat_label.setWordWrap(True)
                card_layout.addWidget(stat_label)
        
        card_layout.addStretch()
        return card
    
    def create_skills_card(self, agent):
        """Создание карточки навыков и прогресса"""
        card = CardFrame(NEON_COLORS['accent_pink'])
        card_layout = QVBoxLayout(card)
        
        # Заголовок
        title_text = self.localization.get('progress_title') if self.localization else "✨ ПРОГРЕСС АГЕНТА"
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {NEON_COLORS['accent_pink']};
            padding: 5px;
        """)
        card_layout.addWidget(title)
        
        # Mindscape
        mindscape_text = self.localization.get('mindscape') if self.localization else "🌟 Mindscape (Созвездия)"
        mindscape_label = QLabel(mindscape_text)
        mindscape_label.setStyleSheet(f"color: {NEON_COLORS['accent_purple']}; font-weight: bold; font-size: 13px;")
        card_layout.addWidget(mindscape_label)
        
        mindscape_widget = self.create_mindscape_widget(agent.get('mindscape', 0))
        card_layout.addWidget(mindscape_widget)
        
        # Core Skills
        core_text = self.localization.get('core_skills') if self.localization else "💎 Core Skill (Пассивки)"
        core_label = QLabel(core_text)
        core_label.setStyleSheet(f"color: {NEON_COLORS['border_neon']}; font-weight: bold; font-size: 13px; margin-top: 10px;")
        card_layout.addWidget(core_label)
        
        core_widget = self.create_core_skills_widget(agent.get('core_skill_level_num', 0))
        card_layout.addWidget(core_widget)
        
        # Боевые навыки
        skills_text = self.localization.get('battle_skills') if self.localization else "⚔️ Боевые навыки"
        skills_label = QLabel(skills_text)
        skills_label.setStyleSheet(f"color: {NEON_COLORS['text_main']}; font-weight: bold; font-size: 13px; margin-top: 10px;")
        card_layout.addWidget(skills_label)
        
        skills_widget = self.create_battle_skills_widget(agent.get('skills', []))
        card_layout.addWidget(skills_widget)
        
        card_layout.addStretch()
        return card
    
    def create_mindscape_widget(self, level):
        """Создание виджета Mindscape"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 5, 0, 5)
        
        for i in range(6):
            is_unlocked = i < level
            
            circle = QLabel(str(i + 1))
            circle.setFixedSize(30, 30)
            circle.setAlignment(Qt.AlignCenter)
            
            if is_unlocked:
                circle.setStyleSheet(f"""
                    background-color: {NEON_COLORS['accent_purple']};
                    color: {NEON_COLORS['background']};
                    border: 2px solid {NEON_COLORS['accent_purple']};
                    border-radius: 15px;
                    font-weight: bold;
                    font-size: 12px;
                """)
            else:
                circle.setStyleSheet(f"""
                    background-color: {NEON_COLORS['card_bg']};
                    color: {NEON_COLORS['text_secondary']};
                    border: 2px solid {NEON_COLORS['text_secondary']};
                    border-radius: 15px;
                    font-size: 12px;
                """)
            
            layout.addWidget(circle)
        
        return widget
    
    def create_core_skills_widget(self, level):
        """Создание виджета Core Skills с интерактивностью"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 5, 0, 5)
        
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for i, letter in enumerate(letters):
            is_unlocked = i < level
            
            # Создаем кастомный виджет с интерактивностью
            skill_widget = CoreSkillButton(letter, is_unlocked)
            layout.addWidget(skill_widget)
        
        return widget
    
    def create_battle_skills_widget(self, skills):
        """Создание виджета боевых навыков"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(3)
        layout.setContentsMargins(0, 5, 0, 5)
        
        skill_icons = {
            0: "👊",  # ATK
            1: "✨",  # SPECIAL
            3: "💫",  # ULT
            2: "🌀",  # DODGE
            6: "🛡️"   # PARRY
        }
        
        skill_colors = {
            0: "#E0E0E0",
            1: "#4FC3F7",
            3: "#FFB74D",
            2: "#81C784",
            6: "#81C784"
        }
        
        skills_dict = {skill['type']: skill for skill in skills}
        # Порядок: удар, уклонение, парирование, способность, ульта
        skills_order = [0, 2, 6, 1, 3]
        
        for skill_type in skills_order:
            if skill := skills_dict.get(skill_type):
                skill_widget = QWidget()
                skill_layout = QVBoxLayout(skill_widget)
                skill_layout.setSpacing(2)
                skill_layout.setContentsMargins(2, 2, 2, 2)
                
                # Иконка
                icon_label = QLabel(skill_icons.get(skill_type, "❓"))
                icon_label.setAlignment(Qt.AlignCenter)
                icon_label.setStyleSheet("font-size: 20px;")
                skill_layout.addWidget(icon_label)
                
                # Уровень
                level_label = QLabel(f"Ур.{skill['level']}")
                level_label.setAlignment(Qt.AlignCenter)
                level_label.setStyleSheet(f"""
                    background-color: {skill_colors.get(skill_type, '#E0E0E0')};
                    color: {NEON_COLORS['background']};
                    border-radius: 6px;
                    padding: 2px 4px;
                    font-weight: bold;
                    font-size: 10px;
                """)
                skill_layout.addWidget(level_label)
                
                skill_widget.setStyleSheet(f"""
                    QWidget {{
                        background-color: {NEON_COLORS['card_bg']};
                        border: 2px solid {skill_colors.get(skill_type, '#E0E0E0')};
                        border-radius: 8px;
                    }}
                """)
                skill_widget.setFixedWidth(45)
                
                layout.addWidget(skill_widget)
        
        return widget
    
    def create_disks_section(self, layout, agent):
        """Создание секции дисков"""
        # Заголовок (просто текст, без рамки)
        disks_text = self.localization.get('disks_title') if self.localization else "💿 ДИСКИ"
        disks_title = QLabel(disks_text)
        disks_title.setAlignment(Qt.AlignCenter)
        disks_title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {NEON_COLORS['accent_green']};
            padding: 10px;
        """)
        layout.addWidget(disks_title)
        
        # Сетка дисков
        disks_widget = QWidget()
        disks_grid = QGridLayout(disks_widget)
        disks_grid.setSpacing(10)
        
        discs = [d for d in agent.get('discs', []) if d]
        for i, disc in enumerate(discs):
            row, col = divmod(i, 3)
            disk_card = self.create_disk_card(disc, i)
            disks_grid.addWidget(disk_card, row, col)
        
        layout.addWidget(disks_widget)
    
    def create_disk_card(self, disc, index):
        """Создание карточки диска"""
        rank = disc.get('rank', 'D')
        border_colors = {
            'SSS': "#FF1744",  # Ярко-красный для супер крутых сборок
            'SS': NEON_COLORS["accent_purple"],
            'S': NEON_COLORS["accent_pink"],
            'A': NEON_COLORS["border_neon"],
            'B': NEON_COLORS["accent_green"],
            'C': NEON_COLORS["text_secondary"],
            'D': NEON_COLORS["text_secondary"]
        }
        
        card = CardFrame(border_colors.get(rank))
        card_layout = QVBoxLayout(card)
        
        # Заголовок
        set_id = disc.get('set_id')
        set_name = DISK_SET_NAMES.get(set_id, disc.get('set_name', f"Set ID {set_id}"))
        # Переводим название диска
        set_name_translated = self.localization.get(set_name, set_name) if self.localization else set_name
        
        disk_text = self.localization.get('disk') if self.localization else "Диск"
        title = QLabel(f"💎 {disk_text} {index + 1}: {set_name_translated}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-weight: bold; color: {NEON_COLORS['text_main']}; font-size: 13px;")
        title.setWordWrap(True)
        card_layout.addWidget(title)
        
        # Ранг и уровень по центру
        rank_label = QLabel(f"[{rank}] +{disc.get('level')}")
        rank_label.setAlignment(Qt.AlignCenter)
        rank_label.setStyleSheet(f"""
            color: {RANK_COLORS.get(rank)}; 
            font-weight: bold;
            font-size: 14px;
        """)
        card_layout.addWidget(rank_label)
        
        # Оценка диска по центру
        rating_label = QLabel(f"⭐ {disc.get('rating')}")
        rating_label.setAlignment(Qt.AlignCenter)
        rating_label.setStyleSheet(f"""
            color: {RANK_COLORS.get(rank)}; 
            font-weight: bold;
            font-size: 16px;
            padding: 5px 0px;
        """)
        card_layout.addWidget(rating_label)
        
        # Основной стат по центру
        main_stat = disc.get('main_stat', {})
        main_label = QLabel(f"{main_stat.get('name')}\n{main_stat.get('formatted_value')}")
        main_label.setAlignment(Qt.AlignCenter)
        main_label.setStyleSheet(f"""
            color: {NEON_COLORS['text_main']}; 
            font-weight: bold; 
            font-size: 13px;
            padding: 8px 0px;
        """)
        card_layout.addWidget(main_label)
        
        # Подстаты в общей рамке
        substats_frame = QFrame()
        substats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {NEON_COLORS['card_hover']};
                border: 1px solid {NEON_COLORS['text_secondary']};
                border-radius: 6px;
                padding: 5px;
            }}
        """)
        substats_layout = QVBoxLayout(substats_frame)
        substats_layout.setContentsMargins(5, 5, 5, 5)
        substats_layout.setSpacing(2)
        
        weights = disc.get('calculation_weights', {})
        for sub_stat in disc.get('sub_stats', []):
            stat_name = sub_stat.get('name', 'N/A')
            formatted_value = sub_stat.get('formatted_value', '0')
            raw_value = sub_stat.get('value', 0)
            
            normalization_value = STAT_NORMALIZATION_VALUES.get(stat_name, 1.0)
            usefulness_score = 0.0
            
            if normalization_value > 0:
                is_percent = '%' in sub_stat.get('format', '')
                actual_value = raw_value / 100.0 if is_percent else raw_value
                num_rolls = actual_value / normalization_value
                weight = weights.get(stat_name, 0)
                usefulness_score = num_rolls * weight
            
            # Желтый для полезных статов, серый для бесполезных
            color = NEON_COLORS["stat_highlight"] if usefulness_score > 0 else NEON_COLORS["text_secondary"]
            
            sub_label = QLabel(f"• {stat_name}: {formatted_value}  [{usefulness_score:+.1f}]")
            sub_label.setStyleSheet(f"color: {color}; font-size: 12px; background: transparent; border: none;")
            substats_layout.addWidget(sub_label)
        
        card_layout.addWidget(substats_frame)
        
        return card


def start_backend():
    """Запуск backend API сервера в фоновом потоке"""
    if run_server:
        print(">>> Запуск фонового API-сервера...")
        run_server()


def wait_for_server(max_attempts=10, delay=0.5):
    """Ожидание готовности сервера"""
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://127.0.0.1:5000", timeout=1)
            print(f">>> Сервер готов (попытка {attempt + 1}).")
            return True
        except (requests.ConnectionError, requests.Timeout):
            if attempt < max_attempts - 1:
                time.sleep(delay)
    return False


def main():
    # Запускаем backend сервер в фоновом потоке
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    print(">>> Ожидание готовности сервера...")
    if not wait_for_server():
        print("!!! ПРЕДУПРЕЖДЕНИЕ: Сервер не отвечает, но GUI будет запущен.")
    
    print(">>> Запуск GUI приложения...")
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ZZZProfilerQt()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
