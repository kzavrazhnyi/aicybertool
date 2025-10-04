"""
AI Cyber Tool - Database Logic
Асинхронна логіка роботи з базою даних
"""

import aiosqlite
from datetime import datetime
from loguru import logger
from ..core.config import get_settings


settings = get_settings()


async def init_database():
    """Асинхронна ініціалізація бази даних SQLite"""
    try:
        async with aiosqlite.connect(settings.database_url) as conn:
            # Створення таблиці для зберігання інформації про сесії
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Створення таблиці для зберігання логів аналізу
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    log_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
            
            await conn.commit()
            logger.info("Database initialized successfully")
            
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_sessions():
    """Отримання списку всіх сесій"""
    try:
        async with aiosqlite.connect(settings.database_url) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute("""
                SELECT id, session_name, created_at, status
                FROM sessions
                ORDER BY created_at DESC
                LIMIT 50
            """)
            sessions_data = await cursor.fetchall()
            sessions = [dict(row) for row in sessions_data]
            return sessions
    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise


async def create_session(session_name: str):
    """Створення нової сесії"""
    try:
        async with aiosqlite.connect(settings.database_url) as conn:
            cursor = await conn.execute("""
                INSERT INTO sessions (session_name, created_at, status)
                VALUES (?, ?, ?)
            """, (session_name, datetime.utcnow().isoformat(), "active"))
            
            await conn.commit()
            session_id = cursor.lastrowid
            
            # Отримуємо створену сесію для відповіді
            cursor = await conn.execute("""
                SELECT id, session_name, created_at, status
                FROM sessions
                WHERE id = ?
            """, (session_id,))
            
            session_data = await cursor.fetchone()
            return session_data
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise


async def create_analysis_log(session_id: int, log_type: str, message: str):
    """Створення нового логу аналізу"""
    try:
        async with aiosqlite.connect(settings.database_url) as conn:
            # Перевіряємо чи існує сесія
            cursor = await conn.execute("""
                SELECT id FROM sessions WHERE id = ?
            """, (session_id,))
            
            if not await cursor.fetchone():
                raise ValueError("Session not found")
            
            # Створюємо лог
            cursor = await conn.execute("""
                INSERT INTO analysis_logs (session_id, log_type, message, timestamp)
                VALUES (?, ?, ?, ?)
            """, (session_id, log_type, message, datetime.utcnow().isoformat()))
            
            await conn.commit()
            log_id = cursor.lastrowid
            return log_id
    except Exception as e:
        logger.error(f"Failed to create analysis log: {e}")
        raise
