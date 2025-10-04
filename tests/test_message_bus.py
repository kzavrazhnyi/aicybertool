# -*- coding: utf-8 -*-
"""
Tests for Message Bus Service
"""

import pytest
import json
import uuid
from datetime import datetime
from unittest.mock import Mock, patch

from services.message_bus import (
    MessageBus, MessageBusConfig, MessageBusPublisher, MessageBusConsumer,
    CommandMessage, EventMessage, MessageType, MessageStatus,
    create_command_message, create_event_message
)


class TestMessageBusConfig:
    """Тести для конфігурації Message Bus"""
    
    def test_default_config(self):
        """Тест створення конфігурації за замовчуванням"""
        config = MessageBusConfig()
        
        assert config.rabbitmq_url == "amqp://localhost:5672/"
        assert config.commands_exchange == "commands.exchange"
        assert config.events_exchange == "events.exchange"
        assert config.dead_letter_exchange == "dead-letter.exchange"
        assert config.message_ttl == 300000
        assert config.max_queue_length == 1000
        assert config.max_retry_attempts == 3


class TestMessageCreation:
    """Тести для створення повідомлень"""
    
    def test_create_command_message(self):
        """Тест створення команди"""
        message_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        step_id = str(uuid.uuid4())
        
        command = create_command_message(
            message_id=message_id,
            task_id=task_id,
            step_id=step_id,
            tool_name="jira_project_finder",
            parameters={"project_name": "Orion"},
            correlation_id="test-correlation"
        )
        
        assert command.message_id == message_id
        assert command.message_type == MessageType.COMMAND
        assert command.task_id == task_id
        assert command.step_id == step_id
        assert command.tool_name == "jira_project_finder"
        assert command.parameters == {"project_name": "Orion"}
        assert command.correlation_id == "test-correlation"
        assert command.routing_key == f"jira_project_finder.{message_id}"
    
    def test_create_event_message(self):
        """Тест створення події"""
        message_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        step_id = str(uuid.uuid4())
        
        event = create_event_message(
            message_id=message_id,
            task_id=task_id,
            step_id=step_id,
            tool_name="jira_project_finder",
            status=MessageStatus.COMPLETED,
            result={"project": {"id": "123", "name": "Orion"}},
            correlation_id="test-correlation"
        )
        
        assert event.message_id == message_id
        assert event.message_type == MessageType.EVENT
        assert event.task_id == task_id
        assert event.step_id == step_id
        assert event.tool_name == "jira_project_finder"
        assert event.status == MessageStatus.COMPLETED
        assert event.result == {"project": {"id": "123", "name": "Orion"}}
        assert event.correlation_id == "test-correlation"
        assert event.routing_key == f"jira_project_finder.completed"


