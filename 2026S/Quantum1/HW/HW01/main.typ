#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "1",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 4, day: 22)
)
//#set math.equation(numbering: "(1)", number-align: top)

#שאלה(כותרת: "העתקות לינאריות", [
    נתונה ההעתקה הלינארית בה עסקנו בתרגול 1:
    #nonum($ T(alpha + beta x + gamma x^2 + delta x^3) =& (3alpha - 2beta + 3gamma - 3delta) + (alpha + 3gamma - 2delta)x +\ + &  (3alpha - 3beta + 5gamma - delta)x^2 + (alpha - beta + gamma + 2delta)x^3 $)
    ])

#let tc = $[T]_cal(C)$
#let ta = $[T]_cal(A)$
#סעיף[
   מצאו בסיס $cal(C)$ למרחב הווקטורי, כך שהמטריצה המייצגת $tc$ תהיה אלכסונית. רשמו את איברי בסיס זה כפולינומים.
]
נמצא ראשית את המטריצה המייצגת של $T$ בבסיס הסטנדרטי
 $cal(A) = {1,x,x^2,x^3}$.
 נפעיל את $T$ על איברי הבסיס:


 $ T(cal(a)_1) = T(1) = T(1 dot 1 + 0 dot x + 0 dot x^2 + 0 dot x^3) = \ 
 (3 dot 1 -2 dot 0 + 3 dot 0 - 3 dot 0) + (1 dot 1 + 3 dot 0 -2 dot 0) x + (3 dot 1 -3 dot 0 + 5 dot 0 -0) x^2 +\
 (1 -0 + 0 +2 dot 0)x^3 = 3 + x + 3x^2 + x^3
 \ 
 T(cal(a)_2) = T(x) = -2 -3x^2 -x^3 \
 T(cal(a)_3) = T(x^2) = 3 + 3x +5x^2 +x^3 \
 T(cal(a)_4) = T(x^3) = -3 -2x -x^2 +2x^3 \
 $
 ניקח וקטורי קוארדינטות של תמונות רכיבי הבסיס, נשים אותם כעמודות מטריצה ונקבל את המטריצה המייצגת של $T$ לפי הבסיס הסטנדרטי:
 $ ta = mat(
            3,-2,3,-3;
            1,0,3,-2;
            3,-3,5,-1;
            1,-1,1,2) $
בשביל ש-$tc$ תהיה אלכסונית, נדרוש ש-$cal(C)$ יהיה בסיס המורכב מווקטורים עצמיים של $T$. נמצא אותם ע"י לכסון $ta$. ראשית, נמצא את הערכים העצמיים:
#let lam = $lambda$

$ p(lam) = abs(ta-lam bb(1)) = &
det(3-lam,-2,3,-3;
    1,-lam,3,-2;
    3,-3,5-lam,-1;
    1,-1,1,2-lam) stretch(=)^(C_1->C_1+C_2)
det(1-lam,-2,3,-3;
    1-lam,-lam,3,-2;
    0,-3,5-lam,-1;
    0,-1,1,2-lam) stretch(=)^(R_2->R_2-R_1) \
= & det(1-lam,-2,3,-3;
        0,2-lam,0,1;
        0,-3,5-lam,-1;
        0,-1,1,2-lam) =
(1-lam)det(2-lam,0,1;
           -3,5-lam,-1;
           -1,1,2-lam) stretch(=)^(C_1->C_1+C_2) \
= & (1-lam)det(2-lam,0,1;
                2-lam,5-lam,-1;
                0,1,2-lam) stretch(=)^(R_2->R_2-R_1)
(1-lam)det(2-lam,0,1;
           0,5-lam,-2;
           0,1,2-lam) = \
= & (1-lam)(2-lam)((5-lam)(2-lam)+2) = (1-lam)(2-lam)(10-5lam-2lam+lam^2+2) = \
= & (1-lam)(2-lam)(lam^2-7lam+12)=(1-lam)(2-lam)(lam-4)(lam-3)
$
לכן הערכים העצמיים הם $1,2,3,4$. יש 4 ערכים עצמיים שונים, לכל לכל ערך עצמי נמצא את הווקטור העצמי היחיד המתאים לו על ידי הצבתו במטריצה האופיינית:
$ lam_1 = 1":" ta - 1 dot bb(1) = 
mat(2,-2,3,-3;
    1,-1,3,-2;
    3,-3,4,-1;
    1,-1,1,1)
  $
