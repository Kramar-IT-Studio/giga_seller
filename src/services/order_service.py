from dataclasses import dataclass
import requests
from src.core.config import get_settings
from src.models.dialog_state import OrderData
from src.services.chat_service import ChatService

@dataclass
class OrderRequest:
    """Данные для создания заказа."""
    name: str
    phone: str
    desc: str
    platform_id: str
    role_id: str

class OrderService:
    """Сервис для работы с заказами."""

    def __init__(self, chat_service: ChatService) -> None:
        """Инициализация сервиса."""
        self._settings = get_settings()
        self._chat_service = chat_service

    def create_order(self, order_data: OrderData) -> None:
        """Создание заказа."""
        if not order_data.client_phone or not order_data.client_name:
            raise ValueError("Телефон и имя обязательны для создания заказа")

        desc = (
            f"Модель: {order_data.phone_model}\n"
            f"Характеристики: {order_data.specifications}"
        )

        # Получаем platform_id и role_id из сессии GigaChat
        session = self._chat_service.get_session()
        
        request = OrderRequest(
            name=order_data.client_name.strip(),
            phone=self._normalize_phone(order_data.client_phone),
            desc=desc.strip(),
            platform_id=session.platform_id,
            role_id=session.role_id
        )

        self._send_order(request)

    def _send_order(self, request: OrderRequest) -> None:
        """Отправка заказа на сервер."""
        try:
            params = {
                'platform_id': request.platform_id,
                'role_id': request.role_id,
                'name': request.name,
                'phone': request.phone,
                'desc': request.desc,
            }
            print(f"Отправка заказа с параметрами: {params}")
            print(f"URL: {self._settings.API_ENDPOINT}")
            
            response = requests.get(
                self._settings.API_ENDPOINT,
                params=params,
                timeout=10
            )
            print(f"Ответ сервера: {response.status_code} - {response.text}")
            response.raise_for_status()
            
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")
            raise ValueError(f"Ошибка при отправке заказа: {e}")

    def _normalize_phone(self, phone: str) -> str:
        """Нормализация номера телефона."""
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) == 10:
            phone = '7' + phone
        elif len(phone) == 11:
            phone = '7' + phone[1:]
        
        if len(phone) != 11:
            raise ValueError(f"Некорректный формат телефона: {phone}")
        return phone