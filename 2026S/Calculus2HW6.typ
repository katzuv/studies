#import "../typst/templates/hw.typ": *
#import "../typst/consts.typ": *
#import "../typst/utils.typ": *

#show: project.with(
  title: "חשבון אינפיניטסימלי 2ת",
  number: "6",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 7, day: 22),
)

#שאלה(מזהה: <1>, כותרת: "חישוב שטח פנים", [
  חשבו את שטח הפנים של המשטח $S_1 = { (x, y, z) | x^2 + y^2 + z^2 = 25, z >= 4 }$.
])
המשטח $S_1$ הוא כיפה כדורית ברדיוס $R = 5$.
נמצא פרמטריזציה להמשטח בעזרת קואורדינטות כדוריות:
$ x = 5 sin phi cos theta, quad y = 5 sin phi sin theta, quad z = 5 cos phi $
התנאי $z >= 4$ גורר $5 cos phi >= 4 => cos phi >= 4/5$.
נסמן $phi_0 = arccos(4/5)$. התחום של הפרמטרים הוא #box[$theta in [0, 2pi]$] ו- $phi in [0, phi_0]$.
אלמנט השטח הוא $dd(S) = R^2 sin phi dd(phi) dd(theta) = 25 sin phi dd(phi) dd(theta)$.
שטח הפנים נתון על ידי האינטגרל:
$
  integral.double_(S_1) dd(S) &= integral_0^(2pi) integral_0^(phi_0) 25 sin phi dd(phi) dd(theta) = 25 (integral_0^(2pi) dd(theta)) (integral_0^(phi_0) sin phi dd(phi)) \
  &= 25 dot 2pi dot evaluated((-cos phi))_0^(phi_0) = 50pi (1 - cos phi_0)
$
מכיוון ש־$cos phi_0 = 4/5$, נקבל:
$ "שטח פנים" = 50pi (1 - 4/5) = 50pi dot 1/5 = 10pi $
#תשובה[
  שטח הפנים של המשטח $S_1$ הוא $10pi$.
]

#שאלה(מזהה: <2>, כותרת: "אינטגרל משטחי", [
  חשבו את האינטגרל $integral.double_S (x^2 - y^2 + z) dd(S)$ כאשר $S$ המשטח הגלילי $x^2 + y^2 = 9$ החסום ע"י המישורים $x = 0, z = 0, z = 1, y = 0$ וגם $x >= 0, y >= 0$.
])
המשטח $S$ הוא חלק מגליל ברדיוס $R=3$ ברביע הראשון.
נמצא פרמטריזציה למשטח בעזרת קואורדינטות גליליות:
$ arrow(r)(theta, z) = (3 cos theta, 3 sin theta, z) $
כאשר $theta in [0, pi/2]$ ו־$z in [0, 1]$.
וקטור הנורמל:
$
  pdv(va(r), theta) times pdv(va(r), z) = (-3 sin theta, 3 cos theta, 0) times (0, 0, 1) = arrow(r)_theta times arrow(r)_z = det(
    vu(i), vu(j), vu(k);
    -3 sin theta, 3 cos theta, 0;
    0, 0, 1;
  ) = (3 cos theta, 3 sin theta, 0)
$
הגודל שלו הוא $abs(arrow(r)_theta times arrow(r)_z) = sqrt(9 cos^2 theta + 9 sin^2 theta) = 3$. לכן $dd(S) = 3 dd(theta) dd(z)$.
הפונקציה על המשטח:
$ x^2 - y^2 + z = 9 cos^2 theta - 9 sin^2 theta + z = 9 cos(2 theta) + z $
נציב באינטגרל:
$
  integral.double_S (x^2 - y^2 + z) dd(S) &= integral_0^1 integral_0^(pi/2) (9 cos(2 theta) + z) 3 dd(theta) dd(z) \
  &= 3 integral_0^1 ( integral_0^(pi/2) 9 cos(2 theta) dd(theta) + integral_0^(pi/2) z dd(theta) ) dd(z)
$
נחשב את האינטגרלים הפנימיים:
$ integral_0^(pi/2) 9 cos(2 theta) dd(theta) = evaluated(9/2 sin(2 theta))_0^(pi/2) = 0 $
$ integral_0^(pi/2) z dd(theta) = pi/2 z $
נחזור לאינטגרל החיצוני:
$ 3 integral_0^1 pi/2 z dd(z) = (3 pi)/2 evaluated(1/2 z^2)_0^1 = (3 pi)/4 $
#תשובה[
  $ integral.double_S (x^2 - y^2 + z) dd(S) = (3 pi)/4 $
]

