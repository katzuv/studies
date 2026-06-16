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

#figure(
  table-from-file("ferrite_results.json"),
  caption: [תוצאות ההתאמה לפונקציית שגיאה עבור מעבר הפאזה (חימום וקירור) ולחוק הקירור של ניוטון עבור ליבת פריט],
) <ferrite_results_table>

#grid(
  columns: (1fr, 1fr),
  gutter: 1em,
  figure(
    image("ferrite_curie_fit.svg", width: 100%),
    caption: [מתח משני כפונקציה של טמפרטורה בחימום ובקירור, יחד עם ההתאמות לפונקציית שגיאה לקביעת טמפרטורת קירי]
  ),
  figure(
    image("ferrite_cooling_fit.svg", width: 100%),
    caption: [פרופיל התקררות הליבה כפונקציה של זמן והתאמה לחוק הקירור של ניוטון]
  )
)

== חימום וקירור של ליבת אינבר

#figure(
  table-from-file("invar_results.json"),
  caption: [תוצאות ההתאמה לפונקציית שגיאה עבור מעבר הפאזה (חימום וקירור) ולחוק הקירור של ניוטון עבור ליבת אינבר],
) <invar_results_table>

#grid(
  columns: (1fr, 1fr),
  gutter: 1em,
  figure(
    image("invar_curie_fit.svg", width: 100%),
    caption: [מתח משני כפונקציה של טמפרטורה בחימום ובקירור, יחד עם ההתאמות לפונקציית שגיאה לקביעת טמפרטורת קירי עבור ליבת אינבר]
  ),
  figure(
    image("invar_cooling_fit.svg", width: 100%),
    caption: [פרופיל התקררות הליבה כפונקציה של זמן והתאמה לחוק הקירור של ניוטון עבור ליבת אינבר]
  )
)

= דיון ומסקנות
