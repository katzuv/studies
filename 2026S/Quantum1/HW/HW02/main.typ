#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "2",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 5, day: 23),
)

#let e1 = $e_1$
#let e1k = $ket(e1)$
#let e1b = $bra(e1)$
#let e2 = $e_2$
#let e2k = $ket(e2)$
#let e2b = $bra(e2)$

#let ps = $ket(psi)$
#שאלה(כותרת: "אופרטורים בסיסיים", [
  נתון מרחב הילברט עם שני מצבים: #e1k, #e2k. המצבים מנורמלים ואורתוגונליים:

  $ braket(#e1, #e2) = delta_(i j) $
  נסמן את הבסיס האורתוגונלי $cal(B)$:
  $ cal(B) = {e1k, e2k} = {vec(1, 0), vec(0, 1)} $
  נתונים שני אופרטורים $A, B$ המוגדרים על ידי פעולתם על #e1k, #e2k:
  $
    & A #e1k = #e1k, #h(2em)   && A #e2k = - #e2k \
    & B #e1k = i #e2k, #h(2em) && B #e2k = -i #e1k
  $


  כמו כן, נתון מצב:

  $ |psi⟩ = 1 / sqrt(2) (#e1 + i#e2) $
])

#let ab = $A_cal(B)$
#let b_b = $B_cal(B)$

#סעיף[
  רשמו את ההצגה המטריצית של האופרטור $A$ לפי הבסיס $cal(B)$. מצאו את הצמוד ההרמיטי של $A$, והראו כי גם הוא הרמיטי.
]
נשתמש בהגדרת אלמנטי מטריצה:
$
  & a_(11) = mel(e1, A, e1) = braket(e_1, e_1) stretch(=)_"בסיס אורתוגונלי" 1 \
  & a_(12) = mel(e1, A, e2) = -braket(e_1, e_2) = 0 \
  & a_(21) = mel(e2, A, e1) = braket(e_2, e_1) = 0 \
  & a_(22) = mel(e2, A, e2) = -braket(e_2, e_2) = -1
$
מכאן נקבל את המטריצה של $A$ לפי הבסיס $cal(B)$:
#תשובה[
  $ A_cal(B) = mat(a_(11), a_(12); a_(21), a_(22)) = mat(1, 0; 0, -1) $
]
כעת נמצא את הצמוד ההרמיטי של $A$:
#תשובה[
  $ A^+_cal(B) = overline(mat(a_(11), a_(12); a_(21), a_(22))) = mat(1, 0; 0, -1) = ab $
]
כפי שניתן לראות, $A^+_cal(B) = A_cal(B)$, ולכן $A=A^+$ ולכן $A$ הוא אופרטור הרמיטי.
בנוסף:
#תשובה[
  $ (ab^+)^+ = overline(mat(1, 0; 0, -1)) = mat(1, 0; 0, -1) = ab $ ]
#let abdag = $ab^+$
כלומר גם $A^+ = A$ ולכן גם $A^+$ הוא הרמיטי.

#סעיף[
  מצאו את הערכים העצמיים $a_n$ והמצבים העצמיים $|a_n⟩$ של האופרטור $A$.
]
מצאנו מטריצה מייצגת אלכסונית של $A$, לכן הערכים העצמיים הם $a_1 = 1, a_2 = -1$. נפתור את משוואת הערכים העצמיים:
$
  & A ket(a_n) = mat(1, 0; 0, -1) vec(x, y) = a_n ket(a_n) = 1 vec(x, y) => \
  & vec(a, -b) = vec(a, b) => ket(a_n) = vec(1, 0)
$
עבור $a_2 = -1$:
$
  & A ket(a_2) = mat(1, 0; 0, -1) vec(x, y) a_2 ket(a_2) = -1 vec(x, y) => \
  & vec(a, -b) = vec(-a, b) => ket(a_2) = vec(0, 1)
$
לכן מצאנו את המצבים העצמיים:
#תשובה[
  $ a_1 = 1, ket(a_1) = vec(1, 0) $
  $ a_2 = -1, ket(a_2) = vec(0, 1) $
]