#שאלה(מזהה: <3>, כותרת: "משפט הדיברגנץ", [
  יהי $a > 0$ מספר ממשי. נגדיר שדה וקטורי:
  $ va(F)(x, y, z) = ((x-1)^2 + y z) vu(i) + ((y+2)^2 + x z) vu(j) + (x^2 + y^2 + z^2) vu(k) $
])
#סעיף(מזהה: <3.א>, [
  מצאו את השטף של השדה $va(F)$ דרך המשטח $S_1 = { (x,y,z) | z=a, x^2+y^2 <= a^2 }$ כאשר #box[הנורמל ל־$S_1$] בעל רכיב $z$ חיובי.
])
המשטח $S_1$ הוא עיגול ברדיוס $a$ במישור $z = a$. הנורמל המכוון כלפי מעלה הוא $vu(n) = (0, 0, 1) = vu(k)$.
השטף נתון על ידי:
$ integral.double_(S_1) arrow(F) dot vu(n) dd(S) = integral.double_(S_1) (x^2 + y^2 + z^2) dd(S) $
על המשטח מתקיים $z = a$, ולכן האינטגרל הוא:
$ integral.double_(x^2+y^2 <= a^2) (x^2 + y^2 + a^2) dd(x) dd(y) $
נעבור לקואורדינטות מעגליות, $x = r cos theta, y = r sin theta$:
$
  integral_0^(2pi) integral_0^a (r^2 + a^2) r dd(r) dd(theta) = 2pi integral_0^a (r^3 + a^2 r) dd(r) = 2pi (r^4/4 + a^2 r^2/2)|_0^a = 2pi (a^4/4 + a^4/2) = (3 pi a^4)/2
$
#תשובה[
  השטף של השדה דרך $S_1$ הוא $(3 pi a^4)/2$.
]

#סעיף(מזהה: <3.ב>, [
  מצאו את השטף של השדה $arrow(F)$ דרך המשטח $S_2 = { (x,y,z) | x^2+y^2+(z-a)^2 = a^2, z <= a }$ כאשר נורמל ל־$S_2$ בעל רכיב $z$ חיובי.
])
יהי $V$ חצי הכדור הכלוא בין $S_1$ ל־$S_2$:
$ V = { (x,y,z) | x^2+y^2+(z-a)^2 <= a^2, z <= a } $
שפת $V$ היא $partial V = S_1 union S_2$.
לפי משפט הדיברגנץ, השטף הכולל החוצה מ־$V$ שווה לאינטגרל המשולש של הדיברגנץ על $V$:
$
  integral.triple_V (arrow(nabla) dot arrow(F)) dd(V) = integral.double_(S_1) arrow(F) dot vu(n)_("out") dd(S) + integral.double_(S_2) arrow(F) dot vu(n)_("out") dd(S)
$
הנורמל היוצא מ־$S_1$ מצביע למעלה ולכן $vu(n)_("out") = vu(k)$. זהו השטף שחישבנו בסעיף א'.
הנורמל היוצא מ־$S_2$ מצביע החוצה מהכדור (כלומר למטה, רכיב $z$ שלילי). השאלה מבקשת את השטף דרך $S_2$ עם נורמל בעל רכיב $z$ חיובי, נסמנו $vu(n)_("up")$. מתקיים $vu(n)_("up") = -vu(n)_("out")$.
לכן, האינטגרל המבוקש הוא:
$
  integral.double_(S_2) arrow(F) dot vu(n)_("up") dd(S) = integral.double_(S_1) arrow(F) dot vu(k) dd(S) - integral.triple_V (arrow(nabla) dot arrow(F)) dd(V)
$
נחשב את הדיברגנץ של $arrow(F)$:
$
  div arrow(F) = pdv(, x) ((x-1)^2+y z) + pdv(, y) ((y+2)^2+x z) + pdv(, z) (x^2+y^2+z^2) = 2(x-1) + 2(y+2) + 2z = 2x + 2y + 2z + 2
$
נחשב את האינטגרל המשולש על $V$. משיקולי סימטריה, האינטגרל של $2x$ ו־$2y$ על חצי הכדור מתאפס. נשאר לחשב:
$ integral.triple_V (2z + 2) dd(V) $
נעבור לקואורדינטות כדוריות המוזזות לנקודה $(0, 0, a)$:
$ x = r sin phi cos theta, quad y = r sin phi sin theta, quad z = a + r cos phi $
$ theta in [0, 2pi], phi in [pi/2, pi], r in [0, a], J = r^2 sin phi $
$
  integral.triple_V (2z + 2) dd(V) &= integral_0^(2pi) dd(theta) integral_(pi/2)^pi sin phi dd(phi) integral_0^a (2(a + r cos phi) + 2) r^2 dd(r) \
  &= 2pi integral_(pi/2)^pi sin phi [ (2a + 2) a^3/3 + 2 cos phi a^4/4 ] dd(phi)
