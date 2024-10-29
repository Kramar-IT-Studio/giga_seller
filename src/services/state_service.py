"""Сервис для управления состояниями диалогов."""
from typing import Dict
from src.models.dialog_state import DialogState


class StateService:
    """Сервис управления состояниями диалогов."""
    
    def __init__(self) -> None:
        """Инициализация сервиса."""
        self._states: Dict[int, DialogState] = {}

    def get_state(self, user_id: int) -> DialogState:
        """Получение состояния диалога для пользователя."""
        if user_id not in self._states:
            self._states[user_id] = DialogState()
        return self._states[user_id]

    def reset_state(self, user_id: int) -> None:
        """Сброс состояния диалога для пользователя."""
        if user_id in self._states:
            self._states[user_id].reset() 