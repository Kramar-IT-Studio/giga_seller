"""Константы для работы с данными о телефонах."""

# Бренды телефонов и их возможные написания
PHONE_BRANDS = {
    "samsung": ["самсунг", "samsung", "галакси", "galaxy"],
    "apple": ["айфон", "iphone", "apple", "эппл"],
    "xiaomi": ["сяоми", "xiaomi", "ксяоми", "ксиаоми"],
    "huawei": ["хуавей", "huawei", "хуавэй"],
    "honor": ["honor", "хонор"],
}

# Модели телефонов по брендам
PHONE_MODELS = {
    "samsung": ["s", "a", "m", "fold", "flip", "note", "ultra"],
    "apple": ["14", "15", "13", "12", "11", "pro", "max", "plus"],
    "xiaomi": ["redmi", "poco", "note", "pro"],
    "huawei": ["p", "mate", "nova"],
    "honor": ["magic", "x", "v"],
}

# Характеристики телефонов
PHONE_SPECS = {
    "memory": ["гб", "гигов", "гигабайт", "памяти", "gb"],
    "colors": ["черный", "белый", "розовый", "голубой", "серый", "фиолетовый", "золотой"],
    "common": ["память", "цвет", "характеристики", "объем"]
}

def get_brand_by_keyword(text: str) -> str | None:
    """
    Определяет бренд телефона по ключевому слову.
    
    Args:
        text: Текст сообщения
    
    Returns:
        str | None: Название бренда или None, если бренд не найден
    """
    text_lower = text.lower()
    for brand, keywords in PHONE_BRANDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return brand
    return None

def get_model_keywords(brand: str) -> list[str]:
    """
    Возвращает список ключевых слов для моделей конкретного бренда.
    
    Args:
        brand: Название бренда
    
    Returns:
        list[str]: Список ключевых слов для моделей
    """
    return PHONE_MODELS.get(brand, [])

def is_spec_related(text: str) -> bool:
    """
    Проверяет, относится ли текст к характеристикам телефона.
    
    Args:
        text: Текст сообщения
    
    Returns:
        bool: True если текст содержит упоминание характеристик
    """
    text_lower = text.lower()
    all_specs = []
    for specs in PHONE_SPECS.values():
        all_specs.extend(specs)
    return any(spec in text_lower for spec in all_specs) 