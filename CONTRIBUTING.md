# Допомога у розробці AI Cyber Tool

Дякуємо за ваш інтерес до проекту AI Cyber Tool!

## Передумови для розробки

### Технічні вимоги
- Python 3.11 або новіша версія
- Git
- Віртуальне середовище Python

### Налаштування середовища розробки

1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/kzavrazhnyi/aicybertool.git
   cd aicybertool
   ```

2. **Створіть та активуйте віртуальне середовище:**
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate   # Linux/macOS
   ```

3. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Запустіть тести:**
   ```bash
   python tests/test_app.py
   pytest
   ```

## Структура роботи з Git

### Основні команди
```bash
# Перевірити статус
git status

# Додати зміни
git add .

# Зробити коміт
git commit -m "Опис змін"

# Відправити зміни
git push

# Отримати останні зміни
git pull
```

### Гілки для розробки
- `master` - головна гілка (стабільна версія)
- `develop` - гілка розробки
- `feature/назва-функції` - гілки для нових функцій

### Правила комітів
Використовуйте описові коміти:
- `feat: add new authentication system`
- `fix: resolve database connection issue`
- `docs: update README with installation steps`
- `test: add security tests for API endpoints`

## Структура проекту

```
aicybertool/
├── app/                 # Основний код додатку
├── tests/              # Тести
├── logs/               # Логи додатку
├── venv/               # Віртуальне середовище
├── requirements.txt    # Залежності Python
├── .gitignore         # Git ignore файл
├── README.md          # Основна документація
├── CONTRIBUTING.md    # Цей файл
└── setup_github.md    # Інструкції налаштування GitHub
```

## Тестування

Перед відправкою змін обов'язково запустіть тести:

```bash
python tests/test_app.py
```

Тести повинні:
- Перевіряти роботу віртуального середовища
- Тестувати підключення до бази даних
- Перевіряти коректність імпорту основних модулів

## Контакти

Якщо у вас є питання щодо розробки проекту:
- Створіть Issue на GitHub
- Опишіть проблему детально
- Додайте інформацію про середовище виконання

## Ліцензія

Проект розробляється відкрито для спільноти з дотриманням принципів відкритого коду.
