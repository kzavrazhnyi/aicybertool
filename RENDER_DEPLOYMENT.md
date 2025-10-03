# Деплой AI Cyber Tool на Render

## Кроки для публікації на Render

### 1. Кнопки та налаштування веб-сервісу

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python -m uvicorn app:app --host 0.0.0.0 --port $PORT
```

**Альтернативний Start Command:**
```bash
python render_deploy.py
```

### 2. Environment Variables

Додайте наступні змінні оточення на Render:

| Змінна | Значення | Опис |
|--------|----------|------|
| `PYTHON_VERSION` | `3.13.7` | Версія Python |
| `DATABASE_URL` | `sqlite:///./app.db` | Шлях до бази даних |
| `RENDER` | `true` | Позначає що додаток працює на Render |

### 3. Структура файлів для Render

Проект повинен містити:
- `app.py` - головний FastAPI додаток
- `requirements.txt` - залежності Python
- `render.yaml` - конфігурація для автоматичного деплою
- `render_deploy.py` - альтернативний скрипт запуску

### 4. Особливості деплою на Render

#### Логування
- На Render використовується stdout замість файлів
- Логи доступні в панелі Render

#### База даних
- SQLite файл зберігається в тимчасовому сховищі
- Для постійного зберігання використовуйте PostgreSQL
- Можна замовкати диск для постійного зберігання

#### Портовий доступ
- Render автоматично збирає порт з змінної $PORT
- Додаток недоачливий на портах 10000+

### 5. Автоматичний деплой

Для автоматичного деплою при пуші до GitHub:

1. Підключіть GitHub репозиторій до Render
2. Визерніть гілку master для деплою
3. Render автоматично виявить змінні у `requirements.txt`

### 6. Перевірка роботи

Після деплою перевірте:
- https://your-app.onrender.com/ - головна сторінка
- https://your-app.onrender.com/docs - API документація
- https://your-app.onrender.com/health - перевірка стану

### 7. Альтернативи для деплою

#### Варіант A: Простий Start Command
```bash
python -m uvicorn app:app --host 0.0.0.0 --port $PORT
```

#### Варіант B: З конфігурацією
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
```

#### Варіант C: Через скрипт
```bash
python render_deploy.py
```

### 8. Можливі проблеми

1. **Timeout при холодному старті**
   - Render має обмежений час старту для free плану
   - Рекомендується оптимізувати час ініціалізації

2. **Переповнення диску**
   - SQLite файли можуть розростатися
   - Використовуйте PostgreSQL для продакшену

3. **Пам'ять**
   - Free план має обмеження пам'яті
   - Слідкуйте за використанням

Зараз проект готовий до деплою на Render!