#pagebreak()
#סעיף[
  הראו מפורשות כי מתקיים פירוק היחידה עבור הבסיס
  $lr({|a_n chevron.r})$
]
$ sum_(n=1,2) ketbra(a_n) = ketbra(a_1) + ketbra(a_2) = mat(0, 0; 0, 1) + mat(1, 0; 0, 0) = mat(1, 0; 0, 1) = bb(1) $
#תשובה[
  $ sum_(n=1,2) ketbra(a_n) = bb(1) $
]

#סעיף[
  רשמו את האופרטורים $A,B$ בעזרת הבסיס
  ${ket(a_n)}_(n=1,2)$
  בכתיב דיראק. האם האופרטור $B$ הוא אופרטור הרמיטי?
]
$
  & b_(11) = mel(e1, B, e1) = i braket(e_1, e_2) stretch(=)_"בסיס אורתוגונלי" 0 \
  & b_(12) = mel(e1, B, e2) = -i braket(e_1, e_2) = -i \
  & b_(21) = mel(e2, B, e1) = i braket(e_2, e_1) = i \
  & b_(22) = mel(e2, B, e2) = -i braket(e_2, e_1) = 0
$
מכאן:
$ B_cal(B) = mat(0, -i; i, 0) $

נרשום את האופרטורים בבסיס המבוקש. קיבלנו כי ${a_n} = {e_n}$, לכן:
$ A = a_11 ketbra(a_1) + a_12 ketbra(a_1, a_2) + a_21 ketbra(a_2, a_1) + a_22 ketbra(a_2) = ketbra(a_1) - ketbra(a_2) $
$
  B = b_11 ketbra(a_1) + b_12 ketbra(a_1, a_2) + b_21 ketbra(a_2, a_1) + b_22 ketbra(a_2) = -i ketbra(a_1, a_2) +i ketbra(a_2, a_1)
$

נבדוק האם המטריצה המייצגת של הצמוד ההרמיטי של $B$ שווה למטריצה המייצגת של $B$:
$ B_cal(B)^+ = overline(mat(0, -i; i, 0)^T) = overline(mat(0, i; -i, 0)) = mat(0, -i; i, 0) = B_cal(B) $
#תשובה[
  $ A = ketbra(a_1) - ketbra(a_2), quad B = -i ketbra(a_1, a_2) +i ketbra(a_2, a_1) $
  $ B_cal(B) = mat(0, -i; i, 0), B_cal(B)^+ = B_cal(B) $
  לכן $B$ הוא אופרטור הרמיטי.
]

#pagebreak()
#סעיף[
  חשבו את פעולת האופרטורים $A,B$ על המצב $ps$. מה ניתן להסיק על המצב $ps$?
]
$ A ps = 1/sqrt(2)(A e1k + i A e2k) = 1/sqrt(2)(e1k - i e2k) $
$ B ps = 1/sqrt(2)(i e2k + e1k) = ps $
לכן:
#תשובה[
  $ A ps = 1/sqrt(2)(e1k - i e2k) $
  $ B ps = 1/sqrt(2)(e1k + i e2k) = 1 dot ps $
  כלומר $ps$ הוא וקטור עצמי של $B$ עם ערך עצמי $1$.
]

#סעיף[
  מצאו את הבסיס המלכסן של האופרטור $B$.
]
נמצא את הערכים העצמיים לפי הפולינום האופייני:
$ p(lambda) = abs(lambda I - B_cal(B)) = mdet(lambda, i; -i, lambda) = lambda^2 - 1 = 0 $
לכן הערכים העצמיים הם $lambda_1 = 1, lambda_2 = -1$. נפתור את משוואת הערכים העצמיים עבור $lambda_1$:
$
  B ket(b_1) = lambda_1 ket(b_1) => mat(0, -i; i, 0) vec(x, y) = 1 dot vec(x, y) => vec(-i y, i x) = vec(x, y) => vec(x, y) = vec(1, i)
