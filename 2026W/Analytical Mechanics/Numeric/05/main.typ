#import "../../template.typ": *
#import "../../consts.typ": *
#import "../../utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "מכניקה אנליטית",
  number: "5 – תרגיל נומרי",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2025, month: 1, day: 15)
)
#set text(font: "Noto Serif Hebrew", weight: 500, lang: "he", region: "il")

#let th = $theta$
#let dth = $dot(th)$
#let ddth = $accent(th,diaer)$
#שאלה(כותרת: "תרגיל נומרי 2 – תיאור מספרי של כוכב חמה", [
בקורס ראינו איך המסלול של כוכב חמה מושפע מיחסות כללית, וחישבנו קירוב של המסלול כאשר ההפרעה המגיעה מיחסת כללית חלשה. כעת נחשב נומרית את המסלול של כוכב חמה בצורת מדויקת, ונראה מה קורה למסלול.

בתרגול הגדרנו את האנרגיה הפוטנציאלית של כוח מרכזי ביחסות כללית בתור:
$ U(r) = -alpha/r - beta/r^3 $
בדרך כלל רואים את האנרגיה הפוטנציאלית של כוח הכבידה ביחסות כללית רשומה כך:
$ (U_"eff" (r))/m = 1/2 (c^2 - (2 M G)/r)(1+ L^2/(m^2 r^2 c^2)) $
כאשר $M$ הוא מסת השמש, $m$ הוא מסת כוכב חמה, $G$ קבוע הכבידה האוניברסלי, ו-$c$ מהירות האור. כאשר משווים את שני הערכים, מקבלים שערכי הקבועים הם:
$ alpha = G M m, beta = (G M L^2)/(m c^2) $
])

#let th = $theta$
#let r0 = $r_0$
#סעיף[
בתרגול ראינו שהקשר בין המרחק של כוכב לכת לשמש והזווית במסלול של כוכב הלכת מקיים:
$ (dif^2 u)/(dif th^2) + u = m/L^2(alpha+3 beta u^2) $
כאשר $u = 1/r$ גודל עם יחידות. בפתרון נומרי של מד"רים, עבודה ישירה עם גדלים בעלי ממדים עלולה לסבך אותנו – הרי מה שאנחנו שמים בפועל במחשב זה מספרים חסרי יחידות. במד"רים לא לינארים כמו המד"ר שמופיע כאן, חוסר זהירות בהצבת הממדים עלול להוביל לטעויות לא רצויות. לכן, כאשר אנחנו נותנים למחשב לפתור משוואות, כדאי להפוך אותן למשוואות חסרות ממדים. כלומר, שכל המשתנים התלויים, המשתנים הבלתי-תלויים, וגם הקבועים, הם לגמרי חסרי ממדים.
נגדיר:
$ u = w/r_0 $
כאשר $r_0$ יתאר את המרחק *המירבי* של כוכב חמה מהשמש (אפהליון), ולו יש יחידות של אורך. ודאו שהמשתנה הדינמי $w$ אכן חסר ממדים. הגדירו קבועים חסרי ממדים חדשים $a,b$ כך שהמד"ר החדשה תהיה:
$ (dif^2 w)/(dif theta ^2) = a - w + 3 b w^2 $
]
נעביר את $u$ אגף ונפתח את הסוגריים:
$ (dif^2 u)/(dif th^2) = (m alpha)/L^2 -u + (3 m beta)/L^2 u^2 space.quad mid(|) dot r0 \ 
  (dif^2 u)/(dif th^2) r0 = (m alpha r0)/L^2 -u r0 + (3 m beta r0)/L^2 u^2
$

נבחין כי:
$ w = u dot r0 => (dif^2 w)/(dif theta ^2) = (dif^2 u)/(dif th^2) r0 $
נחליף במשוואה:
$ (dif^2 w)/(dif th^2) = (m alpha r0)/L^2 - w + (3 m beta cancel(r0))/L^2 w^2/(r0^cancel(2)) = (m alpha r0)/L^2 - w + (m beta) / (L^2 r0) 3 w^2 $
לכן:
#תשובה[
$ a = (m alpha r0)/L^2, b = (m beta)/(L^2 r0) => (dif^2 w)/(dif th^2) = a - w + 3 b w^2 $]
#סעיף[
חשבו את הקבועים $a,b$. היעזרו בגדלים הבאים:
#align(center)[#table(
  columns: 4,
  align: center,
  [מסת כוכב חמה $(m)$], [מסת השמש $(M)$], [אפהליון $(r0)$], [מהירות כוכב חמה באפהליון $(v_0)$],
