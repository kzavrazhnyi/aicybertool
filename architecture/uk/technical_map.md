# Технічна карта проекту AI Cyber Tool

## Огляд проекту

**AI Cyber Tool** - це комплексна система управління цифровою трансформацією, що поєднує штучний інтелект, кібернетичне управління та автоматизоване реагування на загрози. Проект побудований на архітектурі мікросервісів з прогресивним підходом до безпеки та масштабованості.

Проект розроблений з урахуванням прогресівного розвитку архітектури та підтримки багатомовності.

## Архітектурні діаграми

### 1. Прогресівна архітектура

![Прогресівна архітектура](architecture_progressive.png)

Проект розвивається в три етапи:

**Phase 1: MVP (Поточна версія)**
- FastAPI додаток
- SQLite база даних
- Loguru логування
- Базовий API для сесій

**Phase 2: Розширені функції**
- PostgreSQL база даних
- Структуроване логування
- AI Agent Service
- Аутентифікація
- API Gateway

**Phase 3: Повна платформа**
- Мікросервіси
- Розподілена база даних
- Централізоване логування
- AI оркестрація
- RBAC безпека
- Load Balancer
- Моніторинг

### 2. Компоненти API Gateway

![Компоненти API Gateway](api_gateway_components.png)

Архітектура включає:

- **Client Layer**: Web Browser, Mobile App, API Client
- **API Gateway Layer**: Load Balancer, Authentication, Rate Limiting, Cache
- **Application Layer**: FastAPI Application, Session Management, Logging
- **Data Layer**: SQLite Database, File Storage, Log Files
- **External Services**: AI Services, Cyber Security APIs

### 3. Компоненти AI Agent Service

![Компоненти AI Agent Service](ai_agent_service_components.png)

AI сервіс складається з:

- **Agent Manager**: Управління агентами та чергами завдань
- **Worker Pool**: Пул робочих процесів
- **AI Workers**: Analysis, Threat Detection, Response Workers
- **AI Models**: LLM, Threat Classifier, Code Analyzer
- **Data Processing**: Preprocessor, Feature Extractor, Validator
- **Storage & Cache**: Model Cache, Result Store, Temporary Storage

### 4. Потік даних

![Потік даних](data_flow_progressive.png)

Послідовність взаємодії:

1. **Створення сесії**: Client → API Gateway → FastAPI → Database
2. **Запит аналізу**: Client → API Gateway → FastAPI → AI Service
3. **Отримання логів**: Client → API Gateway → FastAPI → Database
4. **Health Check**: Client → API Gateway → FastAPI → Database

### 5. Мережева архітектура

![Мережева архітектура](network_architecture.png)

Мережева топологія:

- **Internet**: Users, External APIs
- **DMZ**: Load Balancer, Web Application Firewall
- **Application Tier**: FastAPI Instances (Port 8000)
- **Data Tier**: SQLite Primary/Replica (Port 5432), Redis Cache (Port 6379)
- **Monitoring Tier**: Prometheus (Port 9090), Grafana (Port 3000)
- **AI Services Tier**: AI Service (Port 8001), Model Server (Port 8002)

### 6. Модель даних

![Модель даних](data_model.png)

Основні таблиці:

- **SESSIONS**: Сесії користувачів
- **ANALYSIS_LOGS**: Логи аналізу
- **USERS**: Користувачі системи
- **AI_ANALYSES**: Результати AI аналізу
- **THREAT_DETECTIONS**: Виявлені загрози
- **SYSTEM_LOGS**: Системні логи

### 7. Архітектура безпеки

![Архітектура безпеки](security_architecture.png)

Рівні безпеки:

- **External Security**: SSL/TLS, DDoS Protection, WAF
- **Authentication & Authorization**: JWT, RBAC, MFA
- **API Security**: Rate Limiting, API Keys, CORS, Validation
- **Data Security**: Encryption, Hashing, Backup, Audit
- **Infrastructure Security**: Firewall, VPN, Monitoring, Alerts
- **AI Security**: Model Security, Data Privacy, AI Audit, Bias Detection

### 8. MVP Архітектура з RabbitMQ

![MVP Архітектура](mvp_architecture.png)

