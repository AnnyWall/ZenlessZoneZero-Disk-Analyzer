# beautiful_app.py

import customtkinter as ctk
import requests
import threading
from PIL import Image, ImageDraw
import io
import os
try:
    from zzz_profiler.config import AGENT_METADATA, STAT_NORMALIZATION_VALUES
except ImportError:
    AGENT_METADATA, STAT_NORMALIZATION_VALUES = {}, {}

# --- ЦВЕТОВАЯ ПАЛИТРА "NEON" ---
NEON_THEME = {
    "background": "#121212",
    "panel_bg": "#1A1B1E",
    "card_bg": "#242424",
    "border_neon": "#00E5FF",
    "text_main": "#EAEAEA",
    "text_secondary": "#757575",
    "text_neon": "#00E5FF",
    "hover_color": "#005662",
    "stat_highlight": "#FFB74D"
}

# --- Настройки ---
ctk.set_appearance_mode("Dark")
RANK_COLORS = {"SS": "#FFB74D", "S": "#BA68C8", "A": "#4FC3F7", "B": "#81C784", "C": "#FFF176", "D": NEON_THEME["text_secondary"]}
ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
SKILL_INFO = {0: ["ATK", "#E0E0E0"], 1: ["SPECIAL", "#4FC3F7"], 3: ["ULT", "#FFB74D"], 2: ["DODGE", "#81C784"], 6: ["PARRY", "#81C784"]}

class ZZZProfilerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ZZZ Showcase Profiler")
        self.geometry("1400x900")
        
        self.current_agents_data = []
        self.load_resources()
        
        self.configure(fg_color=NEON_THEME["background"])
        self.grid_columnconfigure(0, weight=1, minsize=250)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)
        
        self.left_panel = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=NEON_THEME["panel_bg"])
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_rowconfigure(2, weight=1)
        
        input_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.uid_entry = ctk.CTkEntry(input_frame, placeholder_text="Введите UID...", font=self.main_font, border_color=NEON_THEME["border_neon"])
        self.uid_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.search_button = ctk.CTkButton(input_frame, text="🔍", font=self.main_font, width=40, command=self.start_fetch_thread, fg_color=NEON_THEME["border_neon"], text_color=NEON_THEME["background"], hover_color=NEON_THEME["hover_color"])
        self.search_button.pack(side="left", padx=(5, 0))
        
        self.player_label = ctk.CTkLabel(self.left_panel, text="", font=self.bold_font, anchor="w", text_color=NEON_THEME["text_main"])
        self.player_label.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.agent_list_frame = ctk.CTkScrollableFrame(self.left_panel, label_text="Агенты", label_font=self.title_font, fg_color="transparent", label_text_color=NEON_THEME["text_neon"])
        self.agent_list_frame.grid(row=2, column=0, sticky="nsew", padx=5)
        
        self.right_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=NEON_THEME["background"]) # Используем основной фон
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.details_label = ctk.CTkLabel(self.right_panel, text="Выберите агента для просмотра", font=self.title_font, text_color=NEON_THEME["text_secondary"])
        self.details_label.pack(expand=True)

    def update_label_image(self, label, image):
        """Безопасно обновляет изображение виджета, предотвращая его удаление."""
        label.configure(image=image)
        label.image = image

    def load_resources(self):
        self.agent_icons, self.role_icons = {}, {}
        font_family = "Roboto"
        try:
            ctk.FontManager.load_font(os.path.join(ASSETS_PATH, "fonts/Roboto-Regular.ttf"))
        except:
            font_family = None
        self.main_font = ctk.CTkFont(family=font_family, size=14)
        self.title_font = ctk.CTkFont(family=font_family, size=20, weight="bold")
        self.bold_font = ctk.CTkFont(family=font_family, size=16, weight="bold")
        
        try:
            pil_img = Image.open(os.path.join(ASSETS_PATH, "images/icon_w_engine.png"))
            self.w_engine_icon = ctk.CTkImage(pil_img, size=(48, 48))
        except:
            self.w_engine_icon = None

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
        # ... (Код без изменений, но будет использовать новый update_label_image)
        for widget in self.right_panel.winfo_children(): widget.destroy()
        agent = self.current_agents_data[agent_index]
        header = ctk.CTkFrame(self.right_panel, fg_color="transparent"); header.pack(fill="x", padx=20, pady=20)
        icon_label = ctk.CTkLabel(header, text=""); icon_label.pack(side="left", padx=10)
        if icon_url := agent.get("icon", {}).get("round"): self.load_agent_icon(icon_url, icon_label)
        info_frame = ctk.CTkFrame(header, fg_color="transparent"); info_frame.pack(side="left", fill="x")
        ctk.CTkLabel(info_frame, text=agent.get('name', 'N/A'), font=self.title_font, text_color=NEON_THEME["text_neon"]).pack(anchor="w")
        meta = AGENT_METADATA.get(agent.get('name'), {}); meta_text = f"Ур. {agent.get('level')} | {meta.get('specialty', 'N/A')} | {agent.get('rarity')} ★"
        ctk.CTkLabel(info_frame, text=meta_text, font=self.main_font, text_color=NEON_THEME["text_secondary"]).pack(anchor="w")
        score_frame = ctk.CTkFrame(info_frame, fg_color="transparent"); score_frame.pack(anchor="w", pady=(5,0))
        ctk.CTkLabel(score_frame, text="Общий счет:", font=self.main_font, text_color=NEON_THEME["text_main"]).pack(side="left")
        agent_rank = agent.get('agent_rank', 'D'); agent_rank_color = RANK_COLORS.get(agent_rank)
        ctk.CTkLabel(score_frame, text=f"{agent.get('total_score', 'N/A')} [{agent_rank}]", font=self.bold_font, text_color=agent_rank_color).pack(side="left", padx=5)
        center_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent"); center_frame.pack(fill="x", padx=20, pady=10); center_frame.grid_columnconfigure(0, weight=3); center_frame.grid_columnconfigure(1, weight=2); center_frame.grid_columnconfigure(2, weight=2)
        stats_frame = ctk.CTkFrame(center_frame, fg_color=NEON_THEME["card_bg"], border_width=1, border_color=NEON_THEME["border_neon"]); stats_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10)); stats_frame.grid_columnconfigure((0, 2), weight=1)
        stats_to_show = ["HP", "ATK", "DEF", "CRIT Rate", "CRIT DMG", "Energy Regen", "Anomaly Mastery", "Sheer Force", "Impact"]; row, col = 0, 0
        for stat_name in stats_to_show:
            stat_obj = next((s for s in agent.get('stats', {}).values() if s['name'] == stat_name), None)
            if stat_obj: ctk.CTkLabel(stats_frame, text=stat_name, font=self.main_font, text_color=NEON_THEME["text_secondary"]).grid(row=row, column=col, padx=10, pady=5, sticky="w"); ctk.CTkLabel(stats_frame, text=stat_obj['formatted_value'], font=self.bold_font, text_color=NEON_THEME["text_main"]).grid(row=row, column=col+1, padx=10, pady=5, sticky="e"); col += 2;
            if col > 2: col, row = 0, row + 1
        engine_frame = ctk.CTkFrame(center_frame, fg_color=NEON_THEME["card_bg"]); engine_frame.grid(row=0, column=1, sticky="nsew", padx=(0,5))
        if w_engine := agent.get('w_engine'):
            ctk.CTkLabel(engine_frame, image=self.w_engine_icon, text="").pack(pady=5); ctk.CTkLabel(engine_frame, text=w_engine.get('name', 'N/A'), font=self.bold_font, text_color=NEON_THEME["text_neon"]).pack()
            main_stat = f"{w_engine.get('main_stat', {}).get('name')}: {w_engine.get('main_stat', {}).get('formatted_value')}"; sub_stat = f"{w_engine.get('sub_stat', {}).get('name')}: {w_engine.get('sub_stat', {}).get('formatted_value')}"
            ctk.CTkLabel(engine_frame, text=f"{main_stat} | {sub_stat}", font=self.main_font, text_color=NEON_THEME["text_main"]).pack(pady=(0,5))
        skills_and_more_frame = ctk.CTkFrame(center_frame, fg_color=NEON_THEME["card_bg"]); skills_and_more_frame.grid(row=0, column=2, sticky="nsew", padx=(5,0)); skills_and_more_frame.grid_columnconfigure((0,1), weight=1)
        mindscape_frame = ctk.CTkFrame(skills_and_more_frame, fg_color="transparent"); mindscape_frame.grid(row=0, column=0, pady=5); ctk.CTkLabel(mindscape_frame, text="Mindscape", font=self.main_font, text_color=NEON_THEME["text_secondary"]).pack(); ctk.CTkLabel(mindscape_frame, text=f"{agent.get('mindscape', 0)}/6", font=self.title_font, text_color="#BA68C8").pack()
        core_skill_frame = ctk.CTkFrame(skills_and_more_frame, fg_color="transparent"); core_skill_frame.grid(row=0, column=1, pady=5); ctk.CTkLabel(core_skill_frame, text="Core Skill", font=self.main_font, text_color=NEON_THEME["text_secondary"]).pack(); ctk.CTkLabel(core_skill_frame, text=f"{agent.get('core_skill_level_num', 0)}/6", font=self.title_font, text_color="#4FC3F7").pack()
        skills_grid = ctk.CTkFrame(skills_and_more_frame, fg_color="transparent"); skills_grid.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)
        skills_display_order = [0, 1, 3, 2, 6]; skills_data_from_api = {skill['type']: skill for skill in agent.get('skills', [])}
        for i, skill_type in enumerate(skills_display_order):
            row, col = divmod(i, 3); skills_grid.grid_columnconfigure(col, weight=1)
            if skill := skills_data_from_api.get(skill_type):
                skill_info = SKILL_INFO.get(skill_type, ["???", "gray"]); skill_card = ctk.CTkFrame(skills_grid, border_width=2, border_color=skill_info[1]); skill_card.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
                ctk.CTkLabel(skill_card, text=skill_info[0], font=self.main_font, text_color=NEON_THEME["text_secondary"]).pack(); ctk.CTkLabel(skill_card, text=f"Lv. {skill['level']}", font=self.bold_font, text_color=NEON_THEME["text_main"]).pack(pady=(0, 5))
        disks_grid = ctk.CTkFrame(self.right_panel, fg_color="transparent"); disks_grid.pack(fill="both", expand=True, padx=20, pady=10)
        for i, disc in enumerate(agent.get('discs', [])):
            row, col = divmod(i, 3); disks_grid.grid_columnconfigure(col, weight=1);
            if not disc: continue
            disc_card = ctk.CTkFrame(disks_grid, fg_color=NEON_THEME["card_bg"], border_width=1, border_color=NEON_THEME["border_neon"]); disc_card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5); disc_card.grid_columnconfigure(0, weight=3); disc_card.grid_columnconfigure(1, weight=1)
            main_stat, rank, rank_color = disc.get('main_stat',{}), disc.get('rank', 'D'), RANK_COLORS.get(disc.get('rank', 'D'))
            ctk.CTkLabel(disc_card, text=f"{disc.get('set_name', 'N/A')} (+{disc.get('level')})", font=self.bold_font, text_color=NEON_THEME["text_main"]).grid(row=0, column=0, columnspan=2, pady=(5,0)); ctk.CTkLabel(disc_card, text=f"{main_stat.get('name')}: {main_stat.get('formatted_value')}", font=self.main_font, text_color=NEON_THEME["text_secondary"]).grid(row=1, column=0, columnspan=2); ctk.CTkLabel(disc_card, text=f"Счет: {disc.get('rating')} [{rank}]", font=self.bold_font, text_color=rank_color).grid(row=2, column=0, columnspan=2, pady=(0,5))
            weights = disc.get('calculation_weights', {})
            for j, sub_stat in enumerate(disc.get('sub_stats', [])):
                stat_name, formatted_value, raw_value = sub_stat.get('name', 'N/A'), sub_stat.get('formatted_value', '0'), sub_stat.get('value', 0)
                normalization_value = STAT_NORMALIZATION_VALUES.get(stat_name, 1.0); usefulness_score = 0.0
                if normalization_value > 0:
                    is_percent = '%' in sub_stat.get('format', ''); actual_value = raw_value / 100.0 if is_percent else raw_value
                    num_rolls = actual_value / normalization_value; weight = weights.get(stat_name, 0); usefulness_score = num_rolls * weight
                stat_color = NEON_THEME["stat_highlight"] if usefulness_score > 0 else NEON_THEME["text_main"]
                ctk.CTkLabel(disc_card, text=f"• {stat_name}: {formatted_value}", font=self.main_font, text_color=stat_color).grid(row=j+3, column=0, sticky="w", padx=10, pady=1); ctk.CTkLabel(disc_card, text=f"{usefulness_score:+.2f}", font=self.main_font, text_color=NEON_THEME["text_secondary"]).grid(row=j+3, column=1, sticky="e", padx=10, pady=1)
    
    def display_agent_list(self, data):
        for widget in self.agent_list_frame.winfo_children(): widget.destroy()
        self.player_label.configure(text=f"{data.get('player', {}).get('nickname', 'N/A')} (Ур. {data.get('player', {}).get('level', 'N/A')})")
        for i, agent in enumerate(self.current_agents_data):
            btn = ctk.CTkButton(self.agent_list_frame, text=agent.get('name', 'N/A'), font=self.main_font, anchor="w", fg_color="transparent", hover_color=NEON_THEME["hover_color"], command=lambda index=i: self.show_agent_details(index))
            btn.pack(fill="x", pady=2)
        if self.current_agents_data: self.show_agent_details(0)

    def load_agent_icon(self, url, label):
        def _load():
            try:
                if url in self.agent_icons:
                    self.after(0, lambda: self.update_label_image(label, self.agent_icons[url]))
                    return
                response = requests.get(url, stream=True); response.raise_for_status()
                img_data = response.content; pil_image = Image.open(io.BytesIO(img_data)).resize((64, 64), Image.Resampling.LANCZOS)
                mask = Image.new('L', (64, 64), 0); draw = ImageDraw.Draw(mask); draw.ellipse((0, 0, 64, 64), fill=255); pil_image.putalpha(mask)
                ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(64, 64))
                self.agent_icons[url] = ctk_image
                self.after(0, lambda: self.update_label_image(label, ctk_image))
            except Exception: pass
        threading.Thread(target=_load, daemon=True).start()

    # --- Остальные методы без изменений ---
    def start_fetch_thread(self): threading.Thread(target=self.fetch_profile_data, daemon=True).start()
    def fetch_profile_data(self):
        uid = self.uid_entry.get();
        if not uid: return
        self.after(0, lambda: self.player_label.configure(text="Загрузка..."))
        try: response = requests.get(f"http://127.0.0.1:5000/api/profile/{uid}"); response.raise_for_status(); self.current_agents_data = response.json().get('agents', []); self.after(0, lambda: self.display_agent_list(response.json()))
        except Exception as e: self.after(0, lambda err_msg=e: self.player_label.configure(text=f"Ошибка: {err_msg}"))
    def on_resize(self, event):
        self.bg_label.configure(image=None);
        if self.resize_job_id: self.after_cancel(self.resize_job_id)
        self.resize_job_id = self.after(250, self.perform_bg_resize)
    def perform_bg_resize(self):
        self.resize_job_id = None
        if self.original_bg_image:
            new_width, new_height = self.winfo_width(), self.winfo_height()
            self.bg_image = ctk.CTkImage(self.original_bg_image, size=(new_width, new_height))
            self.bg_label.configure(image=self.bg_image); self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

if __name__ == "__main__":
    app = ZZZProfilerApp()
    app.mainloop()