"""
AI Cyber Tool - Main Application
Простий FastAPI додаток для роботи з AI та кібербезпекою
"""

from fastapi import FastAPI, HTTPException
from loguru import logger
import sqlite3
from pathlib import Path

# Налаштування логування
logger.add("logs/app.log", rotation="10 MB", retention="7 days")

# Створення FastAPI додатку
app = FastAPI(
    title="AI Cyber Tool",
    description="AI Cyber Tool - проект для роботи з AI та кібербезпечністю",
    version="1.0.0"
)

# Створення директорії для логів
Path("logs").mkdir(exist_ok=True)

# Створення бази даних SQLite
DATABASE_PATH = "app.db"

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

@app.get("/")
async def root():
    """Коренева сторінка"""
    return {
        "message": "Welcome to<｜tool▁sep｜>AI Cyber Tool!",
        "version": "1.0.0",
        "status": "running"
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
