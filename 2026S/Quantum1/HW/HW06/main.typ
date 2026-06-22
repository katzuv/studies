#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *
#import "constants.typ": *

#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "6",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 6, day: 19),
)

#שאלה(כותרת: "חבילת גלים גאוסית", מזהה: <1>, [
  חבילת גלים גאוסיאנית נתונה על ידי:
  $ psi(x, t = 0) = 1/(pi Delta^2)^(1/4) e^(- (x-x_0)^2 / (2 Delta^2)) e^(i / hbar p_0 x) $

  חשבו את אי-הוודאות בתנע $Delta P$.

  *הדרכה:* חשבו את $expval(P) = mel(psi, P, psi)$ כאשר $P = -i hbar pdv(, x)$. באותו אופן, חשבו את $expval(P^2) = mel(psi, P^2, psi)$.
])
נחשב תחילה את
$pdv(psi, x)$:
$
  pdv(psi, x) = 1/(pi Delta^2)^(1/4) pdv(, x)( e^(- (x-x_0)^2 / (2 Delta^2) + i / hbar p_0 x)) = (i/hbar p_0 - (x-x_0)/(Delta^2)) psi(x)
$
כעת נחשב את $expval(P)$:
$
  expval(P) &= mel(psi, P, psi) = mel(psi, I P, psi) = bra(psi) (integral_(-oo)^oo ketbra(x) dd(x)) P ket(psi) = integral_(-oo)^oo braket(psi, x) mel(x, P, psi) dd(x) \
  &= integral_(-oo)^oo psi^*(x)(-i hbar) pdv(, x) psi(x) dd(x) = integral_(-oo)^oo psi^*(x)(-i hbar)(i/hbar p_0 - (x-x_0)/(Delta^2)) psi(x) dd(x) \
  &= -i hbar integral_(-oo)^oo abs(psi(x))^2 (i/hbar p_0 - (x-x_0)/(Delta^2)) dd(x)
  = p_0 underbrace(integral_(-oo)^oo abs(psi(x))^2 dd(x), 1) + (i hbar)/Delta^2 integral_(-oo)^oo abs(psi(x))^2 (x-x_0) dd(x)
$
וזאת משום שפונקציית הגל מנורמלת. נחשב את האינטגרל השני:
$
  integral_(-oo)^oo abs(psi(x))^2 (x-x_0) dd(x) &= integral_(-oo)^oo abs(1/(pi Delta^2)^(1/4) e^(- (x-x_0)^2 / (2 Delta^2)) e^(i / hbar p_0 x))^2 (x-x_0) dd(x) \
  &= 1/(pi Delta^2)^(1/2) integral_(-oo)^oo e^(- (x-x_0)^2 / (Delta^2)) (x-x_0) dd(x)
  stretch(=)_(x'=x-x_0) 1/(pi Delta^2)^(1/2) integral_(-oo)^oo e^(- x'^2 / (Delta^2)) x' dd(x') = 0
$
מכיוון שהאינטגרנד הוא פונקציה אי-זוגית. נציב זאת חזרה ונקבל:
$expval(P) = p_0$.

#linebreak()
כעת נחשב את $expval(P^2)$:
$
  expval(P^2) &= mel(psi, P^2, psi) = mel(psi, P P, psi) stretch(=)_(P=P^+) mel(psi, P^+ P, psi) = braket(P psi) = mel(P psi, I, P psi) \
  &= integral_(-oo)^oo braket(P psi, x)braket(x, P psi) dd(x) = integral_(-oo)^oo (P psi(x))^* (P psi(x)) dd(x) \
  &= integral_(-oo)^oo abs(P psi(x))^2 dd(x) = integral_(-oo)^oo abs(-i hbar pdv(psi, x))^2 dd(x) = hbar^2 integral_(-oo)^oo abs(pdv(psi, x))^2 dd(x) \
  &= hbar^2 integral_(-oo)^oo abs(1/(pi Delta^2)^(1/4) (i/hbar p_0 - (x-x_0)/(Delta^2)) e^(-(x-x_0)^2/(2 Delta^2)) e^(i / hbar p_0 x))^2 dd(x) = integral_(-oo)^oo hbar^2/(sqrt(pi) Delta) (p_0^2/hbar^2 + (x-x_0)^2/Delta^4)e^(-(x-x_0)^2/Delta^2) dd(x) \
  &= p_0^2 underbrace(integral_(-oo)^oo 1/(sqrt(pi) Delta) e^(-(x-x_0)^2/Delta^2), 1) dd(x) + hbar^2/(sqrt(pi) Delta^5) integral_(-oo)^oo (x-x_0)^2 e^(-(x-x_0)^2/Delta^2) dd(x) = p_0^2 + hbar^2/Delta^4 integral_(-oo)^oo 1/(sqrt(pi) Delta) x'^2 e^(-x'^2/Delta^2) dd(x')
$
נשים לב כי האינטגרל הנותר הוא המומנט השני של גאוסיאן, לכן:
$
  expval(P^2) = p_0^2 + hbar^2/Delta^4 (0^2 + Delta^2/2) = p_0^2 + hbar^2/(2 Delta^2)
$
#תשובה[
  $ Delta P = sqrt(expval(P^2) - expval(P)^2) = sqrt(p_0^2 + hbar^2/(2 Delta^2) - p_0^2) = hbar/ (sqrt(2) Delta) $
]
#שאלה(כותרת: "אופרטור ההתפתחות בזמן עבור חלקיק תחת כוח קבוע (בונוס)", מזהה: <2>, [
  נתון חלקיק בעל מסה $m$ הנע תחת כוח קבוע $f$ במרחב. ההמילטוניאן נתון על ידי:
  $ H = P^2 / (2m) - f X $
])

