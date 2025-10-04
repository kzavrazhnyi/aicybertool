# -*- coding: utf-8 -*-
"""
Example usage of Message Bus Service
Приклад використання Message Bus для асинхронної комунікації
"""

import asyncio
import uuid
from datetime import datetime
from services.message_bus import (
    MessageBus, MessageBusConfig, MessageStatus,
    create_command_message, create_event_message
)


def ai_agent_command_handler(message):
    """Обробник команд для AI Agent"""
    print(f"AI Agent received command: {message}")
    
    # Симуляція обробки команди
    task_id = message.get('task_id')
    tool_name = message.get('tool_name')
    parameters = message.get('parameters', {})
    
    print(f"Processing task {task_id} with tool {tool_name}")
    print(f"Parameters: {parameters}")
    
    # Тут буде реальна логіка обробки
    # Наприклад, виклик інструменту через Integrations Service


def integrations_command_handler(message):
    """Обробник команд для Integrations Service"""
    print(f"Integrations Service received command: {message}")
    
    # Симуляція обробки команди
    task_id = message.get('task_id')
    tool_name = message.get('tool_name')
    parameters = message.get('parameters', {})
    
    print(f"Executing {tool_name} with parameters: {parameters}")
    
    # Симуляція успішного виконання
    result = {
        "status": "success",
        "data": f"Result from {tool_name}",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Публікація події про завершення
    event = create_event_message(
        message_id=str(uuid.uuid4()),
        task_id=task_id,
        step_id=message.get('step_id'),
        tool_name=tool_name,
        status=MessageStatus.COMPLETED,
        result=result
    )
    
    return event


def ai_agent_event_handler(message):
    """Обробник подій для AI Agent"""
    print(f"AI Agent received event: {message}")
    
    task_id = message.get('task_id')
    status = message.get('status')
    result = message.get('result')
    
    print(f"Task {task_id} status: {status}")
    if result:
        print(f"Result: {result}")


def main():
    """Головна функція для демонстрації роботи Message Bus"""
    print("=== Message Bus Demo ===")
    
    # Створення конфігурації
    config = MessageBusConfig()
    
    # Створення Message Bus
    message_bus = MessageBus(config)
    
    try:
        # Отримання Publisher та Consumer
        publisher = message_bus.get_publisher()
        consumer = message_bus.get_consumer()
        
        # Реєстрація обробників
        consumer.register_callback(
            config.ai_agent_commands_queue,
            ai_agent_command_handler
        )
        
        consumer.register_callback(
            config.integrations_commands_queue,
            integrations_command_handler
        )
        
        consumer.register_callback(
            config.ai_agent_events_queue,
            ai_agent_event_handler
        )
        
        print("Message Bus initialized successfully!")
        print("Registered handlers for:")
        print(f"  - {config.ai_agent_commands_queue}")
        print(f"  - {config.integrations_commands_queue}")
        print(f"  - {config.ai_agent_events_queue}")
        
        # Демонстрація публікації команди
        print("\n=== Publishing Command ===")
        
        command = create_command_message(
            message_id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4()),
            step_id=str(uuid.uuid4()),
            tool_name="jira_project_finder",
            parameters={
                "project_name": "Orion",
                "fields": ["id", "name", "key"]
            }
        )
        
        publisher.publish_command(command)
        print(f"Command published: {command.tool_name}")
        
        # Демонстрація публікації події
        print("\n=== Publishing Event ===")
        
        event = create_event_message(
            message_id=str(uuid.uuid4()),
            task_id=command.task_id,
            step_id=command.step_id,
            tool_name="jira_project_finder",
            status=MessageStatus.COMPLETED,
            result={
                "project": {
                    "id": "12345",
                    "name": "Orion",
                    "key": "ORION"
                }
            }
        )
        
        publisher.publish_event(event)
        print(f"Event published: {event.tool_name}.{event.status.value}")
        
        print("\n=== Demo completed ===")
        print("Note: In a real application, consumers would be running")
        print("in separate processes/threads to handle messages.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure RabbitMQ is running on localhost:5672")
    
    finally:
        # Закриття з'єднань
        message_bus.close()
        print("Message Bus connections closed")


if __name__ == "__main__":
    main()
