import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Базовый класс конфигурации приложения Flask."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DISK_TOKEN = os.getenv('DISK_TOKEN')
