#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "פיסיקה סטטיסטית ותרמית",
  number: "1",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 5, day: 10)
)

#let si = $sigma$
#let v1 = $V_1$; #let t1 = $T_1$; #let v2 = $V_2$; #let t2 = $T_2$
#שאלה(כותרת: "לחץ קרינה", [
    נתון תנור שחומם לטמפרטורה גבוהה. בניסוי זה, מקור הלחץ העיקרי בתנור מגיע מקרינה תרמית (מכונה גם קרינת גוף שחור) – אופני התנודה של השדות האלקטרומגנטיים המתפתחים בתנור. ניסיונית, הראו כי כאשר התנור מגיע לשיווי משקל, הלחץ בתנור אינו תלוי בנפח ומשוואת המצב נתונה על-ידי:
    #nonum($ P = 1/3 si T^4 $)
    כאשר $si$ קבוע.
    
    חשבו את העבודה המבוצעת על האלקטרומגנטיים (פוטונים) בין הנקודות
    $(v1,t1)$ ו-$(v2,t2)$
    עבור שני המסלולים הקוואזי-סטטיים $a$ ו-$b$ באיור:
    #figure(
      image("drawing.svg", width: 65%),
      caption: [דיאגרמת $V-T$ של התהליכים]
    )
    ])

#סעיף[כ]
#pagebreak()
#סעיף[נניח שהמשתנים $x,y,z$ הם בעצמם פונקציות של משתנה יחיד $u$. בטאו את $(del(y,x))_(psi,z) $ בעזרת הנגזרות של $x,y$ לפי $u$.
    ]
    פה כבר נמאס לי לכתוב $psi$ ביד, אז עברתי להקליד #emoji.face.inv. נחשב לפי כלל השרשרת את הנגזרת המלאה של $psi$ לפי $u$. נתון כי $u$ הוא המשתנה היחיד של $x,y,z$, לכן הנגזרת החלקית שלהם לפי $u$ היא גם הנגזרת המלאה ($star$):
$ (dif psi)/(dif u) = del(psi,x) (dif x)/(dif u) + del(psi,y) (dif y)/(dif u) + del(psi,z) (dif z)/(dif u) $
$z$ ו־$psi$
קבועות, לכן כמו בסעיף א',
$(dif psi)/(dif u)=(dif z)/(dif u)=0$. נציב, נעביר אגפים ונקבל:
$ del(psi,x) (dif x)/(dif u) = -del(psi,y) (dif y)/(dif u) => -del(psi,x)/del(psi,y) = (dif y)/(dif u) (dif x)/(dif y) $
נצטט את תוצאת סעיף א', נשתמש בתכונה $star$ ונקבל:
#תשובה[
  #nonum($ (del(y,x))_(psi,z) = (dif y)/(dif u) (dif x)/(dif u) = y'(u) x'(u) $) 
]