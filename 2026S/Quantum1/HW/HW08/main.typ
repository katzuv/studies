#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *


#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "8",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 7, day: 5),
)

#שאלה(כותרת: "פולינומי הרמיט", מזהה: <1>, [
  ראינו כי מערכת של אוסילטור הרמוני ניתן לקבל על ידי הפעלה של אופרטור יצירה של $a^dagger$ על מצב היסוד $ket(0)$.
  פונקציות הגל הסטציונריות בהצגת המקום נראות כך:
  $ braket(x, n) = 1 / (pi^(1/4) sqrt(2^n n!)) (x - partial_x)^n e^(-x^2/2) $ <משוואת_מצבים>

  ניתן לבטא את @משוואת_מצבים על ידי פולינומי הרמיט $H_n$:
  $ braket(x, n) = 1 / (pi^(1/4) sqrt(2^n n!)) H_n e^(-x^2/2) $

  מתוך כך נוכל להסיק כי פולינומי הרמיט ניתנים על ידי:
  $ H_n = e^(x^2/2) (x - partial_x)^n e^(-x^2/2) $ <הגדרה_אופרטורית>

  לרוב, $H_n$ מוגדרים על ידי:
  $ H_n = (-1)^n e^(x^2) partial_x^n e^(-x^2) $ <הגדרה_רודריגז>
])

#סעיף(מזהה: <1.א>, [
  הראו כי ההגדרות הניתנות ב@הגדרה_אופרטורית וב@הגדרה_רודריגז שקולות. \
  *הדרכה:* תחילה הראו את יחס הרקורסיה הבא:
  $ H_(n+1) = 2x H_n - H'_n $
])
נתחיל מההגדרה הנתונה ב@הגדרה_אופרטורית. נמצא את $H_0$:
$ H_0 = e^(x^2/2) (x - partial_x)^0 e^(-x^2/2) = e^(x^2/2) e^(-x^2/2) = 1 $
נמצא את יחס הרקורסיה:
$
  H_(n+1) = e^(x^2/2) (x - partial_x)^(n+1) e^(-x^2/2) = e^(x^2/2)(x-partial_x)^n (x e^(-x^2/2) + x e^(-x^2/2)) = e^(x^2/2)(x-partial_x)^n (2x e^(-x^2/2))
$
מצד שני:
$
  2x H_n - H'_n &= 2x e^(x^2/2) (x - partial_x)^n e^(-x^2/2) - x e^(x^2/2)(x-partial_x)^n e^(-x^2/2) - e^(x^2/2) partial_x (x-partial_x)^n e^(-x^2/2) \
  &= e^(x^2/2)(x (x-partial_x)^n e^(-x^2/2) - partial_x (x-partial_x)^n e^(-x^2/2)) = e^(x^2/2)(x-partial_x)(x-partial_x)^n e^(-x^2/2) \
  &= e^(x^2/2)(x-partial_x)^(n+1) e^(-x^2/2) = H_(n+1)
$

כעת נראה אותו דבר עבור ההגדרה הנתונה ב@הגדרה_רודריגז:
$ H_0 = (-1)^0 e^(x^2) partial_x^0 e^(-x^2) = e^x^2 e^(-x^2) = 1 $
כעת נראה את יחס הרקורסיה. נמצא ראשית את $partial_x^(n+1) e^(-x^2)$:
$
  partial_x^n e^(-x^2) = H_n (-1)^n e^(-x^2) space.en backslash pdv(, x) \
  partial_x^(n+1) e^(-x^2) = (-1)^n e^(-x^2)(H'_n - 2x H_n)
$
נמצא את $H_(n+1)$:
$
  H_(n+1) &= (-1)^(n+1) e^x^2 partial_x^(n+1) e^(-x^2) = -cancel((-1)^n) cancel(e^x^2, inverted: #true) dot (-1)^n cancel(e^(-x^2), inverted: #true)(H'_n - 2x H_n) \
  &= 2x H_n - H'_n
$
#תשובה[
  הראינו שלשתי ההגדרות מתקיים:
  $ H_0 = 1, forall n in {0,1,2,...}, space H_(n+1) = 2x H_n - H'_n $
  לכן הן שקולות.
]

#סעיף(מזהה: <1.ב>, [
  חשבו ארבעה פולינומים ראשונים.
])
מצאנו כי $H_0 = 1$. נמצא את שלושת הפולינומים הבאים באמצעות כלל הרקורסיה:
$
  H_1 & = 2x H_0 - H'_0 = 2x dot 1 - 0 = 2x \
  H_2 & = 2x H_1 - H'_1 = 2x dot 2x - 2 = 4x^2 - 2 \
  H_3 & = 2x H_2 - H'_2 = 2x (4x^2 - 2) - 8x = 8x^3 - 4x - 8x = 8x^3 - 12x
