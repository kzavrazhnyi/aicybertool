# Cybernetic Management Service Specification

## Overview
Cybernetic Management Service є "мозковим центром" системи AICyberTool. Керує доменною логікою, користувачами, правами доступу та реєстром інструментів (Tool Registry). Надає AI Agent інформацію про доступні інструменти та способи їх використання.

## Architecture Components

### 1. Auth Service Module
- **User Management**: Створення, оновлення, видалення користувачів
- **Authentication**: Валідація облікових даних
- **Session Management**: Управління активними сесіями
- **Password Management**: Хешування, скидання паролів

### 2. Tool Registry Module
- **Service Catalog**: Реєстр всіх доступних інструментів/сервісів
- **Tool Metadata**: Опис параметрів, схем, версій інструментів
- **Capability Mapping**: Зв'язок між завданнями та інструментами
- **Version Management**: Управління версіями інструментів

### 3. Permissions Module
- **Access Control**: Система дозволів та обмежень
- **Role Management**: Управління ролями користувачів
- **Resource Permissions**: Дозволи на доступ до ресурсів
- **Dynamic Permissions**: Динамічні дозволи на основі контексту

### 4. User Management Module
- **User Profiles**: Профілі користувачів з метаданими
- **User Roles**: Призначення та управління ролями
- **User Preferences**: Налаштування користувачів
- **Audit Trail**: Логування дій користувачів

### 5. Configuration Module
- **System Settings**: Глобальні налаштування системи
- **Service Configuration**: Конфігурація інших сервісів
- **Feature Flags**: Управління функціональними прапорцями
- **Environment Settings**: Налаштування для різних середовищ

## Data Models

### User Model
```python
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    roles: List[Role]
    profile: UserProfile
    preferences: UserPreferences
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    is_active: bool
```

### Tool Model
```python
class Tool:
    id: UUID
    name: str
    description: str
    version: str
    service_name: str
    endpoint: str
    parameters_schema: dict
    response_schema: dict
    capabilities: List[str]
    required_permissions: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

### Role Model
```python
class Role:
    id: UUID
    name: str
    description: str
    permissions: List[Permission]
    is_system_role: bool
    created_at: datetime
    updated_at: datetime
```

## API Endpoints

### User Management
```
GET    /api/users                    # List users
POST   /api/users                    # Create user
GET    /api/users/{user_id}          # Get user
PUT    /api/users/{user_id}          # Update user
DELETE /api/users/{user_id}          # Delete user
POST   /api/users/{user_id}/roles    # Assign roles
```

### Tool Registry
```
GET    /api/tools                    # List tools
POST   /api/tools                    # Register tool
GET    /api/tools/{tool_id}          # Get tool
PUT    /api/tools/{tool_id}          # Update tool
DELETE /api/tools/{tool_id}          # Unregister tool
GET    /api/tools/search              # Search tools by capability
```

### Authentication
```
POST   /api/auth/login               # User login
POST   /api/auth/logout              # User logout
POST   /api/auth/refresh             # Refresh token
GET    /api/auth/me                   # Get current user
POST   /api/auth/reset-password      # Reset password
```

### Permissions
```
GET    /api/permissions              # List permissions
GET    /api/permissions/check        # Check user permissions
POST   /api/permissions/grant        # Grant permission
POST   /api/permissions/revoke       # Revoke permission
```

## Tool Registry Schema

### Tool Registration Format
```json
{
  "name": "jira_project_finder",
  "description": "Find projects in Jira by name",
  "version": "1.0.0",
  "service_name": "integrations",
  "endpoint": "/api/integrations/jira/projects",
  "method": "GET",
  "parameters_schema": {
    "type": "object",
    "properties": {
      "project_name": {
        "type": "string",
        "description": "Name of the project to search"
      },
      "fields": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Fields to return"
      }
    },
    "required": ["project_name"]
  },
  "response_schema": {
    "type": "object",
    "properties": {
      "projects": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "key": {"type": "string"}
          }
        }
      }
    }
  },
  "capabilities": ["jira", "project_management", "search"],
  "required_permissions": ["jira.read"]
}
```

## Security Requirements

### Authentication
- Bcrypt для хешування паролів
- JWT токени для автентифікації
- Multi-factor authentication (MFA) опціонально
- Account lockout після невдалих спроб

### Authorization
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Principle of least privilege
- Regular permission audits

### Data Protection
- Encryption at rest для чутливих даних
- Encryption in transit (TLS 1.3)
- PII data anonymization
- GDPR compliance

## Technology Stack

### Core Technologies
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT + OAuth2
- **Password Hashing**: bcrypt

### Dependencies
- `fastapi`: Web framework
- `sqlalchemy`: ORM
- `alembic`: Database migrations
- `python-jose`: JWT handling
- `passlib`: Password hashing
- `redis`: Caching
- `pydantic`: Data validation

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile JSONB,
    preferences JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Tools Table
```sql
CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    version VARCHAR(20) NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    parameters_schema JSONB NOT NULL,
    response_schema JSONB NOT NULL,
    capabilities TEXT[],
    required_permissions TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Roles Table
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB NOT NULL,
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/cybernetic_mgmt
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Redis
REDIS_URL=redis://localhost:6379
REDIS_SESSION_TTL=3600

# Authentication
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=12
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Monitoring & Logging

### Metrics
- User authentication success/failure rate
- Tool registry access patterns
- Permission check performance
- Database query performance
- Cache hit/miss ratio

### Logging
- Authentication events
- Permission changes
- Tool registry modifications
- User management actions
- Security events

## Testing

### Unit Tests
- User management tests
- Tool registry tests
- Permission system tests
- Authentication tests

### Integration Tests
- Database integration tests
- Cache integration tests
- API endpoint tests
- Security tests

### Performance Tests
- Concurrent user simulation
- Database load testing
- Cache performance testing
- API response time testing
