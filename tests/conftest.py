"""Конфигурация и фикстуры для тестов."""
import sys
from pathlib import Path
from unittest.mock import Mock
import pytest
from src.core.config import Settings
from src.services.chat_service import ChatService

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

@pytest.fixture
def mock_settings() -> Settings:
    """Provide test settings."""
    return Settings(
        TELEGRAM_TOKEN="test_telegram_token",
        GIGACHAT_TOKEN="test_gigachat_token"
    )

@pytest.fixture
def mock_chat_service() -> ChatService:
    """Provide mock chat service."""
    service = Mock(spec=ChatService)
    async def mock_generate_response(message: str) -> str:
        return f"Mocked response for: {message}"
    
    service.generate_response.side_effect = mock_generate_response
    return service