$3.30 times 10^23 "kg"$, $1.99 times 10^30 "kg"$, $6.98 times 10^7 "km"$, $38.86 "km"/"s"$
)]]
#let v0 = $v_0$
בנקודת האפהליון המהירות ניצבת לרדיוס. לכן התנע הזוויתי הוא:
$ L = m v0 r0 $
מכאן:
$ a = (m alpha r0)/L^2 = (cancel(m) G M cancel(m) cancel(r0)) / (cancel(m)^2 v0^2 r0^cancel(2)) = (G M)/(v0^2 r0) = (6.674 times 10^(-11) ( 1.99 times 10^30))/(((38.86 dot 1000)^2)(6.98 times 10^10)) = 1.26 $
$ b = (m beta)/(L^2 r0) = (cancel(m) G M cancel(L^2))/(cancel(m) c^2 cancel(L^2) r0) = (G M)/(r0 c^2) = (6.674 times 10^(-11) ( 1.99 times 10^30))/((3 times 10^8)^2 (6.98 times 10^10)) = 2.11 times 10^(-8) $

#סעיף[
נבחר בתנאי התחלה
$w(0)=1,(dif w)/(dif th)(0)=0$.
פתרו נומרית את המד"ר ודרכו מצאו את $r(th)$. היעזרו בפונקצייה `polarplot` כדי לצייר את המסלול של כוכב חמה סביב השמש במישור $x y$ בתחום#linebreak()
$0<=th<=200pi$.#linebreak()
האם ניתן לראות פרסציה? מה צריך לשנות כדי שההפרעה של הפרסציה תגדל מספיק כדי לראות אותה בגרף זה?
]
#figure(
  image("03.svg"),
  caption: [
מסלול כוכב חמה.]
)
בגרף לא ניתן לראות פרסציה. זאת משום ש-$b$ קטן מאוד, וגם אחרי $100$ הקפות לא רואים שום שינוי בעין.

#סעיף[
נגדיל את $b$ וניקח אותו להיות $b=0.01$. ציירו עכשיו את המסלול של כוכב חמה בתחום $0<=th<=20pi$. תארו את המסלול.]

#figure(
  image("04.svg"),
  caption: [
מסלול כוכב חמה כאשר $b=0.01$.]
)
כעת ניתן לשים לב לפרסציה: המסלול דומה לאליפסה, אבל בכל הקפה, כוכב חמה לא חוזר בדיוק לאותה נקודה. מכיוון שכעת יש לנו גם פוטנציאל שתלוי ב-$1/r^3$, לא פועל רק כוח הכבידה של ניוטון. הפוטנציאל העודף גורם לאליפסה עצמה להסתובב.

#סעיף[
נגדיל את $b$ אף יותר וניקח אותו להיות $b=0.1$. ציירו עכשיו את המסלול של כוכב חמה בתחום $0<=th<=2pi$. מה קרה?]

#figure(
  image("05.svg"),
  caption: [
מסלול כוכב חמה כאשר $b=0.1$.]
)
כעת השתמשנו ב-$b$ גדול מדי. הכוח המשיכה המתוקן (היחסותי) הופך להיות דומיננטי מאוד במרחקים קצרים ומתגבר על הכוח הצנטריפוגלי שאמור להחזיק את הכוכב במסלול. לכן, $w$ שואף ל-$infinity$, ומכאן שהרדיוס $r$ שואף לאפס. כלומר, הכוכב קורס פנימה בספירלה ונופל לתוך השמש.


#pagebreak()
#show raw.where(block: true): block.with(
  fill: luma(240),
  inset: 10pt,
  radius: 4pt,
)
= נספח: קוד
נספח: קוד
```py
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

G = 6.674e-11
M = 1.99e30
r0 = 6.98e10
v0 = 38.86e3
c = 3e8

a_real = (G * M) / (v0**2 * r0)
b_real = (G * M) / (c**2 * r0)

print(f"Calculated a: {a_real:.4f}")
print(f"Calculated b: {b_real:.4e}")


def orbit_ode(theta, y, a, b):
    w = y[0]
    dw = y[1]
    d2w = a - w + 3 * b * (w**2)
    return [dw, d2w]


def solve_and_plot(filename, a_val, b_val, theta_max, title, color="tab:blue"):
    y0 = [1.0, 0.0]

    t_eval = np.linspace(0, theta_max, 10000)

    sol = solve_ivp(
        lambda t, y: orbit_ode(t, y, a_val, b_val),
        (0, theta_max),
        y0,
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    theta = sol.t
    w = sol.y[0]
    r_norm = 1.0 / w

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, projection="polar")

    lw = 2.0 if theta_max < 30 else 1.0

    ax.plot(theta, r_norm, color=color, linewidth=lw)
    ax.set_title(title, pad=20)

    ax.set_yticklabels([])
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(filename, format="svg")
    plt.close()
    print(f"Saved {filename}")


solve_and_plot(
    "03.svg",
    a_real,
    b_real,
    200 * np.pi,
    f"Mercury Orbit (Real parameters)\nb={b_real:.1e}",
)

solve_and_plot(
    "04.svg",
    a_real,
    0.01,
    20 * np.pi,
    "Mercury Orbit (Precession)\nb=0.01",
    color="tab:orange",
)

solve_and_plot(
    "05.svg", a_real, 0.1, 2 * np.pi, "Mercury Orbit (Decay)\nb=0.1", color="tab:red"
)
```