$
עבור $lambda_2$:
$
  B ket(b_2) = lambda_2 ket(b_2) => mat(0, -i; i, 0) vec(x, y) = -1 dot vec(x, y) => vec(-i y, i x) = vec(-x, -y) => vec(x, y) = vec(1, -i)
$
ננרמל את הווקטורים העצמיים:
$ norm(ket(b_1)) = sqrt(|1|^2 + |i|^2) = sqrt(2), norm(ket(b_2)) = sqrt(|1|^2 + |-i|^2) = sqrt(2) $
#pagebreak()
לכן הבסיס המלכסן של $B$ הוא:
#תשובה[
  $ {1/sqrt(2) vec(1, i), 1/sqrt(2) vec(1, -i)} $
]


#שאלה(כותרת: "אופרטורים צמודים הרמיטית", [
  על סמך ההגדרה של אופרטור צמוד הרמיטי
  ($braket(u, T v) = braket(T^+u, v)$)
  הוכיחו את התכונות הבאות:
])
#סעיף[
  $ (T^+)^+ = T $
]
ניקח שני וקטורים במרחב, $u$ ו-$v$. מהגדרת הצמוד ההרמיטי נקבל:
$ braket(u, T^+ v) = braket((T^+)^+u, v) $
מתכונות המכפלה הפנימית נקבל גם:
$ braket(u, T^+ v) = braket(T^+ v, u)^* stretch(=)_"צמוד הרמיטי" braket(v, T u)^* = braket(T u, v) $
זה נכון לכל $u, v$. לכן:
#תשובה[
  $ (T^+)^+ = T $
]

#סעיף[
  כאשר $T$ אופרטור הפיך:
  $ (T^(-1))^+ = (T^+)^(-1) $
]
ניקח שני וקטורים במרחב, $u$ ו-$v$. נגדיר
$x = T u$.
נתון כי $T$ אופרטור הפיך, לכן קיים $T^(-1)$.
מהגדרת הצמוד ההרמיטי נקבל:
$ braket(x, v) = braket(T T^(-1)x, v) = braket(T^(-1) x, T^+v) = braket(x, (T^(-1))^+T^+v) $
מכיוון ששוויון זה מתקיים לכל $x, v$ במרחב, נקבל שוויון בין האופרטורים:$ I = (T^(-1))^+ T^+ $
כלומר
$(T^(-1))^+$ הוא האופרטור ההפוך של $T^+$, ולכן:
#תשובה[
  $ (T^(-1))^+ = (T^+)^(-1) $
]

#שאלה(כותרת: "אופרטורים נורמלים ואוניטריים", [
  נניח כי $T$ הוא אופרטור נורמלי, כלומר:
  $T^+T=T T^+$.
])
#סעיף(מזהה: <3.1>)[
  הראו כי $T$ לכסין.
]
משום שאנחנו עובדים מעל $CC$, ידוע כי יש ל־$T$ לפחות ערך עצמי אחד. יהי $ket(u_1)$ וקטור עצמי של $T$ המקיים $T ket(u_1) = lambda_1 ket(u_1)$.
נשלים בעזרת $ket(u_1)$ בסיס אורתונורמלי:
$cal(B) = {ket(u_1), ket(v_2), dots, ket(v_n)}$. נכתוב את $T$ בבסיס זה:
$
  T = t_(11) ketbra(u_1) + sum_(j=2)^n t_(1j) ketbra(u_1, v_j) + sum_(i=2)^n t_(i 1) ketbra(v_i, u_1) + underbrace(sum_(i=2)^n sum_(j=2)^n t_(i j) ketbra(v_i, v_j), T_perp)
$ <הגדרתי>
נפעיל את האופרטור על $ket(u_1)$:
$
  T ket(u_1) &= t_(11) ket(u_1) braket(u_1, u_1) + sum_(j=2)^n t_(1j) ket(u_1) braket(v_j, u_1) \
  &+ sum_(i=2)^n t_(i 1) ket(v_i) braket(u_1, u_1) + sum_(i=2)^n sum_(j=2)^n t_(i j) ket(v_i) braket(v_j, u_1)
