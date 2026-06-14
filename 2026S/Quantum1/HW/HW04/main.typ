#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *

#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "4",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 6, day: 13),
)

#let psi1 = $ket(psi_1)$; #let psi2 = $ket(psi_2)$
#let c1 = $C_1$; #let c2 = $C_2$
#שאלה(כותרת: "נרמול ומדידות במרחב תלת־מימדי", מזהה: <1>, [
  נתון מרחב מצבים תלת מימדי, בעל המצבים $ket(1), ket(2), ket(3)$. המצבים מקיימים $braket(i, j) = delta_(i, j)$. נתון $ket(psi)$ מנורמל, מהצורה הבאה:

  1. $ psi1 = c1 (ket(1) + 1/2 ket(2)) $
  2. $ psi2 = 1/3 ket(1) + c2 (ket(2) + ket(3)) $

  עבור כל אחד מהמצבים הנ"ל:
])

#סעיף(מזהה: <1.א>, [
  מצאו את $C$.
])
$ket(psi)$  וקטור מנורמל, לכן נמצא את הנורמה שלו ונדרוש שהיא תהיה שווה ל־$1$. נזכור כי המצבים הנתונים מאונכים זה לזה:
$
  norm(psi1)^2 & = braket(psi_1, psi_1) = c1^*(bra(1)+1/2 bra(2)) dot c1(ket(1)+1/2ket(2)) \
               & = |c1|^2(braket(1) + 1/2 braket(2, 1) + 1/2 braket(1, 2) + 1/4 braket(2))
                 stretch(=)_(braket(i, j)=delta_(i j)) |c1|^2(1+1/4) = 5/4 |c1|^2 = 1
$
נפתח את הסוגריים בהגדרת $psi2$:
$ psi2 = 1/3ket(1) + c2 ket(2) + c2 ket(3) $
נחשב את הנורמה בריבוע ונזכור כי המצבים אורתוגונלים זה לזה:
$
  norm(psi2)^2 &= braket(psi_2, psi_2) = (1/3)^2 braket(1) + |c2|^2(braket(2)+braket(3)) = 1/9 + 2|c2|^2=1 => |c2|^2 = 4/9
$
#תשובה[
  $ c1 = e^(i theta) 2/sqrt(5), quad c2 =e^(i theta) 2/3, theta in RR $
]

#pagebreak()
#סעיף(מזהה: <1.ב>, [
  מה ההסתברות למדוד את המצב $ket(3)$ במדידה של $ket(psi)$?
])
$ p_1 = |braket(psi_1, 3)|^2 = 4/5 lr(|braket(1, 3) + 1/2braket(2, 3)|)^2 = 0 $
$ p_2 = |braket(psi_2, 3)|^2 = lr(|1/3braket(1, 3) + 2/3(braket(2, 3) + braket(3, 3))|)^2 = 4/9 dot 1 = 4/9 $
#תשובה[
  $ p_1 = 0, quad p_2 = 4/9 $
]

#שאלה(כותרת: "אופרטורים ושינוי בסיס", מזהה: <2>, [
  נתונים המצבים $ket(r), ket(g), ket(b)$ אורתונורמליים במרחב תלת מימדי.
])

#סעיף[
  מצאו אופרטורים $U_i$ המקיימים:
]
#תתסעיף(מזהה: <2.1.א>, [
  $U_1 ket(psi) prop ket(r)$ לכל מצב $ket(psi)$.
])
נרצה אופרטור שיחזיר לכל מצב, מצב חדש שמורכב רק ממצב בסיס $ket(r)$. ננצל את העובדה שהמצבים מאונכים זה לזה:
$ U_1 = ketbra(r) $

#תתסעיף(מזהה: <2.1.ב>, [
  $U_2 ket(g) = ket(r)$ אבל לא משנה את $ket(r)$ ואת $ket(b)$.
])
נרצה אופרטור שאם נפעילו על $ket(g)$ נקבל $ket(r)$ אך לכל מצב בסיס אחר נקבל חזרה את אותו מצב:
$ U_2 = ketbra(r, g) + ketbra(b) + ketbra(r) $

