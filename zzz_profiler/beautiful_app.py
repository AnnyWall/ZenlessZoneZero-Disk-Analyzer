# beautiful_app.py

import customtkinter as ctk
import requests
import threading
from PIL import Image, ImageDraw
import io
import os
from concurrent.futures import ThreadPoolExecutor

try:
    from zzz_profiler.config import AGENT_METADATA, STAT_NORMALIZATION_VALUES, DISK_SET_NAMES
    from zzz_profiler.performance_config import PERFORMANCE_CONFIG
except ImportError:
    AGENT_METADATA, STAT_NORMALIZATION_VALUES, DISK_SET_NAMES = {}, {}, {}
    PERFORMANCE_CONFIG = {'resize_debounce_delay': 150, 'image_load_timeout': 5, 'api_request_timeout': 10}

# --- ЦВЕТОВАЯ ПАЛИТРА "NEON" ---
NEON_THEME = {
    "background": "#0A0E1A",
    "panel_bg": "#1A1B1E",
    "card_bg": "#1E2433",
    "card_bg_hover": "#252D3F",
    "border_neon": "#00E5FF",
    "border_neon_glow": "#00B8D4",
    "text_main": "#EAEAEA",
    "text_secondary": "#8B92A8",
    "text_neon": "#00E5FF",
    "hover_color": "#005662",
    "stat_highlight": "#FFB74D",
    "accent_purple": "#B388FF",
    "accent_pink": "#FF4081",
    "accent_green": "#69F0AE",
    "gradient_start": "#00E5FF",
    "gradient_end": "#B388FF"
}

# --- Настройки ---
ctk.set_appearance_mode("Dark")

# Оптимизация рендеринга для Windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Включаем DPI awareness
except:
    pass

RANK_COLORS = {"SS": "#FFB74D", "S": "#BA68C8", "A": "#4FC3F7", "B": "#81C784", "C": "#FFF176", "D": NEON_THEME["text_secondary"]}
ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
SKILL_INFO = {0: ["ATK", "#E0E0E0"], 1: ["SPECIAL", "#4FC3F7"], 3: ["ULT", "#FFB74D"], 2: ["DODGE", "#81C784"], 6: ["PARRY", "#81C784"]}

class ZZZProfilerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ZZZ Showcase Profiler")
        self.geometry("1400x900")
        
        # Оптимизация для плавности
        try:
            self._scaling_factor = ctk.ScalingTracker.get_window_dpi_scaling(self)
        except:
            self._scaling_factor = 1.0
        
        # Отключаем обновление при каждом изменении для плавности
        self.update_idletasks()
        
        self.current_agents_data = []
        self.current_agent_index = None
        self.resize_job_id = None
        self._image_cache = {}
        self._resize_timer = None
        self._is_resizing = False
        self._pending_updates = []
        self._last_rendered_agent = None
        
        # Пул потоков для загрузки изображений
        self._image_loader = ThreadPoolExecutor(max_workers=4)
        
        self.load_resources()
        
        self.configure(fg_color=NEON_THEME["background"])
        self.grid_columnconfigure(0, weight=1, minsize=250)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)
        
        # Оптимизация: отслеживаем только изменение размера главного окна
        self.bind("<Configure>", self.on_window_resize, add="+")
        
        self.left_panel = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=NEON_THEME["panel_bg"])
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_rowconfigure(3, weight=1)
        
        # Заголовок приложения
        title_frame = ctk.CTkFrame(self.left_panel, fg_color=NEON_THEME["card_bg"], corner_radius=10)
        title_frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky="ew")
        ctk.CTkLabel(
            title_frame,
            text="⚡ ZZZ PROFILER",
            font=self.title_font,
            text_color=NEON_THEME["text_neon"]
        ).pack(pady=10)
        
        # Поле ввода с неоновым дизайном
        input_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.uid_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Введите UID...", 
            font=self.main_font, 
            border_color=NEON_THEME["border_neon"],
            border_width=2,
            corner_radius=8
        )
        self.uid_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.search_button = ctk.CTkButton(
            input_frame, 
            text="🔍", 
            font=self.main_font, 
            width=45, 
            command=self.start_fetch_thread, 
            fg_color=NEON_THEME["border_neon"], 
            text_color=NEON_THEME["background"], 
            hover_color=NEON_THEME["hover_color"],
            corner_radius=8
        )
        self.search_button.pack(side="left", padx=(5, 0))
        
        # Информация о игроке
        self.player_label = ctk.CTkLabel(
            self.left_panel, 
            text="", 
            font=self.bold_font, 
            anchor="w", 
            text_color=NEON_THEME["text_neon"]
        )
        self.player_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        # Список агентов с неоновым заголовком
        self.agent_list_frame = ctk.CTkScrollableFrame(
            self.left_panel, 
            label_text="👥 АГЕНТЫ", 
            label_font=self.title_font, 
            fg_color="transparent", 
            label_text_color=NEON_THEME["text_neon"],
            scrollbar_button_color=NEON_THEME["border_neon"],
            scrollbar_button_hover_color=NEON_THEME["hover_color"]
        )
        self.agent_list_frame.grid(row=3, column=0, sticky="nsew", padx=5)
        
        self.right_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=NEON_THEME["background"])
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Приветственное сообщение с неоновым дизайном
        welcome_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color=NEON_THEME["card_bg"],
            border_width=2,
            border_color=NEON_THEME["border_neon"],
            corner_radius=15
        )
        welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            welcome_frame,
            text="⚡ ZZZ PROFILER ⚡",
            font=self.huge_title_font,
            text_color=NEON_THEME["text_neon"]
        ).pack(padx=40, pady=(30,10))
        
        ctk.CTkLabel(
            welcome_frame,
            text="Введите UID и выберите агента\nдля просмотра детальной информации",
            font=self.main_font,
            text_color=NEON_THEME["text_secondary"],
            justify="center"
        ).pack(padx=40, pady=(0,30))

    def update_label_image(self, label, image):
        """Безопасно обновляет изображение виджета, предотвращая его удаление."""
        if label.winfo_exists():
            label.configure(image=image)
            label.image = image
    
    def on_window_resize(self, event):
        """Обработчик изменения размера окна с debounce."""
        # Игнорируем события от дочерних виджетов
        if event.widget != self:
            return
            
        self._is_resizing = True
        
        if self._resize_timer:
            self.after_cancel(self._resize_timer)
        
        delay = PERFORMANCE_CONFIG.get('resize_debounce_delay', 200)
        self._resize_timer = self.after(delay, self.handle_resize_complete)

    def handle_resize_complete(self):
        """Вызывается после завершения изменения размера окна."""
        self._resize_timer = None
        self._is_resizing = False
        
        # Обрабатываем отложенные обновления
        if self._pending_updates:
            for update_func in self._pending_updates:
                update_func()
            self._pending_updates.clear()
    
    def load_resources(self):
        self.agent_icons, self.role_icons = {}, {}
        font_family = "Roboto"
        try:
            ctk.FontManager.load_font(os.path.join(ASSETS_PATH, "fonts/Roboto-Regular.ttf"))
        except:
            font_family = None
        
        # Создаем переиспользуемые шрифты для оптимизации
        self.main_font = ctk.CTkFont(family=font_family, size=14)
        self.title_font = ctk.CTkFont(family=font_family, size=20, weight="bold")
        self.bold_font = ctk.CTkFont(family=font_family, size=16, weight="bold")
        self.small_font = ctk.CTkFont(family=font_family, size=11, weight="bold")
        self.tiny_font = ctk.CTkFont(family=font_family, size=10, weight="bold")
        self.large_title_font = ctk.CTkFont(family=font_family, size=24, weight="bold")
        self.huge_title_font = ctk.CTkFont(family=font_family, size=28, weight="bold")
        self.emoji_font = ctk.CTkFont(size=36)
        self.medium_bold_font = ctk.CTkFont(size=14, weight="bold")
        self.skill_level_font = ctk.CTkFont(size=13, weight="bold")
        
        # W-Engine иконка больше не нужна из assets - будем загружать динамически
        self.w_engine_icons = {}

        # Предзагрузка иконок ролей
        for agent_meta in AGENT_METADATA.values():
            if icon_filename := agent_meta.get('icon_file'):
                if icon_filename not in self.role_icons:
                    icon_path = os.path.join(ASSETS_PATH, f"images/{icon_filename}")
                    try:
                        if not os.path.exists(icon_path): raise FileNotFoundError
                        img = ctk.CTkImage(Image.open(icon_path), size=(24, 24))
                        self.role_icons[icon_filename] = img
                    except Exception:
                        print(f"ПРЕДУПРЕЖДЕНИЕ: Иконка роли не найдена в {icon_path}.")

    def show_agent_details(self, agent_index):
        # Если окно изменяется, откладываем обновление
        if self._is_resizing:
            self._pending_updates.append(lambda: self.show_agent_details(agent_index))
            return
        
        # Если уже отображаем этого агента, не перерисовываем
        if self._last_rendered_agent == agent_index:
            return
        
        # Сохраняем текущий индекс
        self.current_agent_index = agent_index
        self._last_rendered_agent = agent_index
        
        # Очищаем панель быстро
        for widget in self.right_panel.winfo_children(): 
            widget.destroy()
        
        agent = self.current_agents_data[agent_index]
        
        # Создаем основной контейнер с прокруткой для больших данных
        # Оптимизация: отключаем сглаживание для лучшей производительности
        main_container = ctk.CTkScrollableFrame(
            self.right_panel, 
            fg_color="transparent",
            scrollbar_button_color=NEON_THEME["border_neon"],
            scrollbar_button_hover_color=NEON_THEME["hover_color"]
        )
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Оптимизация прокрутки
        main_container._parent_canvas.configure(scrollregion=main_container._parent_canvas.bbox("all"))
        
        # Создаем заголовок с неоновым дизайном
        header = ctk.CTkFrame(
            main_container, 
            fg_color=NEON_THEME["card_bg"],
            border_width=2,
            border_color=NEON_THEME["border_neon"],
            corner_radius=15
        )
        header.pack(fill="x", padx=10, pady=10)
        
        # Контейнер для иконки и информации
        content_frame = ctk.CTkFrame(header, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        icon_label = ctk.CTkLabel(content_frame, text="")
        icon_label.pack(side="left", padx=(0,15))
        if icon_url := agent.get("icon", {}).get("round"): 
            self.load_agent_icon(icon_url, icon_label)
        
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Имя агента
        name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        name_frame.pack(anchor="w", fill="x")
        
        ctk.CTkLabel(
            name_frame, 
            text=agent.get('name', 'N/A'), 
            font=self.large_title_font,
            text_color=NEON_THEME["text_neon"]
        ).pack(side="left")
        
        # Рейтинг агента
        agent_rank = agent.get('agent_rank', 'D')
        agent_rank_color = RANK_COLORS.get(agent_rank)
        
        rank_badge = ctk.CTkFrame(
            name_frame,
            fg_color=agent_rank_color,
            corner_radius=6
        )
        rank_badge.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            rank_badge,
            text=f" {agent_rank} ",
            font=self.bold_font,
            text_color=NEON_THEME["background"]
        ).pack(padx=8, pady=2)
        
        # Метаданные с эмодзи
        meta = AGENT_METADATA.get(agent.get('name'), {})
        specialty_icons = {
            'Attack': '⚔️',
            'Anomaly': '⚡',
            'Stun': '💥',
            'Defense': '🛡️',
            'Support': '💚',
            'Rupture': '🔨'
        }
        specialty = meta.get('specialty', 'N/A')
        specialty_icon = specialty_icons.get(specialty, '❓')
        
        # Получаем rarity как число
        rarity = agent.get('rarity', 'S')
        if isinstance(rarity, str):
            # Если rarity это строка (S, A, B), показываем её
            rarity_display = f"[{rarity}]"
        else:
            # Если это число, показываем звездочки
            rarity_display = '⭐' * int(rarity)
        
        meta_text = f"Ур. {agent.get('level')} | {specialty_icon} {specialty} | {rarity_display}"
        ctk.CTkLabel(
            info_frame, 
            text=meta_text, 
            font=self.main_font, 
            text_color=NEON_THEME["text_secondary"]
        ).pack(anchor="w", pady=(5,0))
        
        # Общий счет
        score_frame = ctk.CTkFrame(
            info_frame,
            fg_color=NEON_THEME["card_bg_hover"],
            corner_radius=8
        )
        score_frame.pack(anchor="w", pady=(8,0), fill="x")
        
        ctk.CTkLabel(
            score_frame, 
            text=f"⭐ Общий счет: {agent.get('total_score', 'N/A')}", 
            font=self.bold_font, 
            text_color=agent_rank_color
        ).pack(padx=10, pady=5)
        # Центральная панель со статами
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.pack(fill="x", padx=10, pady=10)
        center_frame.grid_columnconfigure(0, weight=3)
        center_frame.grid_columnconfigure(1, weight=2)
        center_frame.grid_columnconfigure(2, weight=2)
        
        # Фрейм статов с неоновым свечением
        stats_frame = ctk.CTkFrame(
            center_frame, 
            fg_color=NEON_THEME["card_bg"], 
            border_width=2, 
            border_color=NEON_THEME["border_neon"],
            corner_radius=12
        )
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        stats_frame.grid_columnconfigure((0, 2), weight=1)
        
        # Заголовок статов
        ctk.CTkLabel(
            stats_frame,
            text="⚡ ХАРАКТЕРИСТИКИ",
            font=self.bold_font,
            text_color=NEON_THEME["text_neon"]
        ).grid(row=0, column=0, columnspan=4, pady=(10,5))
        
        stats_to_show = ["HP", "ATK", "DEF", "CRIT Rate", "CRIT DMG", "Energy Regen", "Anomaly Mastery", "Sheer Force", "Impact"]
        row, col = 1, 0
        
        for stat_name in stats_to_show:
            stat_obj = next((s for s in agent.get('stats', {}).values() if s['name'] == stat_name), None)
            if stat_obj:
                ctk.CTkLabel(
                    stats_frame, 
                    text=stat_name, 
                    font=self.main_font, 
                    text_color=NEON_THEME["text_secondary"]
                ).grid(row=row, column=col, padx=10, pady=5, sticky="w")
                
                ctk.CTkLabel(
                    stats_frame, 
                    text=stat_obj['formatted_value'], 
                    font=self.bold_font, 
                    text_color=NEON_THEME["text_main"]
                ).grid(row=row, column=col+1, padx=10, pady=5, sticky="e")
                
                col += 2
                if col > 2:
                    col, row = 0, row + 1
        # W-Engine фрейм с неоновым дизайном
        engine_frame = ctk.CTkFrame(
            center_frame, 
            fg_color=NEON_THEME["card_bg"],
            border_width=2,
            border_color=NEON_THEME["accent_purple"],
            corner_radius=12
        )
        engine_frame.grid(row=0, column=1, sticky="nsew", padx=(0,5))
        
        if w_engine := agent.get('w_engine'):
            # Заголовок
            ctk.CTkLabel(
                engine_frame,
                text="⚙️ W-ENGINE",
                font=self.bold_font,
                text_color=NEON_THEME["accent_purple"]
            ).pack(pady=(10,5))
            
            # Иконка W-Engine (загружаем динамически если есть URL)
            engine_icon_label = ctk.CTkLabel(engine_frame, text="")
            engine_icon_label.pack(pady=5)
            
            if icon_url := w_engine.get('icon'):
                self.load_w_engine_icon(icon_url, engine_icon_label)
            
            # Название с рейтингом
            rarity = w_engine.get('rarity', 'S')
            rarity_colors = {'S': NEON_THEME["accent_purple"], 'A': NEON_THEME["border_neon"], 'B': NEON_THEME["accent_green"]}
            
            ctk.CTkLabel(
                engine_frame, 
                text=w_engine.get('name', 'N/A'), 
                font=self.bold_font, 
                text_color=rarity_colors.get(rarity, NEON_THEME["text_neon"])
            ).pack(pady=(0,5))
            
            # Уровень
            level = w_engine.get('level', 0)
            ctk.CTkLabel(
                engine_frame,
                text=f"Ур. {level}",
                font=self.main_font,
                text_color=NEON_THEME["text_secondary"]
            ).pack()
            
            # Статы в рамках
            stats_container = ctk.CTkFrame(engine_frame, fg_color="transparent")
            stats_container.pack(pady=10, padx=10, fill="x")
            
            main_stat = w_engine.get('main_stat', {})
            if main_stat:
                stat_frame = ctk.CTkFrame(
                    stats_container,
                    fg_color=NEON_THEME["card_bg_hover"],
                    corner_radius=8
                )
                stat_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    stat_frame,
                    text=f"▸ {main_stat.get('name')}: {main_stat.get('formatted_value')}",
                    font=self.main_font,
                    text_color=NEON_THEME["text_main"]
                ).pack(pady=5, padx=10)
            
            sub_stat = w_engine.get('sub_stat', {})
            if sub_stat:
                stat_frame = ctk.CTkFrame(
                    stats_container,
                    fg_color=NEON_THEME["card_bg_hover"],
                    corner_radius=8
                )
                stat_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    stat_frame,
                    text=f"▸ {sub_stat.get('name')}: {sub_stat.get('formatted_value')}",
                    font=self.main_font,
                    text_color=NEON_THEME["text_main"]
                ).pack(pady=5, padx=10)
        # Навыки и Mindscape с неоновым дизайном
        skills_and_more_frame = ctk.CTkFrame(
            center_frame, 
            fg_color=NEON_THEME["card_bg"],
            border_width=2,
            border_color=NEON_THEME["accent_pink"],
            corner_radius=12
        )
        skills_and_more_frame.grid(row=0, column=2, sticky="nsew", padx=(5,0))
        skills_and_more_frame.grid_columnconfigure((0,1), weight=1)
        
        # Заголовок
        ctk.CTkLabel(
            skills_and_more_frame,
            text="✨ ПРОГРЕСС АГЕНТА",
            font=self.bold_font,
            text_color=NEON_THEME["accent_pink"]
        ).grid(row=0, column=0, columnspan=2, pady=(10,8))
        
        # Mindscape (Созвездия) - визуальное отображение
        mindscape_frame = ctk.CTkFrame(
            skills_and_more_frame, 
            fg_color=NEON_THEME["card_bg_hover"],
            corner_radius=8
        )
        mindscape_frame.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            mindscape_frame, 
            text="🌟 Mindscape (Созвездия)", 
            font=self.bold_font, 
            text_color=NEON_THEME["accent_purple"]
        ).pack(pady=(8,5))
        
        # Создаем сетку кружков для mindscape
        mindscape_level = agent.get('mindscape', 0)
        mindscape_grid = ctk.CTkFrame(mindscape_frame, fg_color="transparent")
        mindscape_grid.pack(pady=(0,8))
        
        for i in range(6):
            is_unlocked = i < mindscape_level
            
            circle_frame = ctk.CTkFrame(
                mindscape_grid,
                width=35,
                height=35,
                corner_radius=20,
                fg_color=NEON_THEME["accent_purple"] if is_unlocked else NEON_THEME["card_bg"],
                border_width=2,
                border_color=NEON_THEME["accent_purple"] if is_unlocked else NEON_THEME["text_secondary"]
            )
            circle_frame.grid(row=0, column=i, padx=3)
            circle_frame.grid_propagate(False)
            
            label = ctk.CTkLabel(
                circle_frame,
                text=str(i + 1),
                font=self.medium_bold_font,
                text_color=NEON_THEME["background"] if is_unlocked else NEON_THEME["text_secondary"]
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Core Skill (Пассивные навыки) - кружки с буквами A-F
        core_skill_frame = ctk.CTkFrame(
            skills_and_more_frame,
            fg_color=NEON_THEME["card_bg_hover"],
            corner_radius=8
        )
        core_skill_frame.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            core_skill_frame, 
            text="💎 Core Skill (Пассивки)", 
            font=self.bold_font, 
            text_color=NEON_THEME["border_neon"]
        ).pack(pady=(8,5))
        
        # Создаем сетку кружков с буквами A-F
        core_skill_level = agent.get('core_skill_level_num', 0)
        core_grid = ctk.CTkFrame(core_skill_frame, fg_color="transparent")
        core_grid.pack(pady=(0,8))
        
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for i, letter in enumerate(letters):
            is_unlocked = i < core_skill_level
            
            circle_frame = ctk.CTkFrame(
                core_grid,
                width=40,
                height=40,
                corner_radius=22,
                fg_color=NEON_THEME["border_neon"] if is_unlocked else NEON_THEME["card_bg"],
                border_width=2,
                border_color=NEON_THEME["border_neon"] if is_unlocked else NEON_THEME["text_secondary"]
            )
            circle_frame.grid(row=0, column=i, padx=3)
            circle_frame.grid_propagate(False)
            
            label = ctk.CTkLabel(
                circle_frame,
                text=letter,
                font=self.bold_font,
                text_color=NEON_THEME["background"] if is_unlocked else NEON_THEME["text_secondary"]
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Сетка навыков с иконками
        skills_grid = ctk.CTkFrame(skills_and_more_frame, fg_color="transparent")
        skills_grid.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(5,10))
        
        ctk.CTkLabel(
            skills_grid,
            text="⚔️ Боевые навыки",
            font=self.bold_font,
            text_color=NEON_THEME["text_main"]
        ).grid(row=0, column=0, columnspan=5, pady=(0,8), sticky="ew")
        
        # Настраиваем колонки для равномерного распределения
        for col in range(5):
            skills_grid.grid_columnconfigure(col, weight=1, uniform="skills")
        
        # Эмодзи-иконки для навыков (всегда доступны)
        skill_emoji_icons = {
            0: "👊",  # ATK - Basic Attack
            1: "✨",  # SPECIAL - Special Attack
            3: "💫",  # ULT - Ultimate
            2: "🌀",  # DODGE - Dodge
            6: "🛡️"   # PARRY - Parry/Counter
        }
        
        skills_display_order = [0, 1, 3, 2, 6]
        skills_data_from_api = {skill['type']: skill for skill in agent.get('skills', [])}
        
        for i, skill_type in enumerate(skills_display_order):
            if skill := skills_data_from_api.get(skill_type):
                skill_info = SKILL_INFO.get(skill_type, ["???", "gray"])
                skill_emoji = skill_emoji_icons.get(skill_type, "❓")
                
                # Создаем карточку навыка
                skill_card = ctk.CTkFrame(
                    skills_grid, 
                    fg_color=NEON_THEME["card_bg"],
                    border_width=2, 
                    border_color=skill_info[1],
                    corner_radius=10
                )
                skill_card.grid(row=1, column=i, padx=3, pady=3, sticky="nsew")
                
                # Эмодзи-иконка навыка (всегда отображается)
                ctk.CTkLabel(
                    skill_card,
                    text=skill_emoji,
                    font=self.emoji_font
                ).pack(pady=(10,5))
                
                # Уровень навыка
                level_frame = ctk.CTkFrame(
                    skill_card,
                    fg_color=skill_info[1],
                    corner_radius=8,
                    height=26
                )
                level_frame.pack(pady=(2,2), padx=8, fill="x")
                
                level_label = ctk.CTkLabel(
                    level_frame,
                    text=f"Ур. {skill['level']}",
                    font=self.skill_level_font,
                    text_color=NEON_THEME["background"]
                )
                level_label.pack(pady=4)
                
                # Название навыка
                ctk.CTkLabel(
                    skill_card,
                    text=skill_info[0],
                    font=self.tiny_font,
                    text_color=skill_info[1]
                ).pack(pady=(2,10))
        # Заголовок секции дисков
        disks_header = ctk.CTkFrame(
            main_container,
            fg_color=NEON_THEME["card_bg"],
            border_width=2,
            border_color=NEON_THEME["accent_green"],
            corner_radius=10
        )
        disks_header.pack(fill="x", padx=10, pady=(10,5))
        
        ctk.CTkLabel(
            disks_header,
            text="💿 ДИСКИ",
            font=self.title_font,
            text_color=NEON_THEME["accent_green"]
        ).pack(pady=10)
        
        # Сетка дисков
        disks_grid = ctk.CTkFrame(main_container, fg_color="transparent")
        disks_grid.pack(fill="both", expand=True, padx=10, pady=(5,10))
        
        # Предварительно настраиваем колонки
        for col in range(3):
            disks_grid.grid_columnconfigure(col, weight=1)
        
        # Создаем все диски сразу (убираем батчинг для устранения артефактов)
        discs = [d for d in agent.get('discs', []) if d]
        for i, disc in enumerate(discs):
            self._create_disc_card(disks_grid, i, disc)
        
        # Обновляем canvas после создания всех элементов
        main_container.update_idletasks()
    
    def _create_disc_card(self, parent, index, disc):
        """Создает карточку диска с неоновым дизайном."""
        row_idx, col_idx = divmod(index, 3)
        
        # Получаем название сета из конфига
        set_id = disc.get('set_id')
        set_name = DISK_SET_NAMES.get(set_id, disc.get('set_name', f"Set ID {set_id}"))
        
        rank = disc.get('rank', 'D')
        rank_color = RANK_COLORS.get(rank)
        
        # Выбираем цвет рамки в зависимости от ранга
        border_colors = {
            'SS': NEON_THEME["accent_purple"],
            'S': NEON_THEME["accent_pink"],
            'A': NEON_THEME["border_neon"],
            'B': NEON_THEME["accent_green"],
            'C': NEON_THEME["text_secondary"],
            'D': NEON_THEME["text_secondary"]
        }
        
        disc_card = ctk.CTkFrame(
            parent, 
            fg_color=NEON_THEME["card_bg"], 
            border_width=2, 
            border_color=border_colors.get(rank, NEON_THEME["border_neon"]),
            corner_radius=10
        )
        disc_card.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=5)
        disc_card.grid_columnconfigure(0, weight=3)
        disc_card.grid_columnconfigure(1, weight=1)
        
        main_stat = disc.get('main_stat', {})
        
        # Заголовок диска с номером и рангом
        header_frame = ctk.CTkFrame(disc_card, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(8,5), sticky="ew")
        
        # Номер диска (1-6) и название
        disc_number = index + 1
        ctk.CTkLabel(
            header_frame, 
            text=f"💎 Диск {disc_number}: {set_name}", 
            font=self.bold_font, 
            text_color=NEON_THEME["text_main"]
        ).pack()
        
        ctk.CTkLabel(
            header_frame,
            text=f"[{rank}] +{disc.get('level')}",
            font=self.main_font,
            text_color=rank_color
        ).pack()
        
        # Основной стат в рамке
        main_stat_frame = ctk.CTkFrame(
            disc_card,
            fg_color=NEON_THEME["card_bg_hover"],
            corner_radius=6
        )
        main_stat_frame.grid(row=1, column=0, columnspan=2, padx=8, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            main_stat_frame, 
            text=f"▸ {main_stat.get('name')}: {main_stat.get('formatted_value')}", 
            font=self.main_font, 
            text_color=NEON_THEME["stat_highlight"]
        ).pack(pady=5)
        
        # Рейтинг
        rating_frame = ctk.CTkFrame(disc_card, fg_color="transparent")
        rating_frame.grid(row=2, column=0, columnspan=2, pady=(0,5))
        
        ctk.CTkLabel(
            rating_frame, 
            text=f"⭐ Счет: {disc.get('rating')}", 
            font=self.bold_font, 
            text_color=rank_color
        ).pack()
        
        # Подстаты
        weights = disc.get('calculation_weights', {})
        for j, sub_stat in enumerate(disc.get('sub_stats', [])):
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
            
            stat_color = NEON_THEME["stat_highlight"] if usefulness_score > 0 else NEON_THEME["text_main"]
            
            ctk.CTkLabel(
                disc_card, 
                text=f"• {stat_name}: {formatted_value}", 
                font=self.main_font, 
                text_color=stat_color
            ).grid(row=j+3, column=0, sticky="w", padx=10, pady=1)
            
            ctk.CTkLabel(
                disc_card, 
                text=f"{usefulness_score:+.2f}", 
                font=self.main_font, 
                text_color=NEON_THEME["text_secondary"]
            ).grid(row=j+3, column=1, sticky="e", padx=10, pady=1)
    
    def display_agent_list(self, data):
        # Сбрасываем кэш отрисовки
        self._last_rendered_agent = None
        
        # Очищаем список агентов
        for widget in self.agent_list_frame.winfo_children(): 
            widget.destroy()
        
        # Обновляем информацию о игроке
        player_info = data.get('player', {})
        self.player_label.configure(
            text=f"{player_info.get('nickname', 'N/A')} (Ур. {player_info.get('level', 'N/A')})"
        )
        
        # Создаем кнопки для агентов с улучшенным дизайном
        for i, agent in enumerate(self.current_agents_data):
            # Получаем рейтинг агента для цветовой индикации
            agent_rank = agent.get('agent_rank', 'D')
            rank_indicator = {'SS': '⭐⭐', 'S': '⭐', 'A': '▲', 'B': '●', 'C': '○', 'D': '·'}
            
            is_selected = i == self.current_agent_index
            
            btn = ctk.CTkButton(
                self.agent_list_frame, 
                text=f"{rank_indicator.get(agent_rank, '·')} {agent.get('name', 'N/A')}", 
                font=self.main_font, 
                anchor="w", 
                fg_color=NEON_THEME["card_bg_hover"] if is_selected else NEON_THEME["card_bg"],
                hover_color=NEON_THEME["hover_color"],
                border_width=2 if is_selected else 0,
                border_color=NEON_THEME["border_neon"] if is_selected else None,
                corner_radius=8,
                command=lambda index=i: self.show_agent_details(index)
            )
            btn.pack(fill="x", pady=2, padx=5)
        
        # Показываем первого агента
        if self.current_agents_data: 
            self.show_agent_details(0)
    
    def cleanup_cache(self):
        """Очищает старые записи из кэша изображений."""
        max_size = PERFORMANCE_CONFIG.get('max_image_cache_size', 100)
        if len(self._image_cache) > max_size:
            # Удаляем половину кэша (самые старые)
            items_to_remove = len(self._image_cache) - max_size // 2
            for key in list(self._image_cache.keys())[:items_to_remove]:
                del self._image_cache[key]
    
    def destroy(self):
        """Переопределяем destroy для корректной очистки ресурсов."""
        # Останавливаем пул потоков
        self._image_loader.shutdown(wait=False)
        
        # Очищаем кэш
        self._image_cache.clear()
        self.agent_icons.clear()
        
        super().destroy()

    def load_agent_icon(self, url, label):
        # Проверяем кэш сначала
        if url in self._image_cache:
            self.update_label_image(label, self._image_cache[url])
            return
            
        def _load():
            try:
                # Двойная проверка кэша в потоке
                if url in self._image_cache:
                    self.after(0, lambda: self.update_label_image(label, self._image_cache[url]))
                    return
                
                timeout = PERFORMANCE_CONFIG.get('image_load_timeout', 5)
                response = requests.get(url, stream=True, timeout=timeout)
                response.raise_for_status()
                img_data = response.content
                
                # Оптимизация: используем более быстрый алгоритм для маленьких изображений
                pil_image = Image.open(io.BytesIO(img_data)).resize((64, 64), Image.Resampling.BILINEAR)
                mask = Image.new('L', (64, 64), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 64, 64), fill=255)
                pil_image.putalpha(mask)
                ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(64, 64))
                
                # Сохраняем в кэш
                self._image_cache[url] = ctk_image
                self.agent_icons[url] = ctk_image
                
                # Используем after_idle для обновления UI
                self.after_idle(lambda: self.update_label_image(label, ctk_image))
            except Exception as e:
                print(f"Ошибка загрузки иконки: {e}")
        
        # Используем пул потоков вместо создания нового потока
        self._image_loader.submit(_load)
    
    def load_w_engine_icon(self, url, label):
        """Загружает иконку W-Engine динамически."""
        # Проверяем кэш
        cache_key = f"w_engine_{url}"
        if cache_key in self._image_cache:
            self.update_label_image(label, self._image_cache[cache_key])
            return
        
        def _load():
            try:
                if cache_key in self._image_cache:
                    self.after(0, lambda: self.update_label_image(label, self._image_cache[cache_key]))
                    return
                
                timeout = PERFORMANCE_CONFIG.get('image_load_timeout', 3)
                response = requests.get(url, stream=True, timeout=timeout)
                response.raise_for_status()
                img_data = response.content
                
                # Загружаем и обрабатываем изображение
                pil_image = Image.open(io.BytesIO(img_data))
                
                # Изменяем размер с сохранением пропорций
                pil_image.thumbnail((80, 80), Image.Resampling.BILINEAR)
                
                ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(80, 80))
                
                # Сохраняем в кэш
                self._image_cache[cache_key] = ctk_image
                self.w_engine_icons[url] = ctk_image
                
                self.after_idle(lambda: self.update_label_image(label, ctk_image))
            except Exception as e:
                print(f"Ошибка загрузки иконки W-Engine: {e}")
        
        self._image_loader.submit(_load)
    


    def start_fetch_thread(self): 
        threading.Thread(target=self.fetch_profile_data, daemon=True).start()
    
    def fetch_profile_data(self):
        uid = self.uid_entry.get()
        if not uid: 
            return
        
        self.after(0, lambda: self.player_label.configure(text="Загрузка..."))
        
        try:
            timeout = PERFORMANCE_CONFIG.get('api_request_timeout', 10)
            response = requests.get(f"http://127.0.0.1:5000/api/profile/{uid}", timeout=timeout)
            response.raise_for_status()
            data = response.json()
            self.current_agents_data = data.get('agents', [])
            
            # Очищаем кэш перед загрузкой новых данных
            self.cleanup_cache()
            
            self.after(0, lambda: self.display_agent_list(data))
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.player_label.configure(text=f"Ошибка: {error_msg}"))

if __name__ == "__main__":
    app = ZZZProfilerApp()
    app.mainloop()