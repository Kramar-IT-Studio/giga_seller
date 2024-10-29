"""Telegram message handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from src.services.chat_service import ChatService
from src.services.state_service import StateService


class MessageHandler:
    """Handler for telegram messages."""

    def __init__(self, chat_service: ChatService) -> None:
        """Initialize message handler."""
        self._chat_service = chat_service
        self._state_service = StateService()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        if not update.message or not update.effective_user:
            return

        # Сбрасываем состояние при старте
        self._state_service.reset_state(update.effective_user.id)
        
        await update.message.reply_text(
            "👋 Здравствуйте! Я консультант по продаже телефонов. "
            "Расскажите, какой телефон вас интересует?"
        )

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle user messages."""
        if not update.message or not update.effective_user:
            return

        user_id = update.effective_user.id
        message_text = update.message.text or ""
        
        try:
            # Получаем текущее состояние диалога
            state = self._state_service.get_state(user_id)
            
            # Отправляем "печатает..."
            await update.message.chat.send_action("typing")
            
            # Генерируем ответ через GigaChat
            response = await self._chat_service.generate_response(message_text)
            
            # Отправляем ответ пользователю
            await update.message.reply_text(response)
            
        except Exception as e:
            await update.message.reply_text(f"😢 Ошибка: {str(e)}")