#תתסעיף(מזהה: <2.1.ג>, [
  $U ket(r) = ket(g), space U ket(g) = ket(b), space U ket(b) = ket(r)$
])
נבנה את האופרטור כך שלכל מצב יחזיר את המצב המבוקש:
$ U_3 = ketbra(g, r) + ketbra(b, g) + ketbra(r, b) $
#תשובה[
  $
    U_1 = ketbra(r), quad U_2 = ketbra(r, g) + ketbra(b) + ketbra(r), quad U_3 = ketbra(g, r) + ketbra(b, g) + ketbra(r, b)
  $
]

#pagebreak()
#סעיף[נגדיר מצבים מנורמלים אך לא אורתוגונלים $ket(o), ket(y), ket(p)$ על ידי:
  $ ket(r) = 2 ket(o) - sqrt(3) ket(y) $
  $ ket(g) = -sqrt(2) ket(o) + ket(p) + sqrt(6) ket(y) $
  $ ket(b) = -2 ket(o) + sqrt(2) ket(p) + sqrt(3) ket(y) $]

#תתסעיף(מזהה: <2.2.א>, [
  בטאו את $ket(o), ket(y), ket(p)$ באמצעות $ket(r), ket(g), ket(b)$.
])
$ b = -underbrace((2ket(o) - sqrt(3)ket(y)), ket(r)) + sqrt(2)ket(p) => ket(p) = 1/sqrt(2)(ket(b) + ket(r)) $
נחלץ את
$-2 ket(o)$
מהמשוואה השלישית ונציב במשוואה השנייה:
$ -2 ket(o) = ket(b) - sqrt(2)ket(p) - sqrt(3) ket(y) $ <מ15>
נכפול את המשוואה השנייה ב-$sqrt(2)$ ונציב את הביטוי מ@מ15:
$
  sqrt(2) ket(g) = ket(b) - cancel(sqrt(2) ket(p)) - sqrt(3)ket(y) + cancel(sqrt(2)ket(p)) + 2sqrt(3)ket(y) => ket(y) = sqrt(2/3)ket(g) - 1/sqrt(3) ket(b)
$
נציב
$sqrt(3) ket(y)$
במשוואה הראשונה:
$ ket(r) = 2ket(o) + ket(b) - sqrt(2)ket(g) => ket(o) = 1/2 ket(r) + 1/sqrt(2)ket(g) - 1/2ket(b) $
#תשובה[
  $
    ket(p) = 1/sqrt(2)(ket(b) + ket(r)), quad ket(y) = sqrt(2/3)ket(g) - 1/sqrt(3) ket(b), quad ket(o) = 1/2 ket(r) + 1/sqrt(2)ket(g) - 1/2ket(b)
  $
]

#pagebreak()
#תתסעיף(מזהה: <2.2.ב>, [
  מכינים את המערכת במצב $ket(o)$. מה ההסתברות שנמדוד את המערכת במצב $ket(y)$?
])
נראה כי המצבים מנורמלים:
$
  norm(ket(y))^2 = braket(y, y)^2 = (sqrt(2/3))^2 + (1/sqrt(3))^2 = 2/3 + 1/3 = 1, space.quad norm(ket(o))^2 = 1/4 + 1/2 + 1/4 = 1 space.quad #emoji.checkmark.heavy
$
$ p_(o,y) = |braket(y, o)|^2 = abs(1/sqrt(3) + 1/(2sqrt(3)))^2 = abs(3/(2sqrt(3)))^2 = 3/4 $


#תתסעיף(מזהה: <2.2.ג>, [
  מכינים את המערכת במצב $ket(p)$. מה ההסתברות שנמדוד את המערכת במצב $ket(y)$?
])
נראה כי $ket(p)$ מנורמל:
$ norm(ket(p))^2 = 2 dot 1/2 = 1 space.quad #emoji.checkmark.heavy $
$ p_(p,y) = abs(braket(y, p))^2 = abs(-1/sqrt(3) dot 1/sqrt(2))^2 = abs(-1/sqrt(6))^2 = 1/6 $