class TestMessageBusPublisher:
    """Тести для Publisher"""
    
    @patch('services.message_bus.pika.BlockingConnection')
    def test_publisher_initialization(self, mock_connection):
        """Тест ініціалізації Publisher"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        config = MessageBusConfig()
        publisher = MessageBusPublisher(config)
        
        assert publisher.config == config
        assert publisher.channel == mock_channel
        mock_channel.exchange_declare.assert_called()
    
    @patch('services.message_bus.pika.BlockingConnection')
    def test_publish_command(self, mock_connection):
        """Тест публікації команди"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        config = MessageBusConfig()
        publisher = MessageBusPublisher(config)
        
        command = create_command_message(
            message_id="test-123",
            task_id="task-123",
            step_id="step-123",
            tool_name="test_tool",
            parameters={"param": "value"}
        )
        
        publisher.publish_command(command)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        
        assert call_args[1]['exchange'] == config.commands_exchange
        assert call_args[1]['routing_key'] == f"{command.tool_name}.{command.message_id}"
        
        # Перевіряємо, що body містить правильні дані
        body_data = json.loads(call_args[1]['body'])
        assert body_data['task_id'] == command.task_id
        assert body_data['tool_name'] == command.tool_name
        assert body_data['parameters'] == command.parameters
    
    @patch('services.message_bus.pika.BlockingConnection')
    def test_publish_event(self, mock_connection):
        """Тест публікації події"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        config = MessageBusConfig()
        publisher = MessageBusPublisher(config)
        
        event = create_event_message(
            message_id="test-123",
            task_id="task-123",
            step_id="step-123",
            tool_name="test_tool",
            status=MessageStatus.COMPLETED,
            result={"data": "test"}
        )
        
        publisher.publish_event(event)
        
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        
        assert call_args[1]['exchange'] == config.events_exchange
        assert call_args[1]['routing_key'] == f"{event.tool_name}.{event.status.value}"
        
        # Перевіряємо, що body містить правильні дані
        body_data = json.loads(call_args[1]['body'])
        assert body_data['task_id'] == event.task_id
        assert body_data['status'] == event.status.value
        assert body_data['result'] == event.result


class TestMessageBusConsumer:
    """Тести для Consumer"""
    
    @patch('services.message_bus.pika.BlockingConnection')
    def test_consumer_initialization(self, mock_connection):
        """Тест ініціалізації Consumer"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        config = MessageBusConfig()
        consumer = MessageBusConsumer(config)
        
        assert consumer.config == config
        assert consumer.channel == mock_channel
        mock_channel.queue_declare.assert_called()
    
    @patch('services.message_bus.pika.BlockingConnection')
    def test_register_callback(self, mock_connection):
        """Тест реєстрації callback"""
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        config = MessageBusConfig()
        consumer = MessageBusConsumer(config)
        
        def test_callback(message):
            pass
        
        consumer.register_callback("test_queue", test_callback)
        
        assert "test_queue" in consumer.callbacks
        assert consumer.callbacks["test_queue"] == test_callback


class TestMessageBus:
    """Тести для головного класу Message Bus"""
    
    def test_message_bus_initialization(self):
        """Тест ініціалізації Message Bus"""
        config = MessageBusConfig()
        message_bus = MessageBus(config)
        
        assert message_bus.config == config
        assert message_bus.publisher is None
        assert message_bus.consumer is None
    
    @patch('services.message_bus.MessageBusPublisher')
    def test_get_publisher(self, mock_publisher_class):
        """Тест отримання Publisher"""
        mock_publisher = Mock()
        mock_publisher_class.return_value = mock_publisher
        
        message_bus = MessageBus()
        publisher = message_bus.get_publisher()
        
        assert publisher == mock_publisher
        mock_publisher_class.assert_called_once_with(message_bus.config)
    
    @patch('services.message_bus.MessageBusConsumer')
    def test_get_consumer(self, mock_consumer_class):
        """Тест отримання Consumer"""
        mock_consumer = Mock()
        mock_consumer_class.return_value = mock_consumer
        
        message_bus = MessageBus()
        consumer = message_bus.get_consumer()
        
        assert consumer == mock_consumer
        mock_consumer_class.assert_called_once_with(message_bus.config)


class TestIntegration:
    """Інтеграційні тести"""
    
    @pytest.mark.skip(reason="Requires running RabbitMQ instance")
    def test_real_rabbitmq_connection(self):
        """Тест реального з'єднання з RabbitMQ"""
        config = MessageBusConfig()
        message_bus = MessageBus(config)
        
        try:
            publisher = message_bus.get_publisher()
            consumer = message_bus.get_consumer()
            
            # Тест публікації та споживання повідомлення
            command = create_command_message(
                message_id="integration-test",
                task_id="task-123",
                step_id="step-123",
                tool_name="test_tool",
                parameters={"test": "data"}
            )
            
            publisher.publish_command(command)
            
            received_messages = []
            
            def test_callback(message):
                received_messages.append(message)
            
            consumer.register_callback(config.ai_agent_commands_queue, test_callback)
            
            # В реальному тесті тут буде логіка споживання
            # consumer.start_consuming(config.ai_agent_commands_queue)
            
            assert len(received_messages) == 0  # Поки що порожній список
            
        finally:
            message_bus.close()


if __name__ == "__main__":
    pytest.main([__file__])
