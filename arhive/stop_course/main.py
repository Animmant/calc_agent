from dataclasses import dataclass, asdict
import json
import os
import sys
import subprocess
from typing import Sequence
import uuid
from typing import NoReturn, Optional, Sequence

from dotenv import find_dotenv, load_dotenv
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool
from langchain_core.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI
import google.api_core.exceptions as google_exceptions

# --- Конфігурація ---

GOOGLE_MODEL_NAME = "gemini-1.5-flash-latest" # Оновіть, якщо "gemini-2.0-flash" ще немає
OPENAI_MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0
DEFAULT_PROMPT = "Explain what chain of thought is in one sentence."

def _exit_with_error(message: str, error: Optional[Exception] = None) -> NoReturn:
    """Друкує повідомлення про помилку та завершує програму."""
    if error:
        print(f"❌ Error: {message} Details: {error}")
    else:
        print(f"❌ Error: {message}")
    sys.exit(1)

def setup_environment():
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Перевірка наявності ключів
    if not openai_api_key:
        _exit_with_error(
            "OPENAI_API_KEY не встановлено в змінних середовища.\n"
            "💡 Будь ласка, встановіть OPENAI_API_KEY у вашому .env файлі."
        )
    if not google_api_key:
        _exit_with_error(
            "GOOGLE_API_KEY не встановлено в змінних середовища.\n"
            "💡 Будь ласка, встановіть GOOGLE_API_KEY у вашому .env файлі."
        )
    
    print("✅ API_KEY успішно завантажено з .env")

def create_prompts():
    prompt_template = ChatPromptTemplate.from_template(
        "I want to create a new {food_type} for restaurant with {cuisine} for {restaurant_name}. Suggest one concise and appealing name for this food item."
    )
    return prompt_template

def initialize_llm():
    try:
        model_gemi = ChatGoogleGenerativeAI(
            model=GOOGLE_MODEL_NAME,
            temperature=TEMPERATURE
        )
        return model_gemi
    except google_exceptions.InvalidArgument as e:
        _exit_with_error(
            f"Помилка при ініціалізації Google LLM: {e}",e)

def main():
    try:
        setup_environment()
        prompt_template = create_prompts()
        model_gemi = initialize_llm()
        
        response = model_gemi.invoke(DEFAULT_PROMPT)
        print(response.content)

        formatted_prompt = prompt_template.format(
            food_type="Italian pizza", 
            cuisine="Mediterranean",
            restaurant_name="Italian Restaurant"
        )
        restaurant_response = model_gemi.invoke(formatted_prompt)

        print("Ресторан:", "Italian Restaurant")
        print("Назва страви:", restaurant_response.content)
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()