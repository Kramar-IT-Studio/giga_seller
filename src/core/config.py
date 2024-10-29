"""Модуль конфигурации приложения."""
from dataclasses import dataclass
from functools import lru_cache
from typing import Final
import os
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    """Настройки приложения."""
    TELEGRAM_TOKEN: Final[str]
    GIGACHAT_TOKEN: Final[str]

    def validate(self) -> None:
        """Проверка корректности настроек."""
        if not self.TELEGRAM_TOKEN:
            raise ValueError("Не указан токен Telegram в переменных окружения")
        if not self.GIGACHAT_TOKEN:
            raise ValueError("Не указан токен GigaChat в переменных окружения")

@lru_cache
def get_settings() -> Settings:
    """Получение настроек приложения (синглтон)."""
    load_dotenv()
    settings = Settings(
        TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN", ""),
        GIGACHAT_TOKEN=os.getenv("GIGACHAT_TOKEN", "")
    )
    settings.validate()
    return settings 