$
#תשובה[
  $ H_0 = 1, H_1 = 2x, H_2 = 4x^2 - 2, H_3 = 8x^3 - 12x $
]

#pagebreak()
#סעיף(מזהה: <1.ג>, [
  השתמשו בתכונות של מצבים עצמיים של אופרטור הרמיטי על מנת להוכיח אורתוגונליות של פולינומי הרמיט:
  $ integral_(-oo)^oo H_m H_n e^(-x^2) dd(x) = 2^n n! sqrt(pi) delta_(m n) $
])
יהיו מצבים עצמיים $ket(n)$ ו־$ket(m)$ של $H$. משום ש־$H$ אופרטור הרמיטי, המצבים העצמיים שלו אורתונורמליים. לכן:
$
  delta_(m n) & = braket(m, n) = mel(m, I, n) = intoo underbrace(braket(m, x), braket(x, m)^*) braket(x, n) dd(x) \
              & = intoo (1/(pi^(1/4)sqrt(2^m m!)) H_m e^(-x^2/2))^* 1/(pi^(1/4)sqrt(2^n n!)) H_n e^(-x^2/2) dd(x) \
              & = 1/sqrt(pi 2^(n+m) n! m!) intoo H_m H_n e^(-x^2) dd(x)
$
נקבל:
$
  intoo H_m H_n e^(-x^2) dd(x) &= sqrt(pi 2^(n+m) n! m!) delta_(m n) = cases(sqrt(pi 2^(n+m) n! m!) delta_(n m)\, n!=m, sqrt(pi 2^(n+n) n! n!) delta_(n n)\, n=m) \
  &= cases(0\, n!=m, sqrt(pi) 2^n n! delta_(n n)\, n=m) = cases(sqrt(pi) 2^n n! dot 0 \, n!=m, sqrt(pi) 2^n n! delta_(n n) \, n=m) = 2^n n! delta_(n m) sqrt(pi)
$
#תשובה[
  $ intoo H_m H_n e^(-x^2) dd(x) = 2^n n! sqrt(pi) delta_(m n) $
]


#שאלה(כותרת: "התפתחות בזמן של אוסילטור הרמוני", מזהה: <2>, [
  נתון כי מערכת המתוארת בעזרת פוטינציאל הרמוני נמצאת בזמן $t = 0$ במצב הבא:
  $ psi(x, 0) = A (1 + sqrt((m omega) / hbar) x) exp(- 1/2 (m omega) / hbar x^2) $
])

#סעיף(מזהה: <2.א>, [
  מצאו את $psi(x, t)$.
])
ראינו בהרצאה את המצבים העצמיים של $H$ בפוטנציאל הרמוני. בפרט, שני המצבים הראשונים הם:
$
  xi_0(x) = ((m omega)/(pi hbar))^(1/4) e^(-(m omega)/(2 hbar) x^2), space.en xi_1(x) = 1/sqrt(2) (sqrt((m omega)/hbar)x - 1/(sqrt((m omega)/hbar)) pdv(, x)) e^(-(m omega)/(2 hbar) x^2)
$
נחשב מפורשות את $xi_1(x)$:
$
  xi_1(x) &= 1/sqrt(2) ((m omega)/(pi hbar))^(1/4)(sqrt((m omega)/hbar) x - 1/sqrt((m omega)/hbar) dot (-m omega)/(2hbar) dot 2x) e^(-(m omega)/(2 hbar) x^2) \
  &= sqrt(2) (1/pi)^(1/4) ((m omega)/hbar)^(3/4) x e^(-(m omega)/(2 hbar) x^2)
