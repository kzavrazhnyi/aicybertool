# Integrations Service Specification

## Overview
Integrations Service є "руками" AI Agent для взаємодії із зовнішнім світом. Дозволяє агенту отримувати дані із зовнішніх API або надсилати їх туди. Без цього сервісу агент буде обмежений лише внутрішніми даними.

## Architecture Components

### 1. Jira Integration Module
- **Project Management**: Робота з проектами Jira
- **Issue Tracking**: Відстеження задач та багів
- **User Management**: Управління користувачами Jira
- **Workflow Management**: Управління робочими процесами

### 2. GitHub Integration Module
- **Repository Management**: Робота з репозиторіями
- **Code Analysis**: Аналіз коду та комітів
- **Pull Request Management**: Управління pull requests
- **Issue Tracking**: Відстеження GitHub issues

### 3. Slack Integration Module
- **Message Sending**: Надсилання повідомлень
- **Channel Management**: Управління каналами
- **User Notifications**: Сповіщення користувачів
- **Bot Interactions**: Взаємодія з ботом

### 4. Webhook Handler Module
- **Generic HTTP**: Обробка загальних HTTP запитів
- **Custom Integrations**: Підтримка користувацьких інтеграцій
- **Data Transformation**: Трансформація даних
- **Error Handling**: Обробка помилок

### 5. Integration Config Module
- **API Credentials**: Управління API ключами
- **Connection Management**: Управління з'єднаннями
- **Rate Limiting**: Обмеження швидкості запитів
- **Retry Logic**: Логіка повторних спроб

## Supported Integrations

### Jira Integration
```python
class JiraIntegration:
    def __init__(self, base_url: str, username: str, api_token: str):
        self.client = JiraClient(base_url, username, api_token)
    
    async def find_project(self, project_name: str) -> dict:
        """Find project by name"""
        projects = await self.client.get_projects()
        for project in projects:
            if project.name.lower() == project_name.lower():
                return project
        return None
    
    async def get_issues(self, project_key: str, **filters) -> List[dict]:
        """Get issues for project"""
        jql = f"project = {project_key}"
        if filters:
            jql += " AND " + " AND ".join([f"{k} = {v}" for k, v in filters.items()])
        
        return await self.client.search_issues(jql)
    
    async def create_issue(self, project_key: str, summary: str, **fields) -> dict:
        """Create new issue"""
        issue_data = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": fields.get("type", "Task")}
        }
        issue_data.update(fields)
        
        return await self.client.create_issue(issue_data)
```

### GitHub Integration
```python
class GitHubIntegration:
    def __init__(self, token: str):
        self.client = GitHubClient(token)
    
    async def search_repositories(self, query: str) -> List[dict]:
        """Search repositories"""
        return await self.client.search_repositories(query)
    
    async def get_repository(self, owner: str, repo: str) -> dict:
        """Get repository details"""
        return await self.client.get_repository(owner, repo)
    
    async def get_commits(self, owner: str, repo: str, **filters) -> List[dict]:
        """Get commits for repository"""
        return await self.client.get_commits(owner, repo, **filters)
    
    async def create_issue(self, owner: str, repo: str, title: str, **fields) -> dict:
        """Create GitHub issue"""
        issue_data = {
            "title": title,
            "body": fields.get("body", ""),
            "labels": fields.get("labels", [])
        }
        
        return await self.client.create_issue(owner, repo, issue_data)
```

### Slack Integration
```python
class SlackIntegration:
    def __init__(self, bot_token: str):
        self.client = SlackClient(bot_token)
    
    async def send_message(self, channel: str, text: str, **blocks) -> dict:
        """Send message to Slack channel"""
        message_data = {
            "channel": channel,
            "text": text
        }
        if blocks:
            message_data["blocks"] = blocks
        
        return await self.client.chat_postMessage(message_data)
    
    async def get_user_info(self, user_id: str) -> dict:
        """Get user information"""
        return await self.client.users_info(user=user_id)
    
    async def list_channels(self) -> List[dict]:
        """List available channels"""
        return await self.client.conversations_list()
```

## API Endpoints

### Integration Management
```
GET    /api/integrations                    # List available integrations
POST   /api/integrations/{name}/configure   # Configure integration
GET    /api/integrations/{name}/status      # Get integration status
POST   /api/integrations/{name}/test        # Test integration connection
```

### Jira Endpoints
```
GET    /api/integrations/jira/projects      # List projects
GET    /api/integrations/jira/projects/{key} # Get project
GET    /api/integrations/jira/issues       # Search issues
POST   /api/integrations/jira/issues       # Create issue
GET    /api/integrations/jira/users        # List users
```

### GitHub Endpoints
```
GET    /api/integrations/github/repos       # Search repositories
GET    /api/integrations/github/repos/{owner}/{repo} # Get repository
GET    /api/integrations/github/commits      # Get commits
POST   /api/integrations/github/issues      # Create issue
GET    /api/integrations/github/pullrequests # Get pull requests
```

### Slack Endpoints
```
POST   /api/integrations/slack/message      # Send message
GET    /api/integrations/slack/channels     # List channels
GET    /api/integrations/slack/users        # List users
POST   /api/integrations/slack/webhook      # Handle webhook
```

