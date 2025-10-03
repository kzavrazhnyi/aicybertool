#!/usr/bin/env python3
"""
Скрипт запуску AI Cyber Tool сервера
Використання: python start_server.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_venv():
    """Перевірка чи активоване віртуальне середовище"""
    venv_path = str(sys.prefix)
    if "venv" not in venv_path.lower():
        print("❌ Віртуальне середовище не активоване!")
        print("📝 Активуйте віртуальне середовище командою:")
        print("   venv\\Scripts\\Activate.ps1")
        return False
    
    print(f"✅ Віртуальне середовище активоване: {venv_path}")
    return True

def check_requirements():
    """Перевірка встановлених залежностей"""
    try:
        import fastapi
        import uvicorn
        print("✅ Основні залежності встановлені")
        return True
    except ImportError as e:
        print(f"❌ Відсутні необхідні залежності: {e}")
        print("📝 Встановіть залежності командою:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Головна функція запуску сервера"""
    print("🚀 AI Cyber Tool - Запуск сервера")
    print("="*50)
    
    # Перевірки
    if not check_venv():
        sys.exit(1)
    
    if not check_requirements():
        sys.exit(1)
    
    # Перевірка чи існують необхідні файли
    if not Path("app.py").exists():
        print("❌ Файл app.py не знайдено!")
        print("📝 Переконайтеся що ви знаходитесь у кореневій директорії проекту")
        sys.exit(1)
    
    print("="*100)
    print("🌐 Запуск FastAPI сервера...")
    print("📱 Відкрийте браузер та перейдіть за адресою: http://localhost:8000")
    print("📖 API документація: http://localhost:8000/docs")
    print("🔧 Health check: http://localhost:8000/health")
    print("="*100)
    
    try:
        # Запуск сервера через uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка запуску сервера: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
