# Calculator Agent

A natural language processing agent that understands and processes calculation-related queries using Google's Gemini Pro model.

## Features

- Natural language understanding (NLU) for mathematical queries
- Intent and entity extraction from user input
- чітко представляти результати через інтерфейс чату. Можливість командами давати указки що міняти.
- **Взаємодія з Користувачем:** Вести уточнюючі діалоги, коли інформація відсутня або неоднозначна, або незнає, Чесністьб понад усе . ЩОб він необманював
- **Прив'язка Параметрів:** Автоматичне вилучення необхідної інформації із запиту користувача або інших джерел для передачі як аргументів обраному інструменту
- **Потенціал для Оркестрації Агентів:** Дизайн, що дозволяє зв'язувати або координувати роботу кількох спеціалізованих агентів для складних робочих процесів

## Getting Started

See [SETUP.md](SETUP.md) for detailed setup instructions.

### Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set your Google API key as an environment variable
3. Run the application: 

## Project Structure

- `src/agent/nlu.py`: Core NLU functionality using Gemini Pro
- `tests/`: Unit tests for the application
- `main.py`: Entry point for the application

## Requirements

- Python 3.8+
- Google API key for Gemini Pro
- Dependencies listed in requirements.txt


.  **`[Система Управління Командами]`**
,й відповіддю функціюєю видасть результат /reslt , задебажить роз'взяання /debug, оформе документ у стилі матиматичного зошита /maths

* **`/result`**: * Відображає основний результат роботи останнього активного інструмента. Якщо результатом є, наприклад, Python-функція (код), згенерована `MathModelSolver`, відобрази цей код. В інших випадках – результат виконання. * 
* 

    * **`/debug`:** Генерує детальний дебаг, що включає:

* Оригінальний запит користувача. 
* Ланцюжок думок LLM (якщо доступно через Langchain, наприклад, проміжні кроки планування агента). 
* Назва обраного інструмента та його вхідні параметри. 
* Проміжні результати, формули, ключову логіку, використану інструментом.
* Кінцевий результат роботи інструмента або повідомлення про помилку.
* Використані ресурси (напр., назва LLM-моделі, версії ключових бібліотек).

    * **`/maths`:** Генерує PDF у стилі "математичного зошита":

        * Чітке формулювання завдання/проблеми.

        * Покроковий опис рішення або аналізу (можливо, згенерований LLM та перевірений кодом).
          
          * Результати, представлені у зрозумілому форматі.