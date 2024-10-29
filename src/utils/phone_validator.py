"""Валидатор номера телефона."""
import re
from typing import Tuple

def validate_russian_phone(phone: str) -> Tuple[bool, str]:
    """
    Валидация и форматирование российского номера телефона.
    
    Args:
        phone: Строка с номером телефона
    
    Returns:
        Tuple[bool, str]: (валиден ли номер, отформатированный номер или сообщение об ошибке)
    """
    # Убираем все не цифры из номера
    digits = ''.join(filter(str.isdigit, phone))
    
    # Проверяем базовые условия
    if len(digits) < 3:  # Для очень коротких номеров
        return False, "Номер телефона слишком короткий"
    
    # Если номер начинается с 8 или 7, это должен быть 11-значный номер
    if digits.startswith('8') or digits.startswith('7'):
        if len(digits) != 11:
            return False, f"Неверная длина номера: {len(digits)}. Должно быть 11 цифр для номера с 8 или 7"
        # Преобразуем 8 в +7
        formatted = '+7' + digits[1:]
    
    # Если номер начинается с 9, добавляем +7
    elif digits.startswith('9'):
        if len(digits) != 10:
            return False, f"Неверная длина номера: {len(digits)}. Должно быть 10 цифр для номера с 9"
        formatted = '+7' + digits
    
    else:
        return False, "Номер должен начинаться с 7, 8 или 9"
    
    return True, formatted 