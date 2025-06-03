"""
Інструменти для генерації PDF звітів та документів.
"""

import logging
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool

from src.reporting.pdf_generator import (
    generate_debug_pdf, 
    generate_math_notebook_pdf, 
    get_available_engines
)

logger = logging.getLogger(__name__)


@tool
def create_debug_report(
    original_user_query: str,
    reasoning_steps: List[str],
    tool_name: str,
    tool_input: Dict[str, Any],
    tool_output: str,
    final_response: str,
    llm_model: str = "gemini-1.5-flash"
) -> str:
    """
    Створює PDF звіт для дебагу роботи агента.
    
    Args:
        original_user_query: Оригінальний запит користувача
        reasoning_steps: Список кроків міркування агента
        tool_name: Назва використаного інструмента
        tool_input: Вхідні параметри інструмента
        tool_output: Результат роботи інструмента
        final_response: Фінальна відповідь агента
        llm_model: Модель LLM, що використовувалася
    
    Returns:
        Шлях до створеного PDF файлу або повідомлення про помилку
    """
    try:
        debug_data = {
            "original_user_query": original_user_query,
            "llm_reasoning_steps": reasoning_steps,
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "final_agent_response": final_response,
            "resources": {
                "llm_model": llm_model
            }
        }
        
        pdf_path = generate_debug_pdf(debug_data)
        
        if pdf_path:
            return f"✅ PDF звіт дебагу створено: {pdf_path}"
        else:
            return "❌ Не вдалося створити PDF звіт дебагу. Перевірте логи для деталей."
            
    except Exception as e:
        logger.error(f"Помилка при створенні debug PDF: {e}", exc_info=True)
        return f"❌ Помилка при створенні PDF звіту: {str(e)}"


@tool
def create_math_notebook(
    problem_statement: str,
    solution_steps: str,
    final_answer: Optional[str] = None
) -> str:
    """
    Створює PDF математичний зошит з розв'язком задачі.
    
    Args:
        problem_statement: Формулювання математичної задачі
        solution_steps: Покрокове розв'язання (може містити LaTeX)
        final_answer: Фінальна відповідь (опціонально)
    
    Returns:
        Шлях до створеного PDF файлу або повідомлення про помилку
    """
    try:
        # Формуємо LaTeX контент для розв'язку
        latex_content = solution_steps
        
        if final_answer:
            latex_content += f"\n\n\\textbf{{Відповідь:}} {final_answer}"
        
        pdf_path = generate_math_notebook_pdf(problem_statement, latex_content)
        
        if pdf_path:
            return f"✅ PDF математичного зошита створено: {pdf_path}"
        else:
            return "❌ Не вдалося створити PDF математичного зошита. Перевірте логи для деталей."
            
    except Exception as e:
        logger.error(f"Помилка при створенні math notebook PDF: {e}", exc_info=True)
        return f"❌ Помилка при створенні PDF зошита: {str(e)}"


@tool
def create_simple_math_notebook(problem_and_solution: str) -> str:
    """
    Створює простий PDF математичний зошит з задачею та розв'язком.
    
    Args:
        problem_and_solution: Текст з формулюванням задачі та її розв'язком
    
    Returns:
        Шлях до створеного PDF файлу або повідомлення про помилку
    """
    try:
        # Розділяємо на задачу та розв'язок (простий підхід)
        lines = problem_and_solution.split('\n')
        problem_statement = lines[0] if lines else "Математична задача"
        solution_steps = '\n'.join(lines[1:]) if len(lines) > 1 else problem_and_solution
        
        pdf_path = generate_math_notebook_pdf(problem_statement, solution_steps)
        
        if pdf_path:
            return f"✅ PDF математичного зошита створено: {pdf_path}"
        else:
            return "❌ Не вдалося створити PDF математичного зошита. Перевірте логи для деталей."
            
    except Exception as e:
        logger.error(f"Помилка при створенні simple math notebook PDF: {e}", exc_info=True)
        return f"❌ Помилка при створенні PDF зошита: {str(e)}"


