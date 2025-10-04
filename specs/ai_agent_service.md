# AI Agent Service Specification

## Overview
AI Agent Service є ядром системи AICyberTool. Отримує завдання від користувачів, розбиває їх на кроки (планує) та координує роботу інших сервісів (інструментів) для досягнення мети. Це сам "агент", який виконує роботу.

## Architecture Components

### 1. Task Planner Module
- **Step Decomposition**: Розбиття складних завдань на кроки
- **Tool Selection**: Вибір відповідних інструментів для кожного кроку
- **Dependency Resolution**: Визначення залежностей між кроками
- **Plan Optimization**: Оптимізація плану виконання

### 2. Task Executor Module
- **Command Publisher**: Публікація команд до Message Bus
- **Execution Orchestration**: Координація виконання кроків
- **Parallel Execution**: Паралельне виконання незалежних кроків
- **Retry Logic**: Логіка повторних спроб при збоях

### 3. Task Monitor Module
- **Event Consumer**: Слухання подій від Message Bus
- **Progress Tracking**: Відстеження прогресу виконання
- **Status Updates**: Оновлення статусу завдань
- **Error Handling**: Обробка помилок та винятків

### 4. State Manager Module
- **Task Status**: Управління статусами завдань
- **Context Preservation**: Збереження контексту виконання
- **State Transitions**: Переходи між станами
- **Recovery Logic**: Логіка відновлення після збоїв

### 5. Memory Store Module
- **Context & History**: Збереження контексту та історії
- **Learning Data**: Дані для навчання та покращення
- **Pattern Recognition**: Розпізнавання паттернів у завданнях
- **Knowledge Base**: База знань для прийняття рішень

## AI Components

### 1. Large Language Model (LLM)
- **Task Understanding**: Розуміння природної мови завдань
- **Plan Generation**: Генерація планів виконання
- **Tool Selection**: Вибір відповідних інструментів
- **Response Generation**: Генерація відповідей користувачам

### 2. Threat Classifier
- **Threat Detection**: Виявлення загроз у даних
- **Risk Assessment**: Оцінка рівня ризику
- **Classification**: Класифікація типів загроз
- **Confidence Scoring**: Оцінка впевненості в класифікації

### 3. Code Analyzer
- **Code Analysis**: Аналіз коду на предмет вразливостей
- **Pattern Detection**: Виявлення підозрілих паттернів
- **Quality Assessment**: Оцінка якості коду
- **Recommendation Generation**: Генерація рекомендацій

## Data Models

### Task Model
```python
class Task:
    id: UUID
    user_id: UUID
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    created_at: datetime
    updated_at: datetime
    started_at: datetime
    completed_at: datetime
    steps: List[TaskStep]
    context: dict
    result: dict
    error: str
```

### TaskStep Model
```python
class TaskStep:
    id: UUID
    task_id: UUID
    step_number: int
    description: str
    tool_name: str
    parameters: dict
    status: StepStatus
    result: dict
    error: str
    dependencies: List[UUID]
    started_at: datetime
    completed_at: datetime
```

### Agent Memory Model
```python
class AgentMemory:
    id: UUID
    task_id: UUID
    memory_type: MemoryType
    content: dict
    importance_score: float
    created_at: datetime
    accessed_at: datetime
    access_count: int
```

## API Endpoints

### Task Management
```
POST   /api/agent/tasks                    # Create task
GET    /api/agent/tasks                    # List tasks
GET    /api/agent/tasks/{task_id}          # Get task
PUT    /api/agent/tasks/{task_id}          # Update task
DELETE /api/agent/tasks/{task_id}          # Cancel task
GET    /api/agent/tasks/{task_id}/status   # Get task status
GET    /api/agent/tasks/{task_id}/result   # Get task result
```

### Task Execution
```
POST   /api/agent/tasks/{task_id}/execute  # Execute task
POST   /api/agent/tasks/{task_id}/pause    # Pause task
POST   /api/agent/tasks/{task_id}/resume   # Resume task
POST   /api/agent/tasks/{task_id}/retry    # Retry failed task
```

### Agent Management
```
GET    /api/agent/capabilities             # Get agent capabilities
GET    /api/agent/memory                   # Get agent memory
POST   /api/agent/memory/clear             # Clear agent memory
GET    /api/agent/performance              # Get performance metrics
```

## Task Execution Flow