Мінімальний набір сервісів для MVP:

- **API Gateway**: Єдина точка входу з автентифікацією та авторизацією
- **Cybernetic Management**: Управління користувачами та реєстр інструментів
- **AI Agent Service**: Оркестратор завдань та планування кроків
- **Integrations Service**: Взаємодія з зовнішніми API (Jira, GitHub, Slack)
- **RabbitMQ Message Bus**: Асинхронна комунікація між сервісами

### 9. RabbitMQ Workflow

![RabbitMQ Workflow](rabbitmq_workflow.png)

Послідовність виконання завдання:

1. **Синхронний запит**: Користувач надсилає завдання через Flutter App
2. **Публікація Команди**: AI Agent публікує команду в RabbitMQ
3. **Виконання Команди**: Integrations Service виконує HTTP-запит до зовнішнього API
4. **Публікація Події**: Результат публікується як подія
5. **Реакція на Подію**: AI Agent оновлює статус завдання

### 10. Компоненти MVP Сервісів

![Компоненти MVP Сервісів](mvp_services_components.png)

Детальна структура кожного сервісу:

- **API Gateway**: Аутентифікація, авторизація, rate limiting, маршрутизація
- **Cybernetic Management**: Управління користувачами, реєстр інструментів, права доступу
- **AI Agent Service**: Планувальник завдань, виконавець, монітор, управління станом
- **Integrations Service**: Інтеграції з Jira, GitHub, Slack, вебхуки
- **Message Bus**: Exchanges, черги, маршрутизація, персистентність

## Технологічний стек

### Поточні технології
- **Backend**: FastAPI, Python 3.13
- **Database**: SQLite (з підтримкою PostgreSQL)
- **Logging**: Loguru
- **Environment**: Python venv
- **Deployment**: Render.com

### Планові технології для MVP
- **Message Bus**: RabbitMQ для асинхронної комунікації
- **Database**: PostgreSQL для основних даних, Redis для кешування
- **Authentication**: JWT, OAuth2, RBAC
- **AI Services**: OpenAI API, Anthropic API, Local Models
- **Integrations**: Jira API, GitHub API, Slack API
- **Monitoring**: Prometheus, Grafana
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Структура проекту

```
aicybertool/
├── app.py                    # Головний FastAPI додаток
├── requirements.txt          # Залежності Python
├── architecture/             # Технічні діаграми
│   ├── *.mmd               # Mermaid діаграми
│   ├── *.png               # Згенеровані зображення
│   ├── *.svg               # Векторні зображення
│   ├── uk/                 # Українська документація
│   └── en/                 # Англійська документація
├── scripts/                 # Допоміжні скрипти
│   └── utils/
│       └── render_mermaid.py # Генератор зображень
├── tests/                   # Тести
├── logs/                    # Логи додатку
└── venv/                    # Віртуальне середовище
```

## Команди для роботи

### Запуск сервера
```powershell
# Активація venv
venv\Scripts\Activate.ps1

# Запуск сервера
python app.py
```

### Генерація діаграм
```powershell
# Генерація зображень з Mermaid діаграм
.\architecture\generate_images.ps1
```

### Тестування
```powershell
# Запуск тестів
python -m pytest tests/
```

## Розвиток проекту

### Наступні кроки для MVP
1. **Phase 2**: Реалізація MVP архітектури
   - Налаштування RabbitMQ Message Bus
   - Створення Cybernetic Management Service
   - Розробка AI Agent Service з планувальником завдань
   - Інтеграція з зовнішніми API (Jira, GitHub)

2. **Phase 3**: Розширення функціональності
   - Додавання нових інтеграцій
   - Покращення AI планування
   - Система моніторингу та логування
   - Масштабування та оптимізація

3. **Phase 4**: Розширені можливості
   - AI Analysis Service
   - Notifications Service
   - Learning та Quality Services
   - Billing та Transformation Services

### Принципи розробки
- Прогресівний розвиток архітектури
- Багатомовна підтримка (українська/англійська)
- Безпека як пріоритет
- Масштабованість та надійність
- Документація як код

---

*Останнє оновлення: 2025.01.14*