$
משום שבחרנו בסיס אורתונורמלי, $braket(v_j, u_1) = 0$ עבור $j > 1$, ו-$braket(u_1, u_1) = 1$. לכן:
$
  T ket(u_1) = t_(11) ket(u_1) + sum_(i=2)^n t_(i 1) ket(v_i) = lambda_1 ket(u_1) => sum_(i=2)^n t_(i 1) ket(v_i) + (t_11 - lambda_1) ket(u_1) = 0
$
וקטורי בסיס בהגדרה בלתי תלויים אחד בשני, לכן לפי הגדרה נקבל:
$ forall i>1, t_(i 1) = 0; quad t_(11) = lambda_1 $
נציב חזרה ב@הגדרתי:
$ T = lambda_1 ketbra(u_1) + sum_(j=2)^n t_(1j) ketbra(u_1, v_j) + sum_(i=2)^n sum_(j=2)^n t_(i j) ketbra(v_i, v_j) $
נתון כי $T$ נורמלי, לכן:
$T^+T = T T^+$.
לכן גם אלמנטי המטריצה שלהם שווים:
$ mel(u_1, T^+T, u_1) = mel(u_1, T T^+, u_1) $
נחשב את שני האגפים. נתחיל מאגף שמאל:
$
  mel(u_1, T^+T, u_1) = lr((bra(u_1) T^+) (T ket(u_1))) = braket(T u_1) = braket(lambda_1 u_1) = lambda_1 lambda_1^* braket(u_1) = abs(lambda_1)^2
$ <עע1>
כעת לאגף ימין. נמצא ראשית את $T^+$:
$ T^+ = lambda_1^* ketbra(u_1) + sum_(j=2)^n t_(1 j)^* ketbra(v_j, u_1) + T_perp^+ $
נפעיל את שני צדי המשוואה על $ket(u_1)$ ונשתמש בעובדה שבידינו בסיס אורתונורמלי:
$ T^+ ket(u_1) = lambda_1^* ket(u_1) + sum_(j=2)^n t_(1 j)^* ket(v_j) $
כעת נחשב את אגף ימין, שהוא הנורמה בריבוע של $T^+ ket(u_1)$. נזכור כי הבסיס מנורמל:
$ mel(u_1, T T^+, u_1) = abs(lambda_1)^2 + sum_(j=2)^n |t_(1 j)|^2 $
לפי השוויון בין שני האגפים, נקבל:
$ abs(lambda_1)^2 = abs(lambda_1)^2 + sum_(j=2)^n |t_(1 j)|^2 => sum_(j=2)^n |t_(1 j)|^2 = 0 $
משום ש־$abs(t_(1 j))^2$ הם מספרים אי-שליליים שסכומם מתאפס, חייב להתקיים:
$ forall j>1, t_(1 j) = 0 $
נציב חזרה ב@הגדרתי:
$ T = lambda_1 ketbra(u_1) + T_perp $
כלומר המטריצה המייצגת של $T$ נראית כך:
$
  T = mat(
    lambda_1, 0, dots.h.c, 0;
    0, dots.down, , ;
    dots.v, , T_perp, ;
    0, , , dots.down
  )
$
משום שהמטריצה המייצגת הזו נורמלית, גם המטריצה המייצגת של $T_perp$ נורמלית. לכן $T_perp$ נורמלי, ונוכל לחזור על התהליך הנ"ל גם עבור $T_perp$: נמצא עבורו וקטור עצמי, נרוקן את השורה והטור הראשונים שלו (למעט האיבר הראשון במטריצה), נחזור על התהליך עבור $(T_perp)_perp$ וכן הלאה. נחזור על התהליך $n$ פעמים,
כאשר $n$ הוא ממד המרחב. כך נקבל מטריצה מייצגת אלכסונית ל-$T$, כלומר $T$ לכסין.

#סעיף[
  השתמשו בסעיף א' על מנת להראות שאופרטור אוניטרי הוא אופרטור לכסין.
]
אופרטור אוניטרי $T$ מקיים $T^+ T = T T^+ = I$. לכן $T$ נורמלי, ולכן לפי סעיף א' הוא לכסין.

