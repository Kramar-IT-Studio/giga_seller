"""Tests for telegram bot handlers."""
import pytest
from unittest.mock import Mock, AsyncMock
from telegram import Update, Message
from telegram.ext import ContextTypes
from src.bot.message_handler import MessageHandler

@pytest.fixture
def mock_update() -> Mock:
    """Create mock update object."""
    update = Mock(spec=Update)
    message = Mock(spec=Message)
    message.reply_text = AsyncMock()
    update.message = message
    return update

@pytest.fixture
def mock_context() -> Mock:
    """Create mock context object."""
    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    return context

@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context, mock_chat_service):
    """Test start command handler."""
    handler = MessageHandler(mock_chat_service)
    await handler.start(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "👋 Привет!" in call_args

@pytest.mark.asyncio
async def test_message_handling(mock_update, mock_context, mock_chat_service):
    """Test message handling."""
    mock_update.message.text = "Test message"
    handler = MessageHandler(mock_chat_service)
    
    await handler.handle_message(mock_update, mock_context)
    
    # Проверяем, что был отправлен ответ "Думаю над ответом..."
    assert mock_update.message.reply_text.call_args_list[0][0][0] == "🤔 Думаю над ответом..."
    
    # Проверяем, что сервис чата был вызван
    mock_chat_service.generate_response.assert_called_once_with("Test message")
    
    # Проверяем, что ответ от сервиса был отправлен пользователю
    assert len(mock_update.message.reply_text.call_args_list) == 2

@pytest.mark.asyncio
async def test_message_handling_error(mock_update, mock_context, mock_chat_service):
    """Test error handling in message handler."""
    mock_update.message.text = "Test message"
    mock_chat_service.generate_response.side_effect = Exception("Test error")
    
    handler = MessageHandler(mock_chat_service)
    await handler.handle_message(mock_update, mock_context)
    
    # Проверяем, что сообщение об ошибке было отправлено
    assert "😢 Ошибка: Test error" in mock_update.message.reply_text.call_args_list[-1][0][0]