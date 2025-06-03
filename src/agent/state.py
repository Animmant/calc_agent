# src/agent/state.py
from typing import List, TypedDict, Annotated, Sequence, Optional, Dict, Any # Додано Optional, Dict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Стан агента. Зберігає історію повідомлень та проміжні результати.
    """
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]
    # Можливі майбутні доповнення для команд:
    # last_successful_tool_output: Optional[str] = None
    # last_interaction_trace: Optional[List[Dict[str, Any]]] = None # Для детального дебагу