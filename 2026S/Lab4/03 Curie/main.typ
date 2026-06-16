#import "../../../typst/templates/lab.typ": *
#import "../../../typst/utils.typ": *

#show: project.with(
  "ניסוי טמפרטורת קירי",
  "ד\"ר אנטולי גולדמן",
  "מעבדה לפיזיקה 4מח",
  report_title: [מדידת טמפרטורת קירי של חומרים פרומגנטיים ],
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
    (name: "יובל הירשמן", email: "yuval-h@campus.technion.ac.il", id: "322644295"),
  ),
  abstract: [],
  date: datetime(year: 2026, month: 6, day: 16),
)

= מבוא

== רקע תיאורטי

== מערכת הניסוי

= מהלך הניסוי

= חישובים מקדימים <חישובים_מקדימים>
#figure(
  table-from-file("constants.json"),
  caption: [ערכי קבועי המערכת והסלילים שהתקבלו מהחישובים המקדימים],
) <constants_table>

= תוצאות

== מדידת היענות לתדר

== חימום וקירור של ליבת פריט

== חימום וקירור של ליבת אינבר

= דיון ומסקנות
