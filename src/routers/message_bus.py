"""
AI Cyber Tool - Message Bus Router
API ендпоінти для роботи з Message Bus (RabbitMQ)
"""

from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
import uuid
from datetime import datetime
from ..core.config import get_settings
from ..services.message_bus import MessageBus, MessageBusConfig, create_command_message

router = APIRouter()
settings = get_settings()


# Dependency для отримання MessageBus
async def get_message_bus_dependency() -> MessageBus:
    """Отримання MessageBus через Dependency Injection"""
    # Це буде імплементовано в основному app.py
    # Тут ми просто створюємо новий екземпляр для тестування
    message_bus_config = MessageBusConfig(
        rabbitmq_url=settings.rabbitmq_url,
        commands_exchange=settings.rabbitmq_commands_exchange,
        events_exchange=settings.rabbitmq_events_exchange
    )
    return MessageBus(message_bus_config)


@router.get("/api/message-bus/status")
async def get_message_bus_status(message_bus: MessageBus = Depends(get_message_bus_dependency)):
    """Отримати статус Message Bus"""
    try:
        # Перевіряємо з'єднання з RabbitMQ
        publisher = message_bus.get_publisher()
        consumer = message_bus.get_consumer()
        
        return {
            "status": "connected",
            "message": "Message Bus is operational",
            "config": {
                "rabbitmq_url": settings.rabbitmq_url,
                "commands_exchange": settings.rabbitmq_commands_exchange,
                "events_exchange": settings.rabbitmq_events_exchange
            }
        }
    except Exception as e:
        logger.error(f"Message Bus error: {e}")
        return {
            "status": "error",
            "message": f"Message Bus connection failed: {str(e)}",
            "config": {
                "rabbitmq_url": settings.rabbitmq_url,
                "commands_exchange": settings.rabbitmq_commands_exchange,
                "events_exchange": settings.rabbitmq_events_exchange
            }
        }


@router.post("/api/message-bus/test")
async def test_message_bus(message_bus: MessageBus = Depends(get_message_bus_dependency)):
    """Тест Message Bus - відправити тестове повідомлення"""
    try:
        # Створюємо тестову команду
        command = create_command_message(
            message_id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4()),
            step_id=str(uuid.uuid4()),
            tool_name="test_tool",
            parameters={"test": "data", "timestamp": datetime.utcnow().isoformat()}
        )
        
        # Публікуємо команду
        publisher = message_bus.get_publisher()
        publisher.publish_command(command)
        
        return {
            "status": "success",
            "message": "Test command published successfully",
            "command_id": command.message_id,
            "tool_name": command.tool_name
        }
        
    except Exception as e:
        logger.error(f"Message Bus test error: {e}")
        raise HTTPException(status_code=500, detail=f"Message Bus test failed: {str(e)}")
