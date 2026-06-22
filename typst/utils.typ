#import "@preview/physica:0.9.8": *
#show: super-T-as-transpose // Render "..^T" as transposed matrix
#show: super-plus-as-dagger // Render "..^+" as dagger

#let del(a, b) = $(partial #a)/(partial #b)$

$ del(a, b) $


#let nonum(eq) = math.equation(block: true, numbering: none, eq)


#let cal(it) = math.class("normal", context {
  show math.equation: set text(font: "Garamond-Math", stylistic-set: 3)

  let scaling = 100% * (1em.to-absolute() / text.size)
  let wrapper = if scaling < 60% { math.sscript } else if scaling < 100% { math.script } else { it => it }

  box(text(top-edge: "bounds", $wrapper(math.cal(it))$))
})

#let det(..args) = math.mat(delim: "|", ..args)

#set text(lang: "he", dir: rtl)
#show link: underline

#let שם-מייל(גודל: 1em) = {
  text(גודל)[דן קצוב-פייגין 323002915    ]
  link("mailto:dan.k@campus.technion.ac.il")[#text(font: "Consolas", size: .5em)[dan.k\@campus.technion.ac.il] ]
}

#let גיליון(course, semester, number, date) = [
  #set document(title: course + " – " + semester + " – גיליון " + str(number))
  #set align(center)
  #text(3.5em)[#course -- #semester -- גיליון #number \
    #שם-מייל() \
    תאריך הגשה: #date]
  #pagebreak()
  #set align(right)
]
#let הרצאה(number, date, notes-link) = [
  #pagebreak()
  == הרצאה #number | #date \ #link(notes-link, "קישור להרצאה")
]

#let innerp(x, y) = $lr(chevron.l #x, #y chevron.r)$
#let limn(series, n: $n -> infinity$) = $display(lim_(#n)#series)$

#let Rn = [$bb(R)^n$]
#let Cn = [$bb(C)^n$]
#let Rnn = [$bb(R)^(n times n)$]
#let Cnn = [$bb(C)^(n times n)$]

#let קותח(text) = [#underline(text)]

#let משל = [
  #align(left)[$qed$]
]

#let heb(hebrew-text) = { return text(font: "David")[#hebrew-text] }

#import "@preview/codly:1.3.0": *

#let python-icon = (
  box(
    image("Python-logo-notext.svg", height: 1.0em),
    baseline: 0.25em,
    inset: 0pt,
    outset: 0pt,
  )
    + h(0.5em)
)

#let python-lang-config = (
  py: (
    name: "Python",
    icon: python-icon,
    color: rgb("#3776AB"),
  ),
  python: (
    name: "Python",
    icon: python-icon,
    color: rgb("#3776AB"),
  ),
)

#let codly-setup(body) = {
  show: codly-init
  show raw: set text(font: ("Noto Sans Mono", "Noto Sans Hebrew"), size: 0.9em)

  codly(
    languages: python-lang-config,
    radius: 6pt,
    stroke: 0.5pt + rgb("#cbd5e1"),
    fill: rgb("#f8fafc"),
    zebra-fill: rgb("#e2e8f0"),
    number-format: number => text(fill: rgb("#94a3b8"), size: 0.8em)[#number],
    lang-radius: 4pt,
    lang-stroke: lang => 0.5pt + lang.color.lighten(40%),
    lang-fill: lang => lang.color.lighten(90%),
    lang-inset: (x: 8pt, y: 4pt),
    inset: (x: 10pt, y: 4pt),
    breakable: true,
  )
  body
}

