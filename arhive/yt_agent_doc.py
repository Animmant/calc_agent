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
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
# from mail import fetch_recent_emails  # Закоментовано, якщо не потрібно


load_dotenv(find_dotenv())

REQUISITES_FILE = os.path.join("src", "utils", "akt_skylie_groupe_example.pdf")


@dataclass
class Bank:
    """Банковские реквизиты заказчика"""
    name: str  # наименование банка
    BIC: str  # БИК
    current_account: str  # расчётный счёт
    corporate_account: str  # корреспондентский счёт


@dataclass
class Customer:
    """Заказчик"""
    name: str  # полное название юридического лица, наприемер, ООО «Рога и копыта»
    INN: str  # ИНН
    OGRN: str  # ОГРН или ОГРНИП
    address: str  # юридический адрес
    signatory: str  # подписант
    bank: Bank  # банковские реквизиты заказчика


@dataclass
class Job:
    task: str  # выполненная задача
    price: int  # цена за задачу


@tool
def generate_pdf_act(customer: Customer, jobs: list[Job]) -> None:
    """
    Генерирует PDF-акт, в котором заполнены данные
    клиента, его банковские реквизиты, а также выполненные задачи

    Args:
        customer (Customer): данные клиента
        jobs (list[Job]): список выполненных задач для внесения в акт

    Returns:
        None
    """
    try:
        print(f"🔧 DEBUG: Генеруємо акт для {customer.name}")
        print(f"🔧 DEBUG: Кількість робіт: {len(jobs)}")
        
        # Створюємо папку typst якщо її немає
        os.makedirs("typst", exist_ok=True)
        
        act_json = {
            "customer": asdict(customer),
            "jobs": list(map(lambda j: asdict(j), jobs))
        }
        
        json_file_path = os.path.join("typst", "act.json")
        with open(json_file_path, "w", encoding='utf-8') as f:
            json.dump(act_json, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON файл створено: {json_file_path}")
        
        # Перевіряємо чи доступний typst
        try:
            subprocess.run(["typst", "--version"], 
                          check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            typst_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            typst_available = False
            print("⚠️ Typst не доступний. Створюю HTML версію...")
        
        if typst_available:
            # Перевіряємо чи існує typst template
            typst_template = os.path.join("typst", "act.typ")
            if not os.path.exists(typst_template):
                print(f"⚠️ УВАГА: Файл шаблону {typst_template} не знайдено!")
                print("📝 Створюю базовий шаблон...")
                create_basic_typst_template()
            
            command = ["typst", "compile", "--root", "./typst", "typst/act.typ"]
            print(f"🔧 DEBUG: Виконую команду: {' '.join(command)}")
            
            result = subprocess.run(command,
                                   check=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, 
                                   text=True)
            
            print("✅ PDF акт успішно створено!")
        else:
            # Створюємо HTML версію як fallback
            create_html_act(customer, jobs)
            print("✅ HTML акт створено (typst недоступний)")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка при створенні PDF: {e}")
        print(f"❌ STDERR: {e.stderr}")
        print(f"❌ STDOUT: {e.stdout}")
        # Fallback до HTML
        try:
            create_html_act(customer, jobs)
            print("✅ Створено HTML версію як резервну")
        except Exception as fallback_error:
            raise Exception(f"Не вдалося створити ні PDF, ні HTML: {e.stderr}, {fallback_error}")
    except Exception as e:
        print(f"❌ Загальна помилка: {e}")
        raise


@tool
def generate_pdf_invoice(customer: Customer, jobs: list[Job]) -> None:
    """
    Генерирует PDF-счёт, в котором заполнены данные
    клиента, а также выполненные задачи

    Args:
        customer (Customer): данные клиента
        jobs (list[Job]): список выполненных задач для внесения в акт

    Returns:
        None
    """
    try:
        print(f"🔧 DEBUG: Генеруємо рахунок для {customer.name}")
        
        # Створюємо папку typst якщо її немає
        os.makedirs("typst", exist_ok=True)
        
        invoice_json = {
            "customer": asdict(customer),
            "jobs": list(map(lambda j: asdict(j), jobs))
        }
        
        json_file_path = os.path.join("typst", "invoice.json")
        with open(json_file_path, "w", encoding='utf-8') as f:
            json.dump(invoice_json, f, ensure_ascii=False, indent=2)
            
        print(f"✅ JSON файл створено: {json_file_path}")
        
        # Перевіряємо чи доступний typst
        try:
            subprocess.run(["typst", "--version"], 
                          check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            typst_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            typst_available = False
            print("⚠️ Typst не доступний. Створюю HTML версію...")
        
        if typst_available:
            # Перевіряємо чи існує typst template
            typst_template = os.path.join("typst", "invoice.typ")
            if not os.path.exists(typst_template):
                print(f"⚠️ УВАГА: Файл шаблону {typst_template} не знайдено!")
                print("📝 Створюю базовий шаблон...")
                create_basic_invoice_template()
            
            command = ["typst", "compile", "--root", "./typst", "typst/invoice.typ"]
            print(f"🔧 DEBUG: Виконую команду: {' '.join(command)}")
            
            result = subprocess.run(command,
                                   check=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, 
                                   text=True)
            
            print("✅ PDF рахунок успішно створено!")
        else:
            # Створюємо HTML версію як fallback
            create_html_invoice(customer, jobs)
            print("✅ HTML рахунок створено (typst недоступний)")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка при створенні PDF: {e}")
        print(f"❌ STDERR: {e.stderr}")
        print(f"❌ STDOUT: {e.stdout}")
        # Fallback до HTML
        try:
            create_html_invoice(customer, jobs)
            print("✅ Створено HTML версію як резервну")
        except Exception as fallback_error:
            raise Exception(f"Не вдалося створити ні PDF, ні HTML: {e.stderr}, {fallback_error}")
    except Exception as e:
        print(f"❌ Загальна помилка: {e}")
        raise


def create_basic_typst_template():
    """Створює базовий шаблон для акту"""
    template_content = '''
#let data = json("act.json")

#set page(margin: 2cm)
#set text(font: "Times New Roman", size: 12pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[АКТ ВЫПОЛНЕННЫХ РАБОТ]
]

#v(1cm)

*Заказчик:* #data.customer.name

*ИНН:* #data.customer.INN

*Адрес:* #data.customer.address

*Подписант:* #data.customer.signatory

#v(1cm)

*Выполненные работы:*

#for job in data.jobs [
  - #job.task: #job.price руб.
]

#v(2cm)

*Подпись:* ________________
'''
    
    os.makedirs("typst", exist_ok=True)
    with open(os.path.join("typst", "act.typ"), "w", encoding='utf-8') as f:
        f.write(template_content)
    print("✅ Базовий шаблон акту створено!")


def create_basic_invoice_template():
    """Створює базовий шаблон для рахунку"""
    template_content = '''
#let data = json("invoice.json")

#set page(margin: 2cm)
#set text(font: "Times New Roman", size: 12pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[СЧЁТ НА ОПЛАТУ]
]

#v(1cm)

*Заказчик:* #data.customer.name

*ИНН:* #data.customer.INN

*Адрес:* #data.customer.address

#v(1cm)

*К оплате:*

#for job in data.jobs [
  - #job.task: #job.price руб.
]

#let total = data.jobs.map(job => job.price).sum()

#v(1cm)

*Итого к оплате:* #total руб.

#v(2cm)

*Подпись:* ________________
'''
    
    os.makedirs("typst", exist_ok=True)
    with open(os.path.join("typst", "invoice.typ"), "w", encoding='utf-8') as f:
        f.write(template_content)
    print("✅ Базовий шаблон рахунку створено!")


def create_html_act(customer: Customer, jobs: list[Job]):
    """Створює HTML версію акту"""
    total = sum(job.price for job in jobs)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Акт выполненных работ</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 2cm; }}
        .header {{ text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 2cm; }}
        .section {{ margin-bottom: 1cm; }}
        .jobs {{ margin: 1cm 0; }}
        .signature {{ margin-top: 3cm; }}
    </style>
</head>
<body>
    <div class="header">АКТ ВЫПОЛНЕННЫХ РАБОТ</div>
    
    <div class="section">
        <strong>Заказчик:</strong> {customer.name}<br>
        <strong>ИНН:</strong> {customer.INN}<br>
        <strong>ОГРН:</strong> {customer.OGRN}<br>
        <strong>Адрес:</strong> {customer.address}<br>
        <strong>Подписант:</strong> {customer.signatory}
    </div>
    
    <div class="section">
        <strong>Банковские реквизиты:</strong><br>
        Банк: {customer.bank.name}<br>
        БИК: {customer.bank.BIC}<br>
        Расчётный счёт: {customer.bank.current_account}<br>
        Корреспондентский счёт: {customer.bank.corporate_account}
    </div>
    
    <div class="jobs">
        <strong>Выполненные работы:</strong><br>
        <ul>
"""
    
    for job in jobs:
        html_content += f"            <li>{job.task}: {job.price:,} руб.</li>\n"
    
    html_content += f"""
        </ul>
        <strong>Итого: {total:,} руб.</strong>
    </div>
    
    <div class="signature">
        <strong>Подпись:</strong> ________________
    </div>
</body>
</html>
"""
    
    with open("act.html", "w", encoding='utf-8') as f:
        f.write(html_content)


def create_html_invoice(customer: Customer, jobs: list[Job]):
    """Створює HTML версію рахунку"""
    total = sum(job.price for job in jobs)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Счёт на оплату</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 2cm; }}
        .header {{ text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 2cm; }}
        .section {{ margin-bottom: 1cm; }}
        .jobs {{ margin: 1cm 0; }}
        .total {{ font-size: 16px; font-weight: bold; margin-top: 1cm; }}
        .signature {{ margin-top: 3cm; }}
    </style>
</head>
<body>
    <div class="header">СЧЁТ НА ОПЛАТУ</div>
    
    <div class="section">
        <strong>Заказчик:</strong> {customer.name}<br>
        <strong>ИНН:</strong> {customer.INN}<br>
        <strong>ОГРН:</strong> {customer.OGRN}<br>
        <strong>Адрес:</strong> {customer.address}
    </div>
    
    <div class="section">
        <strong>Банковские реквизиты:</strong><br>
        Банк: {customer.bank.name}<br>
        БИК: {customer.bank.BIC}<br>
        Расчётный счёт: {customer.bank.current_account}<br>
        Корреспондентский счёт: {customer.bank.corporate_account}
    </div>
    
    <div class="jobs">
        <strong>К оплате:</strong><br>
        <ul>
"""
    
    for job in jobs:
        html_content += f"            <li>{job.task}: {job.price:,} руб.</li>\n"
    
    html_content += f"""
        </ul>
    </div>
    
    <div class="total">
        <strong>Итого к оплате: {total:,} руб.</strong>
    </div>
    
    <div class="signature">
        <strong>Подпись:</strong> ________________
    </div>
</body>
</html>
"""
    
    with open("invoice.html", "w", encoding='utf-8') as f:
        f.write(html_content)


class LLMAgent:
    def __init__(self, model: LanguageModelLike, tools: Sequence[BaseTool]):
        self._model = model
        self._agent = create_react_agent(
            model,
            tools=tools,
            checkpointer=InMemorySaver())
        self._config: RunnableConfig = {
                "configurable": {"thread_id": uuid.uuid4().hex}}

    def upload_file(self, file):
        """
        Для Google Gemini API файли обробляються інакше.
        Повертаємо шлях до файлу для подальшого використання.
        """
        # Google Gemini API не має прямого методу upload_file як GigaChat
        # Файл буде оброблений через prompt з посиланням на файл
        return file.name if hasattr(file, 'name') else str(file)

    def invoke(
        self,
        content: str,
        attachments: list[str]|None=None,
        temperature: float=0.1
    ) -> str:
        """Відправляє повідомлення в чат"""
        # Для Google Gemini API формуємо повідомлення без attachments
        # Інформацію про файли додаємо в текст промпту
        if attachments:
            content += f"\n\nПрикріплені файли: {', '.join(attachments)}"
            content += "\nБудь ласка, використовуй інформацію з цих файлів для генерації документів."
        
        message: dict = {
            "role": "user",
            "content": content
        }
        
        return self._agent.invoke(
            {
                "messages": [message],
                "temperature": temperature
            },
            config=self._config)["messages"][-1].content


def print_agent_response(llm_response: str) -> None:
    print(f"\033[35m{llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nТы: ")


def main():
    # Замінюємо GigaChat на Google Gemini
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",  # або "gemini-1.5-pro"
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    agent = LLMAgent(model, tools=[generate_pdf_act, generate_pdf_invoice])
    system_prompt = (
        "Твоя задача спросить у пользователя, что он хочет сгенерировать — акт или счёт или оба документа. "
        "Затем нужно сгенерировать акт или счёт, для этого тебе надо взять реквизиты "
        "контрагента из приложенного файла, а также запроси работы для включения в "
        "акт (наименования задач и их стоимость), работ может быть несколько. "
        "Если пользователь указывает в качетсве работы курс, то для документов берём одну работу, в точности такую "
        "\"Обучение одного сотрудника на курсе «Хардкорная веб-разработка»\", стоимостью 170 тыс руб."
        "Никакие данные не придумывай, всё необходимое строго запроси у "
        "пользователя. Мои реквизиты заказчика не запрашивай, они есть в моём коде. "
        "Имя и отчество подписанта сокращаем до одной первой буквы, "
        "например, Иванов А.Е. "
        "Название компании оборачиваем в кавычки ёлочкой, например, "
        "ООО «Рога и копыта», то есть до названия компании ставим « и после названия "
        "ставим »."
        f"\n\nИспользуй информацию из файла: {REQUISITES_FILE}"
    )

    # Для Google Gemini API обробка файлів відрізняється
    try:
        with open(REQUISITES_FILE, "rb") as file:
            file_path = agent.upload_file(file)
            agent_response = agent.invoke(content=system_prompt, attachments=[file_path])
    except FileNotFoundError:
        print(f"⚠️ Файл {REQUISITES_FILE} не знайдено. Продовжую без файлу.")
        agent_response = agent.invoke(content=system_prompt)

    while(True):
        print_agent_response(agent_response)
        agent_response = agent.invoke(get_user_prompt())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nдосвидули!")