#סעיף(מזהה: <2.א>, [
  מצאו את הפתרונות הסטציונריים של משוואת שרדינגר, והציגו אותם בהצגת התנע. סמנו פתרונות אלו ב-$braket(p, E) = tilde(psi)_E (p)$.

  *הערה:* אלמנטי המטריצה של האופרטור $X$ בהצגת התנע: $mel(p, X, f) = i hbar pdv(, p) tilde(f)(p)$.
])
נשתמש במשוואת שרדינגר הבלתי-תלויה בזמן:
$ H ket(E) = E ket(E) $
נציב את $H$ ונכפול משמאל ב-$bra(p)$:
$ mel(p, P^2/(2m) -f X, E) = E braket(p, E) = E tilde(psi)_E (p) $
כמו כן:
$
  mel(p, P^2/(2m) -f X, E) = mel(p, P^2/(2m), E) - f mel(p, X, E) = p^2/(2m) tilde(psi)_E (p) - f i hbar pdv(, p) tilde(psi)_E (p) = E tilde(psi)_E (p)
$
נקבל משוואה דיפרנציאלית:
$ (p^2/(2m) - E) tilde(psi)_E (p) = f i hbar pdv(, p) tilde(psi)_E (p) $
#תשובה[
  $ tilde(psi)_E (p) = C exp(i/(f hbar) (p E - p^3/(6m))) $]

#pagebreak()
#סעיף(מזהה: <2.ב>, [
  דרשו את תנאי הנרמול הבא:
  $ braket(E, E') = delta(E - E') $
  על מנת למצוא את מקדם הנרמול שכתבתם בסעיף א'.
])
$
  braket(E, E') &= integral_(-oo)^oo braket(E, p)braket(p, E') dd(p) = integral_(-oo)^oo (tilde(psi)_E (p))^* tilde(psi)_E' (p) dd(p) = integral_(-oo)^oo abs(C)^2 e^(-i/(f hbar) p(E-E')) dd(p) \
  &= 2 pi |C|^2 delta(1/(f hbar)(E-E')) = 2 pi |C|^2 abs(f hbar) delta(E-E') = 2 pi f hbar |C|^2 delta(E-E') =^! delta(E-E')
$
#תשובה[
  $ C = 1/sqrt(2 pi f hbar) $
]

#סעיף(מזהה: <2.ג>, [
  מצאו את $tilde(psi)_E (p, t)$.
])
משום ש-$tilde(psi)_E (p)$ מצבים עצמיים, בשביל למצוא את
$tilde(psi)_E (p, t)$
מספיק לכפול במופע $e^(-i/hbar E t)$:
$
  tilde(psi)_E (p, t) = 1/sqrt(2 pi f hbar) e^(-i/hbar E t) e^(i/(f hbar) (p E - p^3/(6m))) = 1/sqrt(2 pi f hbar) e^(i/(f hbar) (E(p - f t) - p^3/(6m)))
$
#תשובה[
  $ tilde(psi)_E (p, t) = 1/sqrt(2 pi f hbar) e^(i/(f hbar) (E(p - f t) - p^3/(6m))) $
]

