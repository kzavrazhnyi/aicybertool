# Інструкції для підключення до GitHub

## Крок 1: Створіть репозиторій на GitHub
1. Перейдіть на https://github.com
2. Натисніть "New repository"
3. Назва: `aicybertool`
4. Опис: "AI Cyber Tool - проект для роботи з AI та кібербезпечністю"
5. НЕ ставайте галочки на README, .gitignore, license
6. Натисніть "Create repository"

## Крок 2: Підключіть локальний репозиторій
Замініть `YOUR_USERNAME` на ваш GitHub username і виконайте команди:

```bash
git remote add origin https://github.com/YOUR_USERNAME/aicybertool.git
git branch -M main
git push -u origin main
```

## Після підключення GitHub:

### Крок 3: Встановіть Python та створіть venv
1. Встановіть Python з https://python.org/downloads/
2. Створіть віртуальне середовище:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Встановіть залежністьі:
   ```bash
   pip install -r requirements.txt
   ```

### Типові команди для роботи з Git:
```bash
# Перевірити статус
git status

# Додати зміни
git add .

# Зробити коміт
git commit -m "Опис змін"

# Відправити зміни на GitHub
git push

# Отримати останні зміни з GitHub
git pull
```
