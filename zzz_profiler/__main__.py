import threading
import time
import requests
import sys
import os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, os.path.abspath(os.path.join(application_path, '..')))
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zzz_profiler.beautiful_app import ZZZProfilerApp
from zzz_profiler.run import run_server

def start_backend():
    print(">>> Запуск фонового API-сервера...")
    run_server()

def wait_for_server(max_attempts=10, delay=0.5):
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://127.0.0.1:5000", timeout=1)
            print(f">>> Сервер готов (попытка {attempt + 1}).")
            return True
        except (requests.ConnectionError, requests.Timeout):
            if attempt < max_attempts - 1:
                time.sleep(delay)
    return False

if __name__ == '__main__':
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    print(">>> Ожидание готовности сервера...")
    
    if not wait_for_server():
        print("!!! ПРЕДУПРЕЖДЕНИЕ: Сервер не отвечает, но GUI будет запущен.")
        
    print(">>> Запуск GUI приложения...")
    app = ZZZProfilerApp()
    app.mainloop()

    print(">>> GUI закрыто, приложение завершает работу.")