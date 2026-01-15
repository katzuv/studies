#set text(lang: "he", dir: rtl, font: "David")
#show link: underline

#let שם-מייל(גודל) = {
    text(גודל)[דן קצוב-פייגין 323002915    ]
    link("mailto:dan.k@campus.technion.ac.il")[#text(font: "Consolas", size: .5em)[dan.k\@campus.technion.ac.il] ]
}

#let גיליון(course, semester, number, date) = {
  set align(center)
  text(3.5em)[#course -- #semester\ 
  גיליון #number \
  #שם-מייל(1em)
  #linebreak()
   תאריך הגשה: #date]
  pagebreak()
  set align(right)
}

#let הרצאה(number, date, notes-link) = [
    #pagebreak()
  = הרצאה #number | #date
  #link(notes-link, "קישור להקלטה") \
]

#let innerp(x, y) = $lr(angle.l #x, #y angle.r)$
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
#הרצאה("1","2","3")
#שם-מייל
#outline()