#linebreak()
#תשובה[
  $ p_(o,y) = 3/4, space.en p_(p,y) = 1/6 $
]



#שאלה(כותרת: "מצבים בדו־מימד ואופרטורים", מזהה: <3>, [
  נתונים שמונה מצבים אורתונורמליים, המיוצגים על ידי $ket(theta\, d)$ כאשר:
  $ theta in {0, pi/2, pi, (3pi)/2}, space d = {1, 2} $
  $theta$ מתארת זווית ביחס לציר האופקי, ו־$d$ מרחק מהראשית. ראו איור להמחשה:

  #figure(
    image("q3_states.svg", width: 45%),
    caption: [המצבים הפיזיקליים של המערכת, המיוצגים על ידי $d$ ו־$theta$.],
  )
])

#סעיף(מזהה: <3.1>, [
  רשמו אופרטור $U$ המסובב את כל המצבים נגד כיוון השעון בזווית $pi/2$ אך שומר על המרחק מהראשית.
])
לכל מצב נחזיר את המצב עם אותו מרחק וזווית בתוספת $pi/2$, למעט
$ket(3pi/2\, d)$
עבורו נחזיר את
$ket(0\, d)$:
#תשובה[
  $ U = sum_(d in {1,2})(ketbra(0\, d, 3pi/2\, d) + sum_(theta in {0,pi/2,pi}) ketbra(theta+pi/2\,d, theta\,d)) $
]

#pagebreak()
#סעיף(מזהה: <3.2>, [
  רשמו אופרטור $U$ המשקף מצבים על הציר האופקי (מצבים על הציר האנכי לא משתנים).
])
למצבים עם זווית $0$ נרצה להחזיר מצב אותו מרחק וזווית $pi$ והפוך. את שאר המצבים נחזיר כמו שהם:
#תשובה[$
  U = sum_(d in {1,2}) (ketbra(0\, d, pi\, d) + ketbra(pi\, d, 0\, d) + ketbra(pi/2\, d) + ketbra((3pi)/2\, d))
$ ]

#סעיף(מזהה: <3.3>, [
  נתון אופרטור $D$ המקיים
  $D ket(theta\, d) = d ket(theta\, d)$.
  רשמו את האופרטור באופן מפורש.
])
#תשובה[
  $
    D = & ketbra(0\, 1) + ketbra(pi/2\, 1) + ketbra(pi\, 1) + ketbra((3pi)/2\, 1) \
        & + 2ketbra(0\, 2) + 2ketbra(pi/2\, 2) + 2ketbra(pi\, 2) + 2ketbra((3pi)/2\, 2)
  $
]

#סעיף(מזהה: <3.4>, [
  מצאו מצב $ket(psi)$ המקיים
  $mel(psi, D, psi) = 5/4$.
])
ניקח מצב בצורה הבאה:
$ psi = alpha ket(0\,1) + beta ket(0\, 2), alpha, beta in CC $
נמצא את המקדמים הדרושים על מנת שיתקיים המבוקש:
$
  mel(psi, D, psi) & = bra(psi)(ketbra(0\, 1) dot alpha ket(0\, 1) + 2 ketbra(0\, 2) dot beta ket(0\, 2)) \
                   & = (alpha^* bra(0\,1) + beta^* bra(0\, 2))(alpha ket(0\, 1) + 2beta ket(0\, 2)) \
                   & = abs(alpha)^2 + 2abs(beta)^2 = 5/4
$ <מ29>
כדי ש־$ket(psi)$ יהיה מנורמל, נדרוש בנוסף
$|alpha|^2 + |beta|^2 = 1$.
נחסיר את המשוואה השנייה מ@מ29 ונקבל:
$ |beta|^2 = 1/4 => |alpha|^2 = 3/4 $
מכך נמצא $alpha$ ו־$beta$ המקיימים את המבוקש:
#תשובה[$ ket(psi) = sqrt(3)/2 ket(0\,1) + 1/2 ket(0\, 2) $]

