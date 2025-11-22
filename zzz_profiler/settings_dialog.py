# zzz_profiler/settings_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal


class SettingsDialog(QDialog):
    """Диалог настроек"""
    language_changed = pyqtSignal(str)
    
    def __init__(self, localization, parent=None):
        super().__init__(parent)
        self.localization = localization
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(self.localization.get('settings'))
        self.setFixedSize(400, 200)
        self.setModal(True)
        
        # Стили
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #1A1B1E;
            }}
            QLabel {{
                color: #EAEAEA;
                font-size: 14px;
                font-weight: bold;
            }}
            QComboBox {{
                background-color: #1E2433;
                border: 2px solid #00E5FF;
                border-radius: 8px;
                padding: 8px;
                color: #EAEAEA;
                font-size: 14px;
                min-width: 200px;
            }}
            QComboBox:hover {{
                border-color: #00B8D4;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00E5FF;
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #1E2433;
                border: 2px solid #00E5FF;
                selection-background-color: #252D3F;
                color: #EAEAEA;
            }}
            QPushButton {{
                background-color: #00E5FF;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                color: #0A0E1A;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #00B8D4;
            }}
            QPushButton:pressed {{
                background-color: #0097A7;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel(self.localization.get('settings'))
        title.setStyleSheet("font-size: 18px; color: #00E5FF;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Выбор языка
        lang_layout = QHBoxLayout()
        lang_label = QLabel(self.localization.get('language') + ":")
        lang_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        languages = self.localization.get_available_languages()
        for code, name in languages.items():
            self.lang_combo.addItem(name, code)
        
        # Устанавливаем текущий язык
        current_index = self.lang_combo.findData(self.localization.language)
        if current_index >= 0:
            self.lang_combo.setCurrentIndex(current_index)
        
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)
        
        layout.addStretch()
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        apply_btn = QPushButton(self.localization.get('apply'))
        apply_btn.clicked.connect(self.apply_settings)
        buttons_layout.addWidget(apply_btn)
        
        close_btn = QPushButton(self.localization.get('close'))
        close_btn.clicked.connect(self.reject)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #252D3F;
                color: #EAEAEA;
            }
            QPushButton:hover {
                background-color: #2D3548;
            }
        """)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
    
    def apply_settings(self):
        """Применить настройки"""
        selected_lang = self.lang_combo.currentData()
        if selected_lang != self.localization.language:
            self.language_changed.emit(selected_lang)
        self.accept()
