# API Gateway Service Specification

## Overview
API Gateway є єдиною точкою входу для всіх зовнішніх запитів до системи AICyberTool. Забезпечує централізовану автентифікацію, авторизацію, маршрутизацію та захист внутрішніх сервісів.

## Architecture Components

### 1. Authentication Module
- **JWT Validation**: Перевірка токенів автентифікації
- **Session Management**: Управління сесіями користувачів
- **Token Refresh**: Автоматичне оновлення токенів

### 2. Authorization Module
- **RBAC Check**: Перевірка ролей та прав доступу
- **Permission Validation**: Валідація дозволів для операцій
- **Resource Access Control**: Контроль доступу до ресурсів

### 3. Rate Limiting Module
- **Request Throttling**: Обмеження кількості запитів
- **IP-based Limiting**: Обмеження по IP адресах
- **User-based Limiting**: Обмеження по користувачах

### 4. Request Routing Module
- **Service Discovery**: Пошук доступних сервісів
- **Load Balancing**: Розподіл навантаження
- **Circuit Breaker**: Захист від каскадних збоїв

### 5. Response Cache Module
- **Redis Integration**: Кешування відповідей
- **Cache Invalidation**: Інвалідація кешу
- **TTL Management**: Управління часом життя кешу

## API Endpoints

### Authentication Endpoints
```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
GET  /api/auth/me
```

### Agent Endpoints
```
POST /api/agent/tasks
GET  /api/agent/tasks/{task_id}
GET  /api/agent/tasks/{task_id}/result
GET  /api/agent/tasks/{task_id}/status
```

### Management Endpoints
```
GET  /api/management/tools
GET  /api/management/users
POST /api/management/users
PUT  /api/management/users/{user_id}
```

## Security Requirements

### Authentication
- JWT токени з підписом RS256
- Термін дії токена: 15 хвилин
- Refresh токен: 7 днів
- Secure cookies для refresh токенів

### Authorization
- Role-based access control (RBAC)
- Ролі: admin, user, viewer
- Дозволи: read, write, execute, manage

### Rate Limiting
- 1000 запитів на хвилину на користувача
- 10000 запитів на хвилину на IP
- Burst: 200 запитів за 10 секунд

## Technology Stack

### Core Technologies
- **Framework**: FastAPI
- **Authentication**: JWT + OAuth2
- **Cache**: Redis
- **Database**: PostgreSQL (for sessions)

### Dependencies
- `fastapi`: Web framework
- `python-jose`: JWT handling
- `redis`: Caching
- `asyncpg`: PostgreSQL async driver
- `httpx`: HTTP client for service calls

## Configuration

### Environment Variables
```bash
# Authentication
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=RS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379
REDIS_CACHE_TTL=300

# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# Rate Limiting
RATE_LIMIT_PER_MINUTE=1000
RATE_LIMIT_BURST=200
```

## Monitoring & Logging

### Metrics
- Request count per endpoint
- Response time percentiles
- Error rate by service
- Authentication success/failure rate

### Logging
- Structured logging with JSON format
- Request/response logging
- Security event logging
- Performance metrics logging

## Deployment

### Docker Configuration
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks
- `/health`: Basic health check
- `/health/detailed`: Detailed system status
- `/metrics`: Prometheus metrics

## Testing

### Unit Tests
- Authentication module tests
- Authorization module tests
- Rate limiting tests
- Routing tests

### Integration Tests
- End-to-end API tests
- Service communication tests
- Cache integration tests

### Load Tests
- Concurrent user simulation
- Rate limiting validation
- Performance benchmarking