#pagebreak()
#סעיף[
  הראו כי הע"ע של אופרטור אוניטרי מקיימים שערכם המוחלט הוא 1.
]
יהי $ket(v)$ וקטור עצמי מנורמל כלשהו של אופרטור אוניטרי $T$, עם ערך עצמי $lambda$. כלומר $T ket(v) = lambda ket(v)$.
בדומה לחישוב ב@עע1, נחשב את $mel(u, T^+T, u)$ בשתי דרכים.
מצד אחד, מכיוון ש-$T$ אוניטרי מתקיים $T^+ T = I$:
$ mel(v, T^+T, v) = mel(u, I, u) = braket(v, v) = 1 $
מצד שני, נפעיל את האופרטורים ישירות על הווקטור העצמי:
$ mel(v, T^+T, v) = braket(T v, T v) = braket(lambda v, lambda v) = lambda lambda^* braket(v, v) = abs(lambda)^2 $

#תשובה[
  מהשוואת התוצאות:
  $ forall i in NN, quad abs(lambda_i)^2 = 1 => abs(lambda_i) = 1 $
]

#שאלה(כותרת: "אופרטורי הטלה", [
  אופרטור לינארי המקיים $P^2=P$ נקרא #קותח("אופרטור הטלה").
])
#let p0 = $p_0$; #let p_1 = $p_1$
#סעיף[
  הראו כי לאופרטור הטלה קיימים רק שני ערכים עצמיים:
  $p_0 = 0, p_1 = 1$.
]
יהי $ket(v)!=0$ וקטור עצמי של אופרטור ההטלה $P$ עם ערך עצמי $p$. כלומר $P ket(v) = p ket(v)$.
נפעיל את $P$ על שני צדי המשוואה:
$ P^2 ket(v) = P(p ket(v)) = p P ket(v) = p^2 ket(v) $
ידוע כי $P^2 = P$, לכן:
$ P ket(v) = p^2 ket(v) $
נציב שוב
$P ket(v) = p ket(v)$ ונקבל:
$ p ket(v) = p^2 ket(v) => (p^2 - p) ket(v) = 0 $
כאמור, $ket(v) != 0$, לכן:
$ p^2 - p = p(p - 1) = 0 $
#תשובה[
  למשוואה זו שני פתרונות בלבד, ולכן מקבלים:
  $ p_0 = 0, p_1 = 1 $
]

#pagebreak()
#סעיף[
  אופרטור הטלה המקיים $P^+=P$ נקרא #קותח("הטלה אורתוגונלית"). הראו כי $P=ketbra(u)$ עבור $norm(u)=1$ הוא אופרטור הטלה אורתוגנלי על תת המרחב $"span"{ket(u)}$.
]
נראה ראשית כי $P$ הוא אופרטור הטלה. נחשב את $P^2$:
$ P^2 = (ketbra(u)) (ketbra(u)) = bra(u) braket(u) ket(u) = ket(u) norm(u)^2 bra(u) = 1 ketbra(u) = ketbra(u) = P $
כעת נחשב את $P^+$:
$ P^+ = (ketbra(u))^+ = bra(u)^+ ket(u)^+ = ketbra(u) = P $
יהי וקטור כלשהו $ket(v)$ במרחב. נחשב את $P ket(v)$:
$ P ket(v) = ket(u) underbrace(braket(u, v), "סקלר" = space c) = c ket(u) $
כלומר כל וקטור ש־$P$ פועל עליו, שייך לקבוצה הנפרשת על ידי $ket(u)$.
קיבלנו כי:
#תשובה[
  1. $P=P^2$, לכן $P$ הוא אופרטור הטלה.
  2. $P=P^+$, לכן $P$ הוא אופרטור הטלה אורתוגונלי.
  3. לכל $ket(v)$, $P ket(v) = c ket(u)$, כלומר $P$ מטיל כל וקטור על תת המרחב $"span"{ket(u)}$.
]

