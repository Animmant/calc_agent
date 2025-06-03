#!/usr/bin/env python3
"""
Швидкий тест основної функціональності Calculator Agent
"""

import sys
import os

# Додаємо src до Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Тестує основні імпорти"""
    print("🧪 Тестування імпортів...")
    
    try:
        # Тестуємо основні модулі
        from src.agent.prompts import SYSTEM_PROMPT, MATH_NOTEBOOK_LATEX_PROMPT_TEMPLATE
        from src.reporting.pdf_generator import get_available_engines
        from src.agent.tools.pdf_tools import pdf_tools
        from src.cli.REPL import CalculatorREPL
        
        print("✅ Всі основні модулі імпортуються успішно")
        return True
        
    except Exception as e:
        print(f"❌ Помилка імпорту: {e}")
        return False

def test_pdf_engines():
    """Тестує PDF движки"""
    print("🧪 Тестування PDF движків...")
    
    try:
        from src.reporting.pdf_generator import get_available_engines
        engines = get_available_engines()
        
        print(f"📊 Доступні движки: {engines}")
        available_count = sum(engines.values())
        
        if available_count > 0:
            print(f"✅ Доступно {available_count} движків")
        else:
            print("⚠️  Жоден движок недоступний")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка тестування движків: {e}")
        return False

def test_tools():
    """Тестує інструменти"""
    print("🧪 Тестування інструментів...")
    
    try:
        from src.agent.tools.calculator import calculator_tools
        from src.agent.tools.pdf_tools import pdf_tools
        
        total_tools = len(calculator_tools) + len(pdf_tools)
        print(f"📊 Загальна кількість інструментів: {total_tools}")
        print(f"   • Математичні: {len(calculator_tools)}")
        print(f"   • PDF: {len(pdf_tools)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка тестування інструментів: {e}")
        return False

def test_cli():
    """Тестує CLI"""
    print("🧪 Тестування CLI...")
    
    try:
        from src.cli.REPL import CalculatorREPL
        
        repl = CalculatorREPL()
        print("✅ CLI створено успішно")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка тестування CLI: {e}")
        return False

def main():
    """Головна функція тестування"""
    print("🚀 Швидкий тест Calculator Agent")
    print("=" * 40)
    
    tests = [
        ("Імпорти", test_imports),
        ("PDF движки", test_pdf_engines),
        ("Інструменти", test_tools),
        ("CLI", test_cli),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Критична помилка в тесті '{test_name}': {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Результат: {passed}/{total} тестів пройдено")
    
    if passed == total:
        print("🎉 Всі тести пройшли! Система готова.")
    else:
        print("⚠️  Деякі тести не пройшли.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 