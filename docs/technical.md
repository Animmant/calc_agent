





### arhitectured

your_project_name/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent_executor.py  # Логіка виконання агента (LangGraph)
│   │   ├── state.py           # Визначення стану агента
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── calculator.py    # Наш перший інструмент
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Налаштування, завантаження API ключів
│   ├── cli/
│   │   ├── __init__.py
│   │   └── REPL.py            # Read-Eval-Print Loop для консолі
│   └── utils/
│       ├── __init__.py
│       └── logger_config.py   # Налаштування логування
├── tests/
│   ├── agent/
│   │   └── tools/
│   │       └── test_calculator.py
│   └── __init__.py
├── .env
└── main.py 