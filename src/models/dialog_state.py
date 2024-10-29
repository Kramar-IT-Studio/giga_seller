"""Модуль для хранения состояния диалога."""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import logging
import sys
from datetime import datetime


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

    def __str__(self) -> str:
        """Строковое представление данных заказа."""
        return (
            f"OrderData(model={self.phone_model}, "
            f"specs={self.specifications}, "
            f"name={self.client_name}, "
            f"phone={self.client_phone})"
        )


@dataclass
class DialogState:
    """Класс для хранения состояния диалога."""
    current_step: DialogStep = DialogStep.START
    order_data: OrderData = field(default_factory=OrderData)
    last_error: Optional[str] = None

    def reset(self) -> None:
        """Сброс состояния диалога."""
        self.current_step = DialogStep.START
        self.order_data = OrderData()

    def is_order_complete(self) -> bool:
        """Проверка заполненности всех данных заказа."""
        is_complete = all([
            self.order_data.phone_model,
            self.order_data.specifications,
            self.order_data.client_name,
            self.order_data.client_phone,
            self.current_step == DialogStep.CONFIRMATION
        ])
        
        if is_complete:
            print("Заказ укомплектован и готов к сохранению")
        else:
            print(
                f"Заказ не готов: модель={bool(self.order_data.phone_model)}, "
                f"specs={bool(self.order_data.specifications)}, "
                f"name={bool(self.order_data.client_name)}, "
                f"phone={bool(self.order_data.client_phone)}, "
                f"step={self.current_step}"
            )
        
        return is_complete