$
קיבלנו שניתן לרשום את $psi(x, 0)$ כסופרפוזיציה של שני המצבים העצמיים הראשונים:
$ psi(x, 0) = alpha_0 xi_0(x) + alpha_1 xi_1(x) $
נמצא את המקדמים:
$
  (A + A sqrt((m omega)/hbar) x) e^(-(m omega)/(2 hbar) x^2) = (alpha_0 ((m omega)/(pi hbar))^(1/4) + alpha_1 sqrt(2) (1/pi)^(1/4) ((m omega)/hbar)^(3/4) x) e^(-(m omega)/(2 hbar) x^2) => \
  alpha_0 = ((pi hbar)/(m omega))^(1/4) A, space alpha_1 = 1/sqrt(2) A ((pi hbar)/(m omega))^(1/4) space => space alpha_0 = sqrt(2) alpha_1
$
נדרוש שהמצב ההתחלתי יהיה מנורמל:
$
  1 = alpha_0^2 + alpha_1^2 = alpha_1^2 (2 + 1) = 3/2 A^2 sqrt((pi hbar)/(m omega)) space => A = sqrt(2/3) ((m omega)/(pi hbar))^(1/4)
$
// $
//   alpha_0 &= intoo xi_0(x) psi_0(x) dd(x) = intoo ((m omega)/(pi hbar))^(1/4) e^(-(m omega)/(2 hbar) x^2) A (1 + sqrt((m omega) / hbar) x) e^(- 1/2 (m omega) / hbar x^2) dd(x) \
//   &= A ((m omega)/(pi hbar))^(1/4) intoo (e^(-(m omega)/hbar x^2) + underbrace(cancel(sqrt((m omega)/hbar) x e^(-(m omega)/hbar x^2)), integral "odd" times "even" = 0)) dd(x) = A ((m omega)/(pi hbar))^(1/4) sqrt((pi hbar)/(m omega)) intoo underbrace(sqrt((m omega)/(pi hbar)) e^(-(m omega)/hbar x^2), "Gaussian") dd(x) \
//   &= A ((m omega)/(pi hbar))^(1/4) sqrt((pi hbar)/(m omega)) = A ((pi hbar)/(m omega))^(1/4)
// $
// $
//   alpha_1 &= intoo xi_1(x) psi_0(x) dd(x) \
//   &= intoo 2/sqrt(2) (1/pi)^(1/4) ((m omega)/hbar)^(3/4) x e^(-(m omega)/(2 hbar) x^2) A (1 + sqrt((m omega) / hbar) x) e^(- 1/2 (m omega) / hbar x^2) dd(x) \
//   &= (2A)/sqrt(2) (1/pi)^(1/4) ((m omega)/hbar)^(3/4) intoo (underbrace(cancel(x e^(-(m omega)/hbar x^2)), integral "odd" times "even" = 0) + sqrt((m omega)/hbar) x^2 e^(-(m omega)/hbar x^2)) dd(x) \
//   &= (2A)/sqrt(2) (1/pi)^(1/4) ((m omega)/hbar)^(5/4) dot 1/2 sqrt(pi) (hbar/(m omega))^(3/2) = A/sqrt(2) ((pi hbar)/(m omega))^(1/4)
// $
// קיבלנו כי $alpha_1 = alpha_0/sqrt(2)$.
// כעת, נדרוש שהמצב יהיה מנורמל:
// $
//   1 = alpha_0^2 + alpha_1^2 = alpha_0^2 (1 + 1/2) = 3/2 A^2 sqrt((pi hbar)/(m omega)) space => A = sqrt(2/3) ((m omega)/(pi hbar))^(1/4)
// $
// לכן $alpha_1 = 1/sqrt(3)$.
נקבל כי:
$
  alpha_1 = 1/sqrt(2) ((pi hbar)/(m omega))^(1/4) sqrt(2/3) ((m omega)/(pi hbar))^(1/4) = 1/sqrt(3), space alpha_0 = sqrt(2/3) space => \
  psi(x, 0) = 1/sqrt(3) (sqrt(2) xi_0(x) + xi_1(x))
$
נשתמש בביטוי ההתפתחות בזמן שראינו בהרצאה:
#תשובה[
  $
    psi(x, t) = 1/sqrt(3) (sqrt(2) e^(-1/2 i omega t) xi_0(x) + e^(-3/2 i omega t) xi_1(x)) \
    = sqrt(2/3)((m omega)/(pi hbar))^(1/4) (1 + e^(- i omega t) sqrt((m omega)/hbar) x )exp(- 1/2(i omega t +(m omega)/hbar x^2))
  $
]

