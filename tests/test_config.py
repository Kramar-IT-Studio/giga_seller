"""Тесты для модуля конфигурации."""
import pytest
from src.core.config import Settings

def test_settings_validation_with_valid_tokens():
    """Тест валидации с корректными токенами."""
    settings = Settings(
        TELEGRAM_TOKEN="правильный_токен",
        GIGACHAT_TOKEN="правильный_токен"
    )
    settings.validate()  # Не должно вызывать исключений

def test_settings_validation_with_empty_telegram_token():
    """Тест валидации с пустым токеном Telegram."""
    settings = Settings(
        TELEGRAM_TOKEN="",
        GIGACHAT_TOKEN="правильный_токен"
    )
    with pytest.raises(ValueError, match="Не указан токен Telegram"):
        settings.validate()

def test_settings_validation_with_empty_gigachat_token():
    """Тест валидации с пустым токеном GigaChat."""
    settings = Settings(
        TELEGRAM_TOKEN="правильный_токен",
        GIGACHAT_TOKEN=""
    )
    with pytest.raises(ValueError, match="Не указан токен GigaChat"):
        settings.validate() 