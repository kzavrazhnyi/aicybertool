# -*- coding: utf-8 -*-
"""
Message Bus Service - RabbitMQ Integration
Центральна нервова система для асинхронної комунікації між сервісами
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

import pika
from pika.exchange_type import ExchangeType
from loguru import logger


class MessageType(Enum):
    """Типи повідомлень"""
    COMMAND = "command"
    EVENT = "event"


class MessageStatus(Enum):
    """Статуси повідомлень"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Message:
    """Базовий клас повідомлення"""
    message_id: str
    message_type: MessageType
    routing_key: str
    body: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    priority: int = 0
    retry_count: int = 0


@dataclass
class CommandMessage:
    """Повідомлення-команда"""
    message_id: str
    message_type: MessageType = MessageType.COMMAND
    routing_key: str = ""
    body: Dict[str, Any] = None
    timestamp: datetime = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    priority: int = 0
    retry_count: int = 0
    task_id: str = ""
    step_id: str = ""
    tool_name: str = ""
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.body is None:
            self.body = {}
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.parameters is None:
            self.parameters = {}
        
        self.message_type = MessageType.COMMAND
        self.body = {
            "task_id": self.task_id,
            "step_id": self.step_id,
            "tool_name": self.tool_name,
            "parameters": self.parameters,
            "retry_count": self.retry_count
        }
        self.routing_key = f"{self.tool_name}.{self.message_id}"


@dataclass
class EventMessage:
    """Повідомлення-подія"""
    message_id: str
    message_type: MessageType = MessageType.EVENT
    routing_key: str = ""
    body: Dict[str, Any] = None
    timestamp: datetime = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    priority: int = 0
    retry_count: int = 0
    task_id: str = ""
    step_id: str = ""
    tool_name: str = ""
    status: MessageStatus = MessageStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.body is None:
            self.body = {}
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        
        self.message_type = MessageType.EVENT
        self.body = {
            "task_id": self.task_id,
            "step_id": self.step_id,
            "tool_name": self.tool_name,
            "status": self.status.value,
            "result": self.result,
            "error": self.error
        }
        self.routing_key = f"{self.tool_name}.{self.status.value}"


class MessageBusConfig:
    """Конфігурація Message Bus"""
    
    def __init__(self):
        self.rabbitmq_url = "amqp://localhost:5672/"
        self.commands_exchange = "commands.exchange"
        self.events_exchange = "events.exchange"
        self.dead_letter_exchange = "dead-letter.exchange"
        
        # Queue configurations
        self.ai_agent_commands_queue = "ai_agent.commands.queue"
        self.integrations_commands_queue = "integrations.commands.queue"
        self.ai_agent_events_queue = "ai_agent.events.queue"
        self.dead_letter_queue = "dead-letter.queue"
        
        # Message settings
        self.message_ttl = 300000  # 5 minutes
        self.max_queue_length = 1000
        self.max_retry_attempts = 3


class MessageBusPublisher:
    """Publisher для відправки повідомлень"""
    
    def __init__(self, config: MessageBusConfig):
        self.config = config
        self.connection = None
        self.channel = None
        self._setup_connection()
    
    def _setup_connection(self):
        """Налаштування з'єднання з RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.config.rabbitmq_url)
            )
            self.channel = self.connection.channel()
            self._setup_exchanges()
            logger.info("MessageBus Publisher connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def _setup_exchanges(self):
        """Налаштування exchanges"""
        # Commands exchange
        self.channel.exchange_declare(
            exchange=self.config.commands_exchange,
            exchange_type=ExchangeType.topic,
            durable=True
        )
        
        # Events exchange
        self.channel.exchange_declare(
            exchange=self.config.events_exchange,
            exchange_type=ExchangeType.topic,
            durable=True
        )
        
        # Dead letter exchange
        self.channel.exchange_declare(
            exchange=self.config.dead_letter_exchange,
            exchange_type=ExchangeType.direct,
            durable=True
        )
    
    def publish_command(self, command: CommandMessage):
        """Публікація команди"""
        try:
            routing_key = f"{command.tool_name}.{command.message_id}"
            
            self.channel.basic_publish(
                exchange=self.config.commands_exchange,
                routing_key=routing_key,
                body=json.dumps(asdict(command), default=str),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    correlation_id=command.correlation_id,
                    reply_to=command.reply_to,
                    priority=command.priority,
                    timestamp=int(command.timestamp.timestamp())
                )
            )
            
            logger.info(f"Command published: {command.tool_name} - {command.message_id}")
            
        except Exception as e:
            logger.error(f"Failed to publish command: {e}")
            raise
    
    def publish_event(self, event: EventMessage):
        """Публікація події"""
        try:
            routing_key = f"{event.tool_name}.{event.status.value}"
            
            self.channel.basic_publish(
                exchange=self.config.events_exchange,
                routing_key=routing_key,
                body=json.dumps(asdict(event), default=str),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    correlation_id=event.correlation_id,
                    timestamp=int(event.timestamp.timestamp())
                )
            )
            
            logger.info(f"Event published: {event.tool_name} - {event.status.value}")
            
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            raise
    
    def close(self):
        """Закриття з'єднання"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("MessageBus Publisher connection closed")