@tool
def create_simple_debug_report(query_and_result: str) -> str:
    """
    Створює простий PDF звіт з запитом та результатом.
    
    Args:
        query_and_result: Текст з запитом користувача та результатом роботи
    
    Returns:
        Шлях до створеного PDF файлу або повідомлення про помилку
    """
    try:
        debug_data = {
            "original_user_query": query_and_result,
            "llm_reasoning_steps": ["Обробка запиту", "Генерація відповіді"],
            "tool_name": "general_processing",
            "tool_input": {"query": query_and_result},
            "tool_output": "Результат обробки",
            "final_agent_response": query_and_result,
            "resources": {
                "llm_model": "gemini-1.5-flash"
            }
        }
        
        pdf_path = generate_debug_pdf(debug_data)
        
        if pdf_path:
            return f"✅ PDF звіт створено: {pdf_path}"
        else:
            return "❌ Не вдалося створити PDF звіт. Перевірте логи для деталей."
            
    except Exception as e:
        logger.error(f"Помилка при створенні simple debug PDF: {e}", exc_info=True)
        return f"❌ Помилка при створенні PDF звіту: {str(e)}"


@tool
def check_pdf_engines() -> str:
    """
    Перевіряє доступність PDF движків для генерації документів.
    
    Returns:
        Статус доступних движків
    """
    try:
        engines = get_available_engines()
        available = [name.upper() for name, status in engines.items() if status]
        unavailable = [name.upper() for name, status in engines.items() if not status]
        
        result = "🔧 Статус PDF движків:\n"
        
        if available:
            result += f"✅ Доступні: {', '.join(available)}\n"
        
        if unavailable:
            result += f"❌ Недоступні: {', '.join(unavailable)}\n"
        
        if not available:
            result += "\n💡 Для генерації PDF встановіть:\n"
            result += "• LaTeX: https://www.latex-project.org/get/\n"
            result += "• Typst: https://github.com/typst/typst/releases"
        
        return result
        
    except Exception as e:
        logger.error(f"Помилка при перевірці PDF движків: {e}", exc_info=True)
        return f"❌ Помилка при перевірці движків: {str(e)}"


@tool
def create_enhanced_math_notebook(
    problem_statement: str,
    solution_steps: str,
    include_graphs: bool = False,
    include_verification: bool = False
) -> str:
    """
    Створює розширений PDF математичний зошит з додатковими функціями.
    
    Args:
        problem_statement: Формулювання математичної задачі
        solution_steps: Покрокове розв'язання (LaTeX формат)
        include_graphs: Чи включати графіки (якщо доречно)
        include_verification: Чи включати перевірку розв'язку
    
    Returns:
        Шлях до створеного PDF файлу або повідомлення про помилку
    """
    try:
        # Розширюємо LaTeX контент додатковими секціями
        enhanced_content = solution_steps
        
        if include_verification:
            enhanced_content += "\n\n\\section*{Перевірка розв'язку}\n"
            enhanced_content += "Підставимо отримані значення у вихідне рівняння для перевірки правильності розв'язку."
        
        if include_graphs:
            enhanced_content += "\n\n\\section*{Графічна інтерпретація}\n"
            enhanced_content += "\\begin{center}\n\\textit{Тут може бути розміщено графік функції}\n\\end{center}"
        
        pdf_path = generate_math_notebook_pdf(problem_statement, enhanced_content)
        
        if pdf_path:
            return f"✅ Розширений PDF математичного зошита створено: {pdf_path}"
        else:
            return "❌ Не вдалося створити розширений PDF зошит. Перевірте логи для деталей."
            
    except Exception as e:
        logger.error(f"Помилка при створенні enhanced math notebook PDF: {e}", exc_info=True)
        return f"❌ Помилка при створенні розширеного PDF зошита: {str(e)}"


# Список всіх PDF інструментів для експорту
pdf_tools = [
    create_simple_math_notebook,  # Спрощені версії спочатку
    create_simple_debug_report,
    create_math_notebook,
    create_debug_report,
    check_pdf_engines,
    create_enhanced_math_notebook
] 