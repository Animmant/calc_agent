from dotenv import load_dotenv
import os

load_dotenv() # Завантажує змінні з .env файлу

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY не знайдено! Перевірте ваш .env файл.")
    # Тут можна додати логіку виходу або помилки
else:
    print("✅ OPENAI_API_KEY успішно завантажено з .env")

# Далі ваш код, що використовує api_key або очікує os.environ["OPENAI_API_KEY"]
# Наприклад, для Langchain, після load_dotenv() ключ буде доступний для бібліотеки.