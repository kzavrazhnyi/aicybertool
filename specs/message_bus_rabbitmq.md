# Message Bus (RabbitMQ) Specification

## Overview
Message Bus є центральною нервовою системою для асинхронної комунікації між сервісами AICyberTool. Забезпечує надійність та стійкість до відмов. Якщо один сервіс тимчасово недоступний, завдання не втрачається, а чекає у черзі.

## Architecture Components

### 1. Exchanges Module
- **Commands Exchange**: Обмінник для команд (наказів щось зробити)
- **Events Exchange**: Обмінник для подій (сповіщення про те, що щось сталося)
- **Dead Letter Exchange**: Обмінник для необроблених повідомлень
- **Exchange Management**: Управління обмінниками

### 2. Queues Module
- **Service-specific Queues**: Черги для конкретних сервісів
- **Priority Queues**: Черги з пріоритетами
- **Delayed Queues**: Черги з затримкою
- **Queue Management**: Управління чергами

### 3. Routing Module
- **Message Distribution**: Розподіл повідомлень за routing keys
- **Pattern Matching**: Відповідність паттернів
- **Load Balancing**: Балансування навантаження
- **Routing Rules**: Правила маршрутизації

### 4. Message Persistence Module
- **Durability**: Збереження повідомлень на диск
- **Persistence Settings**: Налаштування збереження
- **Recovery**: Відновлення після збоїв
- **Backup**: Резервне копіювання

### 5. Monitoring Module
- **Queue Health**: Моніторинг стану черг
- **Message Flow**: Відстеження потоку повідомлень
- **Performance Metrics**: Метрики продуктивності
- **Alerting**: Система сповіщень

## Exchange Configuration

### Commands Exchange
```python
COMMANDS_EXCHANGE = {
    "name": "commands.exchange",
    "type": "topic",
    "durable": True,
    "auto_delete": False,
    "arguments": {
        "alternate-exchange": "dead-letter.exchange"
    }
}
```

### Events Exchange
```python
EVENTS_EXCHANGE = {
    "name": "events.exchange",
    "type": "topic",
    "durable": True,
    "auto_delete": False,
    "arguments": {
        "alternate-exchange": "dead-letter.exchange"
    }
}
```

### Dead Letter Exchange
```python
DEAD_LETTER_EXCHANGE = {
    "name": "dead-letter.exchange",
    "type": "direct",
    "durable": True,
    "auto_delete": False
}
```

## Queue Configuration

### Service Queues
```python
SERVICE_QUEUES = {
    "ai_agent_commands": {
        "name": "ai_agent.commands.queue",
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "arguments": {
            "x-message-ttl": 300000,  # 5 minutes
            "x-max-length": 1000,
            "x-dead-letter-exchange": "dead-letter.exchange"
        }
    },
    "integrations_commands": {
        "name": "integrations.commands.queue",
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "arguments": {
            "x-message-ttl": 300000,
            "x-max-length": 1000,
            "x-dead-letter-exchange": "dead-letter.exchange"
        }
    },
    "ai_agent_events": {
        "name": "ai_agent.events.queue",
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "arguments": {
            "x-message-ttl": 600000,  # 10 minutes
            "x-max-length": 5000
        }
    }
}
```

## Message Formats

### Command Message Format
```python
class CommandMessage:
    task_id: str
    step_id: str
    tool_name: str
    parameters: dict
    timestamp: datetime
    retry_count: int = 0
    priority: int = 0
    correlation_id: str
    reply_to: str = None
```

### Event Message Format
```python
class EventMessage:
    task_id: str
    step_id: str
    tool_name: str
    status: str  # completed, failed, started
    result: dict = None
    error: str = None
    timestamp: datetime
    correlation_id: str
```

## Routing Patterns

### Command Routing Keys
```python
COMMAND_ROUTING_PATTERNS = {
    "ai_agent.*": "ai_agent.commands.queue",
    "integrations.*": "integrations.commands.queue",
    "cybernetic_mgmt.*": "cybernetic_mgmt.commands.queue"
}
```

### Event Routing Keys
```python
EVENT_ROUTING_PATTERNS = {
    "*.completed": "ai_agent.events.queue",
    "*.failed": "ai_agent.events.queue",
    "*.started": "ai_agent.events.queue",
    "integrations.*": "integrations.events.queue"
}
```

## Message Bus Client

### Publisher Client
```python
class MessageBusPublisher:
    def __init__(self, connection_url: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_url)
        )
        self.channel = self.connection.channel()
        self.setup_exchanges()
    
    def setup_exchanges(self):
        """Setup required exchanges"""
        # Commands exchange
        self.channel.exchange_declare(
            exchange="commands.exchange",
            exchange_type="topic",
            durable=True
        )
        
        # Events exchange
        self.channel.exchange_declare(
            exchange="events.exchange",
            exchange_type="topic",
            durable=True
        )
    
    def publish_command(self, routing_key: str, message: dict):
        """Publish command message"""
        self.channel.basic_publish(
            exchange="commands.exchange",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                correlation_id=message.get("correlation_id"),
                reply_to=message.get("reply_to"),
                priority=message.get("priority", 0)
            )
        )
    
    def publish_event(self, routing_key: str, message: dict):
        """Publish event message"""
        self.channel.basic_publish(
            exchange="events.exchange",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                correlation_id=message.get("correlation_id")
            )
        )
```

