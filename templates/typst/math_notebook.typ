#import "@preview/cmarker:0.1.6"

#let data = json("data.json")

#set page(margin: 2cm)
#set text(font: "Times New Roman", size: 12pt)

= Математичний Зошит

== Умова задачі:
#data.at("problem_statement", default: "N/A")

== Знайти:
#data.at("sulut_search", default: "N/A")

== Розв'язок:
#if "solution_markdown_content" in data [
  #cmarker.render(data.solution_markdown_content)
] else if "solution_latex_body" in data [
  #raw(data.solution_latex_body, block: true)
  #text(red, size: 9pt)[Попередження: Відображено старий LaTeX формат. Оновіть генерацію контенту до Markdown+TypstMath.]
] else [
  "Розв'язок не надано."
]

== Відповідь:
#data.at("final_answer_summary", default: "Див. детальний розв'язок вище.")
