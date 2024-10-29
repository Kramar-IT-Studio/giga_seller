"""Реализация Telegram бота."""

from telegram.ext import Application, CommandHandler
from telegram.ext import MessageHandler as TGMessageHandler
from telegram.ext import filters

from src.bot.message_handler import MessageHandler
from src.core.config import get_settings
from src.services.chat_service import ChatService


class TelegramBot:
    """Класс Telegram бота."""

    def __init__(self, chat_service: ChatService) -> None:
        """Инициализация бота."""
        self._settings = get_settings()
        self._message_handler = MessageHandler(chat_service)
        self._application = self._create_application()

    def _create_application(self) -> Application:
        """Создание и настройка приложения Telegram."""
        app = Application.builder().token(self._settings.TELEGRAM_TOKEN).build()

        # Добавляем обработчики
        app.add_handler(CommandHandler("start", self._message_handler.start))
        app.add_handler(
            TGMessageHandler(
                filters.TEXT & ~filters.COMMAND, self._message_handler.handle_message
            )
        )

        return app

    def run(self) -> None:
        """Запуск бота."""
        print("🤖 Бот успешно запущен и готов к работе!")
        self._application.run_polling()
