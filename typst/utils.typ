#import "@preview/physica:0.9.8": *
#show: super-T-as-transpose // Render "..^T" as transposed matrix
#show: super-plus-as-dagger // Render "..^+" as dagger

#let del(a,b) = $(partial #a)/(partial #b)$

$ del(a, b) $


#let nonum(eq) = math.equation(block: true, numbering: none, eq)


#let cal(it) = math.class("normal", context {
  show math.equation: set text(font: "Garamond-Math", stylistic-set: 3)

  let scaling = 100% * (1em.to-absolute() / text.size)
  let wrapper = if scaling < 60% { math.sscript }
                else if scaling < 100% { math.script }
                else { it => it }
  
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

#let קותח(text) = [ #underline(text) ]

#let משל = [
  #align(left)[$qed$]
]

#let heb(hebrew-text) = { return text(font: "David")[#hebrew-text] }
