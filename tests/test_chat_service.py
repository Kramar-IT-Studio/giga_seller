"""Тесты для сервиса чата."""
import pytest
from unittest.mock import Mock, patch
from src.services.chat_service import GigaChatService
from langchain.schema import AIMessage

@pytest.mark.asyncio
async def test_gigachat_service_successful_response():
    """Тест успешной генерации ответа."""
    mock_response = AIMessage(content="Тестовый ответ")
    
    with patch('src.services.chat_service.GigaChat') as MockGigaChat:
        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_response
        MockGigaChat.return_value = mock_instance

        service = GigaChatService()
        response = await service.generate_response("Тестовое сообщение")
        
        assert response == "Тестовый ответ"
        mock_instance.invoke.assert_called_once()

@pytest.mark.asyncio
async def test_gigachat_service_invalid_response():
    """Тест обработки некорректного ответа."""
    with patch('src.services.chat_service.GigaChat') as MockGigaChat:
        mock_instance = Mock()
        mock_instance.invoke.return_value = "Некорректный тип ответа"
        MockGigaChat.return_value = mock_instance

        service = GigaChatService()
        with pytest.raises(ValueError, match="Получен некорректный ответ от GigaChat"):
            await service.generate_response("Тестовое сообщение")