#pagebreak()
#סעיף(מזהה: <2.ד>, [
  השתמשו בתוצאות הסעיפים הקודמים כדי לחשב את אלמנטי המטריצה $mel(p, U(t), p')$, כאשר $U(t)$ הוא אופרטור ההתפתחות בזמן. הראו:
  $ mel(p, U(t), p') = e^(i (p'^3 - p^3) / (6 m hbar f)) delta(p - p' - f t) $
])
#let intoo = $integral_(-oo)^oo$
$
  1/C^2 mel(p, U(t), p') &= 1/C^2 intoo mel(p, U(t), E) braket(E, p') dd(E) = 1/C^2 intoo tilde(psi)_E(p, t) (tilde(psi)_E (p'))^* dd(E) \
  &= intoo exp(i/(f hbar) (E(p - f t) - p^3/(6m) - p'E + p'^3/(6m))) dd(E) \
  &= exp(i/(f hbar) (p'^3/(6m) - p^3/(6m))) intoo exp(i/(f hbar) E(p - f t - p')) dd(E) \
  &= 2 pi f hbar delta(p - f t - p') exp(i/(f hbar) (p'^3/(6m) - p^3/(6m)))
$
#תשובה[
  $ mel(p, U(t), p') = e^(i (p'^3 - p^3) / (6 m hbar f)) delta(p - p' - f t) $
]

#שאלה(כותרת: "חלקיק על טבעת (בונוס)", מזהה: <3>, [
  נתון חלקיק הנע על טבעת ברדיוס $R$. אופרטור המייצג את מדידת המיקום (זווית) של החלקיק נתון על ידי $Theta$, והוא מקיים:
  $ Theta ket(theta) = theta ket(theta) $
  בנוסף, נתון אופרטור תנע זוויתי המקיים:
  $ mel(theta, L, f) = -i hbar pdv(, theta) f(theta) $
])
#סעיף(מזהה: <3.א>, [
  נסמן: $L ket(l) = hbar l ket(l)$. מצאו את $braket(theta, l)$ עד כדי קבוע נרמול.
])
נסמן $psi_l (theta) = braket(theta, l)$ ונחשב:
$
  mel(theta, L, l) = hbar l braket(theta, l) \
  - i cancel(hbar) pdv(, theta)psi_l (theta) = cancel(hbar) l psi_l (theta) \
  pdv(, theta)psi_l (theta) -i l psi_l (theta) = 0
$
#תשובה[
  $ braket(theta, l) = C e^(i l theta) $
]
#סעיף(מזהה: <3.ב>, [
  היעזרו בתנאי השפה עבור טבעת, ומצאו את הספקטרום של $L$. מצאו את הנרמול המתאים לסעיף הקודם.
])
$theta$ ו-$theta+2pi$ מייצגים אותה נקודה על הטבעת, לכן:
$ braket(theta, l) = braket(theta+2pi, l) => C e^(i l theta) = C e^(i l(theta+2pi)) $
נחלק את שני אגפי המשוואה ב-$C e^(i l theta)$ ונקבל:
$ e^(i l 2pi) = 1 $
כלומר $l$ יכול להיות כל מספר שלם.

#line(length: 100%, stroke: .25pt + gray)
בשביל לנרמל את המצבים, נדרוש שההסתברות למצוא את החלקיק בזווית כלשהי תהיה $1$:
$
  1 = integral_0^(2pi) abs(braket(theta, l))^2 dd(theta) = C^2 integral_0^(2pi) abs(e^(i l theta))^2 dd(theta) = C^2 integral_0^(2pi) 1 dot dd(theta) = 2 pi |C|^2
$
#תשובה[
  $ l in ZZ, quad C = 1/sqrt(2pi) $
]

#סעיף(מזהה: <3.ג>, [
  חשבו את $[Theta, L]$.
])
ניקח פונקציית גל $psi(theta)$ ונחשב מפורשות:
$ Theta L psi(theta) = Theta(mel(theta, L, psi)) = Theta(-i hbar pdv(, theta) psi(theta)) = -i hbar theta psi'(theta) $
$ L Theta psi(theta) = L(mel(theta, Theta, psi)) = L(theta psi(theta)) = -i hbar (psi(theta) + theta psi'(theta)) $
נחשב את הקוממטור:
$
  [Theta, L]psi(theta) = (Theta L - L Theta)psi(theta) = -i hbar(theta psi'(theta) - psi(theta) - theta psi'(theta)) = i hbar psi(theta)
$
#תשובה[
  $ [Theta, L] = i hbar $
]

#pagebreak()
#סעיף(מזהה: <3.ד>, [
  ההמילטוניאן של חלקיק על טבעת נתון על ידי:
  $ H = L^2 / (2 I) $
  כאשר $I$ הוא מומנט ההתמד של חלקיק נקודתי על טבעת ברדיוס $R$:
  $ I = m R^2 $
  מצאו את האנרגיות העצמיות ואת המצבים העצמיים של $H$.
])
משום ש-$H$ פונקציה של $L$, המצבים העצמיים של $H$ הם המצבים העצמיים של $L$. נסמן את האנרגיות העצמיות ב-$E_l$ ונקבל:
$
  H ket(l) = E_l ket(l) => H ket(l) = L^2/(2I) ket(l) = (hbar^2 l^2)/(2I) ket(l) = E_l ket(l) => E_l = (hbar^2 l^2)/(2I)
$
#תשובה[
  האנרגיות העצמיות הן:
  $ E_l = (hbar^2 l^2)/(2I) $
  המצבים העצמיים הם $ket(l)$ כאשר $l in ZZ$.
]

