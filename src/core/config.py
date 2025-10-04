"""
AI Cyber Tool - Configuration
Централізовані налаштування додатку
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from urllib.parse import urlparse, urlunparse


def mask_url_credentials(url: str) -> str:
    """Замінює логін:пароль у URL на '***'."""
    try:
        parsed = urlparse(url)
        if parsed.password:
            # Створюємо новий netloc з замаскованими даними
            netloc = f"{parsed.username}:***@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            # Збираємо URL назад
            return urlunparse(parsed._replace(netloc=netloc))
        return url
    except (ImportError, AttributeError):
        return "hidden"  # Fallback


def get_database_type(database_url: str) -> str:
    """Отримує тип бази даних з URL"""
    try:
        if ":///" in database_url:
            return database_url.split(":///")[0]
        elif "://" in database_url:
            parsed = urlparse(database_url)
            return parsed.scheme
        else:
            return "sqlite"  # Default для локальних файлів
    except Exception:
        return "unknown"


class Settings(BaseSettings):
    """Централізовані налаштування додатку"""
    # База даних
    database_url: str = "app.db"
    
    # Середовище
    environment: str = "development"
    render_env: bool = False
    
    # Логування
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_rotation: str = "10 MB"
    log_retention: str = "7 days"
    
    # Message Bus
    rabbitmq_url: str = "amqp://localhost:5672"
    rabbitmq_commands_exchange: str = "commands.exchange"
    rabbitmq_events_exchange: str = "events.exchange"
    
    # API
    api_title: str = "AI Cyber Tool"
    api_version: str = "1.0.0"
    api_description: str = "AICyberTool - це комплексна система управління цифровою трансформацією та кібербезпеки, що поєднує штучний інтелект, кібернетичне управління та автоматизоване реагування на загрози. Проект побудований на архітектурі мікросервісів з прогресивним підходом до безпеки та масштабованості."
    
    # Безпека
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings():
    """Отримання кешованих налаштувань"""
    return Settings()
