# main.py
import logging
import sys
import os

# Додаємо кореневу директорію проекту до Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Налаштування логування та завантаження конфігурацій
# Важливо імпортувати їх на початку, щоб налаштування застосувалися.
from src.utils import logger_config # Ініціалізує логер
from src.config import settings     # Завантажує .env та інші налаштування

from src.cli.REPL import run_chat_loop

logger = logging.getLogger(__name__)

def main():
    """Головна функція запуску програми."""
    logger.info("🚀 Запуск головної програми...")
    
    if not settings.GOOGLE_API_KEY:
        logger.error("❌ критична помилка: GOOGLE_API_KEY не знайдено! Перевірте .env файл.")
        print("❌ критична помилка: GOOGLE_API_KEY не знайдено!")
        print("💡 Створіть файл .env в корені проекту з рядком:")
        print("   GOOGLE_API_KEY=your_api_key_here")
        print("💡 Отримати ключ можна тут: https://aistudio.google.com/app/apikey")
        return

    try:
        run_chat_loop()
    except Exception as e:
        logger.critical(f"Неперехоплена помилка на верхньому рівні: {e}", exc_info=True)
        print(f"❌ Сталася критична помилка. Деталі див. у логах.")
    finally:
        logger.info("🏁 Програма завершила роботу.")

if __name__ == "__main__":
    main()