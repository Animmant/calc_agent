#!/usr/bin/env python3
"""
Тест тільки калькулятора без API ключа
"""

import sys
import os

# Додаємо src до path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_calculator():
    """Тестуємо тільки калькулятор"""
    print("🧮 Тестування калькулятора...")
    
    try:
        from src.agent.tools.calculator import basic_calculator, advanced_math_solver
        
        # Тестуємо базовий калькулятор
        print("\n📝 Базовий калькулятор:")
        test_cases = [
            "2 + 3",
            "10 - 4", 
            "3 * 4",
            "15 / 3",
            "2 ** 3",
            "2 + 3 * 4",
            "(2 + 3) * 4"
        ]
        
        for expr in test_cases:
            try:
                result = basic_calculator(expr)
                print(f"  ✅ {expr} = {result}")
            except Exception as e:
                print(f"  ❌ {expr} → Помилка: {e}")
        
        # Тестуємо розширений розв'язувач
        print("\n🔧 Розширений розв'язувач:")
        solver_cases = [
            "квадратний корінь з 25",
            "15% від 100", 
            "площа круга",
            "невідома задача"
        ]
        
        for case in solver_cases:
            try:
                result = advanced_math_solver(case)
                print(f"  ✅ '{case}' → {result[:60]}...")
            except Exception as e:
                print(f"  ❌ '{case}' → Помилка: {e}")
                
        print("\n🎉 Тестування завершено!")
        
    except Exception as e:
        print(f"❌ Помилка імпорту: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_calculator() 