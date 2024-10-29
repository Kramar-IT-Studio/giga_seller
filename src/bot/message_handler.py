"""Telegram message handlers."""
from telegram import Update
from telegram.ext import ContextTypes
from src.services.chat_service import ChatService

class MessageHandler:
    """Handler for telegram messages."""
    def __init__(self, chat_service: ChatService) -> None:
        """Initialize message handler."""
        self._chat_service = chat_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        if update.message is None:
            return

        await update.message.reply_text(
            "👋 Привет! Я бот с GigaChat.\n"
            "✍️ Напиши мне что-нибудь, и я отвечу!"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle user messages."""
        if update.message is None or update.message.text is None:
            return

        try:
            await update.message.reply_text("🤔 Думаю над ответом...")
            response = await self._chat_service.generate_response(update.message.text)
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"😢 Ошибка: {str(e)}") 