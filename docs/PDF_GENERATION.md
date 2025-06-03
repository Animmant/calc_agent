# PDF Генерація в Calculator Agent

## Огляд

Calculator Agent тепер підтримує генерацію PDF документів для створення звітів дебагу та математичних зошитів. Система використовує [Typst](https://typst.app/) - сучасну альтернативу LaTeX для створення високоякісних PDF документів.

## Встановлення Typst

### Windows
```bash
winget install --id Typst.Typst
```

### macOS
```bash
brew install typst
```

### Linux
```bash
cargo install --git https://github.com/typst/typst --locked typst-cli
```

### Перевірка встановлення
```bash
typst --version
```

## Функціональність

### 1. PDF Звіти Дебагу

Створюють детальні звіти про роботу агента, включаючи:
- Оригінальний запит користувача
- Кроки міркування LLM
- Використані інструменти та їх параметри
- Результати роботи інструментів
- Фінальну відповідь агента

#### Використання через агента:
```
👤 Ви: Створи звіт дебагу для останнього обчислення
🤖 Агент: [використає create_debug_report tool]
```

#### Програмне використання:
```python
from src.reporting.pdf_generator import generate_debug_pdf

debug_data = {
    "original_user_query": "Скільки буде 2 + 2 * 3?",
    "llm_reasoning_steps": ["Крок 1", "Крок 2"],
    "tool_name": "calculator",
    "tool_input": {"expression": "2 + 2 * 3"},
    "tool_output": "8",
    "final_agent_response": "Результат: 8",
    "resources": {"llm_model": "gemini-1.5-flash"}
}

pdf_path = generate_debug_pdf(debug_data)
```

### 2. Математичні Зошити

Створюють PDF документи з розв'язками математичних задач у стилі зошита:
- Формулювання задачі
- Покрокове розв'язання (з підтримкою LaTeX)
- Фінальна відповідь

#### Використання через агента:
```
👤 Ви: Створи математичний зошит для задачі про площу круга
🤖 Агент: [використає create_math_notebook tool]
```

#### Програмне використання:
```python
from src.reporting.pdf_generator import generate_math_notebook_pdf

problem = "Знайти площу круга з радіусом 5 см"
solution = r"""
Дано: r = 5 см
Формула: S = \pi r^2
S = \pi \cdot 25 = 25\pi \approx 78.54 см²
"""

pdf_path = generate_math_notebook_pdf(problem, solution)
```

## Структура файлів

```
project/
├── src/
│   └── reporting/
│       ├── __init__.py
│       └── pdf_generator.py
├── templates/
│   └── typst/
│       ├── debug_report.typ
│       └── math_notebook.typ
├── output_pdfs/           # Генеровані PDF файли
└── test_pdf_generation.py # Тестування
```

## Шаблони Typst

### Debug Report Template (`debug_report.typ`)
```typst
#let data = json("data.json")

= Звіт Дебагу

== Оригінальний Запит:
#raw(data.get("original_user_query", "N/A"), block: true)

== Кроки Міркування:
#for step in data.llm_reasoning_steps {
  - #raw(step, block: false)
}

== Використаний Інструмент:
- Назва: #data.get("tool_name", "N/A")
- Параметри: #raw(json.encode(data.get("tool_input", {})), lang: "json")

== Результат:
#raw(data.get("tool_output", "N/A"), block: true)
```

### Math Notebook Template (`math_notebook.typ`)
```typst
#let data = json("data.json")

= Математичний Зошит

== Умова задачі:
#data.get("problem_statement", "N/A")

== Розв'язок:
#raw(data.solution_latex_body, lang: "latex")
```

## Інструменти Агента

### `create_debug_report`
Створює PDF звіт дебагу з детальною інформацією про роботу агента.

**Параметри:**
- `original_query`: Оригінальний запит користувача
- `reasoning_steps`: Список кроків міркування
- `tool_name`: Назва використаного інструмента
- `tool_input`: Вхідні параметри інструмента
- `tool_output`: Результат роботи інструмента
- `final_response`: Фінальна відповідь агента
- `llm_model`: Модель LLM (опціонально)

### `create_math_notebook`
Створює PDF математичний зошит з розв'язком задачі.

**Параметри:**
- `problem_statement`: Формулювання задачі
- `solution_steps`: Покрокове розв'язання (LaTeX)
- `final_answer`: Фінальна відповідь (опціонально)

## Тестування

Запустіть тестовий файл для перевірки функціональності:

```bash
python test_pdf_generation.py
```

Тести перевіряють:
1. Генерацію debug PDF
2. Генерацію math notebook PDF
3. Роботу PDF інструментів агента

## Налаштування

### Шляхи
- `OUTPUT_PDF_DIR`: Директорія для збереження PDF (за замовчуванням: `output_pdfs/`)
- `TYPST_TEMPLATES_DIR`: Директорія з шаблонами Typst

### Логування
PDF генератор використовує стандартну систему логування проекту. Рівень логування можна налаштувати в `src/utils/logger_config.py`.

## Приклади використання

### Через REPL
```
👤 Ви: Розв'яжи рівняння x² - 5x + 6 = 0 і створи математичний зошит

🤖 Агент: Розв'язую квадратне рівняння...
[використовує calculator для обчислень]
[використовує create_math_notebook для створення PDF]

✅ PDF математичного зошита створено: output_pdfs/math_notebook_abc123.pdf
```

### Програмно
```python
from src.agent.tools.pdf_tools import create_math_notebook

result = create_math_notebook(
    problem_statement="Розв'язати x² - 5x + 6 = 0",
    solution_steps=r"""
    Квадратне рівняння: $x^2 - 5x + 6 = 0$
    
    Використовуємо формулу: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
    
    $a = 1, b = -5, c = 6$
    
    $D = (-5)^2 - 4 \cdot 1 \cdot 6 = 25 - 24 = 1$
    
    $x_1 = \frac{5 + 1}{2} = 3$
    $x_2 = \frac{5 - 1}{2} = 2$
    """,
    final_answer="x₁ = 3, x₂ = 2"
)
print(result)
```

## Помилки та Вирішення

### Typst не знайдено
```
FileNotFoundError: Typst не знайдено
```
**Рішення:** Встановіть Typst згідно з інструкціями вище.

### Помилка компіляції шаблону
```
CalledProcessError: Помилка компіляції Typst
```
**Рішення:** Перевірте синтаксис шаблону Typst та валідність JSON даних.

### Відсутні шаблони
Базові шаблони створюються автоматично при першому запуску. Якщо виникають проблеми, видаліть директорію `templates/typst/` - вона буде відтворена.

## Розширення

### Додавання нових шаблонів
1. Створіть новий `.typ` файл в `templates/typst/`
2. Додайте функцію генерації в `pdf_generator.py`
3. Створіть відповідний інструмент в `pdf_tools.py`

### Кастомізація існуючих шаблонів
Відредагуйте файли в `templates/typst/` для зміни зовнішнього вигляду PDF документів. 