#שאלה(כותרת: "ניסוי במדידת מיקום אטום", מזהה: <4>, [
  במהלך ניסוי נמדד מיקום של אטומים במרווחי זמנים של $2, 4, 6, 8$ מיקרו-שניות. מיקום האטום נמדד ב"בינים" (bins) ברוחב מיקרון. ידוע כי האטומים הוכנו עם פונקציית גל התחלתית גאוסיאנית (בהצגת המקום), ברוחב $0.07$ מיקרון. הדאטה הנמדד מצורף בקובץ CSV לגיליון הבית.
])
#סעיף(מזהה: <4.א>, [
  ציירו את פונקציית התפלגות המיקום בכל אחד מהזמנים.
])
#figure(
  image("distributions.svg", width: 85%),
  caption: [התפלגות מיקום האטום בזמנים שונים],
)

#pagebreak()
#סעיף(מזהה: <4.ב>, [
  עבור כל אחת מההתפלגויות שקיבלתם בצעו התאמה לגאוסיאן עם רוחב $Delta$ (כפי שהוגדר בכיתה) ממורכז בראשית, והציגו כל גאוסיאן על גבי פונקצית ההתפלגות המתאימה לו בסעיף הקודם.
])
נבצע התאמה לכל התפלגות לפונקציה מהצורה הבאה:$ P(x) = A e^(-x^2 / Delta^2) $
כאשר הפרמטרים החופשיים להתאמה הם האמפליטודה $A$ ורוחב חבילת הגלים $Delta$.

#figure(
  image("distributions_fit.svg", width: 85%),
  caption: [התאמות גאוסיאניות להתפלגויות מיקום האטום],
)

#סעיף(מזהה: <4.ג>, [
  קבלו את $Delta$ כפונקציה של הזמן.
])
מתוך ההתאמות הגאוסיאניות שבוצעו בסעיף הקודם, קיבלנו את ערכי הרוחב $Delta(t)$ הבאים עבור כל אחד מהזמנים:

#align(center)[
  #table(
    columns: (1fr, 1.5fr),
    align: center,
    [*זמן* ($t$ [$upright(mu s)$])], [*רוחב* ($Delta(t)$ [$upright(mu m)$])],
    [$2$], [#דלתא_2],
    [$4$], [#דלתא_4],
    [$6$], [#דלתא_6],
    [$8$], [#דלתא_8],
  )
]

#pagebreak()
#סעיף(מזהה: <4.ד>, [
  בצעו התאמה לינארית עבור הנתונים שמצאתם עבור $Delta$.
])
נבצע התאמה לינארית של רוחב חבילת הגלים $Delta(t)$ כפונקציה של הזמן $t$:
$ Delta(t) = a t + b $
מתוך ההתאמה הלינארית קיבלנו את ערכי הפרמטרים הבאים:
- השיפוע: $a = #שיפוע$
- החיתוך: $b = #חיתוך$


#figure(
  image("width_fit.svg", width: 85%),
  caption: [התאמה לינארית של רוחב חבילת הגלים כפונקציה של הזמן],
)

#pagebreak()
#סעיף(מזהה: <4.ה>, [
  התאימו את שיפוע הגרף מהסעיף הקודם להתנהגות של המרחות פונקצית הגל בזמנים מאוחרים, וחשבו ממנו את המסה.
])
התפשטות רוחב חבילת הגלים של חלקיק חופשי נתונה לפי הנוסחה:
$ Delta(t) = sqrt(Delta_0^2 + (hbar^2 t^2) / (m^2 Delta_0^2)) = Delta_0 sqrt(1 + (hbar t / (m Delta_0^2))^2) $
בזמנים מאוחרים, כאשר $hbar t / (m Delta_0^2) >> 1$, האיבר השני תחת השורש דומיננטי ונקבל את הקירוב הלינארי:
$ Delta(t) approx hbar / (m Delta_0) t $
ולכן שיפוע הגרף $a$ מקיים:
$ a = hbar / (m Delta_0) $
מכאן נוכל לחשב את המסה של האטום:
$ m = hbar / (a Delta_0) = (1.05457 times 10^(-34)) / (0.1349 times #box[$0.07$]) = #מסה_קג = #מסה_אמו $

#תשובה[
  מסת האטום היא $m approx #מסה_אמו$.
]

#סעיף(מזהה: <4.ו>, [
  לאיזה אטום הדאטה מתאים?
])
המסה שקיבלנו קרובה למסה של אטום ליתיום ובפרט לאיזוטופ  $isotope("Li", a: 7)$ שמסתו האטומית היא $7.016 "u"$. הסטייה היא של פחות מ-$4%$.

#תשובה[
  הנתונים מתאימים לאטום $isotope("Li", a: 7)$.
]
