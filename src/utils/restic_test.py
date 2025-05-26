from dataclasses import dataclass, asdict
import json
import os
import subprocess
from typing import Sequence
import uuid

from dotenv import find_dotenv, load_dotenv
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
# from mail import fetch_recent_emails  # Ваш кастомний модуль

import sys
from typing import NoReturn, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import google.api_core.exceptions as google_exceptions

# --- Конфігурація ---
GOOGLE_MODEL_NAME = "gemini-1.5-flash-latest"
TEMPERATURE = 0

@dataclass
class RestaurantConfig:
    """Конфігурація для генерації назв ресторанів."""
    food_type: str
    cuisine: str
    restaurant_name: str

def _exit_with_error(message: str, error: Optional[Exception] = None) -> NoReturn:
    """Друкує повідомлення про помилку та завершує програму."""
    if error:
        print(f"❌ Error: {message} Details: {error}")
    else:
        print(f"❌ Error: {message}")
    sys.exit(1)

def setup_environment():
    """Налаштування середовища та завантаження змінних."""
    load_dotenv(find_dotenv())
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        _exit_with_error(
            "GOOGLE_API_KEY не встановлено в змінних середовища.\n"
            "💡 Будь ласка, встановіть GOOGLE_API_KEY у вашому .env файлі."
        )
    
    print("✅ API_KEY успішно завантажено з .env")
    return google_api_key

def initialize_llm(api_key: str) -> LanguageModelLike:
    """Ініціалізація LLM моделі."""
    try:
        model_gemi = ChatGoogleGenerativeAI(
            model=GOOGLE_MODEL_NAME,
            temperature=TEMPERATURE,
            google_api_key=api_key
        )
        print(f"✅ Google LLM ({GOOGLE_MODEL_NAME}) ініціалізовано.")
        return model_gemi
    except google_exceptions.InvalidArgument as e:
        _exit_with_error(f"Помилка при ініціалізації Google LLM: {e}", e)

# --- Tools для агента ---

@tool
def generate_restaurant_name(food_type: str, cuisine: str, restaurant_name: str) -> str:
    """Генерує назву страви для ресторану.
    
    Args:
        food_type: Тип їжі (наприклад, "Italian pizza")
        cuisine: Кухня (наприклад, "Mediterranean") 
        restaurant_name: Назва ресторану
    
    Returns:
        Згенерована назва страви
    """
    # Тут буде ваша логіка генерації
    return f"Артизанська {food_type} у стилі {cuisine} від {restaurant_name}"

@tool
def get_restaurant_info() -> str:
    """Отримує інформацію про ресторан."""
    return "Це італійський ресторан з середземноморською кухнею."

@tool 
def save_menu_item(name: str, description: str) -> str:
    """Зберігає новий пункт меню.
    
    Args:
        name: Назва страви
        description: Опис страви
    
    Returns:
        Статус збереження
    """
    menu_item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "created_at": str(uuid.uuid4())
    }
    
    # Збереження в файл (або базу даних)
    try:
        with open("menu_items.json", "a") as f:
            f.write(json.dumps(menu_item) + "\n")
        return f"✅ Пункт меню '{name}' збережено успішно!"
    except Exception as e:
        return f"❌ Помилка збереження: {e}"

def create_calculator_agent(llm: LanguageModelLike) -> any:
    """Створює ReAct агента з інструментами."""
    
    # Список інструментів для агента
    tools = [
        generate_restaurant_name,
        get_restaurant_info,
        save_menu_item
    ]
    
    # Створення агента з memory
    memory = InMemorySaver()
    
    agent = create_react_agent(
        llm, 
        tools,
        checkpointer=memory
    )
    
    return agent

def main():
    """Головна функція програми."""
    try:
        # Налаштування
        api_key = setup_environment()
        llm = initialize_llm(api_key)
        
        # Створення агента
        agent = create_calculator_agent(llm)
        
        # Конфігурація для запуску
        config = RunnableConfig(
            configurable={"thread_id": str(uuid.uuid4())}
        )
        
        # Тестові запити до агента
        print("\n🤖 Тестуємо Calculator Agent...")
        
        # Запит 1: Генерація назви страви
        restaurant_config = RestaurantConfig(
            food_type="Italian pizza",
            cuisine="Mediterranean", 
            restaurant_name="Italian Restaurant"
        )
        
        query1 = f"Створи назву для {restaurant_config.food_type} в стилі {restaurant_config.cuisine} для ресторану {restaurant_config.restaurant_name}"
        
        response1 = agent.invoke(
            {"messages": [("user", query1)]}, 
            config=config
        )
        
        print("📋 Відповідь агента:")
        print(response1["messages"][-1].content)
        
        # Запит 2: Збереження в меню
        query2 = "Збережи цю страву в меню з описом 'Автентична італійська піца з середземноморськими інгредієнтами'"
        
        response2 = agent.invoke(
            {"messages": [("user", query2)]},
            config=config
        )
        
        print("\n💾 Результат збереження:")
        print(response2["messages"][-1].content)
        
    except KeyboardInterrupt:
        print("\n⚠️ Програма перервана користувачем")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
