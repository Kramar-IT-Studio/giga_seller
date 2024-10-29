"""Main application entry point."""
from src.bot.telegram_bot import TelegramBot
from src.services.chat_service import GigaChatService

def main() -> None:
    """Run the application."""
    chat_service = GigaChatService()
    bot = TelegramBot(chat_service)
    bot.run()

if __name__ == "__main__":
    main() 