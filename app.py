"""
AI Cyber Tool - Main Application
AICyberTool - це комплексна система управління цифровою трансформацією та кібербезпеки, що поєднує штучний інтелект, кібернетичне управління та автоматизоване реагування на загрози. Проект побудований на архітектурі мікросервісів з прогресивним підходом до безпеки та масштабованості.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
import sqlite3
from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Завантаження змінних оточення
load_dotenv()

# Налаштування логування
if os.getenv("RENDER"):
    # На Render використовуємо стандартне логування
    logger.add(sys.stdout, level="INFO")
else:
    # Локально використовуємо файлове логування
    Path("logs").mkdir(exist_ok=True)
    logger.add("logs/app.log", rotation="10 MB", retention="7 days")

# Створення FastAPI додатку
app = FastAPI(
    title="AI Cyber Tool",
    description="AICyberTool - це комплексна система управління цифровою трансформацією та кібербезпеки, що поєднує штучний інтелект, кібернетичне управління та автоматизоване реагування на загрози. Проект побудований на архітектурі мікросервісів з прогресивним підходом до безпеки та масштабованості.",
    version="1.0.0"
)

# Налаштування статичних файлів та шаблонів
# Створюємо папки якщо вони не існують
Path("static").mkdir(exist_ok=True)
Path("architecture").mkdir(exist_ok=True)

# Монтуємо статичні файли тільки якщо папки існують
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
if Path("architecture").exists():
    app.mount("/architecture", StaticFiles(directory="architecture"), name="architecture")

# Налаштування шаблонів
templates = Jinja2Templates(directory="templates")

# Створення директорії для логів (тільки локально)
if not os.getenv("RENDER"):
    Path("logs").mkdir(exist_ok=True)

# Створення бази даних SQLite
DATABASE_PATH = os.getenv("DATABASE_URL", "app.db")

def init_database():
    """Ініціалізація бази даних SQLite"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Створення таблиці для зберігання інформації про сесії
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        """)
        
        # Створення таблиці для зберігання логів аналізу
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                log_type TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise HTTPException(status_code=500, detail="Database initialization failed")

@app.on_event("startup")
async def startup_event():
    """Під час запуску додатку"""
    logger.info("AI Cyber Tool is starting up...")
    init_database()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Коренева сторінка з меню"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "version": "1.0.0",
        "status": "running"
    })

@app.get("/api")
async def api_root():
    """API коренева сторінка"""
    return {
        "message": "Welcome to AI Cyber Tool!",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "tech_map": "/tech-map",
            "docs": "/docs",
            "health": "/health",
            "api_diagrams": "/tech-map/api"
        }
    }

@app.get("/health")
async def health_check():
    """Перевірка здоров'я додатку"""
    try:
        # Перевірка підключення до бази даних
        conn = sqlite3.connect(DATABASE_PATH)
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "service": "AI Cyber Tool"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")

@app.get("/sessions")
async def get_sessions():
    """Отримання списку всіх сесій"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, session_name, created_at, status 
            FROM sessions 
            ORDER BY created_at DESC 
            LIMIT 50
        """)
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                "id": row[0],
                "session_name": row[1],
                "created_at": row[2],
                "status": row[3]
            })
        
        conn.close()
        return {"payload": sessions, "count": len(sessions)}
        
    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sessions")

@app.post("/sessions")
async def create_session(session_name: str):
    """Створення нової сесії"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (session_name) 
            VALUES (?)
        """, (session_name,))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created new session: {session_name} (ID: {session_id})")
        
        return {
            "message": "Session created successfully",
            "session_id": session_id,
            "session_name": session_name
        }
        
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@app.get("/sessions/{session_id}/logs")
async def get_session_logs(session_id: int):
    """Отримання логів для конкретної сесії"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT log_type, message, timestamp 
            FROM analysis_logs 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 100
        """, (session_id,))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                "log_type": row[0],
                "message": row[1],
                "timestamp": row[2]
            })
        
        conn.close()
        return {"payload": logs, "count": len(logs)}
        
    except Exception as e:
        logger.error(f"Failed to get session logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session logs")

