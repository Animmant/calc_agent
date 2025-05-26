import os
from dotenv import load_dotenv, find_dotenv

def load_api_keys():
    """Loads API keys from .env file."""
    if not find_dotenv():
        print("⚠️  Файл .env не знайдено. Будь ласка, створіть його з GOOGLE_API_KEY.")
        # Можна реалізувати більш строгу обробку помилки, якщо ключ критичний
    load_dotenv(find_dotenv())

# Завантажуємо ключі при імпорті модуля
load_api_keys()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Модельні налаштування ---
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest"  # Або інша доступна модель
DEFAULT_TEMPERATURE = 0.1

# --- Інші налаштування ---
# Тут можна додавати інші конфігурації проєкту 