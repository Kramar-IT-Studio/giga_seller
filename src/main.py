"""Основная точка входа приложения."""
import os
import sys
from pathlib import Path
from src.bot.telegram_bot import TelegramBot
from src.services.chat_service import ChatService

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

def main() -> None:
    """Запуск приложения."""
    chat_service = ChatService()
    bot = TelegramBot(chat_service)
    bot.run()

if __name__ == "__main__":
    main()
