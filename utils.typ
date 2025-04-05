#set text(lang: "he", dir: rtl, font: "David")
#show link: underline

#let שם-מייל = [ == דן קצוב-פייגין #link("mailto:dan.k@campus.technion.ac.il")[`dan.k@campus.technion.ac.il`] ]

#let הרצאה(number, date, notes-link) = [
  == הרצאה #number | #date | #link(notes-link, "קישור לרשימות")
]