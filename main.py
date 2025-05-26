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
from src.cli.REPL import run_chat_loop, run_chat_loop_with_streaming

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
        print("\n🎯 Режими роботи:")
        print("1. Звичайний режим (рекомендований)")
        print("2. Потоковий режим (експериментальний)")
        print("3. Вихід")
        
        while True:
            try:
                choice = input("\n👤 Оберіть режим (1-3): ").strip()
                
                if choice == "1":
                    print("\n🚀 Запуск звичайного режиму...")
                    run_chat_loop()
                    break
                elif choice == "2":
                    print("\n🚀 Запуск потокового режиму...")
                    run_chat_loop_with_streaming()
                    break
                elif choice == "3":
                    print("👋 До побачення!")
                    break
                else:
                    print("❌ Невірний вибір. Введіть 1, 2 або 3.")
                    
            except KeyboardInterrupt:
                print("\n👋 Програма завершена користувачем.")
                break
                
    except Exception as e:
        logger.error(f"Критична помилка: {e}", exc_info=True)
        print(f"❌ Критична помилка: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
