# zzz_profiler/__init__.py

from flask import Flask

def create_app():
    """Фабрика для создания экземпляра приложения Flask."""
    app = Flask(__name__)

    # Импортируем и регистрируем наш Blueprint с API-маршрутами
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app