#שאלה(כותרת: "קומוטטורים", [
  בהרצאה הראינו כי אם לשני אופרטורים $A,B$ לכסינים קיים בסיס משותף של וקטורים עצמיים, אז
  $[A,B]=0$.
  בנסף, הראינו כי אם $[A,B]=0$
  ו#בולד[אין ניוון] עבור הערכים העצמיים של $A$, אז הבסיס העצמי של $A$ הוא הבסיס העצמי של $B$.

  כעת נוכיח את הטענה עבור המקרה המנוון. נניח כי $[A,B]=0$ וכי $A,B$ אופרטורים לכסינים. נסמן בנוסף $A ket(a) = a ket(a)$.
])
#סעיף(מזהה: <5.1>, [
  הראו כי $B ket(a)$ הוא וקטור עצמי של $A$ עם ערך עצמי $a$.
])
נתון כי $[A,B]=0$, כלומר $A B=B A$.
נחשב את $A(B ket(a))$:
$ A(B ket(a)) = A B ket(a) stretch(=)_(A B = B A) B A ket(a) = B a ket(a) = a dot B ket(a) $
#תשובה[
  קיבלנו כי
  $A(B ket(a)) = a (B ket(a))$,
  כלומר
  $B ket(a)$
  הוא וקטור עצמי של $A$ עם ערך עצמי $a$.
]

#pagebreak()
#סעיף[
  הניחו כי ישנם שני וקטורים עצמיים המתאימים לאותו ערך עצמי של $A$. נסמנם ב-
  $ket(a\, 1), ket(a\, 2)$.
  הראו כי ניתן למצוא צירופים לינאריים של וקטורים אלו שהם וקטורים עצמיים של $A$ וגם של $B$.
]
יהי וקטור $v=alpha ket(a\, 1) + beta ket(a\, 2)$, ואז:
$
  A ket(v) = & A (alpha ket(a\, 1) + beta ket(a\, 2)) = alpha A ket(a\, 1) + beta A ket(a\, 2) \
           = & alpha a ket(a\, 1) + beta a ket(a\, 2) = a (alpha ket(a\, 1) + beta ket(a\, 2))
$
כלומר, $ket(v)$ הוא וקטור עצמי של $A$ עם ערך עצמי $a$.

לפי הנתון, המרחב העצמי של $A$ המתאים לערך עצמי $a$ נפרש על ידי שני הווקטורים $ket(a\, 1)$ ו־$ket(a\, 2)$.
ב@5.1 ראינו כי אם מפעילים את $B$ על וקטור עצמי של $A$, מקבלים שוב וקטור עצמי של $A$, שניתן לרשום כצירוף לינארי של $ket(a\, 1), ket(a\, 2)$.
כמובן, גם $ket(a\, 1), ket(a\, 2)$ הם וקטורים עצמיים של $A$, לכן נסמן:
$ B ket(a\, 1) = b_11 ket(a\, 1) + b_21 ket(a\, 2), quad B ket(a\, 2) = b_12 ket(a\, 1) + b_22 ket(a\, 2) $

נדרוש כי $ket(v)$ יהיה וקטור עצמי של $B$ עם ערך עצמי $c$, כלומר נמצא $alpha$, $beta$ ו־$c$ כך שיתקיים:
$ B ket(v) = c ket(v) = c(alpha ket(a\, 1) + beta ket(a\, 2)) = alpha c ket(a\, 1) + beta c ket(a\, 2) $
נחשב במפורש:
$
  B ket(v) & = B(alpha ket(a\, 1) + beta ket(a\, 2)) = alpha B ket(a\, 1) + beta B ket(a\, 2) \
           & =
             alpha (b_11 ket(a\, 1) + b_21 ket(a\, 2)) + beta (b_12 ket(a\, 1) + b_22 ket(a\, 2)) \
           & =
             alpha b_11 ket(a\, 1) + alpha b_21 ket(a\, 2) + beta b_12 ket(a\, 1) + beta b_22 ket(a\, 2) \
           & =
             (alpha b_11 + beta b_12) ket(a\, 1) + (alpha b_21 + beta b_22) ket(a\, 2)
