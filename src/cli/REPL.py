import logging
import uuid  # Для генерації унікальних ID потоків для LangGraph

from src.agent.agent_executor import create_llm, create_agent_executor
from src.agent.tools.calculator import calculator_tools  # Імпортуємо наші інструменти

logger = logging.getLogger(__name__)

def run_chat_loop():
    """Запускає консольний цикл чату з агентом."""
    try:
        llm = create_llm()
        tools = calculator_tools  # Поки що лише калькулятор
        agent_executor = create_agent_executor(llm, tools)

        # Генеруємо унікальний ID для сесії (thread_id для LangGraph)
        # Це важливо для того, щоб агент пам'ятав контекст розмови в межах однієї сесії.
        # Для кожного нового запуску REPL буде нова сесія.
        session_id = uuid.uuid4().hex 
        config = {"configurable": {"thread_id": session_id}}

        logger.info(f"🤖 Агент готовий до спілкування! Починайте діалог. (Session ID: {session_id})")
        logger.info("Введіть 'exit' або 'quit' для завершення.")

        # Початкове системне повідомлення (можна зробити його більш детальним)
        # Для create_react_agent системний промпт формується переважно ним самим,
        # але ми можемо спробувати "направити" його початковим запитом.
        # initial_messages = [("system", "You are a helpful assistant that can use a calculator.")]
        # current_state = agent_executor.invoke({"messages": initial_messages}, config=config)
        # if current_state and 'messages' in current_state and current_state['messages']:
        #     logger.info(f"Агент: {current_state['messages'][-1].content}")
        
        print("\n🤖 Агент: Привіт! Я готовий допомогти з математичними обчисленнями. Чим можу бути корисним?")
        print("💡 Приклади: 'скільки буде 2+2*3?', 'як знайти площу круга?', '15% від 200'")

        while True:
            try:
                user_input = input("\n👤 Ви: ").strip()
                if user_input.lower() in ["exit", "quit", "вихід", "q"]:
                    logger.info("👋 Завершення сесії користувачем.")
                    break
                if not user_input:
                    continue

                # В LangGraph ReAct агент очікує список повідомлень
                # Формуємо вхід для агента
                payload = {"messages": [("user", user_input)]}
                
                # Викликаємо агента
                # `stream` або `invoke` залежно від бажаної поведінки
                # Для простого REPL `invoke` може бути достатньо.
                # Для поступового виводу відповіді краще `stream`.
                
                logger.info(f"Відправка запиту агенту: {user_input}")
                
                # Використовуємо invoke для простішої обробки
                try:
                    response = agent_executor.invoke(payload, config=config)
                    
                    # Отримуємо останнє повідомлення від агента
                    if response and 'messages' in response and response['messages']:
                        ai_message = response['messages'][-1]
                        if hasattr(ai_message, 'content') and ai_message.content:
                            print(f"🤖 Агент: {ai_message.content}")
                        else:
                            print("🤖 Агент: Отримано відповідь без текстового контенту.")
                    else:
                        print("🤖 Агент: Не вдалося отримати відповідь.")
                        
                except Exception as invoke_error:
                    logger.error(f"Помилка при виклику агента: {invoke_error}", exc_info=True)
                    print(f"❌ Помилка: {invoke_error}")
                    print("💡 Спробуйте переформулювати запит або перезапустити програму.")

            except KeyboardInterrupt:
                logger.info("\n👋 Завершення сесії через Ctrl+C.")
                break
            except Exception as e:
                logger.error(f"Сталася помилка в циклі REPL: {e}", exc_info=True)
                print(f"❌ Виникла помилка: {e}")
                print("💡 Спробуйте ще раз або перезапустіть ('exit').")
                
    except Exception as setup_error:
        logger.error(f"Помилка при ініціалізації агента: {setup_error}", exc_info=True)
        print(f"❌ Не вдалося запустити агента: {setup_error}")
        print("💡 Перевірте налаштування API ключа в файлі .env")

def run_chat_loop_with_streaming():
    """Альтернативна версія з потоковим виводом (експериментальна)"""
    try:
        llm = create_llm()
        tools = calculator_tools
        agent_executor = create_agent_executor(llm, tools)

        session_id = uuid.uuid4().hex 
        config = {"configurable": {"thread_id": session_id}}

        print("\n🤖 Агент: Привіт! Я готовий допомогти з математичними обчисленнями (потоковий режим).")
        print("💡 Приклади: 'скільки буде 2+2*3?', 'як знайти площу круга?'")

        while True:
            try:
                user_input = input("\n👤 Ви: ").strip()
                if user_input.lower() in ["exit", "quit", "вихід", "q"]:
                    break
                if not user_input:
                    continue

                payload = {"messages": [("user", user_input)]}
                
                print("🤖 Агент: ", end="", flush=True)
                
                # Використовуємо stream для поступового виводу
                response_stream = agent_executor.stream(payload, config=config)
                
                full_response_content = ""
                for chunk in response_stream:
                    # Обробляємо чанки від LangGraph
                    messages = chunk.get("messages")
                    if messages:
                        ai_message = messages[-1]
                        if hasattr(ai_message, 'content') and ai_message.content:
                            # Для ReAct агента зазвичай отримуємо повні повідомлення
                            # а не токен-за-токеном стрімінг
                            full_response_content = ai_message.content

                if full_response_content:
                    print(full_response_content)
                else:
                    print("Отримано відповідь без текстового контенту.")

            except KeyboardInterrupt:
                print("\n👋 Завершення сесії.")
                break
            except Exception as e:
                logger.error(f"Помилка в потоковому режимі: {e}", exc_info=True)
                print(f"\n❌ Помилка: {e}")

    except Exception as setup_error:
        logger.error(f"Помилка при ініціалізації: {setup_error}", exc_info=True)
        print(f"❌ Не вдалося запустити агента: {setup_error}")

if __name__ == "__main__":
    # Можна запустити REPL напряму
    run_chat_loop() 