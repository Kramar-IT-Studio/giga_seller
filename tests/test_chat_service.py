"""Тесты для сервиса чата."""
import os
import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, patch

from src.services.chat_service import ChatService  # Исправленный импорт

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

@pytest.mark.asyncio
async def test_generate_response():
    """Тест генерации ответа."""
    # Создаем мок для GigaChat
    mock_response = AsyncMock()
    mock_response.content = "Тестовый ответ"
    
    with patch('src.services.chat_service.GigaChat') as mock_giga:
        # Настраиваем мок
        mock_instance = mock_giga.return_value
        mock_instance.ainvoke = AsyncMock(return_value=mock_response)
        
        # Создаем экземпляр сервиса
        service = ChatService()
        
        # Тестируем генерацию ответа
        response = await service.generate_response("Тестовый запрос")
        
        # Проверяем результат
        assert response == "Тестовый ответ"
        assert mock_instance.ainvoke.called