$
מהשוואת מקדמים נקבל:
$
  cases(alpha b_11 + beta b_12 = alpha c, alpha b_21 + beta b_22 = beta c) =>
  mat(
    b_11, b_12;
    b_21, b_22
  )
  vec(alpha, beta) = c vec(alpha, beta) => B_(2 times 2) vec(alpha, beta) = c vec(alpha, beta)
$
נתון כי $B$ לכסין, לכן גם $B_(2 times 2)$ לכסינה. לכן קיימים $alpha$, $beta$ ו־$c$ שפותרים את המשוואה (משוואת הערכים העצמיים).
#תשובה[
  הגדרנו $ket(v) = alpha ket(a \, 1) + beta ket(a \, 2)$. מצאנו כי קיימים $alpha$, ו־$c$ שמקיימים:
  1. $A ket(v) = a ket(v)$
  2. $B ket(v) = c ket(v)$
  כלומר, קיימים צירופים לינאריים של $ket(a\, 1)$ ושל $ket(a\, 2)$ שהם וקטורים עצמיים של $A$ וגם של $B$.
]

#pagebreak()
#סעיף[
  הכלילו למקרה בו יש $n$ וקטורים עצמיים המתאימים לערך עצמי מסוים של $A$.
]
#let setun = ${ket(u_i)}_(i=1)^n$
נסמן $setun = {ket(u_1), ket(u_2), dots, ket(u_n)}$ בסיס למרחב העצמי של $A$ המתאים לערך עצמי $a$.

יהי $ket(v) = sum_(i=1)^n alpha_i ket(u_i)$. נראה כי $ket(v)$ הוא וקטור עצמי של $A$ עם ערך עצמי $a$. נזכור ש-$A$ וסכימה הם פעולות לינאריות:
$
  A ket(v) = A sum_(i=1)^n alpha_i ket(u_i) = sum_(i=1)^n A (alpha_i ket(u_i)) = sum_(i=1)^n alpha_i A ket(u_i) = sum_(i=1)^n alpha_i a ket(u_i) = a sum_(i=1)^n alpha_i ket(u_i) = a ket(v)
$
כלומר, $ket(v)$ הוא וקטור עצמי של $A$ עם ערך עצמי $a$.
לפי הנתון, המרחב העצמי של $A$ המתאים לערך עצמי $a$ נפרש על ידי הבסיס
$setun$.
ב@5.1 ראינו כי אם מפעילים את $B$ על וקטור עצמי של $A$, מקבלים שוב וקטור עצמי של $A$, שניתן לרשום כצירוף לינארי של
$setun$.
כמובן, גם $setun$ הם וקטורים עצמיים של $A$, לכן נסמן:
$ B ket(u_i) = sum_(j=1)^n b_(j i) ket(u_j) $

נדרוש כי $ket(v)$ יהיה וקטור עצמי של $B$ עם ערך עצמי $c$, כלומר נמצא $alpha_i$ ו־$c$ כך שיתקיים:
$ B ket(v) = c ket(v) = c sum_(j=1)^n alpha_j ket(u_j) = sum_(j=1)^n c alpha_j ket(u_j) $
נחשב במפורש את אגף שמאל:
$
  B ket(v) & = B sum_(i=1)^n alpha_i ket(u_i) = sum_(i=1)^n alpha_i B ket(u_i) = sum_(i=1)^n alpha_i (sum_(j=1)^n b_(j i) ket(u_j)) =
             sum_(j=1)^n (sum_(i=1)^n b_(j i) alpha_i) ket(u_j)
$
מהשוואת מקדמים נקבל:
$
  sum_(i=1)^n b_(j i) alpha_i = c alpha_j <=> B_(n times n) vec(alpha_1, dots.v, alpha_n) = c vec(alpha_1, dots.v, alpha_n)
$
נתון כי $B$ לכסין, לכן גם $B_(n times n)$ לכסינה. לכן קיימים $alpha_i$, $beta_(i j)$ ו־$c$ שפותרים את המשוואה (משוואת הערכים העצמיים).