נשים לב כי $C_1=-C_2$ לכן נבחר
$[v_1]_cal(A)=(1,1,0,0)^T$.
נקבל כי $v1=1+x$ הוא וקטור עצמי המתאים ל-$lam_1=1$.
$ lam_2 = 2":" ta - 2bb(1) = 
mat(1,-2,3,-3;
    1,-2,3,-2;
    3,-3,3,-1;
    1,-1,1,0) stretch(->)^(R_2->R_2-R_1 \ R_3->R_3-3R_1 \ R_4->R_4-R_1)
mat(1,-2,3,-3;
    0,0,0,1;
    0,3,-6,8;
    0,1,-2,3) 
  $
נסמן
$[v_2]_cal(A)=(a,b,c,d)$.
מהשורה השנייה נקבל $d=0$. מהשורה הרביעית נקבל $b=2c$, נבחר למשל 
#box[$b=2,c=1$.]
נציב בשורה הראשונה ונקבל:
$ a -2b + 3c - 3d = a -4 + 3 - 0 = 0 => a = 1 $
לכן $[v_2]_cal(A)=(1,2,1,0)^T$ והווקטור העצמי המתאים הוא $v_2 = 1 + 2x + x^2$.
$ lam_3 = 3":" ta - 3bb(1) = 
mat(0,-2,3,-3;
    1,-3,3,-2;
    3,-3,2,-1;
    1,-1,1,-1) stretch(->)^(R_2->R_2-R_1)
mat(0,-2,3,-3;
    1,-1,0,1;
    3,-3,2,-1;
    1,-1,1,-1) stretch(->)^(R_3->R_3-3R_2 \ R_4->R_4-R_2)
mat(0,-2,3,-3;
    1,-1,0,1;
    0,0,2,-4;
    0,0,1,-2)
$
נסמן $[v_3]_cal(A)=(a,b,c,d)$. נפתור
$(ta - 3bb(1))v_3=0$
ונקבל:
$ cases(R_1 => 2b = 3(c-d), R_2 => a = b - d, R_4 => c = 2d) $
נציב את המשוואה השלישית בראשונה ונקבל $2b=3d$, ואז מהמשוואה השנייה נקבל $2a = d$. נבחר 
#box[$a=1$]
ונקבל $d=2,c=4$. נציב שוב במשוואה הראשונה ונקבל $b=3$. \
לכן $[v_3]_cal(A)=(1,3,4,2)^T$ והווקטור העצמי המתאים הוא $v_3=1+3x+4x^2+2x^3$.
$ lam_4 = 4":" ta - 4bb(1) = 
& mat(-1,-2,3,-3;
    1,-4,3,-2;
    3,-3,1,-1;
    1,-1,1,-2) stretch(->)^(R_2->R_2+R_1 \ R_3->R_3+3R_1 \ R_4->R_4-R_2)
mat(-1,-2,3,-3;
    0,-6,6,-5;
    0,-9,10,-10;
    0,3,-2,0) stretch(->)^(R_2->R_2+2R_4 \ R_3->R_3+3R_4) \
& mat(-1,-2,3,-3;
    0,0,2,-5;
    0,0,4,-10;
    0,3,-2,0) 
