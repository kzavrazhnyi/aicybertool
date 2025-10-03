"""
Тести для AI Cyber Tool додатку
"""

import pytest
import sys
import os
from pathlib import Path

# Додаємо кореневу директорію проекту до Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_venv_environment():
    """Тест перевіряє чи працює віртуальне середовище"""
    import fastapi
    import uvicorn
    import sqlalchemy
    import loguru
    
    # Перевірка що основні пакети доступні
    assert fastapi is not None
    assert uvicorn is not None
    assert sqlalchemy is not None
    assert loguru is not None
    
    print(f"SUCCESS: All packages imported successfully")
    print(f"FastAPI version: {fastapi.__version__}")
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")

def test_database_creation():
    """Тест перевіряє створення бази даних"""
    import sqlite3
    
    # Створюємо тестову базу даних
    test_db = "test_app.db"
    
    try:
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Тестуємо створення таблиці
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        
        # Тестуємо вставку даних
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        
        # Тестуємо читання даних
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        
        assert len(rows) == 1
        assert rows[0][1] == "test"
        
        conn.commit()
        conn.close()
        
        # Видаляємо тестову базу даних
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print("SUCCESS: Database operations work correctly")
        
    except Exception as e:
        # Видаляємо тестову базу даних в разі помилки
        if os.path.exists(test_db):
            os.remove(test_db)
        raise e

def test_app_import():
    """Тест перевіряє імпорт головного додатку"""
    try:
        from app import app
        assert app is not None
        print("SUCCESS: App imported successfully")
        
        # Перевірка що app є FastAPI додатком
        assert hasattr(app, 'routes')
        assert hasattr(app, 'get')
        
    except Exception as e:
        print(f"ERROR: Failed to import app: {e}")
        raise e

if __name__ == "__main__":
    print("AI Cyber Tool - Testing")
    print("="*50)
    
    # Перевірка чи працюємо у віртуальному середовищі
    import sys
    venv_path = str(sys.prefix)
    if "venv" in venv_path.lower():
        print(f"VIRTUAL ENV: {venv_path}")
    else:
        print(f"WARNING: Virtual environment not activated. Current prefix: {venv_path}")
    
    print("="*50)
    
    # Запускаємо тести
    test_venv_environment()
    test_database_creation()
    test_app_import()
    
    print("="*50)
    print("SUCCESS: All tests passed!")