#סעיף(מזהה: <2.ב>, [
  חשבו את $expval(X)(t)$ ואת $expval(P)(t)$.
])
נבטא את פונקציית הגל באמצעות בכתיב דיראק:
$
  bra(psi(k, t)) = 1/sqrt(3) (sqrt(2) e^(1/2 i omega t) bra(0) + e^(3/2 i omega t) bra(1), space ket(psi(x, t)) = 1/sqrt(3) (sqrt(2) e^(-1/2 i omega t) ket(0) + e^(-3/2 i omega t) ket(1)
$
ראינו כי ניתן לתאר את אופרטורי המיקום והתנע באמצעות אופרטורי הסולם:
$ X = sqrt(hbar/(2m omega)) (a + a^+), space P = -i sqrt(m hbar omega / 2) (a - a^+) $
נזכור כי מתקיימים הקשרים הבאים:
$ a ket(0) = 0, space a ket(1) = ket(0), space a^+ ket(0) = ket(1), space a^+ ket(1) = sqrt(2) ket(2) $
בנוסף, $braket(n, m) = delta_(n m)$. לכן:
$
  mel(0, a+a^+, 0) & = bra(0)(0 + ket(1)) = 0 \
  mel(0, a+a^+, 1) & = bra(0)(ket(0) + sqrt(2) ket(2)) = 1 \
  mel(1, a+a^+, 0) & = bra(1)(0 + ket(1)) = 1 \
  mel(1, a+a^+, 1) & = bra(1)(ket(0) + sqrt(2) ket(2)) = 0
$
כעת, נחשב את המבוקש:
$
  expval(X)(t) &= expval(X, psi(x, t)) = 1/3 sqrt(hbar/(2 m omega)) sqrt(2) (e^(1/2 i omega t) e^(-3/2 i omega t) + e^(3/2 i omega t) e^(-1/2 i omega t)) \
  = &1/3 sqrt(hbar/(m omega)) (e^(-i omega t) + e^(i omega t)) = 2/3 sqrt(hbar/(m omega)) cos(omega t)
$
כעת נעבור לחישוב $expval(P)(t)$. נחשב תחילה את אלמנטי המטריצה:
$
  mel(0, a-a^+, 0) & = bra(0)(0 - ket(1)) = 0 \
  mel(0, a-a^+, 1) & = bra(0)(ket(0) - sqrt(2) ket(2)) = 1 \
  mel(1, a-a^+, 0) & = bra(1)(0 - ket(1)) = -1 \
  mel(1, a-a^+, 1) & = bra(1)(ket(0) - sqrt(2) ket(2)) = 0
$
לכן:
$
  expval(P)(t) &= expval(P, psi(x, t)) = -i/3 sqrt((m hbar omega) / 2) sqrt(2) (e^(1/2 i omega t) e^(-3/2 i omega t) - e^(3/2 i omega t) e^(-1/2 i omega t)) \
  &= -i/3 sqrt(m hbar omega) (e^(-i omega t) - e^(i omega t)) = -2/3 sqrt(m hbar omega) sin(omega t)
$
#תשובה[
  $ expval(X) = 2/3 sqrt(hbar/(m omega)) cos(omega t), space.en expval(P) = -2/3 sqrt(m hbar omega) sin(omega t) $
]

#שאלה(כותרת: "יחסי אנטי חילוף", מזהה: <3>, [
  נגדיר יחסי אנטי חילוף באופן הבא:
  $ {A, B} = A B + B A $

  נתון המילטוניאן
  $H = b^+ b$,
  כאשר:
  $ {b^+, b^+} = {b, b} = 0 , space space {b^+, b} = 1 $
])

#סעיף(מזהה: <3.א>, [
  הראו כי הספקטרום אי שלילי.
])
נתחיל ממשוואת הערכים העצמיים:
$
  H ket(E) = E ket(E) \
  mel(E, H, E) = E braket(E, E)
$
נגדיר $ket(phi.alt) = b ket(E)$:
$ mel(E, H, E) = mel(E, b^+ b, E) = braket(phi.alt) >= 0 $
וזאת מתכונות המכפלה הפנימית. נקבל מאגף ימין של המשוואה:
$ E underbrace(braket(E, E), >0) >= 0 $
לכן נקבל כי $E>=0$ כמבוקש.

#סעיף(מזהה: <3.ב>, [
  נתון כי $b ket(n) = 0$. מהו $n$?
])
נתחיל ממשוואת הערכים העצמיים:
$
  H ket(n) = n ket(n) => H ket(n) = b^+ underbrace(b ket(n), 0) = 0 b^+ = 0
