"""Сервис для работы с чат-моделями."""
from abc import ABC, abstractmethod
from typing import Protocol
from langchain.schema import AIMessage, HumanMessage
from langchain_community.chat_models import GigaChat
from src.core.config import get_settings

class ChatResponse(Protocol):
    """Протокол ответа чат-модели."""
    content: str

class ChatService(ABC):
    """Абстрактный класс сервиса чата."""
    @abstractmethod
    async def generate_response(self, message: str) -> str:
        """Генерация ответа на сообщение пользователя."""
        pass

class GigaChatService(ChatService):
    """Реализация сервиса чата через GigaChat."""
    def __init__(self) -> None:
        """Инициализация сервиса GigaChat."""
        self._chat = GigaChat(
            credentials=get_settings().GIGACHAT_TOKEN,
            verify_ssl_certs=False
        )

    async def generate_response(self, message: str) -> str:
        """Генерация ответа с помощью GigaChat."""
        response = self._chat.invoke([HumanMessage(content=message)])
        if not isinstance(response, AIMessage) or not isinstance(response.content, str):
            raise ValueError("Получен некорректный ответ от GigaChat")
        return response.content