import logging
import uuid  # Для генерації унікальних ID потоків для LangGraph
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from src.agent.agent_executor import create_llm, create_agent_executor
from src.agent.tools.calculator import calculator_tools  # Імпортуємо наші інструменти
from src.agent.tools.pdf_tools import pdf_tools  # Імпортуємо PDF інструменти
from src.agent.prompts import MATH_NOTEBOOK_LATEX_PROMPT_TEMPLATE, DEBUG_REPORT_PROMPT_TEMPLATE
from src.reporting.pdf_generator import generate_math_notebook_pdf, generate_debug_pdf, get_available_engines

logger = logging.getLogger(__name__)


@dataclass
class LastInteractionData:
    """Зберігає дані про останню взаємодію з агентом."""
    original_user_query: Optional[str] = None
    final_agent_response: Optional[str] = None
    tool_invocations: Optional[List[Dict[str, Any]]] = None
    reasoning_steps: Optional[List[str]] = None


class CalculatorREPL:
    """Оптимізований REPL для Calculator Agent."""
    
    def __init__(self):
        self.llm = None
        self.agent_executor = None
        self.session_id = None
        self.config = None
        self.last_interaction = LastInteractionData()
        
    def initialize(self):
        """Ініціалізує агента та налаштування."""
        try:
            self.llm = create_llm()
            # Об'єднуємо всі доступні інструменти
            all_tools = calculator_tools + pdf_tools
            self.agent_executor = create_agent_executor(self.llm, all_tools)

            # Генеруємо унікальний ID для сесії
            self.session_id = uuid.uuid4().hex 
            self.config = {"configurable": {"thread_id": self.session_id}}

            logger.info(f"🤖 Агент готовий до спілкування! (Session ID: {self.session_id})")
            return True
            
        except Exception as e:
            logger.error(f"Помилка при ініціалізації агента: {e}", exc_info=True)
            print(f"❌ Не вдалося запустити агента: {e}")
            print("💡 Перевірте налаштування API ключа в файлі .env")
            return False
    
    def show_welcome_message(self):
        """Показує привітальне повідомлення."""
        engines = get_available_engines()
        available_engines = [name for name, available in engines.items() if available]
        
        print("\n🤖 Calculator Agent готовий до роботи!")
        print("=" * 50)
        print("💡 Приклади запитів:")
        print("   • 'скільки буде 2+2*3?'")
        print("   • 'як знайти площу круга з радіусом 5?'")
        print("   • '15% від 200'")
        print("   • 'розв'яжи рівняння x² - 5x + 6 = 0'")
        print("\n📄 Спеціальні команди:")
        print("   • /maths - створити PDF математичного зошита з останнього розв'язку")
        print("   • /debug - створити PDF звіт дебагу останньої взаємодії")
        print("   • /engines - показати доступні PDF движки")
        print("   • /help - показати цю довідку")
        print("   • /exit або /quit - завершити роботу")
        
        if available_engines:
            print(f"\n🔧 Доступні PDF движки: {', '.join(available_engines)}")
        else:
            print("\n⚠️  PDF движки недоступні. Встановіть LaTeX або Typst для генерації PDF.")
        
        print("=" * 50)
    
    def handle_special_command(self, command: str) -> bool:
        """
        Обробляє спеціальні команди.
        Повертає True, якщо команда була оброблена.
        """
        command = command.lower().strip()
        
        if command in ["/exit", "/quit"]:
            print("👋 До побачення!")
            return True
            
        elif command == "/help":
            self.show_welcome_message()
            return False
            
        elif command == "/engines":
            self.show_engines_status()
            return False
            
        elif command == "/maths":
            self.handle_maths_command()
            return False
            
        elif command == "/debug":
            self.handle_debug_command()
            return False
            
        return False
    
    def show_engines_status(self):
        """Показує статус доступних PDF движків."""
        engines = get_available_engines()
        print("\n🔧 Статус PDF движків:")
        for name, available in engines.items():
            status = "✅ Доступний" if available else "❌ Недоступний"
            print(f"   • {name.upper()}: {status}")
        
        if not any(engines.values()):
            print("\n💡 Для генерації PDF встановіть:")
            print("   • LaTeX: https://www.latex-project.org/get/")
            print("   • Typst: https://github.com/typst/typst/releases")
    
    def handle_maths_command(self):
        """Обробляє команду /maths для створення математичного зошита."""
        logger.info("Обробка команди /maths")

        if not self.last_interaction.original_user_query:
            print("🤷 Немає попереднього запиту для форматування як математичний зошит.")
            return

        # Визначаємо "сирий" розв'язок
        raw_solution_content = None
        if self.last_interaction.tool_invocations:
            # Беремо результат останнього викликаного інструменту
            raw_solution_content = self.last_interaction.tool_invocations[-1].get("tool_output")
        
        if not raw_solution_content and self.last_interaction.final_agent_response:
            raw_solution_content = self.last_interaction.final_agent_response
        
        if not raw_solution_content:
            print("🤷 Не знайдено контенту розв'язку для форматування.")
            return

        problem_statement = self.last_interaction.original_user_query
        
        # Формуємо запит до LLM для генерації тіла LaTeX
        formatting_request_content = MATH_NOTEBOOK_LATEX_PROMPT_TEMPLATE.format(
            problem_statement=problem_statement,
            raw_solution_content=raw_solution_content
        )
        
        print("🧮 Генерую LaTeX розв'язок для математичного зошита...")
        
        try:
            # Використовуємо той самий LLM для форматування
            formatted_latex_response = self.llm.invoke(formatting_request_content)
            solution_latex_body = formatted_latex_response.content

            if not solution_latex_body or not solution_latex_body.strip():
                logger.error("LLM повернула порожнє тіло LaTeX для /maths.")
                print("⚠️ LLM не змогла згенерувати LaTeX розв'язок. Спробуйте інший запит.")
                return

            logger.info(f"LaTeX тіло отримано (довжина: {len(solution_latex_body)}).")

            # Викликаємо генератор PDF
            pdf_path = generate_math_notebook_pdf(problem_statement, solution_latex_body)
            if pdf_path:
                print(f"📚 Математичний зошит згенеровано: {pdf_path}")
            else:
                print(f"⚠️ Не вдалося згенерувати PDF математичного зошита. Див. логи.")

        except Exception as e:
            logger.error(f"Помилка під час форматування або генерації /maths PDF: {e}", exc_info=True)
            print("⚠️ Помилка під час обробки команди /maths.")
    
    def handle_debug_command(self):
        """Обробляє команду /debug для створення звіту дебагу."""
        logger.info("Обробка команди /debug")

        if not self.last_interaction.original_user_query:
            print("🤷 Немає попередньої взаємодії для створення звіту дебагу.")
            return

        # Формуємо дані для звіту дебагу
        debug_data = {
            "original_user_query": self.last_interaction.original_user_query,
            "llm_reasoning_steps": self.last_interaction.reasoning_steps or ["Обробка запиту"],
            "tool_name": "general_processing",
            "tool_input": {"query": self.last_interaction.original_user_query},
            "tool_output": "Результат обробки",
            "final_agent_response": self.last_interaction.final_agent_response or "Відповідь не збережена",
            "resources": {
                "llm_model": "gemini-1.5-flash"
            }
        }

        # Якщо є дані про виклики інструментів, використовуємо їх
        if self.last_interaction.tool_invocations:
            last_tool = self.last_interaction.tool_invocations[-1]
            debug_data.update({
                "tool_name": last_tool.get("tool_name", "unknown"),
                "tool_input": last_tool.get("tool_input", {}),
                "tool_output": last_tool.get("tool_output", "")
            })

        print("🔍 Створюю звіт дебагу...")
        
        try:
            pdf_path = generate_debug_pdf(debug_data)
            if pdf_path:
                print(f"📋 Звіт дебагу створено: {pdf_path}")
            else:
                print("⚠️ Не вдалося створити звіт дебагу. Див. логи.")
                
        except Exception as e:
            logger.error(f"Помилка під час створення debug PDF: {e}", exc_info=True)
            print("⚠️ Помилка під час обробки команди /debug.")
    
    def process_user_input(self, user_input: str):
        """Обробляє введення користувача."""
        # Перевіряємо спеціальні команди
        if user_input.startswith('/'):
            if self.handle_special_command(user_input):
                return False  # Команда завершення
            return True  # Продовжуємо роботу
        
        # Звичайний запит до агента
        payload = {"messages": [("user", user_input)]}
        
        logger.info(f"Відправка запиту агенту: {user_input}")
        
        try:
            response = self.agent_executor.invoke(payload, config=self.config)
            
            # Зберігаємо дані про взаємодію
            self.last_interaction.original_user_query = user_input
            
            # Отримуємо останнє повідомлення від агента
            if response and 'messages' in response and response['messages']:
                ai_message = response['messages'][-1]
                if hasattr(ai_message, 'content') and ai_message.content:
                    self.last_interaction.final_agent_response = ai_message.content
                    print(f"🤖 Агент: {ai_message.content}")
                else:
                    print("🤖 Агент: Отримано відповідь без текстового контенту.")
            else:
                print("🤖 Агент: Не вдалося отримати відповідь.")
                
            # TODO: Додати логіку для збереження tool_invocations та reasoning_steps
            # Це потребує додаткового аналізу структури відповіді LangGraph
                
        except Exception as invoke_error:
            logger.error(f"Помилка при виклику агента: {invoke_error}", exc_info=True)
            print(f"❌ Помилка: {invoke_error}")
            print("💡 Спробуйте переформулювати запит або перезапустити програму.")
        
        return True
    
    def run(self):
        """Запускає основний цикл REPL."""
        if not self.initialize():
            return
        
        self.show_welcome_message()
        
        while True:
            try:
                user_input = input("\n👤 Ви: ").strip()
                if not user_input:
                    continue
                
                if not self.process_user_input(user_input):
                    break  # Команда завершення
                    
            except KeyboardInterrupt:
                print("\n👋 Завершення сесії через Ctrl+C.")
                break
            except Exception as e:
                logger.error(f"Сталася помилка в циклі REPL: {e}", exc_info=True)
                print(f"❌ Виникла помилка: {e}")
                print("💡 Спробуйте ще раз або введіть /exit для завершення.")


def run_chat_loop():
    """Запускає консольний цикл чату з агентом (основна функція)."""
    repl = CalculatorREPL()
    repl.run()


if __name__ == "__main__":
    # Можна запустити REPL напряму
    run_chat_loop() 