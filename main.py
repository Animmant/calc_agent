#!/usr/bin/env python3
"""
Calculator Agent - Головний файл запуску
Інтелектуальний агент для математичних обчислень з використанням LangGraph та Google Gemini
"""

import sys
import os

# Додаємо src до Python path для імпортів
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Ініціалізуємо логування перед іншими імпортами
from src.utils.logger_config import setup_logging
setup_logging()

import logging
from src.cli.REPL import run_chat_loop

logger = logging.getLogger(__name__)

def main():
    """Головна функція запуску програми"""
    logger.info("🚀 Запуск Calculator Agent")
    
    print("=" * 60)
    print("🧮 CALCULATOR AGENT")
    print("Інтелектуальний асистент для математичних обчислень")
    print("Powered by Google Gemini + LangGraph")
    print("=" * 60)
    
    try:
        # Перевіряємо наявність API ключа
        from src.config.settings import GOOGLE_API_KEY
        if not GOOGLE_API_KEY:
            print("❌ ПОМИЛКА: GOOGLE_API_KEY не знайдено!")
            print("💡 Створіть файл .env з рядком:")
            print("   GOOGLE_API_KEY=your_api_key_here")
            print("💡 Отримати ключ можна тут: https://aistudio.google.com/app/apikey")
            return 1
        
        # Запускаємо інтерактивний чат
        print("\n🚀 Запуск оптимізованого Calculator Agent...")
        run_chat_loop()
                
    except Exception as e:
        logger.error(f"Критична помилка: {e}", exc_info=True)
        print(f"❌ Критична помилка: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
