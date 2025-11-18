# zzz_profiler/__main__.py

import threading
import time
import requests
import sys
import os

# --- ИЗМЕНЕНИЕ ЗДЕСЬ: Добавляем путь к проекту для PyInstaller ---
# Это "костыль", который говорит Python, где искать пакет zzz_profiler
# Он нужен, чтобы абсолютные импорты работали внутри .exe
if getattr(sys, 'frozen', False):
    # Если запущено из .exe, добавляем путь к папке .exe
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, os.path.abspath(os.path.join(application_path, '..')))
else:
    # Если запущено из кода, добавляем путь к корневой папке проекта
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- ИЗМЕНЕНИЕ ЗДЕСЬ: Абсолютные импорты ---
from zzz_profiler.beautiful_app import ZZZProfilerApp
from zzz_profiler.run import run_server

def start_backend():
    print(">>> Запуск фонового API-сервера...")
    run_server()

if __name__ == '__main__':
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    print(">>> Ожидание готовности сервера...")
    time.sleep(3) # Возвращаем простую паузу для надежности

    try:
        requests.get("http://127.0.0.1:5000")
        print(">>> Сервер готов и отвечает.")
    except requests.ConnectionError:
        print("!!! ОШИБКА: Не удалось запустить фоновый сервер.")
        # Не выходим, чтобы пользователь мог увидеть ошибку в GUI
        
    print(">>> Запуск GUI приложения...")
    app = ZZZProfilerApp()
    app.mainloop()

    print(">>> GUI закрыто, приложение завершает работу.")