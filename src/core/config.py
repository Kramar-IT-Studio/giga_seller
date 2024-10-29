"""Модуль конфигурации приложения."""

import os
from dataclasses import dataclass
from typing import Final

from dotenv import find_dotenv, load_dotenv


@dataclass(frozen=True)
class Settings:
    """Настройки приложения."""

    TELEGRAM_TOKEN: Final[str]
    GIGACHAT_TOKEN: Final[str]

    def validate(self) -> None:
        """Проверка корректности настроек."""
        if not self.TELEGRAM_TOKEN:
            raise ValueError("Не указан токен Telegram в переменных окружения")
        if "your_telegram_token" in self.TELEGRAM_TOKEN.lower():
            raise ValueError(
                "Используется placeholder вместо реального токена Telegram"
            )

        if not self.GIGACHAT_TOKEN:
            raise ValueError("Не указан токен GigaChat в переменных окружения")
        if "your_gigachat_token" in self.GIGACHAT_TOKEN.lower():
            raise ValueError(
                "Используется placeholder вместо реального токена GigaChat"
            )


def get_settings() -> Settings:
    """Получение настроек приложения."""
    if "TELEGRAM_TOKEN" in os.environ:
        del os.environ["TELEGRAM_TOKEN"]
    if "GIGACHAT_TOKEN" in os.environ:
        del os.environ["GIGACHAT_TOKEN"]

    dotenv_path = find_dotenv()
    if not dotenv_path:
        raise FileNotFoundError("Файл .env не найден")

    load_dotenv(dotenv_path, override=True)

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    gigachat_token = os.getenv("GIGACHAT_TOKEN")

    if not telegram_token or not gigachat_token:
        raise ValueError("Не удалось загрузить токены из .env файла")

    settings = Settings(TELEGRAM_TOKEN=telegram_token, GIGACHAT_TOKEN=gigachat_token)
    settings.validate()
    return settings
