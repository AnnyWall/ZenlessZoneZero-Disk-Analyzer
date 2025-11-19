# zzz_profiler/run.py

from . import create_app

# Создаем экземпляр приложения Flask
app = create_app()

def run_server():
    """Функция для запуска сервера, которую мы будем вызывать из __main__.py."""
    # use_reloader=False ОБЯЗАТЕЛЕН для стабильного запуска в потоке.
    # debug=False рекомендуется для фонового режима, чтобы избежать лишних логов.
    # threaded=True для обработки нескольких запросов одновременно
    app.run(port=5000, use_reloader=False, debug=False, threaded=True)

if __name__ == '__main__':
    # Эта часть нужна, только если вы хотите запустить сервер отдельно для теста.
    run_server()