#תשובה[
  הגדרנו $ket(v) = sum_(i=1)^n alpha_i ket(u_i)$. מצאנו כי קיימים $alpha_i$, ו־$c$ שמקיימים:
  1. $A ket(v) = a ket(v)$
  2. $B ket(v) = c ket(v)$
  כלומר, קיימים צירופים לינאריים של $setun$ שהם וקטורים עצמיים של $A$ וגם של $B$.
]


#שאלה(כותרת: "אי-שוויונות", [
  יהיו $ket(u), ket(v)$ שני וקטורים במרחב מכפלה פנימית.
])
#סעיף[
  הוכיחו את אי-שוויון קושי-שוורץ:
  $ |braket(u, v)| <= abs(u) abs(v) $
]
נחלק למקרים. אם $ket(v) = 0$ או $ket(u) = 0$, אז $|braket(u, v)| = 0$ וגם $abs(u)abs(v)=0$. כלומר
$abs(braket(u, v)) <= abs(u) abs(v)$ כנדרש.

כעת נניח שמתקיים $ket(u) != 0$ ו־$ket(v) != 0$. לכן גם
$braket(u), braket(v)$ שונים מאפס.
נגדיר את הקבוע $c$ והווקטור $ket(w)$:
$ c = frac(braket(v, u), braket(v, v)), quad ket(w) = ket(u) - c ket(v) $
נשים לב כי מתקיים:
$ c braket(u, v) = frac(braket(u, v), braket(v, v)) braket(u, v) = (|braket(u, v)|^2)/braket(v) in RR $
משום שמונה ומכנה השבר, שניהם ממשיים. לכן גם מתקיים:
$ c braket(u, v) = (c braket(u, v))^* = c^* braket(v, u) $
נחשב את
$braket(w) = |w|^2$.
מתכונות המכפלה הפנימית, נקבל כי $|w|>=0$. מכאן:
$
  0 <= |w|^2 =& (bra(u)-c^*bra(v))(ket(u)-c ket(v)) = braket(u) - c braket(u, v) - underbrace(c^* braket(v, u), = c braket(u, v)) + c c^* braket(v) \
  =& |u|^2 - 2 (|braket(u, v)|^2)/braket(v) + abs(braket(v, u))^2/braket(v)^2 braket(v) = |u|^2 - 2 (|braket(u, v)|^2)/braket(v) + abs(braket(u, v))^2/braket(v) \
  =& |u|^2 - (|braket(u, v)|^2)/(|v|^2) >= 0
$
נזכור כי $ket(v)!=0$, לכן $|v|^2!=0$. מכאן:
$ (abs(u) abs(v))^2 >= abs(braket(u, v))^2 $
שני האגפים חיוביים, לכן:
#תשובה[
  $ abs(u) abs(v) >= abs(braket(u, v)) $

]
#pagebreak()
#סעיף[
  הוכיחו את אי-שוויון המשולש:
  $ |u+v| <= abs(u) + abs(v) $
]
נחשב את הביטוי הבא:
$
  |u+v|^2 = & braket(u + v, u + v) = braket(u) + braket(u, v) + braket(v, u) + braket(v) \
          = & |u|^2 + braket(u, v) + braket(u, v)^* + |v|^2
$

נזכור כי לכל מספר מרוכב מתקיים
$a + a^* = 2Re(a)$. לכן:
$ braket(u, v) + braket(u, v)^* = 2Re(braket(u, v)) $
מודול של מספר מרוכב תמיד גדול או שווה מגודל כל אחד מרכיביו, לכן:
$
  |u+v|^2 & = |u|^2 + 2Re(braket(u, v)) + |v|^2 \
          & <= |u|^2 + 2|braket(u, v)| + |v|^2 \
          & <=_("Cauchy-Schwarz") |u|^2 + 2abs(u)abs(v) + |v|^2 \
          & = (|u|+|v|)^2
$
שני האגפים הם נורמה או סכום נורמות של וקטורים, לכן הם אי-שליליים. לכן נוכל להוציא שורש משני האגפים ולקבל:
#תשובה[
  $ |u+v| <= |u| + |v| $
]