$
כלומר, נקבל $n ket(n) = 0$. משום ש-$ket(n)$ וקטור עצמי, $ket(n)!=0$. לכן:
#תשובה[
  $ n = 0 $
]

#pagebreak()
#סעיף(מזהה: <3.ג>, [
  נתון כי $b^dagger ket(m) = 0$. מהו $m$?
])
נבטא ראשית את $b^+ b$ באמצעות יחס האנטי־חילוף הנתון:
$ {b^+, b} = b^+ b + b b^+ = bb(1) => b^+ b = bb(1) - b b^+ $
נציב במשוואת הערכים העצמיים:
$
  m ket(m) = H ket(m) = b^+ b ket(m) = (bb(1) - b b^+)ket(m) = ket(m) - b(b^+ ket(m)) = ket(m) - b dot 0 = 1 dot ket(m)
$
#תשובה[
  $ m = 1 $
]

#סעיף(מזהה: <3.ד>, [
  בהינתן ש־$b ket(n) != 0$, הראו כי $b ket(n)$ וקטור עצמי של $H$. מהו הערך העצמי?
])
נתחיל ממשוואת הערכים העצמיים:
$ H (b ket(n))= b^+ b (b ket(n)) = b^+ (b b) ket(n) = b^+ b^2 ket(n) $
נמצא את $b^2$ באמצעות יחס האנטי־חילוף הנתון:
$ 0 = {b, b} = b b + b b = 2 b^2 => b^2 = 0 $ <רגיל_בריבוע>
נציב חזרה:
$ H (b ket(n)) = b^+ 0 = 0 = 0 dot b ket(n) $
#תשובה[
  $b ket(n)$ הוא וקטור עצמי של $H$ עם ערך עצמי $0$.
]

#pagebreak()
#סעיף(מזהה: <3.ה>, [
  בהינתן ש־$b^dagger ket(n) != 0$, הראו כי $b^dagger ket(n)$ וקטור עצמי של $H$. מהו הערך העצמי?
])
נתחיל ממשוואת הערכים העצמיים:
$ H (b^+ ket(n)) = b^+ b b^+ ket(n) = b^+ (b b^+) ket(n) $
נמצא את $b b^+$:
$ {b^+, b} = b^+ b + b b^+ = bb(1) => b b^+ = bb(1) - b^+b $
נציב:
$ b^+(b b^+) ket(n) = b^+ (bb(1) - b^+ b) ket(n) = b^+ ket(n) - (b^+)^2 b ket(n) $
ראינו כי $b b = 0$. נפעיל צמוד על המשוואה:
$ 0^* = (b b)^+ = b^+ b^+ = (b^+)^2 => (b^+)^2 = 0 $ <פגיון_בריבוע>
נציב חזרה:
$ H (b^+ ket(n)) = b^+ ket(n) - (b^+)^2 b ket(n) = b^+ ket(n) - 0 dot b ket(n) = 1 dot b^+ ket(n) $
#תשובה[
  $b^+ ket(n)$ הוא וקטור עצמי של $H$ עם ערך עצמי $1$.
]

#pagebreak()
#סעיף(מזהה: <3.ו>, [
  מצאו את הערכים העצמיים המותרים של $H$ ואת המימד של מרחב ההילברט במקרה בו מצב היסוד אינו מנוון.
])
נצא מהמצבים העצמיים שאנחנו מכירים ונראה האם נוכל ליצור מצבים חדשים באמצעות הפעלת #box[$b$ ו־$b^+$].

נגדיר את $ket(0)$ להיות המצב העצמי של $H$ עם ערך עצמי $0$. נקבל כי $b ket(0) = 0$. זאת משום כי, אם נסמן $ket(psi) = b ket(0)$:
$ braket(psi) = mel(0, b^+ b, 0) = mel(0, H, 0) = 0 braket(0) = 0 $
ומתקיים $norm(b ket(0)) = 0 <=> b ket(0) = 0$.

כעת נפעיל את $b^+$ ונסמן $ket(phi.alt) = b^+ ket(0)$. מ@3.ג נקבל כי $ket(phi.alt) != 0$, אחרת הערך העצמי של $ket(0)$ היה $1$ ולא $0$ כפי שהגדרנו. מ@3.ה נקבל כי $ket(phi.alt)$ הוא מצב עצמי עם ערך עצמי $1$. נגדיר $ket(1) = b^+ ket(0)$.

