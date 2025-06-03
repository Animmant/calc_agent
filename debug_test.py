#!/usr/bin/env python3
"""
Простий скрипт для діагностики проблем
"""

print("=== ДІАГНОСТИКА CALCULATOR AGENT ===")

# Тест 1: Базова функціональність Python
print("✅ Python працює")

# Тест 2: Імпорт sys та os
import sys
import os
print(f"✅ Python версія: {sys.version}")
print(f"✅ Поточна директорія: {os.getcwd()}")

# Тест 3: Перевірка структури проекту
print("\n📁 Структура проекту:")
if os.path.exists("src"):
    print("✅ Директорія src існує")
    if os.path.exists("src/config"):
        print("✅ Директорія src/config існує")
    if os.path.exists("src/agent"):
        print("✅ Директорія src/agent існує")
    if os.path.exists("src/cli"):
        print("✅ Директорія src/cli існує")
else:
    print("❌ Директорія src не існує")

# Тест 4: Перевірка .env файлу
if os.path.exists(".env"):
    print("✅ Файл .env існує")
else:
    print("❌ Файл .env не існує")
    print("💡 Створіть файл .env з вмістом:")
    print("GOOGLE_API_KEY=your_api_key_here")

# Тест 5: Спроба імпорту модулів
print("\n🔧 Тестування імпортів:")

# Додаємо src до path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.config.settings import GOOGLE_API_KEY
    if GOOGLE_API_KEY:
        print(f"✅ GOOGLE_API_KEY завантажено (довжина: {len(GOOGLE_API_KEY)})")
    else:
        print("⚠️ GOOGLE_API_KEY порожній або не встановлений")
except Exception as e:
    print(f"❌ Помилка імпорту config: {e}")

try:
    from src.agent.tools.calculator import basic_calculator
    result = basic_calculator("2+2")
    print(f"✅ Калькулятор працює: 2+2 = {result}")
except Exception as e:
    print(f"❌ Помилка калькулятора: {e}")

print("\n=== КІНЕЦЬ ДІАГНОСТИКИ ===") 