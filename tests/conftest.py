"""Конфигурация и фикстуры для тестов."""
import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import pytest
from unittest.mock import Mock
from src.core.config import Settings
from src.services.chat_service import ChatService

@pytest.fixture
def mock_settings() -> Settings:
    """Создание тестовых настроек."""
    return Settings(
        TELEGRAM_TOKEN="тестовый_токен_telegram",
        GIGACHAT_TOKEN="тестовый_токен_gigachat"
    )

@pytest.fixture
def mock_chat_service() -> ChatService:
    """Создание мок-объекта сервиса чата."""
    service = Mock(spec=ChatService)
    async def mock_generate_response(message: str) -> str:
        return f"Тестовый ответ на: {message}"
    
    service.generate_response.side_effect = mock_generate_response
    return service