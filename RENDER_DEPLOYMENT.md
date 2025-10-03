# Розгортання на Render.com

## Налаштування Web Service на Render

### 1. Build Command (Команда збірки)
```bash
pip install -r requirements.txt
```

### 2. Start Command (Команда запуску)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT
```

## Пояснення команди запуску

- **gunicorn**: Менеджер процесів для production
- **-w 4**: 4 воркери (робочі процеси) для обробки запитів
- **-k uvicorn.workers.UvicornWorker**: Використання Uvicorn для асинхронних запитів
- **app:app**: 
  - Перше `app` - назва файлу (app.py)
  - Друге `app` - назва екземпляра FastAPI
- **--bind 0.0.0.0:$PORT**: Прив'язка до порту, наданого Render

## Змінні середовища (Environment Variables)

Додайте в налаштуваннях Render:

- **PYTHON_VERSION**: `3.13`
- **PYTHONUTF8**: `1` (для підтримки UTF-8)

## Структура проєкту

```
aicybertool/
├── app.py                 # Головний файл FastAPI
├── requirements.txt       # Залежності (включає gunicorn)
├── architecture/         # Статичні файли діаграм
├── templates/           # HTML шаблони
├── static/             # CSS/JS файли
└── RENDER_DEPLOYMENT.md # Цей файл
```

## Переваги цього підходу

✅ **Надійність**: Gunicorn забезпечує стабільність в production
✅ **Масштабованість**: 4 воркери обробляють кілька запитів одночасно  
✅ **Стандартність**: Рекомендований підхід для FastAPI
✅ **Простота**: Не потрібен складний скрипт запуску

## Примітки

- Скрипт `start_server.py` призначений тільки для локальної розробки
- Прапор `--reload` не використовується в production
- Render автоматично керує віртуальним середовищем
- Порт встановлюється автоматично через змінну `$PORT`