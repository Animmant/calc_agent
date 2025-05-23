import os
import sys # Додано для sys.exit
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import google.api_core.exceptions as google_exceptions
import openai # Для перехоплення специфічних помилок OpenAI

# --- Конфігурація ---
MODEL_NAME = "gemini-2.0-flash"
TEMPERATURE = 0
DEFAULT_PROMPT = "Hello! Explain what LangChain is in one sentence."

def setup_environment():
    """
    Завантажує змінні середовища з .env файлу та перевіряє наявність GOOGLE_API_KEY.
    Повертає True, якщо ключ знайдено, інакше False.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY не знайдено!")
        print("Будь ласка, переконайтеся, що у вас є файл .env у поточному каталозі (або в корені проєкту)")
        print("і він містить рядок типу: GOOGLE_API_KEY=\"ВАШ_API_КЛЮЧ_ТУТ\"")
        print("Також переконайтеся, що бібліотека python-dotenv встановлена (`pip install python-dotenv`).")
        return False
    print("✅ GOOGLE_API_KEY знайдено в середовищі (ймовірно, завантажено з .env).")
    return True

def initialize_llm():
    """
    Ініціалізує та повертає екземпляр ChatOpenAI LLM.
    Очікує, що GOOGLE_API_KEY вже встановлено в середовищі.
    """
    print("🤖 Створюю LangChain LLM...")
    try:
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE
            # Ключ API буде автоматично підхоплено з змінних середовища
        )
        return llm
    except Exception as e: # Загальна помилка при ініціалізації, якщо щось піде не так
        print(f"❌ Помилка під час ініціалізації LLM: {e}")
        return None

def run_chat_interaction(llm, prompt_content):
    """
    Виконує тестовий запит до LLM та друкує відповідь.
    """
    print("💬 Тестую LangChain Chat...")
    messages = [HumanMessage(content=prompt_content)]
    response = llm.invoke(messages)
    
    print("\n✅ LangChain Chat відповідь:")
    print(response.content)
    print("\n🎉 LangChain успішно працює!")

def main():
    """
    Головна функція для запуску скрипта.
    """
    if not setup_environment():
        sys.exit(1)

    llm = initialize_llm()
    if not llm:
        sys.exit(1)

    try:
        run_chat_interaction(llm, DEFAULT_PROMPT)
    # 🔽 Обробка специфічних помилок Google API
    except google_exceptions.PermissionDenied as e:
        print("\n❌ Помилка доступу до Google API (PermissionDenied).")
        print(f"   Деталі: {e}")
        print("\n💡 Проблема з API ключем або налаштуваннями проекту Google Cloud:")
        print("1. Перевірте правильність вашого GOOGLE_API_KEY у файлі .env.")
        print("2. Переконайтеся, що Generative Language API (або Vertex AI API, залежно від вашого ключа) увімкнено у вашому проекті Google Cloud.")
        print("3. Ваш ключ може не мати дозволів на використання вказаної моделі або сервісу.")
        print("4. Перевірте налаштування білінгу для проекту Google Cloud.")
    except google_exceptions.ResourceExhausted as e:
        print("\n❌ Вичерпано квоту Google API (ResourceExhausted).")
        print(f"   Деталі: {e}")
        print("\n💡 Проблема з квотами:")
        print("1. Перевірте ваші квоти для Generative Language API у Google Cloud Console.")
        print("2. Ви могли досягти безкоштовного ліміту або денного ліміту запитів.")
        print("3. Розгляньте можливість запиту на збільшення квоти або оптимізуйте кількість запитів.")
    except google_exceptions.InvalidArgument as e:
        print("\n❌ Неправильний аргумент для Google API (InvalidArgument).")
        print(f"   Деталі: {e}")
        print("\n💡 Можливі причини:")
        print(f"1. Назва моделі '{MODEL_NAME}' може бути неправильною або недоступною для вашого ключа.")
        print("2. Перевірте інші параметри, що передаються до моделі.")
    except Exception as e:
        error_str = str(e)
        print(f"\n❌ Неочікувана помилка під час взаємодії з Gemini: {error_str}")
        print("\n💡 Загальні рекомендації:")
        print("1. Перевірте інтернет-з'єднання.")
        print("2. Переконайтеся, що встановлені необхідні бібліотеки: `pip install langchain-google-genai python-dotenv`.")

if __name__ == "__main__":
    main()