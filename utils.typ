#set text(lang: "he", dir: rtl, font: "David")
#show link: underline

#let שם-מייל = [ == דן קצוב-פייגין #link("mailto:dan.k@campus.technion.ac.il")[`dan.k@campus.technion.ac.il`] ]

#let הרצאה(number, date, notes-link) = [
  == הרצאה #number | #date | #link(notes-link, "קישור לרשימות")
]

#let innerp(x, y) = $lr(angle.l #x, #y angle.r)$

#let Rn = [$bb(R)^n$]
#let Cn = [$bb(C)^n$]
#let Rnn = [$bb(R)^(n times n)$]
#let Cnn = [$bb(C)^(n times n)$]