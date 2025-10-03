# -*- coding: utf-8 -*-
"""
Mermaid Diagram Renderer
Скрипт для генерації зображень з Mermaid діаграм
"""

import argparse
import sys
import os
from pathlib import Path
import subprocess
import json

def info(msg):
    """Вивести інформаційне повідомлення"""
    print(f"INFO: {msg}")

def ok(msg):
    """Вивести повідомлення про успіх"""
    print(f"OK: {msg}")

def err(msg):
    """Вивести повідомлення про помилку"""
    print(f"ERROR: {msg}")

def check_mermaid_cli():
    """Перевірити чи встановлений Mermaid CLI"""
    try:
        # Спробувати знайти mmdc в PATH
        result = subprocess.run(['mmdc', '--version'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Спробувати знайти mmdc.cmd в стандартному місці npm
            result = subprocess.run(['C:\\Users\\KZ\\AppData\\Roaming\\npm\\mmdc.cmd', '--version'], 
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def install_mermaid_cli():
    """Встановити Mermaid CLI через npm"""
    try:
        info("Installing Mermaid CLI...")
        subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'], 
                      check=True)
        ok("Mermaid CLI installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        err(f"Failed to install Mermaid CLI: {e}")
        return False

def render_diagram(input_file, output_file, format_type='png'):
    """Рендерити Mermaid діаграму в зображення"""
    try:
        # Перевірити чи існує вхідний файл
        if not os.path.exists(input_file):
            err(f"Input file not found: {input_file}")
            return False
        
        # Визначити команду mmdc
        mmdc_cmd = 'mmdc'
        try:
            subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            mmdc_cmd = 'C:\\Users\\KZ\\AppData\\Roaming\\npm\\mmdc.cmd'
        
        # Команда для рендерингу з високою якістю
        cmd = [
            mmdc_cmd,
            '-i', input_file,
            '-o', output_file,
            '-e', format_type,
            '-w', '2400',      # Збільшена ширина для кращої якості
            '-H', '1600',      # Збільшена висота для кращої якості
            '-b', 'white',     # Білий фон
            '--scale', '2'     # Масштаб 2x для кращої якості
        ]
        
        info(f"Rendering {input_file} to {output_file} ({format_type})")
        
        # Виконати команду
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            ok(f"Successfully rendered {output_file}")
            return True
        else:
            err(f"Failed to render diagram: {result.stderr}")
            return False
            
    except Exception as e:
        err(f"Error rendering diagram: {e}")
        return False

def main():
    """Головна функція"""
    parser = argparse.ArgumentParser(description='Render Mermaid diagrams to images')
    parser.add_argument('--input', '-i', required=True, help='Input Mermaid file (.mmd)')
    parser.add_argument('--output', '-o', required=True, help='Output image file')
    parser.add_argument('--format', '-f', default='png', choices=['png', 'svg', 'pdf'], 
                       help='Output format (default: png)')
    
    args = parser.parse_args()
    
    # Перевірити чи встановлений Mermaid CLI
    if not check_mermaid_cli():
        info("Mermaid CLI not found. Attempting to install...")
        if not install_mermaid_cli():
            err("Failed to install Mermaid CLI. Please install manually:")
            err("npm install -g @mermaid-js/mermaid-cli")
            sys.exit(1)
    
    # Рендерити діаграму
    if render_diagram(args.input, args.output, args.format):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