$
נפריד לשני אינטגרלים על $phi$:
$ integral_(pi/2)^pi sin phi dd(phi) = evaluated(-cos phi)_(pi/2)^pi = 1 $
$ integral_(pi/2)^pi sin phi cos phi dd(phi) = evaluated((sin^2 phi)/2)_(pi/2)^pi = -1/2 $
נציב חזרה:
$
  integral.triple_V (div arrow(F)) dd(V) = 2pi ( 2(a+1) a^3/3 - a^4/4 ) = (4 pi a^4)/3 + (4 pi a^3)/3 - (pi a^4)/2 = (5 pi a^4)/6 + (4 pi a^3)/3
$
נציב במשוואת השטף יחד עם התוצאה מסעיף א':
$
  integral.double_(S_2) arrow(F) dot hat(n)_("up") dd(S) = (3 pi a^4)/2 - ( (5 pi a^4)/6 + (4 pi a^3)/3 ) = (4 pi a^4)/6 - (4 pi a^3)/3 = (2 pi a^4)/3 - (4 pi a^3)/3
$
#תשובה[
  השטף של השדה דרך $S_2$ הוא $(2 pi a^4)/3 - (4 pi a^3)/3$.
]

#שאלה(מזהה: <4>, כותרת: "משפט סטוקס", [
  חשבו את האינטגרל $integral_L (e^x + y x^2 - z) dd(x) + (x^3 + sin y) dd(y) - x dd(z)$ כאשר $L$ הוא עקום החיתוך של המשטחים $z = 1 - x^2 - y^2$ ו־$3x^2 + 3y^2 + (z-1)^2 = 4$ עם מגמה נגד כיוון השעון בהסתכלות מלמעלה.
])
נמצא את עקום החיתוך. מהמשוואה הראשונה נקבל $z - 1 = -(x^2 + y^2)$. נציב במשוואה השנייה:
$ 3(x^2 + y^2) + (-(x^2 + y^2))^2 = 4 $
נסמן $u = x^2 + y^2$ (מתקיים $u >= 0$). המשוואה היא $u^2 + 3u - 4 = 0$, שפירוקה הוא #box[$(u+4)(u-1) = 0$]. מכיוון ש־$u >= 0$ בהכרח $u = 1$, כלומר $x^2 + y^2 = 1$.
נציב חזרה ונקבל $z = 1 - 1 = 0$.
לכן העקום $L$ הוא המעגל $x^2 + y^2 = 1$ במישור $z = 0$, מכוון נגד כיוון השעון.

נשתמש במשפט סטוקס. יהי $S$ העיגול $x^2 + y^2 <= 1$ במישור $z=0$. הנורמל התואם למגמת העקום הוא $vu(n) = vu(k) = (0, 0, 1)$.
השדה הווקטורי הוא $arrow(F) = (e^x + y x^2 - z, x^3 + sin y, -x)$.
נחשב את הרוטור של $arrow(F)$:
$
  curl arrow(F) & = det(
                    vu(i), vu(j), vu(k);
                    pdv(, x), pdv(, y), pdv(, z);
                    e^x + y x^2 - z, x^3 + sin y, -x;
                  ) \
                & = (0 - 0) vu(i) - (-1 - (-1)) vu(j) + (pdv(, x)(x^3 + sin y) - pdv(, y)(e^x + y x^2 - z)) vu(k) \
                & = (0, 0, 3x^2 - x^2) = (0, 0, 2x^2)
$
לפי משפט סטוקס:
$
  integral_L arrow(F) dot dd(arrow(r)) = integral.double_S (curl arrow(F)) dot vu(n) dd(S) = integral.double_(x^2+y^2 <= 1) 2x^2 dd(x) dd(y)
$
נעבור לקואורדינטות מעגליות:
$
  integral_0^(2pi) integral_0^1 2(r cos theta)^2 r dd(r) dd(theta) = 2 (integral_0^(2pi) cos^2 theta dd(theta)) (integral_0^1 r^3 dd(r)) = 2dot pi dot 1/4 = pi/2
$
#תשובה[
  $ integral_L (e^x + y x^2 - z) dd(x) + (x^3 + sin y) dd(y) - x dd(z) = pi/2 $
]