### Consumer Client
```python
class MessageBusConsumer:
    def __init__(self, connection_url: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_url)
        )
        self.channel = self.connection.channel()
        self.setup_queues()
    
    def setup_queues(self):
        """Setup required queues"""
        # AI Agent commands queue
        self.channel.queue_declare(
            queue="ai_agent.commands.queue",
            durable=True,
            arguments={
                "x-message-ttl": 300000,
                "x-max-length": 1000,
                "x-dead-letter-exchange": "dead-letter.exchange"
            }
        )
        
        # Bind to commands exchange
        self.channel.queue_bind(
            exchange="commands.exchange",
            queue="ai_agent.commands.queue",
            routing_key="ai_agent.*"
        )
    
    def consume_commands(self, callback):
        """Consume command messages"""
        self.channel.basic_consume(
            queue="ai_agent.commands.queue",
            on_message_callback=callback,
            auto_ack=False
        )
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
    
    def consume_events(self, callback):
        """Consume event messages"""
        self.channel.basic_consume(
            queue="ai_agent.events.queue",
            on_message_callback=callback,
            auto_ack=False
        )
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
```

## Error Handling

### Dead Letter Queue
```python
class DeadLetterHandler:
    def __init__(self, channel):
        self.channel = channel
        self.setup_dead_letter_queue()
    
    def setup_dead_letter_queue(self):
        """Setup dead letter queue"""
        self.channel.queue_declare(
            queue="dead-letter.queue",
            durable=True
        )
        
        self.channel.queue_bind(
            exchange="dead-letter.exchange",
            queue="dead-letter.queue",
            routing_key=""
        )
    
    def handle_dead_letter(self, method, properties, body):
        """Handle dead letter messages"""
        try:
            message = json.loads(body)
            logger.error(f"Dead letter received: {message}")
            
            # Log to database
            await self.log_dead_letter(message, properties)
            
            # Send alert
            await self.send_alert(message)
            
        except Exception as e:
            logger.error(f"Error handling dead letter: {e}")
        finally:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
```

### Retry Logic
```python
class RetryHandler:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    def should_retry(self, message: dict) -> bool:
        """Check if message should be retried"""
        retry_count = message.get("retry_count", 0)
        return retry_count < self.max_retries
    
    def increment_retry_count(self, message: dict) -> dict:
        """Increment retry count"""
        message["retry_count"] = message.get("retry_count", 0) + 1
        return message
    
    def get_retry_delay(self, retry_count: int) -> int:
        """Calculate retry delay with exponential backoff"""
        return min(1000 * (2 ** retry_count), 30000)  # Max 30 seconds
```

## Monitoring & Metrics

### Queue Monitoring
```python
class QueueMonitor:
    def __init__(self, connection_url: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_url)
        )
        self.channel = self.connection.channel()
    
    def get_queue_stats(self, queue_name: str) -> dict:
        """Get queue statistics"""
        method = self.channel.queue_declare(
            queue=queue_name,
            passive=True
        )
        
        return {
            "queue_name": queue_name,
            "message_count": method.method.message_count,
            "consumer_count": method.method.consumer_count
        }
    
    def get_all_queue_stats(self) -> List[dict]:
        """Get statistics for all queues"""
        queues = [
            "ai_agent.commands.queue",
            "integrations.commands.queue",
            "ai_agent.events.queue",
            "dead-letter.queue"
        ]
        
        return [self.get_queue_stats(queue) for queue in queues]
```

### Performance Metrics
```python
class PerformanceMetrics:
    def __init__(self):
        self.metrics = {
            "messages_published": 0,
            "messages_consumed": 0,
            "messages_failed": 0,
            "average_processing_time": 0,
            "queue_lengths": {}
        }
    
    def record_message_published(self):
        """Record message published"""
        self.metrics["messages_published"] += 1
    
    def record_message_consumed(self, processing_time: float):
        """Record message consumed"""
        self.metrics["messages_consumed"] += 1
        
        # Update average processing time
        total = self.metrics["messages_consumed"]
        current_avg = self.metrics["average_processing_time"]
        self.metrics["average_processing_time"] = (
            (current_avg * (total - 1) + processing_time) / total
        )
    
    def record_message_failed(self):
        """Record message failed"""
        self.metrics["messages_failed"] += 1
```

## Configuration

### Environment Variables
```bash
# RabbitMQ Connection
RABBITMQ_URL=amqp://user:password@localhost:5672/
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=user
RABBITMQ_PASSWORD=password
RABBITMQ_VHOST=/

# Exchange Configuration
COMMANDS_EXCHANGE=commands.exchange
EVENTS_EXCHANGE=events.exchange
DEAD_LETTER_EXCHANGE=dead-letter.exchange

# Queue Configuration
AI_AGENT_COMMANDS_QUEUE=ai_agent.commands.queue
INTEGRATIONS_COMMANDS_QUEUE=integrations.commands.queue
AI_AGENT_EVENTS_QUEUE=ai_agent.events.queue
DEAD_LETTER_QUEUE=dead-letter.queue

# Message Configuration
MESSAGE_TTL=300000
MAX_QUEUE_LENGTH=1000
MAX_RETRY_ATTEMPTS=3
RETRY_BACKOFF_FACTOR=2
```

### Docker Configuration
```yaml
version: '3.8'
services:
  rabbitmq:
    image: rabbitmq:3.11-management
    container_name: aicybertool-rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: user
      RABBITMQ_DEFAULT_PASS: password
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - aicybertool-network

volumes:
  rabbitmq_data:

networks:
  aicybertool-network:
    driver: bridge
```

## Security

### Authentication
- Username/password authentication
- SSL/TLS encryption
- Virtual host isolation
- User permissions management

### Authorization
- Queue-level permissions
- Exchange-level permissions
- Resource-level access control
- Admin user separation

## Testing

### Unit Tests
- Message publishing tests
- Message consumption tests
- Error handling tests
- Retry logic tests

### Integration Tests
- End-to-end message flow tests
- Queue persistence tests
- Dead letter handling tests
- Performance tests

### Load Tests
- High-volume message publishing
- Concurrent consumer testing
- Queue performance under load
- Memory usage optimization