$
נסמן $[v_4]_cal(A)=(a,b,c,d)$. מהמטריצה נקבל:
$ cases(R_1 => a = -2b+3c-3d, R_2 => 2c=5d, R_4 => 3b=2c) $
כלומר $3b=2c=5d$. נבחר $c=15$ ונקבל $b=10,d=6$ ואז $a=-20+45-18=7$. \
לכן $[v_4]_cal(A)=(7,10,15,6)^T$ ומכאן $v_4=7+10x+15x^2+6x^3$.
#תשובה[
    בסיס למרחב הווקטורי שהמטריצה המייצגת של $T$ לפיו היא אלכסונית הוא:
    $ cal(C) = {1+x, 1+2x+x^2, 1+3x+4x^2+2x^3, 7+10x+15x^2+6x^3} $
]
#סעיף[
מצאו את מטריצת המעבר
$P_(cal(B)->cal(C))$
(כאשר $cal(B)$ הוא אחד הבסיסים עליהם דנו בתרגול) והראו כי מתקיים:
#nonum($ P_(cal(C) -> cal(B)) [T]_cal(B) P_(cal(B) -> cal(C)) = [T]_cal(C) $)    
]
נזכיר את הבסיס $cal(B)$:
$ cal(B) = {1 + x, x + x^2, x^2 + x^3, 1 + x + x^2} $
בשביל למצוא את מטריצת המעבר $P_(cal(B) -> cal(C))$ נגדיר את $M_cal(B), M_cal(C)$ להיות מטריצות המעבר מהבסיסים אל הבסיס הסטנדרטי, $cal(A)$:
$ M_cal(B) = mat(1,0,0,1;1,1,0,1;0,1,1,1;0,0,1,0),
  M_cal(C) = mat(1,1,1,7;1,2,3,10;0,1,4,15;0,0,2,6) $

$M_cal(C)$
מעבירה וקטור קואורדינטות מבסיס $cal(A)$ לבסיס $cal(C)$, ו-$M_cal(B)^(-1)$ מעבירה וקטור קואורדינטות מבסיס $cal(B)$ לבסיס $cal(A)$. לכן אם נרצה לקבל את $P_(cal(B)->cal(C))$, נחשב את
$M_cal(B)^(-1)M_cal(C) $
שתעביר וקטור קואורדינטות לפי בסיס $cal(C)$ לווקטור קואורדינטות לפי בסיס $cal(A)$ ואז לווקטור קואורדינטות לפי בסיס $cal(B)$, כמבוקש מ-$P_(cal(B)->cal(C))$.

