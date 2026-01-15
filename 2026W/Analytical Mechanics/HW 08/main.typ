#import "../template.typ": *
#import "../consts.typ": *
#import "../utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "מכניקה אנליטית",
  number: 8,
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2025, month: 1, day: 15)
)
#set text(font: "Noto Serif Hebrew", weight: 500, lang: "he", region: "il")

#שאלה(כותרת: "קוביה אחידה", [
תהי קופסה בעלת צפיפות אחידה בעלת מסה $M$ ואורכי צלעות
$a>b>c$.
#figure(
  image("q1.png", width: 80%),
)
])
#סעיף[
חשבו את טנזור האינרציה של הקוביה סביב מרכז המסה שלה.]
משיקולי סימטריה נסיק שמרכז המסה נמצא ב


































