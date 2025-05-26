import unittest
import sys
import os

# Додаємо src до Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from src.agent.tools.calculator import basic_calculator, advanced_math_solver, safe_eval

class TestCalculatorTools(unittest.TestCase):
    """Тести для інструментів калькулятора"""
    
    def test_basic_calculator_simple_operations(self):
        """Тестуємо прості арифметичні операції"""
        # Додавання
        result = basic_calculator("2 + 3")
        self.assertEqual(result, "5")
        
        # Віднімання
        result = basic_calculator("10 - 4")
        self.assertEqual(result, "6")
        
        # Множення
        result = basic_calculator("3 * 4")
        self.assertEqual(result, "12")
        
        # Ділення
        result = basic_calculator("15 / 3")
        self.assertEqual(result, "5")
        
        # Степінь
        result = basic_calculator("2 ** 3")
        self.assertEqual(result, "8")
    
    def test_basic_calculator_complex_expressions(self):
        """Тестуємо складні вирази"""
        # Порядок операцій
        result = basic_calculator("2 + 3 * 4")
        self.assertEqual(result, "14")
        
        # Дужки
        result = basic_calculator("(2 + 3) * 4")
        self.assertEqual(result, "20")
        
        # Десяткові числа
        result = basic_calculator("3.5 + 2.5")
        self.assertEqual(result, "6")
        
        # Від'ємні числа
        result = basic_calculator("-5 + 3")
        self.assertEqual(result, "-2")
    
    def test_basic_calculator_invalid_input(self):
        """Тестуємо обробку неправильного вводу"""
        # Недозволені символи
        result = basic_calculator("2 + abc")
        self.assertIn("недозволені символи", result.lower())
        
        # Неправильний синтаксис
        result = basic_calculator("2 + + 3")
        self.assertIn("помилка", result.lower())
        
        # Ділення на нуль
        result = basic_calculator("5 / 0")
        self.assertIn("помилка", result.lower())
    
    def test_safe_eval_function(self):
        """Тестуємо безпечну функцію eval"""
        # Правильні вирази
        self.assertEqual(safe_eval("2 + 3"), 5)
        self.assertEqual(safe_eval("10 * 2"), 20)
        self.assertEqual(safe_eval("2 ** 3"), 8)
        
        # Неправильні вирази повинні викидати помилку
        with self.assertRaises(ValueError):
            safe_eval("import os")
        
        with self.assertRaises(ValueError):
            safe_eval("__import__('os')")
    
    def test_advanced_math_solver_responses(self):
        """Тестуємо відповіді розширеного розв'язувача"""
        # Квадратний корінь
        result = advanced_math_solver("як знайти квадратний корінь з 25")
        self.assertIn("25 ** 0.5", result)
        
        # Відсотки
        result = advanced_math_solver("як обчислити 15% від 100")
        self.assertIn("0.15", result)
        
        # Площа круга
        result = advanced_math_solver("площа круга з радіусом 5")
        self.assertIn("π", result)
        
        # Загальний випадок
        result = advanced_math_solver("складна математична задача")
        self.assertIn("розробляється", result)

class TestCalculatorIntegration(unittest.TestCase):
    """Інтеграційні тести для калькулятора"""
    
    def test_calculator_tools_import(self):
        """Тестуємо імпорт інструментів"""
        from src.agent.tools.calculator import calculator_tools
        
        self.assertEqual(len(calculator_tools), 2)
        self.assertEqual(calculator_tools[0].name, "basic_calculator")
        self.assertEqual(calculator_tools[1].name, "advanced_math_solver")
    
    def test_tool_descriptions(self):
        """Тестуємо описи інструментів"""
        from src.agent.tools.calculator import calculator_tools
        
        basic_calc = calculator_tools[0]
        advanced_solver = calculator_tools[1]
        
        # Перевіряємо, що описи містять корисну інформацію
        self.assertIn("арифметичні операції", basic_calc.description)
        self.assertIn("математичні задачі", advanced_solver.description)

if __name__ == "__main__":
    # Запускаємо тести
    unittest.main(verbosity=2) 