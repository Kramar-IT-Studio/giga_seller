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
    API_ENDPOINT: Final[str]

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
            
        if not self.API_ENDPOINT:
            raise ValueError("Не указан API_ENDPOINT в переменных окружения")
        if not self.API_ENDPOINT.startswith(("http://", "https://")):
            raise ValueError("API_ENDPOINT должен начинаться с http:// или https://")


def get_settings() -> Settings:
    """Получение настроек приложения."""
    if "TELEGRAM_TOKEN" in os.environ:
        del os.environ["TELEGRAM_TOKEN"]
    if "GIGACHAT_TOKEN" in os.environ:
        del os.environ["GIGACHAT_TOKEN"]
    if "API_ENDPOINT" in os.environ:
        del os.environ["API_ENDPOINT"]

    dotenv_path = find_dotenv()
    if not dotenv_path:
        raise FileNotFoundError("Файл .env не найден")

    load_dotenv(dotenv_path, override=True)

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    gigachat_token = os.getenv("GIGACHAT_TOKEN")
    api_endpoint = os.getenv("API_ENDPOINT")

    # Проверяем, что все значения не None
    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN не найден в .env файле")
    if not gigachat_token:
        raise ValueError("GIGACHAT_TOKEN не найден в .env файле")
    if not api_endpoint:
        raise ValueError("API_ENDPOINT не найден в .env файле")

    settings = Settings(
        TELEGRAM_TOKEN=telegram_token,
        GIGACHAT_TOKEN=gigachat_token,
        API_ENDPOINT=api_endpoint
    )
    settings.validate()
    return settings