### 1. Task Creation
```python
# User submits task
task = {
    "title": "Find project 'Orion' in Jira",
    "description": "Search for project with name 'Orion' in Jira system",
    "priority": "normal",
    "context": {"user_preferences": {...}}
}

# Agent creates task and plans execution
task_id = agent.create_task(task)
plan = agent.plan_task(task_id)
```

### 2. Plan Generation
```python
# Agent decomposes task into steps
steps = [
    {
        "step_number": 1,
        "description": "Search for project 'Orion' in Jira",
        "tool_name": "jira_project_finder",
        "parameters": {"project_name": "Orion"},
        "dependencies": []
    }
]
```

### 3. Execution
```python
# Agent publishes commands to Message Bus
for step in steps:
    command = {
        "task_id": task_id,
        "step_id": step.id,
        "tool_name": step.tool_name,
        "parameters": step.parameters
    }
    message_bus.publish_command(command)
```

### 4. Monitoring
```python
# Agent monitors events and updates task status
def handle_event(event):
    if event.type == "tool_completed":
        update_step_status(event.step_id, "completed", event.result)
        check_task_completion(event.task_id)
    elif event.type == "tool_failed":
        handle_step_failure(event.step_id, event.error)
```

## Message Bus Integration

### Command Publishing
```python
# Publish command to execute tool
command = {
    "task_id": "uuid-123",
    "step_id": "uuid-456",
    "tool_name": "jira_project_finder",
    "parameters": {"project_name": "Orion"},
    "timestamp": datetime.utcnow(),
    "retry_count": 0
}

message_bus.publish(
    exchange="commands.exchange",
    routing_key="integrations.jira_project_finder",
    message=command
)
```

### Event Consumption
```python
# Consume events from Message Bus
@message_bus.subscribe("events.exchange", "integrations.*")
def handle_integration_event(event):
    if event.routing_key.endswith("_completed"):
        handle_tool_completion(event)
    elif event.routing_key.endswith("_failed"):
        handle_tool_failure(event)
```

## AI Model Integration

### LLM Integration
```python
class LLMService:
    def __init__(self):
        self.openai_client = OpenAI()
        self.anthropic_client = Anthropic()
    
    async def generate_plan(self, task_description: str) -> List[dict]:
        prompt = f"""
        Analyze this task and create an execution plan:
        Task: {task_description}
        
        Available tools: {self.get_available_tools()}
        
        Return a JSON array of steps.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.choices[0].message.content)
```

### Threat Classification
```python
class ThreatClassifier:
    def __init__(self):
        self.model = load_model("threat_classifier.pkl")
    
    def classify_threat(self, data: dict) -> dict:
        features = self.extract_features(data)
        prediction = self.model.predict_proba(features)
        
        return {
            "threat_level": self.get_threat_level(prediction),
            "threat_type": self.get_threat_type(prediction),
            "confidence": float(max(prediction[0]))
        }
```

## Technology Stack

### Core Technologies
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Bus**: RabbitMQ
- **AI Models**: OpenAI, Anthropic, Local models

### Dependencies
- `fastapi`: Web framework
- `sqlalchemy`: ORM
- `celery`: Task queue
- `pika`: RabbitMQ client
- `openai`: OpenAI API client
- `anthropic`: Anthropic API client
- `scikit-learn`: ML models
- `numpy`: Numerical computing
- `pandas`: Data manipulation

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/ai_agent
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379
REDIS_TASK_TTL=3600

# Message Bus
RABBITMQ_URL=amqp://user:pass@localhost:5672
RABBITMQ_COMMANDS_EXCHANGE=commands.exchange
RABBITMQ_EVENTS_EXCHANGE=events.exchange

# AI Models
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
LOCAL_MODEL_PATH=/models/threat_classifier.pkl

# Task Execution
MAX_CONCURRENT_TASKS=10
TASK_TIMEOUT_SECONDS=300
MAX_RETRY_ATTEMPTS=3
```

## Monitoring & Logging

### Metrics
- Task completion rate
- Average task execution time
- Tool usage statistics
- AI model performance
- Error rates by tool

### Logging
- Task creation and completion
- Step execution details
- AI model interactions
- Error and exception handling
- Performance metrics

## Testing

### Unit Tests
- Task planning tests
- Step execution tests
- AI model integration tests
- Message bus integration tests

### Integration Tests
- End-to-end task execution
- Tool integration tests
- Database integration tests
- Cache integration tests

### Performance Tests
- Concurrent task execution
- AI model response time
- Database query performance
- Memory usage optimization
