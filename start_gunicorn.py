# -*- coding: utf-8 -*-
"""
Локальний запуск з Uvicorn для тестування production конфігурації
(Windows-сумісна версія з перевіркою venv)
"""

import subprocess
import sys
import os
import platform

def check_venv():
    """Перевірка чи активоване віртуальне середовище"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activate_venv():
    """Знайти Python з віртуального середовища"""
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return None

def check_requirements(python_executable):
    """Перевірка встановлених залежностей"""
    try:
        result = subprocess.run([python_executable, "-c", "import fastapi, uvicorn"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("OK: Main dependencies installed")
            return True
        else:
            print(f"ERROR: Missing required dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: Error checking dependencies: {e}")
        return False

def main():
    """Запуск сервера з Uvicorn для тестування production налаштувань"""
    print("INFO: AI Cyber Tool - Starting with Uvicorn (Production mode)")
    print("="*60)
    
    # Перевірити віртуальне середовище
    if not check_venv():
        print("ERROR: Virtual environment not activated!")
        print("INFO: Activate virtual environment with command:")
        print("   venv\\Scripts\\Activate.ps1")
        
        # Спробувати використати venv Python напряму
        venv_python = activate_venv()
        if venv_python:
            print("INFO: Attempting to use venv Python directly...")
            python_executable = venv_python
        else:
            print("ERROR: Virtual environment not found!")
            sys.exit(1)
    else:
        print("OK: Virtual environment is activated")
        python_executable = sys.executable
    
    # Перевірити залежності
    if not check_requirements(python_executable):
        print("INFO: Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # На Windows використовуємо uvicorn замість gunicorn
    if platform.system() == "Windows":
        print("INFO: Windows detected - using Uvicorn instead of Gunicorn")
        cmd = [
            python_executable, "-m", "uvicorn",
            "app:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--workers", "1",  # На Windows використовуємо 1 worker
            "--access-log",  # Логи в консоль
            "--log-level", "info"
        ]
    else:
        # На Unix-системах використовуємо gunicorn
        cmd = [
            "gunicorn",
            "-w", "4",  # 4 воркери
            "-k", "uvicorn.workers.UvicornWorker",  # Uvicorn worker
            "app:app",  # app.py:app
            "--bind", "0.0.0.0:8000",  # Локальний порт
            "--access-logfile", "-",  # Логи в консоль
            "--error-logfile", "-"    # Помилки в консоль
        ]
    
    print("INFO: Starting server...")
    print("INFO: Server will be available at: http://localhost:8000")
    print("INFO: Technical map: http://localhost:8000/tech-map")
    print("INFO: Press Ctrl+C to stop")
    print("="*60)
    
    try:
        # Запустити сервер
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nINFO: Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
