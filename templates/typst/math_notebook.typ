#let data = json("data.json")

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