#סעיף(מזהה: <3.5>, [
  הראו כי לכל $ket(psi)$ מתקיים:
  $1 <= mel(psi, D, psi) <= 2$.
])
כל מצב ניתן לבטא כצירוף לינארי של מצבי בסיס:
$ ket(psi) = sum_(theta, d) c_(theta, d) ket(theta\, d) $
כאשר המקדמים מקיימים:
$
  p_d_0 equiv P("Being at distance" d_0) = sum_theta abs(braket(psi, theta\, d_0))^2 = sum_theta |c_(theta, d_0)|^2
$
מכאן נקבל:
$
  mel(psi, D, psi) & = bra(psi) sum_(theta, d) D (c_(theta, d) ket(theta\, d)) = sum_(theta, d) d |c_(theta, d)|^2 \
                   & = 1 dot sum_theta |c_(theta, 1)|^2 + 2 dot sum_theta |c_(theta, 2)|^2 \
                   & = 1 dot p_1 + 2 dot p_2
$ $$
$1$ ו־$2$
הם המרחקים האפשריים היחידים, לכן
$p_1 = 1-p_2$. בנוסף, $0 <= p_2 <= 1$ כי זו הסתברות של מאורע:
$ mel(psi, D, psi) = 1-p_2 + 2p_2 = p_2 + 1 in [1,2] $
#תשובה[
  $ forall ket(psi), space.en 1 <= mel(psi, D, psi) <= 2 $
]

#סעיף(מזהה: <3.6>, [
  נתון אופרטור $X$ כך ש:
  $ X ket(theta\, d) = "Proj"_x ket(theta\, d) $
  כאשר $"Proj"_x$ הוא ההיטל על ציר ה־$x$ של המצב. לדוגמה:
  $ X ket(1\, pi) = -ket(1\, pi) $
  רשמו את $X$ באופן מפורש.
])
ההיטל של מצבים בכיוון ציר $y$ על ציר $x$ הוא אפס, לכן:
#תשובה[$ X = sum_(d in {1,2}) d (ketbra(0\, d) - ketbra(pi\, d)) $]

#סעיף(מזהה: <3.7>, [
  מצאו שישה מצבים אורתונורמליים המקיימים
  $mel(psi, X, psi) = 0$.
])
כאמור, היטל כל מצב שנמצא על ציר $y$ הוא אפס, לכן נוכל ראשית לבחור את ארבעת המצבים המקיימים זאת:
$ A = {ket(pi/2\,1), ket((3pi)/2\,1), ket(pi/2\,2), ket((3pi)/2\,2)} $
כעת ניקח מצב כללי המורכב ממצבים הנותרים, ונבחר למשל $d=1$:
$ ket(psi) = alpha ket(0\, 1) + beta ket(pi\, 1), space.en alpha, beta in CC $
נחשב מפורשות:
$
  mel(psi, X, psi) = bra(psi) (alpha ket(0\,1) - beta ket(pi\,1)) = (alpha^* bra(0\,1) + beta^* bra(pi\,1)) (alpha ket(0\,1) - beta ket(pi\,1))
  = |alpha|^2 - |beta|^2 = 0
$
כדי ש־$ket(psi)$ יהיה מנורמל, נדרוש כי
$|alpha|^2 + |beta|^2 = 1$. נחבר בין המשוואות ונקבל:
$ 2|alpha|^2 = 1 => alpha stretch(=)_"בחירה" 1/sqrt(2), beta = pm 1/sqrt(2) $
משום ש־$ket(psi_i)$
מכילים את הזוויות $0$ ו־$pi$
שלא מופיעות באף מצב ב־$A$, ומשום ש־$A$ מכיל מצבי בסיס אורתונורמליים, נסיק כי
$ket(psi_i)$
אורתונרמליים לכל מצב ב־$A$.
#תשובה[
  $
    forall ket(psi) in {ket(pi/2\,1), ket((3pi)/2\,1), ket(pi/2\,2), ket((3pi)/2\,2), 1/sqrt(2)(ket(0\,1)-ket(pi\,1)), 1/sqrt(2)(ket(0\,1)+ket(pi\,1))}, \
    mel(psi, X, psi) = 0
  $
]


