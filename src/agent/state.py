from typing import List, TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
# Якщо ви будете використовувати Pydantic для більш строгої валідації стану:
# from pydantic import BaseModel, Field

# Для простоти почнемо з TypedDict
class AgentState(TypedDict):
    """
    Стан агента. Зберігає історію повідомлень та проміжні результати.
    """
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]  # Дозволяє додавати повідомлення
    # Тут можна додавати інші поля стану, наприклад:
    # last_tool_result: dict | None
    # current_task_description: str | None 