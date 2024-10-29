"""Обработчик сообщений телеграм бота."""
import logging
import sys
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from src.services.chat_service import ChatService
from src.services.state_service import StateService
from src.models.dialog_state import DialogState, DialogStep
from src.utils.phone_validator import validate_russian_phone
from src.constants.phone_data import (
    get_brand_by_keyword,
    get_model_keywords,
    is_spec_related,
    PHONE_SPECS
)
from src.services.order_service import OrderService

class MessageHandler:
    """Обработчик сообщений."""

    def __init__(self, chat_service: ChatService) -> None:
        """Инициализация обработчика."""
        self._chat_service = chat_service
        self._state_service = StateService()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработка команды /start."""
        if not update.message or not update.effective_user:
            return

        # Сбрасываем состояние при старте
        self._state_service.reset_state(update.effective_user.id)
        
        await update.message.reply_text(
            "👋 Здравствуйте! Я консультант по проаже телефонов. "
            "Расскажите, какой телефон вас интересует?"
        )

    def _build_prompt(self, state: DialogState, message: str) -> str:
        """Формирование промпта для GigaChat на основе состояния диалога."""
        system_prompt = """Ты - дружелюбный консультант по продажам телефонов. 
        Строго следуй этим правилам при общении:
        
        1. СТИЛЬ ОБЩЕНИЯ:
        - НЕ ИСПОЛЬЗУЙ приветствие "Здравствуйте" в ответах
        - Если клиент указал модель телефона, сразу переходи к уточнению деталей
        - При получении модели телефона спроси о желаемых характеристиках
        - Используй фразы "Отличный выбор!", "Хороший выбор!"
        
        2. ПОСЛЕДОВАТЕЛЬНОСТЬ ДИАЛОГА:
        - При указании модели: "Отличный выбор! Какие характеристики вас интересуют (память, цвет)?"
        - Если клиент отвечает "нет" на вопрос о характеристиках: "Хорошо! Тогда давайте перейдем к оформлению. Как могу к вам обращаться?"
        - При готовности к покупке: "Отлично! Для оформления заказа, пожалуйста, представьтесь - как могу к вам обращаться?"
        - После получения имени: "Спасибо, {имя}! Теперь, пожалуйста, укажите ваш контактный номер телефона"
        - После получения телефона: "Спасибо, {имя}. Ваш заказ принят. Мы свяжемся с вами в ближайшее время для подтверждения деталей."
        
        3. ВАЖНО:
        - НИКОГДА не повторяй приветствие в ответах
        - Сразу реагируй на указанную модель телефона
        - При ответе "нет" на вопрос о характеристиках, переходи к запросу имени
        - Строго следуй последовательности: модель -> (характеристики) -> имя -> телефон
        """

        context = f"\nТекущий этап диалога: {state.current_step.name}\n"
        if state.order_data.phone_model:
            context += f"Выбранная модель: {state.order_data.phone_model}\n"
        if state.order_data.specifications:
            context += f"Характеристики: {state.order_data.specifications}\n"
        if state.order_data.client_name:
            context += f"Имя клиента: {state.order_data.client_name}\n"
        if state.order_data.client_phone:
            context += f"Телефон клиента: {state.order_data.client_phone}\n"
        
        context += f"\nСообщение пользователя: {message}"
        
        return system_prompt + context

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработка входящих сообщений."""
        if not update.message or not update.effective_user or not update.message.text:
            return

        user_id = update.effective_user.id
        message_text = update.message.text
        
        try:
            state = self._state_service.get_state(user_id)
            
            # Обработка ошибок валидации
            if hasattr(state, 'last_error') and state.last_error:
                error_message = state.last_error
                state.last_error = None
                
                if error_message == "name_validation_error":
                    await update.message.reply_text(
                        "Пожалуйста, введите ваше настоящее имя (например: Иван, Мария).\n"
                        "Имя должно содержать только буквы."
                    )
                    return
                elif state.current_step == DialogStep.GET_PHONE:
                    await update.message.reply_text(
                        f"❌ {error_message}\n\n"
                        "Пожалуйста, введите номер телефона в одном из форматов:\n"
                        "• +79XXXXXXXXX\n"
                        "• 89XXXXXXXXX\n"
                        "• 9XXXXXXXXX"
                    )
                    return

            prompt = self._build_prompt(state, message_text)
            response = await self._chat_service.generate_response(prompt)
            
            old_step = state.current_step
            self._update_state(state, message_text, response)
            
            # Проверяем, был ли переход к следующему шагу
            if old_step == state.current_step and state.current_step == DialogStep.GET_PHONE:
                # Если шаг не изменился при вводе телефона, значит была ошибка валидации
                await update.message.reply_text(
                    "❌ Неверный формат номера телефона.\n\n"
                    "Пожалуйста, введите номер телефона в одном из форматов:\n"
                    "• +79XXXXXXXXX\n"
                    "• 89XXXXXXXXX\n"
                    "• 9XXXXXXXXX"
                )
                return
            
            # Если заказ завершен
            if state.is_order_complete():
                await self._handle_complete_order(update, state)
                self._state_service.reset_state(user_id)
            # Если переходим к запросу телефона
            elif old_step == DialogStep.GET_NAME and state.current_step == DialogStep.GET_PHONE:
                await update.message.reply_text(
                    f"Спасибо, {state.order_data.client_name}! "
                    "Теперь, пожалуйста, укажите ваш контактный номер телефона в формате:\n"
                    "• +79XXXXXXXXX\n"
                    "• 89XXXXXXXXX\n"
                    "• 9XXXXXXXXX"
                )
            # Если запрашиваем имя
            elif state.current_step == DialogStep.GET_NAME:
                await update.message.reply_text(
                    "Как могу к вам обращаться? Пожалуйста, введите ваше имя."
                )
            # В остальных случаях отправляем ответ от GigaChat
            else:
                await update.message.reply_text(response)
            
        except Exception as e:
            if update.message:
                await update.message.reply_text(f"😢 Произошла ошибка: {str(e)}")

    def _update_state(self, state: DialogState, message: str, response: str) -> None:
        """Обновление состояния диалога."""
        message_lower = message.lower()
        
        if state.current_step == DialogStep.START:
            brand = get_brand_by_keyword(message)
            if brand:
                state.order_data.phone_model = message
                state.current_step = DialogStep.SPECS_SELECTION
                print(f"Выбрана модель: {message}")
        
        elif state.current_step == DialogStep.SPECS_SELECTION:
            state.order_data.specifications = message
            state.current_step = DialogStep.GET_NAME
            print(f"Указаны характеристики: {message}")
        
        elif state.current_step == DialogStep.GET_NAME:
            if (2 <= len(message) <= 20 and 
                not any(char.isdigit() for char in message) and 
                not get_brand_by_keyword(message) and 
                not is_spec_related(message) and 
                message_lower not in ["да", "нет", "конечно", "хорошо", "ок"]):
                
                state.order_data.client_name = message
                state.current_step = DialogStep.GET_PHONE
                print(f"Указано имя клиента: {message}")
                return
            else:
                state.last_error = "name_validation_error"
                print(f"Неверный формат имени: {message}")
                return
        
        elif state.current_step == DialogStep.GET_PHONE:
            is_valid, result = validate_russian_phone(message)
            if is_valid:
                state.order_data.client_phone = result
                state.current_step = DialogStep.CONFIRMATION
                print(f"Указан номер телефона: {result}")
            else:
                state.last_error = result
                print(f"Неверный формат телефона: {message}")
                return

    async def _handle_complete_order(self, update: Update, state: DialogState) -> None:
        """Обработка завершённого заказа."""
        if not update.message:
            return
        
        try:
            # Создаем заказ через сервис
            order_service = OrderService(self._chat_service)
            order_service.create_order(state.order_data)
            
            # Формируем информацию о заказе для логов
            order_info = (
                f"\n{'=' * 20} НОВЫЙ ЗАКАЗ {'=' * 20}\n"
                f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Модель: {state.order_data.phone_model}\n"
                f"Характеристики: {state.order_data.specifications}\n"
                f"Имя клиента: {state.order_data.client_name}\n"
                f"Телефон: {state.order_data.client_phone}\n"
                f"{'=' * 55}\n"
            )
            print(order_info, flush=True)
            
            # Отправляем подтверждение пользователю
            confirmation_message = (
                f"Отличный выбор, {state.order_data.client_name}! "
                f"Вы выбрали {state.order_data.phone_model} "
                f"с характеристиками: {state.order_data.specifications}. "
                "Мы свяжемся с вами в ближайшее время для подтверждения деталей."
            )
            await update.message.reply_text(confirmation_message)
            
        except Exception as e:
            error_message = f"Ошибка при создании заказа: {str(e)}"
            print(error_message)
            await update.message.reply_text(
                "😢 Произошла ошибка при оформлении заказа. "
                "Пожалуйста, попробуйте позже или свяжитесь с поддержкой."
            )
