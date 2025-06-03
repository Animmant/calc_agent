import logging
import json
import os
import subprocess
import uuid
import tempfile
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Конфігурація шляхів
OUTPUT_PDF_DIR = "output_pdfs"
TYPST_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'typst')
LATEX_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'latex')

# Створюємо необхідні директорії
os.makedirs(OUTPUT_PDF_DIR, exist_ok=True)
os.makedirs(TYPST_TEMPLATES_DIR, exist_ok=True)
os.makedirs(LATEX_TEMPLATES_DIR, exist_ok=True)


def _check_latex_installation() -> bool:
    """Перевіряє, чи встановлено LaTeX."""
    try:
        result = subprocess.run(["pdflatex", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _check_typst_installation() -> bool:
    """Перевіряє, чи встановлено Typst."""
    try:
        result = subprocess.run(["typst", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _compile_latex_template(template_path: str, latex_content: str, output_filename_base: str) -> Optional[str]:
    """
    Компілює LaTeX шаблон з вставленим контентом.
    """
    if not _check_latex_installation():
        logger.error("LaTeX не встановлено. Встановіть TeX Live або MiKTeX.")
        return None

    # Читаємо шаблон
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        logger.error(f"Помилка читання шаблону {template_path}: {e}")
        return None

    # Замінюємо плейсхолдер на контент
    final_latex = template_content.replace('{LATEX_CONTENT}', latex_content)

    # Створюємо тимчасову директорію для компіляції
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_tex_path = os.path.join(temp_dir, "document.tex")
        
        # Записуємо LaTeX файл
        try:
            with open(temp_tex_path, 'w', encoding='utf-8') as f:
                f.write(final_latex)
        except Exception as e:
            logger.error(f"Помилка запису LaTeX файлу: {e}")
            return None

        # Компілюємо PDF (двічі для правильних посилань)
        try:
            for i in range(2):
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "document.tex"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    logger.error(f"Помилка компіляції LaTeX (прохід {i+1}): {result.stderr}")
                    logger.error(f"LaTeX stdout: {result.stdout}")
                    return None

            # Переміщуємо готовий PDF
            temp_pdf_path = os.path.join(temp_dir, "document.pdf")
            if not os.path.exists(temp_pdf_path):
                logger.error("PDF файл не створено після компіляції LaTeX")
                return None

            unique_id = uuid.uuid4().hex
            output_pdf_filename = f"{output_filename_base}_{unique_id}.pdf"
            output_pdf_path = os.path.join(OUTPUT_PDF_DIR, output_pdf_filename)
            
            shutil.copy2(temp_pdf_path, output_pdf_path)
            logger.info(f"✅ LaTeX PDF згенеровано: {output_pdf_path}")
            return os.path.abspath(output_pdf_path)

        except Exception as e:
            logger.error(f"Помилка під час компіляції LaTeX: {e}")
            return None


def _compile_typst_template(template_name: str, data: Dict[str, Any], output_filename_base: str) -> Optional[str]:
    """
    Допоміжна функція для компіляції Typst шаблону.
    Дані записуються в тимчасовий JSON, який читається шаблоном.
    """
    if not _check_typst_installation():
        logger.error("Typst не встановлено. Встановіть його з https://github.com/typst/typst/releases")
        return None

    template_path = os.path.join(TYPST_TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        logger.error(f"Шаблон Typst не знайдено: {template_path}")
        # Спробуємо створити базовий шаблон, якщо його немає
        if template_name == "debug_report.typ":
            create_basic_debug_template()
        elif template_name == "math_notebook.typ":
            create_basic_math_template()
        else:
            return None
        
        # Якщо шаблон все одно не створено/не знайдено після спроби створення
        if not os.path.exists(template_path):
            logger.error(f"Базовий шаблон {template_name} не вдалося створити або знайти.")
            return None

    # Унікальне ім'я для JSON та PDF файлів
    unique_id = uuid.uuid4().hex
    output_pdf_filename = f"{output_filename_base}_{unique_id}.pdf"
    output_pdf_path = os.path.join(OUTPUT_PDF_DIR, output_pdf_filename)

    try:
        # Створюємо data.json в тій же директорії, що й шаблон
        data_for_template_path = os.path.join(TYPST_TEMPLATES_DIR, "data.json")
        with open(data_for_template_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Дані для Typst збережено в: {data_for_template_path}")

        # Абсолютні шляхи для команди
        abs_template_path = os.path.abspath(template_path)
        abs_output_path = os.path.abspath(output_pdf_path)

        command = [
            "typst", "compile",
            abs_template_path,  # Шлях до файлу шаблону
            abs_output_path     # Шлях до вихідного PDF
        ]
        logger.info(f"Виконання команди Typst: {' '.join(command)}")
        
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
        logger.info(f"Typst stdout: {result.stdout}")
        logger.info(f"✅ PDF згенеровано: {abs_output_path}")
        
        # Прибираємо тимчасовий data.json
        if os.path.exists(data_for_template_path):
            os.remove(data_for_template_path)
        
        return abs_output_path

    except FileNotFoundError:
        logger.error("Typst не знайдено. Переконайтеся, що він встановлений та доступний у PATH.")
        return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Помилка компіляції Typst: {e}")
        logger.error(f"Typst stderr: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Невідома помилка при генерації PDF: {e}", exc_info=True)
        return None


def generate_debug_pdf(debug_data: Dict[str, Any]) -> Optional[str]:
    """Генерує PDF звіт для дебагу."""
    logger.info(f"Запит на генерацію /debug PDF з даними: {json.dumps(debug_data, indent=2, ensure_ascii=False)}")
    
    # Спочатку пробуємо Typst, потім LaTeX
    pdf_path = _compile_typst_template("debug_report.typ", debug_data, "debug_report")
    
    if not pdf_path:
        logger.info("Typst недоступний, пробуємо альтернативний метод...")
        # Тут можна додати альтернативний метод генерації
    
    if pdf_path:
        logger.info(f"PDF для дебагу створено: {pdf_path}")
    else:
        logger.warning("Не вдалося створити PDF для дебагу.")
    return pdf_path


def generate_math_notebook_pdf(problem_statement: str, solution_latex: str) -> Optional[str]:
    """
    Генерує PDF у стилі математичного зошита.
    Спочатку пробує LaTeX, потім Typst як fallback.
    """
    logger.info(f"Запит на генерацію /maths PDF.")
    logger.debug(f"Умова задачі: {problem_statement}")
    logger.debug(f"LaTeX розв'язку:\n{solution_latex}")
    
    # Спочатку пробуємо LaTeX (кращий для математики)
    latex_template_path = os.path.join(LATEX_TEMPLATES_DIR, "math_notebook_template.tex")
    
    if os.path.exists(latex_template_path) and _check_latex_installation():
        logger.info("Використовуємо LaTeX для генерації математичного зошита...")
        pdf_path = _compile_latex_template(latex_template_path, solution_latex, "math_notebook")
        if pdf_path:
            logger.info(f"PDF математичного зошита створено через LaTeX: {pdf_path}")
            return pdf_path
    
    # Fallback до Typst
    logger.info("LaTeX недоступний, використовуємо Typst...")
    data_for_pdf = {
        "problem_statement": problem_statement,
        "solution_latex_body": solution_latex  # Тіло LaTeX, без \documentclass
    }
    pdf_path = _compile_typst_template("math_notebook.typ", data_for_pdf, "math_notebook")

    if pdf_path:
        logger.info(f"PDF математичного зошита створено через Typst: {pdf_path}")
    else:
        logger.warning("Не вдалося створити PDF математичного зошита.")
    return pdf_path


def get_available_engines() -> Dict[str, bool]:
    """Повертає інформацію про доступні движки для генерації PDF."""
    return {
        "latex": _check_latex_installation(),
        "typst": _check_typst_installation()
    }


def create_basic_debug_template():
    """Створює базовий шаблон для звітів дебагу."""
    template_path = os.path.join(TYPST_TEMPLATES_DIR, "debug_report.typ")
    if os.path.exists(template_path):
        return
    
    content = '''#let data = json("data.json")

#set page(margin: 2cm)
#set text(font: "Times New Roman", size: 11pt)

#show heading.where(level: 1): it => block[
  #set text(weight: "bold", size: 16pt)
  #it
  #line(length: 100%)
  #v(1em)
]

= Звіт Дебагу

== Оригінальний Запит Користувача:
#raw(data.at("original_user_query", default: "N/A"), block: true)

== Ланцюжок Думок LLM / Кроки Агента:
#if "llm_reasoning_steps" in data and data.llm_reasoning_steps.len() > 0 [
  #for step in data.llm_reasoning_steps [
    - #step
  ]
] else [
  "N/A"
]

== Обраний Інструмент та Вхідні Параметри:
- Назва інструмента: #data.at("tool_name", default: "N/A")
- Вхідні параметри:
  ```json
  #raw(repr(data.at("tool_input", default: (:))), lang: "json")
  ```

== Результат Роботи Інструмента:
#raw(data.at("tool_output", default: "N/A"), block: true)

== Фінальна Відповідь Агента:
#raw(data.at("final_agent_response", default: "N/A"), block: true)

== Використані Ресурси:
Модель LLM: #data.at("resources", default: (:)).at("llm_model", default: "N/A")
'''
    
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Створено базовий шаблон: {template_path}")


def create_basic_math_template():
    """Створює базовий шаблон для математичних зошитів."""
    template_path = os.path.join(TYPST_TEMPLATES_DIR, "math_notebook.typ")
    if os.path.exists(template_path):
        return

    content = '''#let data = json("data.json")

#set page(margin: 2cm)
#set text(font: "Times New Roman", size: 12pt)

= Математичний Зошит

== Умова задачі:
#data.at("problem_statement", default: "N/A")

== Покроковий Розв'язок:
#if "solution_latex_body" in data [
  #raw(data.solution_latex_body, block: true)
] else [
  "Розв'язок не надано."
]

== Відповідь:
#data.at("final_answer_summary", default: "Див. детальний розв'язок вище.")
'''
    
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Створено базовий шаблон: {template_path}")


# Створюємо шаблони при імпорті, якщо їх немає
create_basic_debug_template()
create_basic_math_template() 