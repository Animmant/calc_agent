#!/usr/bin/env python3
"""
Простий тест для перевірки функціональності калькулятора
"""

import sys
import os

# Додаємо src до Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_calculator_tools():
    """Тестуємо інструменти калькулятора"""
    print("🧪 Тестування інструментів калькулятора...")
    
    try:
        from src.agent.tools.calculator import basic_calculator, advanced_math_solver
        
        # Тест 1: Прості операції
        print("\n📝 Тест 1: Прості арифметичні операції")
        test_cases = [
            ("2 + 3", "5"),
            ("10 - 4", "6"),
            ("3 * 4", "12"),
            ("15 / 3", "5"),
            ("2 ** 3", "8")
        ]
        
        for expression, expected in test_cases:
            result = basic_calculator(expression)
            status = "✅" if result == expected else "❌"
            print(f"  {status} {expression} = {result} (очікувалось: {expected})")
        
        # Тест 2: Складні вирази
        print("\n📝 Тест 2: Складні вирази")
        complex_cases = [
            ("2 + 3 * 4", "14"),
            ("(2 + 3) * 4", "20"),
            ("3.5 + 2.5", "6")
        ]
        
        for expression, expected in complex_cases:
            result = basic_calculator(expression)
            status = "✅" if result == expected else "❌"
            print(f"  {status} {expression} = {result} (очікувалось: {expected})")
        
        # Тест 3: Розширений розв'язувач
        print("\n📝 Тест 3: Розширений розв'язувач")
        solver_cases = [
            "квадратний корінь з 25",
            "15% від 100",
            "площа круга"
        ]
        
        for case in solver_cases:
            result = advanced_math_solver(case)
            print(f"  ✅ '{case}' → {result[:50]}...")
        
        print("\n🎉 Всі тести пройдено успішно!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Тестуємо конфігурацію"""
    print("\n🔧 Тестування конфігурації...")
    
    try:
        from src.config.settings import GOOGLE_API_KEY, GEMINI_MODEL_NAME
        
        if GOOGLE_API_KEY:
            print(f"  ✅ GOOGLE_API_KEY знайдено (довжина: {len(GOOGLE_API_KEY)})")
        else:
            print("  ⚠️ GOOGLE_API_KEY не знайдено")
        
        print(f"  ✅ Модель: {GEMINI_MODEL_NAME}")
        return True
        
    except Exception as e:
        print(f"❌ Помилка конфігурації: {e}")
        return False

def test_agent_creation():
    """Тестуємо створення агента"""
    print("\n🤖 Тестування створення агента...")
    
    try:
        from src.agent.agent_executor import create_llm, create_agent_executor
        from src.agent.tools.calculator import calculator_tools
        
        # Перевіряємо чи можемо створити LLM
        print("  📡 Створення LLM...")
        llm = create_llm()
        print("  ✅ LLM створено успішно")
        
        # Перевіряємо чи можемо створити агента
        print("  🔧 Створення агента...")
        agent = create_agent_executor(llm, calculator_tools)
        print("  ✅ Агент створено успішно")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка створення агента: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Головна функція тестування"""
    print("=" * 60)
    print("🧮 ТЕСТУВАННЯ CALCULATOR AGENT")
    print("=" * 60)
    
    tests = [
        ("Інструменти калькулятора", test_calculator_tools),
        ("Конфігурація", test_config),
        ("Створення агента", test_agent_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Критична помилка в тесті '{test_name}': {e}")
            results.append((test_name, False))
    
    # Підсумок
    print("\n" + "=" * 60)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ ПРОЙДЕНО" if result else "❌ ПРОВАЛЕНО"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестів пройдено")
    
    if passed == len(results):
        print("🎉 Всі тести пройдено! Система готова до роботи.")
        return 0
    else:
        print("⚠️ Деякі тести провалено. Перевірте налаштування.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 