#שאלה(מזהה: <5>, כותרת: "עבודה של שדה", [
  תהיינה $h, g in C^2(RR^3)$ פונקציות גזירות ברציפות פעמיים בכל $RR^3$.
  נתון שלכל $(x, y, z) in RR^3$ מתקיים $grad h times grad g = (2x, 2y, 3)$.
  יהי השדה הווקטורי $arrow(H) = h arrow(nabla) g$. חשבו את העבודה $integral.cont_C arrow(H) dot va(dd(l))$ כאשר $C = { (x,y,2) : x^2 + y^2 = 9 }$ מכוון נגד כיוון השעון כאשר מסתכלים מלמעלה.
])
נשתמש במשפט סטוקס:
$ integral.cont_C arrow(H) dot va(dd(l)) = integral.double_S (curl arrow(H)) dot vu(n) dd(S) $
נחשב את הרוטור של $arrow(H)$:
$ curl (h grad g) = grad h times grad g + h (curl grad g) $
מכיוון שהרוטור של גרדיאנט הוא תמיד שדה אפס ($curl grad g = 0$), נקבל:
$ curl arrow(H) = grad h times grad g = (2x, 2y, 3) $
יהי $S$ העיגול החסום על ידי $C$: $x^2 + y^2 <= 9$ במישור $z = 2$.
הנורמל למשטח המוגדר על ידי מגמת העקום הוא $vu(n) = (0, 0, 1) = vu(k)$.
$
  integral.double_S (curl arrow(H)) dot vu(n) dd(S) = integral.double_(x^2+y^2 <= 9) (2x, 2y, 3) dot (0, 0, 1) dd(x) dd(y) = integral.double_(x^2+y^2 <= 9) 3 dd(x) dd(y)
$
זהו פשוט $3$ פעמים שטח העיגול $S$.
רדיוס העיגול הוא $R = 3$, ולכן שטחו הוא $pi dot 3^2 = 9 pi$.
העבודה היא $3 dot 9pi = 27pi$.
#תשובה[
  $ integral.cont_C arrow(H) dot dd(arrow(l)) = 27pi $
]

#שאלה(מזהה: <6>, כותרת: "שטף דרך ספירה", [
  נתון שדה וקטורי:
  $ arrow(F)(x,y,z) = (x, y, z) / (4x^2 + 4y^2 + z^2)^(3/2) $
  שמוגדר לכל $(x,y,z) != (0,0,0)$.
  חשבו את השטף של השדה דרך ספירת היחידה #box[$x^2 + y^2 + z^2 = 1$] עם נורמל חיצוני.
])
נחשב תחילה את הדיברגנץ של $arrow(F)$. נסמן $D = 4x^2 + 4y^2 + z^2$, ולכן $arrow(F) = (x D^(-3/2), y D^(-3/2), z D^(-3/2))$.
$ pdv(F_x, x) = D^(-3/2) - 3/2 x D^(-5/2) (8x) = (D - 12x^2) / D^(5/2) = (-8x^2 + 4y^2 + z^2) / D^(5/2) $
מטעמי סימטריה:
$ pdv(F_y, y) = D^(-3/2) - 3/2 y D^(-5/2) (8y) = (D - 12y^2) / D^(5/2) = (4x^2 - 8y^2 + z^2) / D^(5/2) $
ועבור $z$:
$ pdv(F_z, z) = D^(-3/2) - 3/2 z D^(-5/2) (2z) = (D - 3z^2) / D^(5/2) = (4x^2 + 4y^2 - 2z^2) / D^(5/2) $
סכום הנגזרות הוא הדיברגנץ:
$ arrow(nabla) dot arrow(F) = ((-8x^2+4y^2+z^2) + (4x^2-8y^2+z^2) + (4x^2+4y^2-2z^2)) / D^(5/2) = 0 $
מכיוון שהדיברגנץ מתאפס בכל המרחב פרט לראשית (שבה השדה אינו מוגדר), לפי משפט הדיברגנץ השטף דרך כל מעטפת סגורה המקיפה את הראשית הוא זהה.
נבחר לחשב את השטף דרך האליפסואיד $E: 4x^2 + 4y^2 + z^2 = R^2$ שעוטף את הראשית (למשל עם $R=1$, האליפסואיד מוכל בספירת היחידה).
על המשטח $E$ מתקיים $D = R^2$, ולכן השדה הוא:
$ arrow(F) = 1/R^3 (x, y, z) $
נמצא פרמטריזציה לאליפסואיד:
$ x = R/2 sin phi cos theta, quad y = R/2 sin phi sin theta, quad z = R cos phi $
הנורמל היוצא מהמשטח נתון על ידי:
$
  arrow(r)_phi times arrow(r)_theta &= (R/2 cos phi cos theta, R/2 cos phi sin theta, -R sin phi) times (-R/2 sin phi sin theta, R/2 sin phi cos theta, 0) \
  &= (R^2/2 sin^2 phi cos theta, R^2/2 sin^2 phi sin theta, R^2/4 sin phi cos phi)
