#import "../../../typst/templates/lab.typ": *
#import "../../../typst/utils.typ": *

#show: project.with(
  "ניסוי פרנק-הרץ",
  "ד\"ר אנטולי גולדמן",
  "מעבדה לפיזיקה 4מח",
  report_title: [מדידת אנרגיית עירור ופוטנציאל יינון של אטומי כספית בניסוי פרנק-הרץ],
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  abstract: [],
  date: datetime(year: 2026, month: 6, day: 7),
)

= מבוא

== רקע תיאורטי

== מערכת הניסוי

= מהלך הניסוי

= תוצאות וניתוח

#figure(
  image("fh_characteristic_curves.svg", width: 85%),
  caption: none,
)

#figure(
  image("fh_ionization_curve.svg", width: 85%),
  caption: none,
)

= דיון ומסקנות
