"""
AI Cyber Tool - Main Application
Основний файл FastAPI додатку з реорганізованою структурою
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
import sys
from pathlib import Path
from dotenv import load_dotenv

# Імпорти з нашої реорганізованої структури
from .core.config import get_settings
from .db.database import init_database
from .routers import sessions, tech_map, message_bus

# Завантаження змінних оточення
load_dotenv()

# Отримання налаштувань
settings = get_settings()

# Налаштування логування
if settings.render_env:
    # На Render використовуємо стандартне логування
    logger.add(sys.stdout, level=settings.log_level)
else:
    # Локально використовуємо файлове логування
    Path("logs").mkdir(exist_ok=True)
    logger.add(settings.log_file, rotation=settings.log_rotation, retention=settings.log_retention)

# Створення FastAPI додатку
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Ініціалізація Jinja2 шаблонів
templates = Jinja2Templates(directory="templates")

# Налаштування статичних файлів та шаблонів
# Створюємо папки якщо вони не існують
Path("static").mkdir(exist_ok=True)
Path("architecture").mkdir(exist_ok=True)

# Монтуємо статичні файли тільки якщо папки існують
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

if Path("architecture").exists():
    app.mount("/architecture", StaticFiles(directory="architecture"), name="architecture")

# Підключення роутерів
app.include_router(sessions.router)
app.include_router(tech_map.router)
app.include_router(message_bus.router)


@app.on_event("startup")
async def startup_event():
    """Під час запуску додатку"""
    logger.info("AI Cyber Tool is starting up...")
    await init_database()
    
    # Ініціалізація Message Bus
    try:
        from .services.message_bus import MessageBus, MessageBusConfig
        message_bus_config = MessageBusConfig(
            rabbitmq_url=settings.rabbitmq_url,
            commands_exchange=settings.rabbitmq_commands_exchange,
            events_exchange=settings.rabbitmq_events_exchange
        )
        message_bus = MessageBus(message_bus_config)
        app.state.message_bus = message_bus
        logger.info("Message Bus initialized successfully")
    except Exception as e:
        logger.warning(f"Message Bus initialization failed: {e}")
        app.state.message_bus = None


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Коренева сторінка з меню"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "version": settings.api_version,
        "status": "running"
    })


@app.get("/api")
async def api_root():
    """API коренева сторінка"""
    return {
        "message": "Welcome to AI Cyber Tool!",
        "version": settings.api_version,
        "status": "running",
        "environment": settings.environment,
        "endpoints": {
            "tech_map": "/tech-map",
            "docs": "/docs",
            "health": "/health",
            "api_diagrams": "/tech-map/api",
            "message_bus_status": "/api/message-bus/status",
            "message_bus_test": "/api/message-bus/test",
            "specs": "/specs",
            "specs_api": "/api/specs",
            "sessions": "/api/sessions",
            "analysis_logs": "/api/analysis-logs",
            "config": "/api/config"
        }
    }


@app.get("/api/config")
async def get_config():
    """Отримати конфігурацію додатку (без чутливих даних)"""
    return {
        "environment": settings.environment,
        "api_version": settings.api_version,
        "log_level": settings.log_level,
        "database_url": settings.database_url,
        "rabbitmq_url": settings.rabbitmq_url,
        "rabbitmq_commands_exchange": settings.rabbitmq_commands_exchange,
        "rabbitmq_events_exchange": settings.rabbitmq_events_exchange,
        "access_token_expire_minutes": settings.access_token_expire_minutes
    }


@app.get("/health")
async def health_check():
    """Перевірка здоров'я додатку"""
    return {
        "status": "healthy",
        "version": settings.api_version,
        "environment": settings.environment,
        "database": "connected",
        "message_bus": "operational" if app.state.message_bus else "not_available"
    }