סיכום ביניים של המצבים העצמיים שמצאנו:
1. $ket(0)$ עם ערך עצמי $0$.
2. $ket(1)$ עם ערך עצמי $1$.

נראה אם נוכל ליצור מצבים נוספים. נפעיל את $b$ על $ket(0)$ שוב:
$ b b ket(0) = b^2 ket(0) = 0 ket(0) $
וזאת מ@רגיל_בריבוע. לכן סולם המצבים נקטע כאן.
כעת נפעיל שוב את $b^+$ על $ket(0)$:
$ b^+ b^+ ket(0) = (b^+)^2 ket(0) = 0 ket(0) = 0 $
וזאת מ@פגיון_בריבוע. לכן, סולם האנרגיה עוצר כאן.

נפעיל את $b$ ואת $b^+$ על $ket(1)$:
$ b ket(1) = b b^+ ket(0) = (bb(1) - b^+ b) ket(0) = ket(0) - b^+ 0 = ket(0) $
כלומר לא יצרנו מצב עצמי חדש.
$ b^+ ket(1) = b^+ b^+ ket(0) = (b^+)^2 ket(0) = 0 ket(0) $
#תשובה[
  לא יכולנו ליצור מצבים עצמיים נוספים מאלו שקיבלנו, לכן הערכים העצמיים המותרים הם $0$ ו-$1$ והם אינם מנוונים. לכן, ממד המרחב הוא $2$.
]

#שאלה(כותרת: [מולקולת $"HCl"$], מזהה: <4>, [
  מולקולת $"HCl"$ היא מצב קשור של אטום מימן ואטום כלור. היות והכלור כבד יותר מהמימן, אפשר לחשוב על תנועת המימן סביב מולקולת הכלור (שנמצאת במקומה). הפוטנציאל עבור המימן הוא:
  $ U = D (1 - e^(-a(x-x_0)))^2 - D $
  $ D = 4.618 "eV" $
  $ a = 1.869 dot 10^(10) space "m"^(-1) $
  $ x_0 = 1.275 dot 10^(-10) "m" $

  העריכו את האנרגיה הנדרשת על מנת לעורר את המולקולה ממצב היסוד למצב המעורר הראשון.
])
נתחיל מלמצוא את נקודת המינימום של הפוטנציאל:
$
  U'(x) = 2 D(1-e^(-a(x-x_0))) a underbrace(e^(-a(x-x_0)), >0) = 0 \
  e^(-a(x-x_0)) = 1 => x_"min" = x_0
$
בשביל לפשט את החישובים נחליף את $x$ ב־$y = x-x_0$. כלומר, הפוטנציאל הוא:
$ U(y) = D(1-e^(-a y))^2 - D, space y_"min" = 0 $
עבור סטייה קלה $var(y)$ מהמינימום, נבצע קירוב טיילור:
$ 1 - e^(-a var(y)) approx 1 - (1 + (-a var(y))^1/1! + (-a var(y))^2/2!) = a var(y) - a^2/2 var(y)^2 $
$ U(var(y)) approx D(a var(y) - a^2/2 var(y)^2)^2 - D approx D a^2 var(y)^2 - D $
וזאת אחרי שהזנחנו סדרים גבוהים. נשווה את $U(y)$ לפונקציית פוטנציאל של מתנד הרמוני קלאסי:
$ U(y) = V(x) => -D + D a^2 y^2 = V_0 + 1/2 m omega^2 x^2 $
מהשוואת מקדמים נקבל:
$ 1/2 omega^2 = D a^2 => omega = sqrt((2 D a^2)/m) $
אנרגיית העירור הראשונה היא:

#let hbar_v = 1.054e-34
#let eV = 1.602e-19
#let D_v = 4.618 * eV
#let a_v = 1.869e10
#let m_v = 1.008 * 1.6605e-27
#let omega_v = calc.sqrt((2 * D_v * calc.pow(a_v, 2)) / m_v)
#let DeltaE = (hbar_v * omega_v) / eV
#let DeltaE_rounded = calc.round(DeltaE, digits: 3)
#תשובה[
  $ Delta E = hbar omega approx hbar sqrt((2 D a^2)/m) approx #DeltaE_rounded "eV" $
]