### Generic Webhook Endpoints
```
POST   /api/integrations/webhook/{name}     # Generic webhook handler
GET    /api/integrations/webhook/{name}/logs # Get webhook logs
POST   /api/integrations/webhook/{name}/test # Test webhook
```

## Message Bus Integration

### Command Consumption
```python
@message_bus.subscribe("commands.exchange", "integrations.*")
async def handle_integration_command(command: dict):
    """Handle integration commands from AI Agent"""
    tool_name = command.get("tool_name")
    parameters = command.get("parameters", {})
    task_id = command.get("task_id")
    step_id = command.get("step_id")
    
    try:
        # Execute the integration tool
        result = await execute_tool(tool_name, parameters)
        
        # Publish success event
        await publish_event({
            "task_id": task_id,
            "step_id": step_id,
            "tool_name": tool_name,
            "status": "completed",
            "result": result,
            "timestamp": datetime.utcnow()
        })
        
    except Exception as e:
        # Publish failure event
        await publish_event({
            "task_id": task_id,
            "step_id": step_id,
            "tool_name": tool_name,
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow()
        })
```

### Event Publishing
```python
async def publish_event(event_data: dict):
    """Publish event to Message Bus"""
    routing_key = f"integrations.{event_data['tool_name']}_{event_data['status']}"
    
    await message_bus.publish(
        exchange="events.exchange",
        routing_key=routing_key,
        message=event_data
    )
```

## Tool Registry Integration

### Tool Registration
```python
class IntegrationToolRegistry:
    def __init__(self):
        self.tools = {}
        self.register_default_tools()
    
    def register_default_tools(self):
        """Register default integration tools"""
        # Jira tools
        self.register_tool({
            "name": "jira_project_finder",
            "description": "Find projects in Jira by name",
            "service": "integrations",
            "endpoint": "/api/integrations/jira/projects",
            "parameters_schema": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"}
                },
                "required": ["project_name"]
            }
        })
        
        # GitHub tools
        self.register_tool({
            "name": "github_repo_search",
            "description": "Search GitHub repositories",
            "service": "integrations",
            "endpoint": "/api/integrations/github/repos",
            "parameters_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        })
```

## Configuration Management

### Integration Configuration
```python
class IntegrationConfig:
    def __init__(self):
        self.configs = {}
    
    async def load_config(self, integration_name: str) -> dict:
        """Load configuration for integration"""
        if integration_name not in self.configs:
            config = await self.get_from_database(integration_name)
            self.configs[integration_name] = config
        
        return self.configs[integration_name]
    
    async def save_config(self, integration_name: str, config: dict):
        """Save configuration for integration"""
        await self.save_to_database(integration_name, config)
        self.configs[integration_name] = config
```

### Environment Variables
```bash
# Jira Configuration
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@domain.com
JIRA_API_TOKEN=your-api-token

# GitHub Configuration
GITHUB_TOKEN=your-github-token
GITHUB_API_URL=https://api.github.com

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# Generic Configuration
INTEGRATION_TIMEOUT=30
MAX_RETRY_ATTEMPTS=3
RATE_LIMIT_PER_MINUTE=100
```

## Error Handling

### Retry Logic
```python
class RetryHandler:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic"""
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise e
                
                wait_time = self.backoff_factor * (2 ** attempt)
                await asyncio.sleep(wait_time)
```

### Error Classification
```python
class IntegrationError(Exception):
    def __init__(self, message: str, error_type: str, retryable: bool = False):
        self.message = message
        self.error_type = error_type
        self.retryable = retryable
        super().__init__(message)

class AuthenticationError(IntegrationError):
    def __init__(self, message: str):
        super().__init__(message, "authentication", False)

class RateLimitError(IntegrationError):
    def __init__(self, message: str):
        super().__init__(message, "rate_limit", True)

class NetworkError(IntegrationError):
    def __init__(self, message: str):
        super().__init__(message, "network", True)
```

## Technology Stack

### Core Technologies
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Bus**: RabbitMQ
- **HTTP Client**: httpx

### Dependencies
- `fastapi`: Web framework
- `httpx`: HTTP client
- `pika`: RabbitMQ client
- `sqlalchemy`: ORM
- `redis`: Caching
- `pydantic`: Data validation
- `jira`: Jira API client
- `PyGithub`: GitHub API client
- `slack-sdk`: Slack API client

## Monitoring & Logging

### Metrics
- Integration success/failure rates
- API response times
- Rate limit usage
- Error rates by integration
- Tool usage statistics

### Logging
- Integration requests and responses
- Error and exception handling
- Rate limiting events
- Authentication failures
- Performance metrics

## Testing

### Unit Tests
- Integration module tests
- Tool execution tests
- Configuration management tests
- Error handling tests

### Integration Tests
- External API integration tests
- Message bus integration tests
- Database integration tests
- End-to-end tool execution tests

### Performance Tests
- Concurrent tool execution
- API rate limiting tests
- Memory usage optimization
- Response time benchmarking
