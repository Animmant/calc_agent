import logging
from typing import Sequence

from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import LanguageModelLike
from langchain_google_genai import ChatGoogleGenerativeAI  # Використовуємо Gemini
from langgraph.checkpoint.memory import InMemorySaver  # Для збереження стану в пам'яті
from langgraph.prebuilt import create_react_agent  # Готовий ReAct агент
# Або якщо ви хочете більше контролю, можна створити кастомний граф:
# from langgraph.graph import StateGraph, END

from src.config import settings  # Наші налаштування
from src.agent.state import AgentState  # Визначення стану

logger = logging.getLogger(__name__)

def create_llm() -> LanguageModelLike:
    """Створює та повертає екземпляр LLM."""
    logger.info(f"Ініціалізація LLM: {settings.GEMINI_MODEL_NAME} з температурою {settings.DEFAULT_TEMPERATURE}")
    
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY не знайдено в змінних середовища. Перевірте файл .env")
    
    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        temperature=settings.DEFAULT_TEMPERATURE,
        google_api_key=settings.GOOGLE_API_KEY,
        convert_system_message_to_human=True  # Для сумісності деяких моделей Gemini
    )
    return llm

def create_agent_executor(llm: LanguageModelLike, tools: Sequence[BaseTool]):
    """
    Створює та повертає виконавця агента (LangGraph).
    Використовує попередньо створений ReAct агент для простоти.
    """
    logger.info(f"Створення виконавця агента з {len(tools)} інструментами.")

    # Для ReAct агента часто потрібен системний промпт, що пояснює як використовувати інструменти.
    # LangGraph prebuilt `create_react_agent` може мати свій внутрішній промпт,
    # але можна спробувати його кастомізувати, якщо це підтримується.
    # Або, якщо створювати граф вручну, промпт задається явно.

    # Використовуємо create_react_agent для швидкого старту
    # Він використовує LangChain Expression Language (LCEL) під капотом.
    # `checkpointer` потрібен для збереження стану між викликами (для історії діалогу).
    memory_saver = InMemorySaver()
    
    # Створюємо системний промпт для кращої поведінки агента
    system_message = """Ти корисний асистент-математик, який може виконувати обчислення та розв'язувати математичні задачі.

Доступні інструменти:
- basic_calculator: для простих арифметичних операцій (+, -, *, /, **)
- advanced_math_solver: для складніших математичних задач

Правила:
1. Завжди використовуй інструменти для обчислень, навіть для простих прикладів
2. Пояснюй кроки розв'язання
3. Перевіряй результати на розумність
4. Відповідай українською мовою
5. Будь точним та зрозумілим

Приклади використання:
- "Скільки буде 2+2?" → використай basic_calculator("2+2")
- "Як знайти площу круга?" → використай advanced_math_solver("площа круга")"""
    
    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory_saver,
        # Додаємо системне повідомлення через messages_modifier
        messages_modifier=system_message
    )
    logger.info("✅ Виконавець ReAct агента створений.")
    return agent_executor

# Приклад, як можна було б створити кастомний граф (закоментовано, для майбутнього)
# def _should_continue(state: AgentState) -> str:
#     # Логіка, чи продовжувати роботу, чи завершувати
#     # ...
#     if not state['messages'] or state['messages'][-1].type == "ai_tool_call": # Приклад умови
#         return "continue" # Викликати інструмент
#     return "end" # Завершити

# def _call_model(state: AgentState, config): # config передається LangGraph
#     # Логіка виклику LLM
#     # ...
#     # response = llm.invoke(state['messages'], config=config)
#     # return {"messages": [response]}
#     pass

# def _call_tool(state: AgentState, config):
#     # Логіка виклику інструменту
#     # ...
#     pass

# def create_custom_agent_executor(llm: LanguageModelLike, tools: Sequence[BaseTool]):
#     workflow = StateGraph(AgentState)
#     workflow.add_node("agent", _call_model)
#     workflow.add_node("action", _call_tool)
#     workflow.set_entry_point("agent")
#     workflow.add_conditional_edges(
#         "agent",
#         _should_continue,
#         {
#             "continue": "action",
#             "end": END,
#         },
#     )
#     workflow.add_edge("action", "agent")
#     app = workflow.compile(checkpointer=InMemorySaver())
#     return app 