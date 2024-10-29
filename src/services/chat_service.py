"""Сервис для работы с чат-моделями."""
from typing import List
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_community.chat_models import GigaChat
from src.core.config import get_settings
from dataclasses import dataclass
from gigachat import GigaChat
from gigachat.models import Chat, Messages


@dataclass
class ChatSession:
    """Данные сессии чата."""
    platform_id: str = "1"  # ID платформы по умолчанию
    role_id: str = "1"     # ID роли по умолчанию


class ChatService:
    """Сервис для работы с чат-моделями."""

    def __init__(self) -> None:
        """Инициализация сервиса."""
        self._chat = GigaChat(
            credentials=get_settings().GIGACHAT_TOKEN,
            verify_ssl_certs=False
        )
        self._messages: List[HumanMessage | AIMessage | SystemMessage] = []
        self._init_system_prompt()
        self._session = ChatSession()

    def get_session(self) -> ChatSession:
        """Получение текущей сессии."""
        return self._session

    def _init_system_prompt(self) -> None:
        """Инициализация системного промпта."""
        system_prompt = """Ты - дружелюбный консультант по продажам телефонов. 
        Строго следуй этим правилам при общении:
        
        1. СТИЛЬ ОБЩЕНИЯ:
        - НЕ ИСПОЛЬЗУЙ приветствие "Здравствуйте" в ответах
        - Если клиент указал модель телефона, сразу переходи к уточнению деталей
        - При получении модели телефона спроси о желаемых характеристиках
        - Используй фразы "Отличный выбор!", "Хороший выбор!"
        
        2. ПОСЛЕДОВАТЕЛЬНОСТЬ ДИАЛОГА:
        - При указании модели: "Отличный выбор! Какие характеристики вас интересуют (память, цвет)?"
        - При готовности к покупке: "Отлично! Для оформления заказа, пожалуйста, представьтесь - ка могу к вам обращаться?"
        - После получения имени: "Спасибо, {имя}! Теперь, пожалуйста, укажите ваш контактный номер телефона"
        - После получения телефона: "Спасибо, {имя}. Ваш заказ принят. Мы свяжемся с вами в ближайшее время для подтверждения деталей."
        
        3. ВАЖНО:
        - НИКОГДА не повторяй приветствие в ответах
        - Сразу реагируй на указанную модель телефона
        - Строго следуй последовательности: модель -> характеристики -> имя -> телефон
        
        4. ОФОРМЛЕНИЕ ЗАКАЗА:
        - Когда клиент говорит о покупке или оформлении, скажи:
          "Отлично! Для оформления заказа, пожалуйста, представьтесь - как могу к вам обращаться?"
        - После получения имени скажи:
          "Спасибо, {имя}! Теперь, пожалуйста, укажите ваш контактный номер еелфона"
        
        5. ВАЖНО:
        - НЕ спрашивай адрес доставки
        - НЕ спрашивай номер карты
        - ТОЛЬКО имя и номер телефона для связи
        - Если клиент хочет сразу оформить заказ, всё равно сначала спроси имя, потом телефон
        
        6. ЗАПРЕЩЕНО:
        - Пропускать этап получения имени
        - Пропускать этап получения номера телефона
        - Спрашивать что-либо кроме имени и телефона при оформлении
        
        7. ФОРМАТЫ НОМЕРА ТЕЛЕФОНА:
        - Принимай любой формат: +7XXX, 8XXX, без кода
        - Главное - получить номер для связи
        
        Помни: твоя главная задача - получить имя клиента и номер телефона для оформления заказа!"""
        
        self._messages = [SystemMessage(content=system_prompt)]

    async def generate_response(self, message: str) -> str:
        """Генерация ответа с помощью GigaChat."""
        self._messages.append(HumanMessage(content=message))
        
        # Преобразуем сообщения в формат GigaChat
        payload = {
            "messages": [
                {
                    "role": "system" if isinstance(msg, SystemMessage) else 
                            "assistant" if isinstance(msg, AIMessage) else "user",
                    "content": msg.content
                }
                for msg in self._messages
            ]
        }
        
        # Отправляем в правильном формате
        response = await self._chat.achat(payload)
        
        # Извлекаем текст из ответа
        response_text = response.choices[0].message.content
        
        # Добавляем ответ в историю
        self._messages.append(AIMessage(content=response_text))
        
        return response_text

    def reset_conversation(self) -> None:
        """Сброс истории диалога."""
        self._messages = []
        self._init_system_prompt()

    def set_session_params(self, data: dict) -> None:
        """Установка параметров сессии."""
        if 'platform_id' in data:
            self._session.platform_id = data['platform_id']
        if 'role_id' in data:
            self._session.role_id = data['role_id']
