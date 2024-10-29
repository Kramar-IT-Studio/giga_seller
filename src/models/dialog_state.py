"""Модуль для хранения состояния диалога."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class DialogStep(Enum):
    """Этапы диалога с пользователем."""
    START = auto()          # Начало диалога
    PHONE_SELECTION = auto()  # Выбор телефона
    SPECS_SELECTION = auto()  # Выбор характеристик
    GET_NAME = auto()       # Получение имени
    GET_PHONE = auto()      # Получение номера телефона
    CONFIRMATION = auto()   # Подтверждение заказа


@dataclass
class OrderData:
    """Данные заказа."""
    phone_model: Optional[str] = None
    specifications: Optional[str] = None
    client_name: Optional[str] = None
    client_phone: Optional[str] = None


class DialogState:
    """Класс для хранения состояния диалога."""
    
    def __init__(self) -> None:
        """Инициализация состояния диалога."""
        self.current_step = DialogStep.START
        self.order_data = OrderData()

    def reset(self) -> None:
        """Сброс состояния диалога."""
        self.current_step = DialogStep.START
        self.order_data = OrderData()

    def is_order_complete(self) -> bool:
        """Проверка заполненности всех данных заказа."""
        return all([
            self.order_data.phone_model,
            self.order_data.specifications,
            self.order_data.client_name,
            self.order_data.client_phone
        ]) 