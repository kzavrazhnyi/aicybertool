# AI Cyber Tool

**AI Cyber Tool** - це комплексна система управління цифровою трансформацією, що поєднує штучний інтелект, кібернетичне управління та автоматизоване реагування на загрози. Проект побудований на архітектурі мікросервісів з прогресивним підходом до безпеки та масштабованості.

## Встановлення та запуск

### Передумови
- Python 3.11 або новіша версія
- Git

### Кроки встановлення

1. **Встановіть Python** (якщо ще не встановлений):
   - Перейдіть на https://python.org/downloads/
   - Завантажте останню версію для Windows
   - Під час встановлення обов'язково поставте галочку "Add Python to PATH"

2. **Клонуйте репозиторій**:
   ```bash
   git clone <ваш-репозиторій-url>
   cd aicybertool
   ```

3. **Створіть та активуйте віртуальне середовище**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Встановіть залежністьі**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Запуск сервера**:

   **Для локальної розробки (з автоперезавантаженням):**
   ```bash
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

   **Для тестування production режиму:**
   ```bash
   python start_gunicorn.py
   ```

6. **Відкрийте браузер**:
   - Головна сторінка: http://localhost:8000
   - Технічна карта: http://localhost:8000/tech-map
   - API документація: http://localhost:8000/docs

## Структура проекту

```
aicybertool/
├── app.py                 # Головний файл FastAPI
├── start_gunicorn.py      # Скрипт для production тестування
├── requirements.txt       # Залежності Python (включає gunicorn)
├── RENDER_DEPLOYMENT.md   # Інструкції для розгортання на Render
├── architecture/          # Архітектурні діаграми та документація
├── templates/            # HTML шаблони
├── static/               # CSS/JS файли
├── scripts/              # Допоміжні скрипти
├── tests/                # Тести
├── venv/                 # Віртуальне середовище
└── README.md             # Цей файл
```

## Розгортання на Render.com

Для розгортання на Render.com використовуйте налаштування з файлу `RENDER_DEPLOYMENT.md`:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT
```

## Розробка

Для розробки рекомендується:

1. Активувати віртуальне середовище:
   ```bash
   venv\Scripts\activate
   ```

2. Запустити тести:
   ```bash
   pytest
   ```

## Ліцензія

[Додайте інформацію про ліцензію]
