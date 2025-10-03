#!/usr/bin/env python3
"""
Render deployment script для AI Cyber Tool
Використовується для запуску додатку на Render
"""

import os
import sys

def main():
    """Головна функція для запуску на Render"""
    print("Starting AI Cyber Tool on Render...")
    
    # Перевірка змінних оточення
    port = os.environ.get('PORT', '8000')
    host = '0.0.0.0'
    
    print(f"Server will run on {host}:{port}")
    
    # Імпорт та запуск uvicorn
    try:
        import uvicorn
        from app import app
        
        # Запуск сервера
        uvicorn.run(
            "app:app",
            host=host,
            port=int(port),
            workers=1,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