נמצא זאת על ידי דירוג:
$ [M_cal(B) mid(|) M_cal(C)] =
& mat(1,0,0,1,1,1,1,7;
    1,1,0,1,1,2,3,10;
    0,1,1,1,0,1,4,15;
    0,0,1,0,0,0,2,6; augment: #4) stretch(->)^(R_2->R_2-R_1)
mat(1,0,0,1,1,1,1,7;
    0,1,0,0,0,1,2,3;
    0,1,1,1,0,1,4,15;
    0,0,1,0,0,0,2,6; augment: #4) stretch(->)^(R_3->R_3-R_2) \
& mat(1,0,0,1,1,1,1,7;
    0,1,0,0,0,1,2,3;
    0,0,1,1,0,0,2,12;
    0,0,1,0,0,0,2,6; augment: #4) stretch(->)^(R_4<=>R_3)
mat(1,0,0,1,1,1,1,7;
    0,1,0,0,0,1,2,3;
    0,0,1,0,0,0,2,6;
    0,0,1,1,0,0,2,12; augment: #4) stretch(->)^(R_4->R_4-R_3) \
& mat(1,0,0,1,1,1,1,7;
    0,1,0,0,0,1,2,3;
    0,0,1,0,0,0,2,6;
    0,0,0,1,0,0,0,6; augment: #4) stretch(->)^(R_1->R_1-R_4)
mat(1,0,0,0,1,1,1,1;
    0,1,0,0,0,1,2,3;
    0,0,1,0,0,0,2,6;
    0,0,0,1,0,0,0,6; augment: #4) = [I mid(|) M_cal(B)^(-1)M_cal(C)]
$
לכן קיבלנו:
#תשובה[
 $ P_(cal(B)->cal(C)) = mat(1,1,1,1;
    0,1,2,3;
    0,0,2,6;
    0,0,0,6) $
]
#let tb = $[T]_cal(B)$

כעת נמצא את $tc$, $tb$ ו-$P_(cal(C)->cal(B))$. מצאנו ש-$cal(C)$ הוא בסיס של וקטורים עצמיים של $T$, לכן $tc$ מכילה באלכסון את הערכים העצמיים של $T$:
$ tc = mat(1,0,0,0;0,2,0,0;0,0,3,0;0,0,0,4) $
נמצא את $tb$ על ידי הפעלת $T$ על איברי בסיס $cal(B)$ ונשים את וקטורי הקואורדינטות של התמונות כעמודות מטריצה:
$ T(cal(b)_1) = T(1 + x) = 1 + x => [T(cal(b)_1)]_cal(B) = (1,0,0,0)^T \ 
T(cal(b)_2) = T(x + x^2) = 1 + 3x + 2x^2 => [T(cal(b)_2)]_cal(B) = (1,2,0,0)^T \
T(cal(b)_3) = T(x^2 + x^3) = x + 4x^2 + 3x^3 => [T(cal(b)_3)]_cal(B) = (0,1,3,0)^T \
T(cal(b)_4) = T(1+x+x^2) = 4 + 4x + 5x^2 + x^3 => [T(cal(b)_4)]_cal(B) = (0,0,1,4)^T 
$
מכאן נקבל:
$ tb = mat(1, 1, 0, 0;
           0, 2, 1, 0;
           0, 0, 3, 1;
           0, 0, 0, 4) $

נחשב את $P_(cal(C) -> cal(B))$ על ידי דירוג כפי שעשינו קודם:
$ [P_(cal(B) -> cal(C)) mid(|) I] = & mat(1,1,1,1,1,0,0,0;
    0,1,2,3,0,1,0,0;
    0,0,2,6,0,0,1,0;
    0,0,0,6,0,0,0,1; augment: #4) stretch(->)^(R_3->R_3-R_4 \ R_2->R_2 - 1/2 R_4 \ R_1->R_1 - 1/6 R_4)
mat(1,1,1,0,1,0,0,-1/6;
    0,1,2,0,0,1,0,-1/2;
    0,0,2,0,0,0,1,-1;
    0,0,0,6,0,0,0,1; augment: #4) stretch(->)^(R_4->1/6 R_4 \ R_2->R_2 - R_3 \ R_1->R_1 - 1/2 R_3) \
& mat(1,1,0,0,1,0,-1/2,1/3;
    0,1,0,0,0,1,-1,1/2;
    0,0,2,0,0,0,1,-1;
    0,0,0,1,0,0,0,1/6; augment: #4) stretch(->)^(R_3->1/2 R_3 \ R_1->R_1 - R_2)
mat(1,0,0,0,1,-1,1/2,-1/6;
    0,1,0,0,0,1,-1,1/2;
    0,0,1,0,0,0,1/2,-1/2;
    0,0,0,1,0,0,0,1/6; augment: #4) = [I mid(|) P_(cal(C) -> cal(B))] 
    $
ולכן:
$ P_(cal(C) -> cal(B)) =
mat(1, -1, 1/2, -1/6;
    0, 1, -1, 1/2;
    0, 0, 1/2, -1/2;
    0, 0, 0, 1/6) $
#box[כעת נחשב את אגף שמאל של המשוואה:
$ P_(cal(C) -> cal(B)) [T]_cal(B) P_(cal(B) -> cal(C)) = 
& mat(1, -1, 1/2, -1/6;
    0, 1, -1, 1/2;
    0, 0, 1/2, -1/2;
    0, 0, 0, 1/6)
mat(1, 1, 0, 0;
    0, 2, 1, 0;
    0, 0, 3, 1;
    0, 0, 0, 4)
mat(1, 1, 1, 1;
    0, 1, 2, 3;
    0, 0, 2, 6;
    0, 0, 0, 6) = \
& mat(1, -1, 1/2, -1/6;
    0, 1, -1, 1/2;
    0, 0, 1/2, -1/2;
    0, 0, 0, 1/6)
mat(1, 2, 3, 4;
    0, 2, 6, 12;
    0, 0, 6, 24;
    0, 0, 0, 24) =
mat(1, 0, 0, 0;
    0, 2, 0, 0;
    0, 0, 3, 0;
    0, 0, 0, 4) $
]
לכן קיבלנו:
#תשובה[
    #nonum($ P_(cal(C) -> cal(B)) [T]_cal(B) P_(cal(B) -> cal(C)) = [T]_cal(C) $)
    #משל
]

#let ff = $hat(f)$
#שאלה(כותרת: "התמרת פורייה", [
    מצאו את $ff(k)$, התמרת פורייה הבאה:
    #nonum($ ff(k) = cal(F) [1/(sqrt(2pi)sigma) e^(-x^2/(2sigma^2))] $)
]
)
נתחיל לפתח לפי הגדרת התמרת פורייה:
$ ff(k) = 1/sqrt(2pi) integral_(-infinity)^infinity f(x) e^(-i k x) dif x = integral_(-infinity)^infinity 1/(2pi sigma) e^(-x^2/(2sigma^2)) e^(-i k x) dif x $ <הגדרה>
נגזור את שני צדדי המשוואה לפי $k$. משום שהאינטגרל לפי $x$ ולא לפי $k$, נכניס את הנגזרת לתוך האינטגרל:
$ ff'(k) = 1/sqrt(2pi) integral_(-infinity)^infinity dif / (dif k) (f(x) e^(-i k x)) dif x = 1/sqrt(2pi) integral_(-infinity)^infinity (-i x) f(x) e^(-i k x) dif x $
נציב את $f(x)$:
$ ff'(k) = -i/sqrt(2pi) integral_(-infinity)^infinity 1/(sqrt(2pi)sigma) x e^(-x^2/(2sigma^2)) e^(-i k x) dif x = (i sigma)/(2pi) integral_(-infinity)^infinity -x/(sigma^2) e^(-x^2/(2sigma^2)) dot e^(-i k x) dif x $
נבצע אינטגרציה בחלקים. נסמן:
$ cases(
    u' = -x/(sigma^2) e^(-x^2/(2sigma^2))\, u = e^(-x^2/(2sigma^2)),
    v = e^(-i k x)\, v' = -i k e^(-i k x)) =>
hat(f)'(k) = (i sigma) / (2 pi) ( underbrace(lr("" e^(-i k x - x^2/(2 sigma^2)) |)_(-infinity)^infinity, 0) - integral_(-infinity)^infinity -i k e^(-i k x) e^(-x^2/(2sigma^2)) dif x) = \
 i sigma^2 dot i k integral_(-infinity)^infinity 1/(2pi sigma) e^(-x^2/(2 sigma^2))e^(-i k x) dif x = -sigma^2 k ff(k) $
קיבלנו מד"ר ב-$ff(k)$. מכאן:
$ (ff'(k))/ff(k) = -sigma^2 k $
נבצע על המשוואה אינטגרציה לפי $k$:
$ ln(ff(k)) = -(sigma^2 k^2) / 2 + C => ff(k) = C e^((-sigma^2 k^2)/2) $
נמצא את $C$ ע"י מציאת $ff(0)$. לפי @הגדרה:
$ ff(0) = 1/sqrt(2pi) integral_(-infinity)^infinity f(x) e^(-i 0 x) dif x = integral_(-infinity)^infinity 1/(2pi sigma) e^(-x^2/(2sigma^2)) dif x $ <פאפס>
נמצא את ערך האינטגרל הזה לפי השיטה המוכרת. נסמן 
$I=integral_(-infinity)^infinity 1/(2pi sigma) e^(-x^2/(2sigma^2)) dif x$ ואז:
$ I^2 = integral_(-infinity)^infinity 1/(2pi sigma) e^(-x^2/(2sigma^2)) dif x integral_(-infinity)^infinity 1/(2pi sigma) e^(-y^2/(2sigma^2)) dif y =_"פוביני" integral.double_(RR^2) 1/(2pi sigma)^2 e^(-(x^2+y^2)/(2sigma^2)) dif x dif y $
נבצע החלפת משתנים: $x=r cos theta, y=r sin theta, |J| = r$:
$ I^2 = 1/(2pi sigma)^2 integral_(r=0)^infinity integral_(theta=0)^(2pi) r e^(-r^2/(2sigma^2)) dif theta dif r = (2pi)/(2pi sigma)^2 dot sigma^2 (lr("" -e^(-r^2/(2sigma^2)) |)_0^infinity) = 1/(2 pi) (0 - (-1)) = 1/(2pi) $
מכאן, $I = 1/sqrt(2pi)$. נציב חזרה ב@פאפס:
$ ff(0) = 1/sqrt(2pi) = C e^((-sigma^2 0^2)/2) = C $
לכן:
#תשובה[
    #nonum($ ff(k) = 1/sqrt(2pi)e^((-sigma^2 k^2)/2) $)
]
#שאלה(כותרת: "התמרת פורייה", [
    נתונה הפונקציה הבאה:
    $ f(t) = 1/tau e^(-abs(t)/tau) cos(omega_0 t) $
])
#let om = $omega$; #let om0 = $omega_0$

#סעיף[
    מצאו את $ff(om)$, התמרת פורייה של $f(t)$.
]
ראשית, נשתמש בזהות אוילר:
$ cos(om0 t) = (e^(i om0 t) + e^(-i om0 t))/2 $
נגדיר $g(t)=1/tau e^(-abs(t)/tau)$:
$ f(t) = 1/2[e^(i om0 t)g(t) + e^(-i om0 t)g(t)] $
 ואז לפי זהויות 3 ו-5 מהתרגול:
 #let gg = $hat(g)$
$ ff(om) = cal(F)[1/2[e^(i om0 t)g(t) + e^(-i om0 t)g(t)]] = 1/2 ( cal(F)[e^(i om0 t)g(t)] + cal(F)[e^(-i om0 t)g(t)]) = \ 1/2[gg(om-om0)+gg(om+om0)] $ <פיצול>
נמצא את $gg(om)$ לפי הגדרת התמרת פורייה:
$ tau sqrt(2pi) gg(om) = integral_(-infinity)^infinity e^(-abs(t)/tau) e^(-i om t) dif t = integral_(-infinity)^0 e^(t/tau) e^(-i om t) dif t + integral_0^infinity e^(-t/tau) e^(-i om t) dif t = \ integral_(-infinity)^0 e^((1/tau - i om)t) dif t + integral_0^infinity e^(-(1/tau + i om)t)dif t = [lr("" 1/(1/tau - i om)e^((1/tau - i om)t)|)_(-infinity)^0] - [lr("" 1/(1/tau + i om)e^(-(1/tau + i om)t)|)_0^infinity] =\ 
1/(1/tau - i om)(1-0) - 1/(1/tau + i om)(0-1) = 1/(1/tau - i om) + 1/(1/tau + i om) = (1/tau + cancel(i om) + 1/tau cancel(-i om))/(1/tau^2 - (i om)^2) = 2/tau / (1/tau^2 + om^2) = (2 tau)/(1+om^2 tau^2) $
מכאן נקבל:
$ gg(om) = 2/(sqrt(2pi)(1+om^2 tau^2)) $
נציב ב@פיצול ונקבל:
#תשובה[
    $ ff(om) = 1/sqrt(2pi)[1/(1+(om-om0)^2tau^2)+1/(1+(om+om0)^2tau^2)]  $
]
#pagebreak()
#סעיף[
    הסבירו כיצד הפרמטרים $tau,omega_0$ משפיעים על צורת הפונקציה במישור פורייה ($omega,ff$) וציירו גרף של ההתמרה.
]
#figure(
    image("single_version.svg", width: 90%),
    caption: [גרף של $ff(om)$]
)
בהנחה ש-$tau!=0$ (לא פונקציה קבועה), השבר מקסימלי כאשר $om=om0$, ולכן $ff(om)$ מקבלת מקסימום ב-$om = plus.minus om0$. אם $om0=0$ יש לפונקציה נקודת מקסימום אחת. אחרת, יש שתיים, וככל ש-$abs(om0)$ גדל, כך המרחק ביניהן גדל.
#figure(
    image("varying_w0.svg", width: 90%),
    caption: [גרף של $ff(om)$ עם ערכי $om0$ שונים. ניתן לראות שכאשר $om0=0$, יש נקודת מקסימום יחידה.]
)

בשביל להבין את השפעתו של $tau$, נסתכל על $om$ קרוב ל-$om0$. זו נקודה שקרובה לנקודת המקסימום הימנית. כאשר $tau$ גדול, $(om-om0)^2tau^2$ גדל, והשבר קטן. כלומר, ככל ש-$tau$ גדל, כך $ff(om)$ יורדת מהר יותר מהמקסימום, ולכן הגבעות יהיו צרות יותר.
#figure(
    image("varying_tau.svg", width: 90%),
    caption: [גרף של $ff(om)$ עם ערכי $tau$ שונים. ניתן לראות שככל ש-$tau$ גדל, הגבעות צרות יותר.]
)
