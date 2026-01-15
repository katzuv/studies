#import "../template.typ": *
#import "../consts.typ": *
#import "../utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "מכניקה אנליטית",
  number: "3 – תרגיל נומרי",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2025, month: 1, day: 15)
)
#set text(font: "Noto Serif Hebrew", weight: 500, lang: "he", region: "il")

#let th = $theta$
#let dth = $dot(th)$
#let ddth = $accent(th,diaer)$
#שאלה(כותרת: "תרגיל נומרי 1 – תיאור מספרי של המסלול של מטוטלת הרמונית", [
בתרגיל זה ננסה למצוא מסלול למטוטלת הרמונית. משוואת התנועה של המטוטלת היא:

$ ddth = - g/l sin th $
])
#סעיף[
עיינו בדף העזרה לפונקציה שבחרתם. מהם הפרמטרים שצריך לספר לפונקציה כדי להשתמש בה? מה צריכה להיות המעלה של מערכת המד"רים שמספקים לפונקציה?]
בתרגיל זה בחרתי להשתמש בפונקציה 
`scipy.integrate.solve_ivp()`
בשביל לפתור בשיטת Runge-Kutta מד"ר מהצורה
$dif y = f(t,y) dif t$.

הפרמטרים שצריך לספק לפונקציה הם כלהלן:
- `fun`:
 הפונקציה $f$ שנמצאת באגף ימין של המד"ר שהיא הנגזרת של $y$ לפי הזמן.
- `t_span`:
 תחום הזמן עליו נפעיל את האינטגרציה.
- `y0`:
 תנאי ההתחלה של המשוואה. אורך המערך הוא כמספר המשוואות.

שאר הפרמטרים בעלי ערכי ברירת מחדל. הפונקציה יודעת לפתור מערכת משוואות מסדר ראשון.

#סעיף[
שימו לב שאי אפשר להכניס את המד"ר שהתחלנו איתו ישירות לשיטה הנומרית. היעזרו בהצבה
$y(t)=dth$
כדי לרשום צורה אחרת למד"רים כך שיהיה אפשר להכניס אותה לפונקציה שבחרתם.]
נסמן $y$ להיות וקטור המשתנים שלנו כך:
#set math.vec(delim: "[")
$ y = vec(th, dth) $
נגזור את $y$ לפי הזמן:
$ (dif y)/(dif t) = dif/(dif t) = vec(dth, ddth) = vec(dth, -g/l sin th) = vec(y[1], -g/l sin y[0]) $

#pagebreak()
#סעיף[
היעזרו בפונקציה שבחרתם כדי למצוא את המסלול של מטוטלת הרמונית עם פרמטר
$g/l=10 space.narrow "s"^(-2)$
לפרק הזמן
$Delta t = 10 space.narrow "s"$
כאשר המטוטלת מתחילה ממנוחה ומזווית התחלתית:
$th_0 = 1,2,2.5,2.75,3$.
ציירו את $th(t)$ לכל אחד מתנאי ההתחלה בגרף אחד.]
#figure(
  image("pendulum_ode.svg"),
  caption: [
זווית המטוטלת כתלות בזמן עם זוויות התחלתיות שונות. המשולשים מסמנים את נקודות המינימום.]
)
#סעיף[מה קורה לזמן המחזור של המטוטלת ככל שמגדילים את $th_0$?
]
נתבונן במספר נקודת המינימום שיש בכל גרף. ניתן לראות שככל שהזווית ההתחלתית גדולה יותר, כך יש יותר מרווח בין משולש לזה שאחריו. למשל, כאשר $th_0=1$ יש חמישה משולשים, אך כאשר $th_0=3$ יש רק שניים. כלומר, באותו פרק זמן המטוטלת מבקרת פחות פעמים באותו מיקום. זה אומר כי:
#תשובה[
ככל שמגדילים את $th_0$, כך זמן המחזור עולה.]
#show link: underline

= נספח: קוד
נספח: קוד. זמין גם 
#link("https://github.com/katzuv/studies/blob/main/2026W/Analytical%20Mechanics/Numeric/03.py")[כאן].
```py
import matplotlib.pyplot as plt
import numpy as np
import scipy

gravity = 9.81
length = 0.981
time_frame = (0, 10)


def pendulum_ode(t, y):
    theta, omega = y
    second_derivative = -(gravity / length) * np.sin(theta)
    return np.array((omega, second_derivative))


if __name__ == "__main__":
    initial_condition = (1, 2, 2.5, 2.75, 3)
    for ic in initial_condition:
        sol = scipy.integrate.solve_ivp(
            pendulum_ode,
            time_frame,
            (ic, 0),
            t_eval=np.linspace(0, 10, 1000),
            rtol=1e-9,  # Reducing allowed errors.
            atol=1e-9,
        )

        time, theta = sol.t, sol.y[0]
        (line,) = plt.plot(time, theta, label=f"$\\theta_0$: {ic} rad")
        color = line.get_color()

        minima_indices = scipy.signal.argrelextrema(theta, np.less)[0]
        plt.scatter(
            time[minima_indices],
            theta[minima_indices],
            color=color,
            marker="^",
            s=50,
            zorder=5,
        )

        for count, index in enumerate(minima_indices):
            x_pos = time[index]
            y_pos = theta[index]

            plt.text(
                x_pos,
                y_pos + 0.4,
                str(count + 1),
                color=color,
                ha="center",
                va="top",
                fontweight="bold",
            )

    plt.xlabel("Time (s)")
    plt.grid()
    plt.legend()
    plt.ylabel("Angular Displacement (rad)")
    plt.savefig("pendulum_ode.svg", format="svg")
    plt.show()
```

