@app.get("/tech-map", response_class=HTMLResponse)
async def tech_map(request: Request, lang: str = "uk"):
    """Технічна карта проекту"""
    try:
        # Перевірити чи існує файл документації
        doc_path = f"architecture/{lang}/technical_map.md"
        if not os.path.exists(doc_path):
            # Якщо файл не існує, використати українську версію
            doc_path = "architecture/uk/technical_map.md"
        
        # Читати Markdown файл
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Список діаграм
        diagrams = [
            {
                "name": "Прогресівна архітектура" if lang == "uk" else "Progressive Architecture",
                "file": "architecture_progressive",
                "description": "Розвиток проекту в три етапи" if lang == "uk" else "Project evolution in three phases"
            },
            {
                "name": "Компоненти API Gateway" if lang == "uk" else "API Gateway Components", 
                "file": "api_gateway_components",
                "description": "Архітектура шлюзу API" if lang == "uk" else "API Gateway architecture"
            },
            {
                "name": "AI Agent Service" if lang == "uk" else "AI Agent Service Components",
                "file": "ai_agent_service_components", 
                "description": "Компоненти AI сервісу" if lang == "uk" else "AI service components"
            },
            {
                "name": "Потік даних" if lang == "uk" else "Data Flow",
                "file": "data_flow_progressive",
                "description": "Послідовність взаємодії" if lang == "uk" else "Interaction sequence"
            },
            {
                "name": "Мережева архітектура" if lang == "uk" else "Network Architecture",
                "file": "network_architecture",
                "description": "Топологія мережі" if lang == "uk" else "Network topology"
            },
            {
                "name": "Модель даних" if lang == "uk" else "Data Model",
                "file": "data_model",
                "description": "ER діаграма бази даних" if lang == "uk" else "Database ER diagram"
            },
            {
                "name": "Архітектура безпеки" if lang == "uk" else "Security Architecture",
                "file": "security_architecture",
                "description": "Рівні безпеки системи" if lang == "uk" else "System security layers"
            },
            {
                "name": "MVP Архітектура з RabbitMQ" if lang == "uk" else "MVP Architecture with RabbitMQ",
                "file": "mvp_architecture",
                "description": "Мінімальний набір сервісів для MVP" if lang == "uk" else "Minimum viable product services"
            },
            {
                "name": "RabbitMQ Workflow" if lang == "uk" else "RabbitMQ Workflow",
                "file": "rabbitmq_workflow",
                "description": "Послідовність виконання завдань" if lang == "uk" else "Task execution sequence"
            },
            {
                "name": "Компоненти MVP Сервісів" if lang == "uk" else "MVP Services Components",
                "file": "mvp_services_components",
                "description": "Структура кожного сервісу" if lang == "uk" else "Structure of each service"
            }
        ]
        
        return templates.TemplateResponse("tech_map.html", {
            "request": request,
            "content": content,
            "diagrams": diagrams,
            "lang": lang
        })
        
    except Exception as e:
        logger.error(f"Failed to load tech map: {e}")
        raise HTTPException(status_code=500, detail="Failed to load technical map")

@app.get("/tech-map/api")
async def tech_map_api():
    """API для отримання інформації про технічну карту"""
    try:
        diagrams = []
        architecture_dir = Path("architecture")
        
        # Знайти всі PNG файли
        for png_file in architecture_dir.glob("*.png"):
            svg_file = png_file.with_suffix('.svg')
            mmd_file = png_file.with_suffix('.mmd')
            
            diagrams.append({
                "name": png_file.stem,
                "png_url": f"/architecture/{png_file.name}",
                "svg_url": f"/architecture/{svg_file.name}" if svg_file.exists() else None,
                "source_url": f"/architecture/{mmd_file.name}" if mmd_file.exists() else None
            })
        
        return {
            "diagrams": diagrams,
            "count": len(diagrams),
            "languages": ["uk", "en"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get tech map API: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve technical map data")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting AI Cyber Tool server...")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