class MessageBusConsumer:
    """Consumer для отримання повідомлень"""
    
    def __init__(self, config: MessageBusConfig):
        self.config = config
        self.connection = None
        self.channel = None
        self.callbacks = {}
        self._setup_connection()
    
    def _setup_connection(self):
        """Налаштування з'єднання з RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.config.rabbitmq_url)
            )
            self.channel = self.connection.channel()
            self._setup_queues()
            logger.info("MessageBus Consumer connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def _setup_queues(self):
        """Налаштування черг"""
        # AI Agent commands queue
        self.channel.queue_declare(
            queue=self.config.ai_agent_commands_queue,
            durable=True,
            arguments={
                "x-message-ttl": self.config.message_ttl,
                "x-max-length": self.config.max_queue_length,
                "x-dead-letter-exchange": self.config.dead_letter_exchange
            }
        )
        
        # Integrations commands queue
        self.channel.queue_declare(
            queue=self.config.integrations_commands_queue,
            durable=True,
            arguments={
                "x-message-ttl": self.config.message_ttl,
                "x-max-length": self.config.max_queue_length,
                "x-dead-letter-exchange": self.config.dead_letter_exchange
            }
        )
        
        # AI Agent events queue
        self.channel.queue_declare(
            queue=self.config.ai_agent_events_queue,
            durable=True,
            arguments={
                "x-message-ttl": self.config.message_ttl * 2,  # 10 minutes
                "x-max-length": self.config.max_queue_length * 5
            }
        )
        
        # Dead letter queue
        self.channel.queue_declare(
            queue=self.config.dead_letter_queue,
            durable=True
        )
        
        # Bind queues to exchanges
        self._bind_queues()
    
    def _bind_queues(self):
        """Прив'язка черг до exchanges"""
        # Bind AI Agent commands queue
        self.channel.queue_bind(
            exchange=self.config.commands_exchange,
            queue=self.config.ai_agent_commands_queue,
            routing_key="ai_agent.*"
        )
        
        # Bind Integrations commands queue
        self.channel.queue_bind(
            exchange=self.config.commands_exchange,
            queue=self.config.integrations_commands_queue,
            routing_key="integrations.*"
        )
        
        # Bind AI Agent events queue
        self.channel.queue_bind(
            exchange=self.config.events_exchange,
            queue=self.config.ai_agent_events_queue,
            routing_key="*.completed"
        )
        self.channel.queue_bind(
            exchange=self.config.events_exchange,
            queue=self.config.ai_agent_events_queue,
            routing_key="*.failed"
        )
        
        # Bind dead letter queue
        self.channel.queue_bind(
            exchange=self.config.dead_letter_exchange,
            queue=self.config.dead_letter_queue,
            routing_key=""
        )
    
    def register_callback(self, queue_name: str, callback: Callable):
        """Реєстрація callback функції для черги"""
        self.callbacks[queue_name] = callback
        logger.info(f"Callback registered for queue: {queue_name}")
    
    def start_consuming(self, queue_name: str):
        """Початок споживання повідомлень з черги"""
        if queue_name not in self.callbacks:
            raise ValueError(f"No callback registered for queue: {queue_name}")
        
        callback = self.callbacks[queue_name]
        
        def message_handler(ch, method, properties, body):
            try:
                message_data = json.loads(body)
                callback(message_data)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=message_handler,
            auto_ack=False
        )
        
        logger.info(f"Started consuming from queue: {queue_name}")
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
    
    def close(self):
        """Закриття з'єднання"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("MessageBus Consumer connection closed")


class MessageBus:
    """Головний клас Message Bus"""
    
    def __init__(self, config: Optional[MessageBusConfig] = None):
        self.config = config or MessageBusConfig()
        self.publisher = None
        self.consumer = None
    
    def get_publisher(self) -> MessageBusPublisher:
        """Отримання publisher"""
        if not self.publisher:
            self.publisher = MessageBusPublisher(self.config)
        return self.publisher
    
    def get_consumer(self) -> MessageBusConsumer:
        """Отримання consumer"""
        if not self.consumer:
            self.consumer = MessageBusConsumer(self.config)
        return self.consumer
    
    def close(self):
        """Закриття всіх з'єднань"""
        if self.publisher:
            self.publisher.close()
        if self.consumer:
            self.consumer.close()
        logger.info("MessageBus closed")
    
    async def ping(self) -> bool:
        """Перевірка з'єднання з RabbitMQ"""
        try:
            publisher = self.get_publisher()
            # Спроба перевірити, чи активне з'єднання
            if publisher.connection and not publisher.connection.is_closed:
                # Перевіряємо канал
                if publisher.channel and not publisher.channel.is_closed:
                    return True
            return False
        except Exception as e:
            logger.warning(f"MessageBus ping failed: {e}")
            return False


# Utility functions
def create_command_message(
    message_id: str,
    task_id: str,
    step_id: str,
    tool_name: str,
    parameters: Dict[str, Any],
    correlation_id: Optional[str] = None
) -> CommandMessage:
    """Створення команди"""
    return CommandMessage(
        message_id=message_id,
        message_type=MessageType.COMMAND,
        routing_key=f"{tool_name}.{message_id}",
        body={},
        timestamp=datetime.utcnow(),
        correlation_id=correlation_id,
        task_id=task_id,
        step_id=step_id,
        tool_name=tool_name,
        parameters=parameters
    )


def create_event_message(
    message_id: str,
    task_id: str,
    step_id: str,
    tool_name: str,
    status: MessageStatus,
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    correlation_id: Optional[str] = None
) -> EventMessage:
    """Створення події"""
    return EventMessage(
        message_id=message_id,
        message_type=MessageType.EVENT,
        routing_key=f"{tool_name}.{status.value}",
        body={},
        timestamp=datetime.utcnow(),
        correlation_id=correlation_id,
        task_id=task_id,
        step_id=step_id,
        tool_name=tool_name,
        status=status,
        result=result,
        error=error
    )
