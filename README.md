# 🤖 GigaChat Telegram Bot

Умный телеграм-бот для продажи телефонов, работающий на базе GigaChat API.

## ✨ Возможности

- 💬 Естественный диалог с клиентом
- 📱 Консультация по моделям телефонов
- 🎯 Сбор данных для оформления заказа
- 📋 Валидация контактных данных
- 🔄 Сохранение состояния диалога
- 🌐 Интеграция с внешним API для заказов

## 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Kramar-IT-Studio/giga_seller.git
cd giga_seller
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` и добавьте необходимые переменные:
```env
TELEGRAM_TOKEN=your_telegram_token
GIGACHAT_TOKEN=your_gigachat_token
API_ENDPOINT=https://your-api-endpoint.com
```

## 🛠️ Разработка

Установите дополнительные зависимости для разработки:
```bash
pip install -r requirements-dev.txt
```

### Доступные команды:

```bash
# Форматирование кода
invoke format

# Проверка линтером
invoke lint

# Запуск тестов
invoke test

# Обновление зависимостей
invoke deps-update
```

## 📦 Структура проекта

```
src/
├── bot/                # Telegram бот
├── core/              # Конфигурация
├── models/            # Модели данных
├── services/          # Бизнес-логика
├── utils/             # Утилиты
└── constants/         # Константы

tests/                 # Тесты
```

## 🧪 Тестирование

Проект использует pytest для тестирования. Запуск тестов:

```bash
pytest tests/ -v
```

## 🔧 Конфигурация

Основные настройки находятся в файле `src/core/config.py`:

```10:17:src/core/config.py
@dataclass(frozen=True)
class Settings:
    """Настройки приложения."""

    TELEGRAM_TOKEN: Final[str]
    GIGACHAT_TOKEN: Final[str]
    API_ENDPOINT: Final[str]

```


## 📝 Пример использования

```python
from src.bot.telegram_bot import TelegramBot
from src.services.chat_service import ChatService

def main():
    chat_service = ChatService()
    bot = TelegramBot(chat_service)
    bot.run()
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте изменения в репозиторий (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License. См. файл [LICENSE](./LICENSE.md) для деталей.

## 👥 Авторы

- Крамарь Игорь - [Гитхаб](https://github.com/igorkramar)

## 🙏 Благодарности

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [GigaChat API](https://developers.sber.ru/docs/ru/gigachat/overview)