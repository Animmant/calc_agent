import os
import sys # Додано для sys.exit
from typing import NoReturn, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import google.api_core.exceptions as google_exceptions
from langchain.prompts import ChatPromptTemplate

# --- Конфігурація ---
GOOGLE_MODEL_NAME = "gemini-1.5-flash-latest" # Оновіть, якщо "gemini-2.0-flash" ще немає
OPENAI_MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0
DEFAULT_PROMPT = "Hello! Explain what LangChain is in one sentence."

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
        llm = ChatGoogleGenerativeAI(
            model=GOOGLE_MODEL_NAME,
            temperature=TEMPERATURE
        )
        return llm
    except google_exceptions.InvalidArgument as e:
        _exit_with_error(
            f"Помилка при ініціалізації Google LLM: {e}",e)

def main():
    try:
        setup_environment()
        prompt_template = create_prompts()
        llm = initialize_llm()
        
        response = llm.invoke(DEFAULT_PROMPT)
        print(response.content)

        formatted_prompt = prompt_template.format(
            food_type="Italian pizza", 
            cuisine="Mediterranean",
            restaurant_name="Italian Restaurant"
        )
        restaurant_response = llm.invoke(formatted_prompt)

        print("Ресторан:", "Italian Restaurant")
        print("Назва страви:", restaurant_response.content)
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()