#שאלה(כותרת: "אופרטורים ומדידות", מזהה: <4>, [
  נתונה מערכת עם שני מצבי צבע, $ket(b)$ ו־$ket(w)$. נתון אופרטור המייצג מדידה של טמפרטורה $T$ המקיים:
  $ T = 20 ketbra(b) + 40 ketbra(b, w) + 40 ketbra(w, b) + 80 ketbra(w) $
])
#סעיף(מזהה: <4.א>, [
  מה הערכים האפשריים שנקבל אם נמדוד את הטמפרטורה?
])
ערכי המדידה הם הערכים העצמיים של האופרטור $T$.
נסמן ב־$A$ את המטריצה המייצגת של $T$:
$ A = mat(20, 40; 40, 80) $
נסמן את הערכים העצמיים שלה ב־$lambda_1$ וב־$lambda_2$.
ידוע כי דטרמיננטת מטריצה היא מכפלת הערכים העצמיים שלה, לכן:
$ lambda_1 dot lambda_2 = |A| = det(20, 40; 40, 80) = 1600-1600 = 0 $
נבחר $lambda_1 = 0$. כעת, ניזכר כי סכום הערכים העצמיים הוא עקבת המטריצה:
$ lambda_1 + lambda_2 = 0 + lambda_2 = 20 + 80 = 100 $
#תשובה[
  הערכים האפשריים שנקבל אם נמדוד את הטמפרטורה הם $0$ ו־$100$.
]

#סעיף(מזהה: <4.ב>, [
  מה תהיה תוצאת מדידת הטמפרטורה של מצב $ket(b)$?
])
נמצא את המצבים העצמיים של $T$:
$ (A - 0 I) arrow(v) = mat(20, 40; 40, 80) vec(v_1, v_2) = vec(0, 0) => v_1 = -2, v_2 = 1 $
ננרמל את המצב העצמי:
$ norm(arrow(v)) = sqrt((-2)^2 + 1^2) = sqrt(5) => arrow(v_0) = 1/sqrt(5) vec(-2, 1) $
$ (A - 100 I) arrow(v) = mat(-80, 40; 40, -20) vec(v_1, v_2) = vec(0, 0) => v_1 = 1, v_2 = 2 $
ננרמל את המצב העצמי:
$ norm(arrow(v)) = sqrt(1^2 + 2^2) = sqrt(5) => arrow(v_100) = 1/sqrt(5) vec(1, 2) $
נרשום את $ket(0)$ ואת $ket(100)$ בבסיס הצבע:
$ ket(0) = 1/sqrt(5)(-2 ket(b) + 1 ket(w)), space.en ket(100) = 1/sqrt(5)(ket(b) + 2ket(w)) $
נחשב את ההסתברות למדוד כל טמפרטורה:
$ P(T_b = 0) = abs(braket(b, 0))^2 = abs(-2/sqrt(5))^2 = 4/5, space.en P(T_b = 100) = abs(braket(b, 100))^2 = 1/5 $
נחשב את תוחלת מדידת הטמפרטורה של מצב $ket(b)$:
$
  expval(T)_(b) & = 0 dot P(T = 0) + 100 dot P(T = 100) \
                & = 100 abs(braket(100, b))^2 = 100 abs(1/sqrt(5)(braket(b) + 2 braket(b, w)))^2 = 100/5 = 20
$
ניתן גם לראות כי:
$ expval(T)_(b) = T_(11) = 20 $
#תשובה[
  ניתן למדוד את הטמפרטורה של $ket(b)$ ולקבל את הטמפרטורות $0$ ו־$100$ בהסתברויות הבאות:
  $ P(T_b = 0) = 4/5, space.en P(T_b = 100) = 1/5 $
  תוחלת המדידות היא:
  $ expval(T)_(b) = 20 $
]
