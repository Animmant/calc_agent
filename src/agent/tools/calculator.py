import logging
import re
import ast
import operator
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Безпечні операції для eval
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expression: str) -> float:
    """Безпечне обчислення математичних виразів"""
    try:
        # Парсимо вираз в AST
        node = ast.parse(expression, mode='eval')
        return _eval_node(node.body)
    except Exception as e:
        raise ValueError(f"Неможливо обчислити вираз: {e}")

def _eval_node(node):
    """Рекурсивно обчислює вузли AST"""
    if isinstance(node, ast.Constant):  # Числа
        return node.value
    elif isinstance(node, ast.BinOp):  # Бінарні операції
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Непідтримувана операція: {type(node.op)}")
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):  # Унарні операції
        operand = _eval_node(node.operand)
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Непідтримувана унарна операція: {type(node.op)}")
        return op(operand)
    else:
        raise ValueError(f"Непідтримуваний тип вузла: {type(node)}")

@tool
def basic_calculator(expression: str) -> str:
    """
    Виконує прості арифметичні операції (+, -, *, /, **) над рядком.
    Наприклад: "2 + 2", "10 * 5 / 2 - 3", "2 ** 3".
    Використовує безпечний парсер виразів замість eval().
    """
    logger.info(f"🧮 Інструмент 'basic_calculator' викликано з виразом: '{expression}'")
    
    # Очищуємо вираз від зайвих пробілів
    expression = expression.strip()
    
    # Перевіряємо на дозволені символи
    allowed_pattern = r'^[0-9+\-*/().\s**]+$'
    if not re.match(allowed_pattern, expression):
        logger.warning(f"Недозволені символи у виразі: '{expression}'")
        return "Помилка: вираз містить недозволені символи. Дозволені: цифри, +, -, *, /, **, (), ."
    
    try:
        result = safe_eval(expression)
        logger.info(f"Результат обчислення '{expression}': {result}")
        
        # Форматуємо результат
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        else:
            return f"{result:.6g}"  # Обмежуємо кількість знаків після коми
            
    except Exception as e:
        logger.error(f"Помилка при обчисленні виразу '{expression}': {e}", exc_info=True)
        return f"Помилка обчислення: {e}"

@tool
def advanced_math_solver(problem_description: str) -> str:
    """
    Розв'язує складніші математичні задачі, описані природною мовою.
    Поки що це заглушка для майбутнього розширення.
    """
    logger.info(f"🛠️ Інструмент 'advanced_math_solver' викликано з описом: '{problem_description}'")
    
    # Простий приклад розпізнавання деяких типів задач
    problem_lower = problem_description.lower()
    
    if "квадрат" in problem_lower and "корінь" in problem_lower:
        return "Для обчислення квадратного кореня використовуйте basic_calculator з виразом типу '25 ** 0.5'"
    elif "відсоток" in problem_lower or "%" in problem_lower:
        return "Для обчислення відсотків використовуйте basic_calculator. Наприклад: '100 * 0.15' для 15% від 100"
    elif "площа" in problem_lower:
        if "круг" in problem_lower:
            return "Площа круга = π * r². Використовуйте basic_calculator з виразом '3.14159 * r * r'"
        elif "прямокутник" in problem_lower:
            return "Площа прямокутника = довжина * ширина. Використовуйте basic_calculator"
    
    # Загальна відповідь
    return ("Функціонал розв'язання складних математичних задач ще розробляється. "
            "Спробуйте переформулювати задачу як математичний вираз для basic_calculator.")

# Збираємо всі інструменти цього модуля
calculator_tools = [basic_calculator, advanced_math_solver] 