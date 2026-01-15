#import "../template.typ": *
#import "../consts.typ": *
#import "../utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "מכניקה אנליטית",
  number: 8,
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


#סעיף[
היעזרו בפונקציה שבחרתם כדי למצוא את המסלול של מטוטלת הרמונית עם פרמטר
$g/l=10 space.narrow "s"^(-2)$
לפרק הזמן
$Delta t = 10 space.narrow "s"$
כאשר המטוטללת מתחילה ממנוחה ומזווית התחלתית:
$th_0 = 1,2,2.5,2.75,3$.
ציירו את $th(t)$ לכל אחד מתנאי ההתחלה בגרף אחד.]




























