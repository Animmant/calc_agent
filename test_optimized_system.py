#!/usr/bin/env python3
"""
Тестовий файл для перевірки оптимізованої системи Calculator Agent.
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

def test_prompts():
    """Тестує промпти агента."""
    print("🧪 Тестування промптів...")
    
    try:
        from src.agent.prompts import (
            MATH_NOTEBOOK_LATEX_PROMPT_TEMPLATE,
            DEBUG_REPORT_PROMPT_TEMPLATE,
            SYSTEM_PROMPT
        )
        
        # Перевіряємо, що промпти містять необхідні плейсхолдери
        assert "{problem_statement}" in MATH_NOTEBOOK_LATEX_PROMPT_TEMPLATE
        assert "{raw_solution_content}" in MATH_NOTEBOOK_LATEX_PROMPT_TEMPLATE
        assert "{original_query}" in DEBUG_REPORT_PROMPT_TEMPLATE
        
        print("✅ Промпти завантажено успішно")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні промптів: {e}")
        return False

def test_pdf_engines():
    """Тестує доступність PDF движків."""
    print("🧪 Тестування PDF движків...")
    
    try:
        from src.reporting.pdf_generator import get_available_engines
        
        engines = get_available_engines()
        print(f"📊 Статус движків: {engines}")
        
        available_count = sum(engines.values())
        if available_count > 0:
            print(f"✅ Доступно {available_count} движків з {len(engines)}")
        else:
            print("⚠️  Жоден PDF движок недоступний")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні движків: {e}")
        return False

def test_latex_template():
    """Тестує LaTeX шаблон."""
    print("🧪 Тестування LaTeX шаблону...")
    
    try:
        template_path = "templates/latex/math_notebook_template.tex"
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Перевіряємо наявність плейсхолдера
            if "{LATEX_CONTENT}" in content:
                print("✅ LaTeX шаблон містить правильний плейсхолдер")
            else:
                print("⚠️  LaTeX шаблон не містить плейсхолдера {LATEX_CONTENT}")
            
            # Перевіряємо основні пакети
            required_packages = ["amsmath", "tikz", "pgfplots", "ukrainian"]
            missing_packages = []
            
            for package in required_packages:
                if package not in content:
                    missing_packages.append(package)
            
            if missing_packages:
                print(f"⚠️  Відсутні пакети: {missing_packages}")
            else:
                print("✅ Всі необхідні пакети присутні")
            
            return True
        else:
            print(f"❌ LaTeX шаблон не знайдено: {template_path}")
            return False
            
    except Exception as e:
        print(f"❌ Помилка при тестуванні LaTeX шаблону: {e}")
        return False

def test_pdf_tools():
    """Тестує PDF інструменти."""
    print("🧪 Тестування PDF інструментів...")
    
    try:
        from src.agent.tools.pdf_tools import pdf_tools
        
        print(f"📊 Знайдено {len(pdf_tools)} PDF інструментів:")
        for tool in pdf_tools:
            print(f"   • {tool.name}: {tool.description[:50]}...")
        
        # Тестуємо інструмент перевірки движків
        from src.agent.tools.pdf_tools import check_pdf_engines
        
        result = check_pdf_engines.invoke({})
        print(f"🔧 Результат перевірки движків:\n{result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні PDF інструментів: {e}")
        return False

def test_cli_structure():
    """Тестує структуру CLI."""
    print("🧪 Тестування структури CLI...")
    
    try:
        from src.cli.REPL import CalculatorREPL, LastInteractionData
        
        # Створюємо екземпляр REPL
        repl = CalculatorREPL()
        
        # Перевіряємо структуру даних
        interaction = LastInteractionData()
        assert hasattr(interaction, 'original_user_query')
        assert hasattr(interaction, 'final_agent_response')
        assert hasattr(interaction, 'tool_invocations')
        assert hasattr(interaction, 'reasoning_steps')
        
        print("✅ Структура CLI правильна")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні CLI: {e}")
        return False

def test_agent_initialization():
    """Тестує ініціалізацію агента."""
    print("🧪 Тестування ініціалізації агента...")
    
    try:
        from src.agent.agent_executor import create_llm, create_agent_executor
        from src.agent.tools.calculator import calculator_tools
        from src.agent.tools.pdf_tools import pdf_tools
        
        # Перевіряємо наявність інструментів
        all_tools = calculator_tools + pdf_tools
        print(f"📊 Загальна кількість інструментів: {len(all_tools)}")
        
        # Спробуємо створити LLM (може не вдатися без API ключа)
        try:
            llm = create_llm()
            print("✅ LLM створено успішно")
            
            # Спробуємо створити агента
            agent_executor = create_agent_executor(llm, all_tools)
            print("✅ Агент створено успішно")
            
        except Exception as llm_error:
            print(f"⚠️  Не вдалося створити LLM/агента (можливо, відсутній API ключ): {llm_error}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка при тестуванні ініціалізації: {e}")
        return False

def test_directory_structure():
    """Тестує структуру директорій."""
    print("🧪 Тестування структури директорій...")
    
    required_dirs = [
        "src/agent",
        "src/agent/tools",
        "src/cli",
        "src/reporting",
        "templates/typst",
        "templates/latex",
        "output_pdfs"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"⚠️  Відсутні директорії: {missing_dirs}")
        return False
    else:
        print("✅ Всі необхідні директорії присутні")
        return True

def main():
    """Головна функція тестування."""
    print("🚀 Запуск тестів оптимізованої системи Calculator Agent...")
    print("=" * 60)
    
    tests = [
        ("Структура директорій", test_directory_structure),
        ("Промпти", test_prompts),
        ("PDF движки", test_pdf_engines),
        ("LaTeX шаблон", test_latex_template),
        ("PDF інструменти", test_pdf_tools),
        ("CLI структура", test_cli_structure),
        ("Ініціалізація агента", test_agent_initialization),
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
    
    print("\n" + "=" * 60)
    print(f"📊 Результати тестування: {passed}/{total} тестів пройдено")
    
    if passed == total:
        print("🎉 Всі тести пройшли успішно! Система готова до роботи.")
    elif passed >= total * 0.7:
        print("✅ Більшість тестів пройшла. Система працездатна з деякими обмеженнями.")
    else:
        print("⚠️  Багато тестів не пройшли. Потрібне додаткове налаштування.")
    
    print("\n💡 Для запуску системи використовуйте: python main.py")

if __name__ == "__main__":
    main() 