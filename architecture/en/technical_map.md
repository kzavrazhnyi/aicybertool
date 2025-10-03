# Technical Map - AI Cyber Tool Project

## Project Overview

**AI Cyber Tool** is a comprehensive digital transformation management system that combines artificial intelligence, cybernetic management, and automated threat response. The project is built on a microservices architecture with a progressive approach to security and scalability.

The project is developed with progressive architecture evolution and multilingual support in mind.

## Architecture Diagrams

### 1. Progressive Architecture

![Progressive Architecture](architecture_progressive.png)

The project evolves in three phases:

**Phase 1: MVP (Current Version)**
- FastAPI application
- SQLite database
- Loguru logging
- Basic sessions API

**Phase 2: Enhanced Features**
- PostgreSQL database
- Structured logging
- AI Agent Service
- Authentication
- API Gateway

**Phase 3: Full Platform**
- Microservices
- Distributed database
- Centralized logging
- AI orchestration
- RBAC security
- Load Balancer
- Monitoring

### 2. API Gateway Components

![API Gateway Components](api_gateway_components.png)

Architecture includes:

- **Client Layer**: Web Browser, Mobile App, API Client
- **API Gateway Layer**: Load Balancer, Authentication, Rate Limiting, Cache
- **Application Layer**: FastAPI Application, Session Management, Logging
- **Data Layer**: SQLite Database, File Storage, Log Files
- **External Services**: AI Services, Cyber Security APIs

### 3. AI Agent Service Components

![AI Agent Service Components](ai_agent_service_components.png)

AI service consists of:

- **Agent Manager**: Agent management and task queues
- **Worker Pool**: Worker process pool
- **AI Workers**: Analysis, Threat Detection, Response Workers
- **AI Models**: LLM, Threat Classifier, Code Analyzer
- **Data Processing**: Preprocessor, Feature Extractor, Validator
- **Storage & Cache**: Model Cache, Result Store, Temporary Storage

### 4. Data Flow

![Data Flow](data_flow_progressive.png)

Interaction sequence:

1. **Session Creation**: Client → API Gateway → FastAPI → Database
2. **Analysis Request**: Client → API Gateway → FastAPI → AI Service
3. **Log Retrieval**: Client → API Gateway → FastAPI → Database
4. **Health Check**: Client → API Gateway → FastAPI → Database

### 5. Network Architecture

![Network Architecture](network_architecture.png)

Network topology:

- **Internet**: Users, External APIs
- **DMZ**: Load Balancer, Web Application Firewall
- **Application Tier**: FastAPI Instances (Port 8000)
- **Data Tier**: SQLite Primary/Replica (Port 5432), Redis Cache (Port 6379)
- **Monitoring Tier**: Prometheus (Port 9090), Grafana (Port 3000)
- **AI Services Tier**: AI Service (Port 8001), Model Server (Port 8002)

### 6. Data Model

![Data Model](data_model.png)

Main tables:

- **SESSIONS**: User sessions
- **ANALYSIS_LOGS**: Analysis logs
- **USERS**: System users
- **AI_ANALYSES**: AI analysis results
- **THREAT_DETECTIONS**: Detected threats
- **SYSTEM_LOGS**: System logs

### 7. Security Architecture

![Security Architecture](security_architecture.png)

Security layers:

- **External Security**: SSL/TLS, DDoS Protection, WAF
- **Authentication & Authorization**: JWT, RBAC, MFA
- **API Security**: Rate Limiting, API Keys, CORS, Validation
- **Data Security**: Encryption, Hashing, Backup, Audit
- **Infrastructure Security**: Firewall, VPN, Monitoring, Alerts
- **AI Security**: Model Security, Data Privacy, AI Audit, Bias Detection

### 8. MVP Architecture with RabbitMQ

![MVP Architecture](mvp_architecture.png)

Minimum viable product services:

- **API Gateway**: Single entry point with authentication and authorization
- **Cybernetic Management**: User management and tool registry
- **AI Agent Service**: Task orchestrator and step planner
- **Integrations Service**: External API interactions (Jira, GitHub, Slack)
- **RabbitMQ Message Bus**: Asynchronous communication between services

### 9. RabbitMQ Workflow

![RabbitMQ Workflow](rabbitmq_workflow.png)

Task execution sequence:

1. **Synchronous Request**: User sends task through Flutter App
2. **Command Publishing**: AI Agent publishes command to RabbitMQ
3. **Command Execution**: Integrations Service executes HTTP request to external API
4. **Event Publishing**: Result is published as an event
5. **Event Reaction**: AI Agent updates task status

### 10. MVP Services Components

![MVP Services Components](mvp_services_components.png)

Detailed structure of each service:

- **API Gateway**: Authentication, authorization, rate limiting, routing
- **Cybernetic Management**: User management, tool registry, access control
- **AI Agent Service**: Task planner, executor, monitor, state management
- **Integrations Service**: Jira, GitHub, Slack integrations, webhooks
- **Message Bus**: Exchanges, queues, routing, persistence

## Technology Stack

### Current Technologies
- **Backend**: FastAPI, Python 3.13
- **Database**: SQLite (with PostgreSQL support)
- **Logging**: Loguru
- **Environment**: Python venv
- **Deployment**: Render.com

### Planned Technologies for MVP
- **Message Bus**: RabbitMQ for asynchronous communication
- **Database**: PostgreSQL for main data, Redis for caching
- **Authentication**: JWT, OAuth2, RBAC
- **AI Services**: OpenAI API, Anthropic API, Local Models
- **Integrations**: Jira API, GitHub API, Slack API
- **Monitoring**: Prometheus, Grafana
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Project Structure

```
aicybertool/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── architecture/             # Technical diagrams
│   ├── *.mmd               # Mermaid diagrams
│   ├── *.png               # Generated images
│   ├── *.svg               # Vector images
│   ├── uk/                 # Ukrainian documentation
│   └── en/                 # English documentation
├── scripts/                 # Utility scripts
│   └── utils/
│       └── render_mermaid.py # Image generator
├── tests/                   # Tests
├── logs/                    # Application logs
└── venv/                    # Virtual environment
```

## Working Commands

### Start Server
```powershell
# Activate venv
venv\Scripts\Activate.ps1

# Start server
python app.py
```

### Generate Diagrams
```powershell
# Generate images from Mermaid diagrams
.\architecture\generate_images.ps1
```

### Testing
```powershell
# Run tests
python -m pytest tests/
```

## Project Development

### Next Steps for MVP
1. **Phase 2**: Implement MVP architecture
   - Set up RabbitMQ Message Bus
   - Create Cybernetic Management Service
   - Develop AI Agent Service with task planner
   - Integrate with external APIs (Jira, GitHub)

2. **Phase 3**: Expand functionality
   - Add new integrations
   - Improve AI planning
   - Monitoring and logging system
   - Scaling and optimization

3. **Phase 4**: Advanced capabilities
   - AI Analysis Service
   - Notifications Service
   - Learning and Quality Services
   - Billing and Transformation Services

### Development Principles
- Progressive architecture evolution
- Multilingual support (Ukrainian/English)
- Security as priority
- Scalability and reliability
- Documentation as code

---

*Last updated: 2025.01.14*