$
מכאן:
$
  arrow(F) dot (arrow(r)_phi times arrow(r)_theta) &= 1/R^3 (R/2 sin phi cos theta, R/2 sin phi sin theta, R cos phi) dot (R^2/2 sin^2 phi cos theta, R^2/2 sin^2 phi sin theta, R^2/4 sin phi cos phi) \
  &= 1/R^3 (R^3/4 sin^3 phi cos^2 theta + R^3/4 sin^3 phi sin^2 theta + R^3/4 sin phi cos^2 phi) \
  &= 1/4 (sin^3 phi + sin phi cos^2 phi) = 1/4 sin phi (sin^2 phi + cos^2 phi) = 1/4 sin phi
$
השטף נתון על ידי האינטגרל הכפול:
$
  integral.double_E arrow(F) dot dd(arrow(S)) = integral_0^(2pi) integral_0^pi 1/4 sin phi dd(phi) dd(theta) = 2pi dot 1/4 [-cos phi]_0^pi = pi/2 dot 2 = pi
$
לכן השטף דרך ספירת היחידה הוא גם $pi$.
#תשובה[
  השטף של השדה דרך ספירת היחידה הוא $pi$.
]

#שאלה(מזהה: <7>, כותרת: "שטף דרך משטח איחוד", [
  יהי $S$ משטח שהוא איחוד המשטחים:
  $ S_1 = { (x,y,z) | x^2+y^2 <= 4, z=1 }, quad S_2 = { (x,y,z) | z = sqrt(x^2+y^2)-1, -1 <= z <= 1 } $
  ונתון השדה:
  $
    arrow(F)(x,y,z) = ( & x+y+z + x/(x^2+y^2+z^2)^(3/2), \
                        & 2x+2y+2z + y/(x^2+y^2+z^2)^(3/2), \
                        & 3x+3y+3z + z/(x^2+y^2+z^2)^(3/2))
  $
  חשבו את השטף של השדה $arrow(F)$ דרך $S$ עם נורמל חיצוני.
])
המשטח $S = S_1 union S_2$ הוא משטח סגור. $S_1$ הוא עיגול במישור $z=1$ ברדיוס $2$, ו־$S_2$ הוא מעטפת חרוט עם קודקוד ב־$(0,0,-1)$ ובסיס זהה ל־$S_1$ ב־$z=1$.
הראשית $(0,0,0)$ נמצאת בתוך הנפח $V$ הכלוא #box[בתוך $S$.]
נפצל את השדה לשני חלקים, $arrow(F) = arrow(F)_1 + arrow(F)_2$:
$ arrow(F)_1 = (x+y+z, 2x+2y+2z, 3x+3y+3z) $
$ arrow(F)_2 = (x, y, z) / (x^2+y^2+z^2)^(3/2) $
נחשב את השטף של $arrow(F)_1$ בעזרת משפט הדיברגנץ:
$ div arrow(F)_1 = 1 + 2 + 3 = 6 $
לכן האינטגרל על הנפח הוא:
$ integral.triple_V (div arrow(F)_1) dd(V) = 6 integral.triple_V dd(V) = 6 "Vol"(V) $
נחשב את נפחו. שפת החרוט היא $z = r - 1$, ולכן לכל $z in [-1, 1]$ הרדיוס נע בין $0$ ל־$z + 1$:
$
  "Vol"(V) & = integral.triple_V dd(V) = integral_(-1)^1 integral_0^(2pi) integral_0^(z+1) r dd(r) dd(theta) dd(z) \
           & = 2pi integral_(-1)^1 [r^2 / 2]_0^(z+1) dd(z) = pi integral_(-1)^1 (z+1)^2 dd(z) \
           & = pi [(z+1)^3 / 3]_(-1)^1 = pi (2^3 / 3 - 0) = (8 pi)/3
$
השטף של $arrow(F)_1$ הוא $6 dot (8 pi)/3 = 16 pi$.
השטף של השדה המרכזי $arrow(F)_2 = (arrow(r))/r^3$ דרך כל משטח סגור המקיף את הראשית הוא $4pi$.
סך הכל, השטף הכולל הוא סכום השטפים:
$ integral.double_S arrow(F) dot hat(n) dd(S) = 16 pi + 4 pi = 20 pi $
#תשובה[
  השטף הכולל של השדה $arrow(F)$ דרך המשטח $S$ הוא $20 pi$.
]
