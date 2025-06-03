#let data = json("data.json")

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
