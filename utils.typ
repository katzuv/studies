#set text(lang: "he", dir: rtl, font: "David")
#show link: underline

#let שם-מייל = [ == דן קצוב-פייגין #link("mailto:dan.k@campus.technion.ac.il")[`dan.k@campus.technion.ac.il`] ]

#let גיליון(course, semester, number, date) = [
  #set align(center)
  #text(3.5em)[#course -- #semester\ 
  גיליון #number \
  מגיש: דן קצוב-פייגין 323002915 
   תאריך הגשה: #date]
  #pagebreak()
  #set align(right)
]
#let הרצאה(number, date, notes-link) = [
  == הרצאה #number | #date \ #link(notes-link, "קישור להרצאה")
]

#let innerp(x, y) = $lr(angle.l #x, #y angle.r)$

#let Rn = [$bb(R)^n$]
#let Cn = [$bb(C)^n$]
#let Rnn = [$bb(R)^(n times n)$]
#let Cnn = [$bb(C)^(n times n)$]

#let קותח(text) = [ #underline(text) ]

#let משל = [
  #align(left)[$qed$]
]
