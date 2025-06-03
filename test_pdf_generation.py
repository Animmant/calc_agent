#!/usr/bin/env python3
"""
Тестовий файл для перевірки PDF генерації.
"""

import sys
import os
import logging

# Додаємо кореневу директорію проекту до Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from src.reporting.pdf_generator import generate_debug_pdf, generate_math_notebook_pdf

def test_debug_pdf():
    """Тестує генерацію PDF звіту дебагу."""
    print("🧪 Тестування генерації debug PDF...")
    
    debug_data = {
        "original_user_query": "Скільки буде 2 + 2 * 3?",
        "llm_reasoning_steps": [
            "Аналізую математичний вираз",
            "Застосовую порядок операцій: спочатку множення, потім додавання",
            "2 * 3 = 6",
            "2 + 6 = 8"
        ],
        "tool_name": "calculator",
        "tool_input": {"expression": "2 + 2 * 3"},
        "tool_output": "8",
        "final_agent_response": "Результат обчислення виразу 2 + 2 * 3 дорівнює 8.",
        "resources": {
            "llm_model": "gemini-1.5-flash"
        }
    }
    
    pdf_path = generate_debug_pdf(debug_data)
    
    if pdf_path:
        print(f"✅ Debug PDF створено: {pdf_path}")
        return True
    else:
        print("❌ Не вдалося створити debug PDF")
        return False

def test_math_notebook_pdf():
    """Тестує генерацію PDF математичного зошита."""
    print("🧪 Тестування генерації math notebook PDF...")
    
    problem_statement = "Знайти площу круга з радіусом 5 см"
    solution_latex = r"""
Дано: радіус r = 5 см

Формула площі круга: S = \pi r^2

Підставляємо значення:
S = \pi \cdot 5^2 = \pi \cdot 25 = 25\pi

Обчислюємо числове значення:
S = 25 \cdot 3.14159... \approx 78.54 см²
"""
    
    pdf_path = generate_math_notebook_pdf(problem_statement, solution_latex)
    
    if pdf_path:
        print(f"✅ Math notebook PDF створено: {pdf_path}")
        return True
    else:
        print("❌ Не вдалося створити math notebook PDF")
        return False

def test_pdf_tools():
    """Тестує PDF інструменти агента."""
    print("🧪 Тестування PDF інструментів агента...")
    
    try:
        from src.agent.tools.pdf_tools import create_debug_report, create_math_notebook
        
        # Тест debug report tool
        debug_result = create_debug_report.invoke({
            "original_user_query": "Тестовий запит",
            "reasoning_steps": ["Крок 1", "Крок 2"],
            "tool_name": "test_tool",
            "tool_input": {"param": "value"},
            "tool_output": "Тестовий результат",
            "final_response": "Фінальна відповідь"
        })
        print(f"Debug tool result: {debug_result}")
        
        # Тест math notebook tool
        math_result = create_math_notebook.invoke({
            "problem_statement": "Тестова задача",
            "solution_steps": "Крок 1: ...\nКрок 2: ...",
            "final_answer": "42"
        })
        print(f"Math tool result: {math_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні PDF інструментів: {e}")
        return False

def test_simple_pdf_tools():
    """Тестує спрощені PDF інструменти агента."""
    print("🧪 Тестування спрощених PDF інструментів агента...")
    
    try:
        from src.agent.tools.pdf_tools import create_simple_math_notebook, create_simple_debug_report
        
        # Тест simple math notebook tool
        math_result = create_simple_math_notebook.invoke({
            "problem_and_solution": "Знайти площу круга з радіусом 5 см\nS = π × r²\nS = π × 25 = 78.54 см²"
        })
        print(f"Simple math tool result: {math_result}")
        
        # Тест simple debug report tool
        debug_result = create_simple_debug_report.invoke({
            "query_and_result": "Користувач запитав: 2+2*3\nРезультат: 8"
        })
        print(f"Simple debug tool result: {debug_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні спрощених PDF інструментів: {e}")
        return False

def main():
    """Головна функція тестування."""
    print("🚀 Запуск тестів PDF генерації...")
    
    # Перевіряємо, чи встановлено Typst
    import subprocess
    try:
        result = subprocess.run(["typst", "--version"], capture_output=True, text=True)
        print(f"✅ Typst знайдено: {result.stdout.strip()}")
    except FileNotFoundError:
        print("⚠️  Typst не знайдено. Встановіть його для роботи PDF генерації:")
        print("   https://github.com/typst/typst/releases")
        print("   Або через package manager:")
        print("   - Windows: winget install --id Typst.Typst")
        print("   - macOS: brew install typst")
        print("   - Linux: cargo install --git https://github.com/typst/typst --locked typst-cli")
        return
    
    tests_passed = 0
    total_tests = 4
    
    # Тест 1: Debug PDF
    if test_debug_pdf():
        tests_passed += 1
    
    # Тест 2: Math Notebook PDF
    if test_math_notebook_pdf():
        tests_passed += 1
    
    # Тест 3: PDF Tools
    if test_pdf_tools():
        tests_passed += 1
    
    # Тест 4: Simple PDF Tools
    if test_simple_pdf_tools():
        tests_passed += 1
    
    print(f"\n📊 Результати тестування: {tests_passed}/{total_tests} тестів пройдено")
    
    if tests_passed == total_tests:
        print("🎉 Всі тести пройшли успішно!")
    else:
        print("⚠️  Деякі тести не пройшли. Перевірте логи для деталей.")

if __name__ == "__main__":
    main() 