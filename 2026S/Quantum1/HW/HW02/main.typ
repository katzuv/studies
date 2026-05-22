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
  date: datetime(year: 2026, month: 5, day: 22)
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
$ cal(B) = {e1k, e2k} = {vec(1,0), vec(0,1)} $
נתונים שני אופרטורים $A, B$ המוגדרים על ידי פעולתם על #e1k, #e2k:
$
  
  & A #e1k = #e1k, #h(2em)&& A #e2k = - #e2k \
  & B #e1k = i #e2k, #h(2em)&& B #e2k = -i #e1k
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
$ & a_(11) = mel(e1, A, e1) = braket(e_1,e_1) stretch(=)_"בסיס אורתוגונלי" 1 \
  & a_(12) = mel(e1, A, e2) = -braket(e_1,e_2) = 0 \ 
  & a_(21) = mel(e2, A, e1) = braket(e_2,e_1) = 0 \ 
  & a_(22) = mel(e2, A, e2) = -braket(e_2,e_2) = -1
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
   $ (ab^+_cal(B))^+_cal(B) = overline(mat(1, 0; 0, -1)) = mat(1, 0; 0, -1) = ab $ ]
#let abdag = $ab^+$
  כלומר גם $A^+ = A$ ולכן גם $A^+$ הוא הרמיטי.

#סעיף[
  מצאו את הערכים העצמיים $a_n$ והמצבים העצמיים $|a_n⟩$ של האופרטור $A$.
]
מצאנו מטריצה מייצגת אלכסונית של $A$, לכן הערכים העצמיים הם $a_1 = 1, a_2 = -1$. נפתור את משוואת הערכים העצמיים:
$ & A ket(a_n) = mat(1, 0; 0, -1) vec(x, y) = a_n ket(a_n) = 1 vec(x,y) => \
  & vec(a,-b) = vec(a,b) => ket(a_n) = vec(1, 0) $
  עבור $a_2 = -1$:
$ & A ket(a_2) = mat(1, 0; 0, -1) vec(x, y) a_2 ket(a_2) = -1 vec(x,y) => \
  & vec(a,-b) = vec(-a,b) => ket(a_2) = vec(0, 1) $
לכן מצאנו את המצבים העצמיים:
#תשובה[
  $ a_1 = 1, ket(a_1) = vec(1, 0) $
  $ a_2 = -1, ket(a_2) = vec(0, 1) $
]

#סעיף[
  הראו מפורשות כי מתקיים פירוק היחידה עבור הבסיס
  $lr({|a_n chevron.r})$
]
$ sum_(n=1,2) ketbra(a_n) = ketbra(a_1) + ketbra(a_2) = mat(0, 0; 0, 1) + mat(1,0;0,0) = mat(1, 0; 0, 1) = bb(1) $
#תשובה[
  $ sum_(n=1,2) ketbra(a_n) = bb(1) $
]

#סעיף[
  רשמו את האופרטורים $A,B$ בעזרת הבסיס
  ${ket(a_n)}_(n=1,2)$
  בכתיב דיראק. האם האופרטור $B$ הוא אופרטור הרמיטי?
]
$ & b_(11) = mel(e1, B, e1) = i braket(e_1,e_2) stretch(=)_"בסיס אורתוגונלי" 0 \
  & b_(12) = mel(e1, B, e2) = -i braket(e_1,e_2) = -i \ 
  & b_(21) = mel(e2, B, e1) = i braket(e_2,e_1) = i \ 
  & b_(22) = mel(e2, B, e2) = -i braket(e_2,e_1) = 0
  $
  מכאן:
$ B_cal(B) = mat(0, -i; i, 0) $

נרשום את האופרטורים בבסיס המבוקש. קיבלנו כי ${a_n} = {e_n}$, לכן:
$ A = a_11 ketbra(a_1) + a_12 ketbra(a_1, a_2) + a_21 ketbra(a_2, a_1) + a_22 ketbra(a_2) = ketbra(a_1) - ketbra(a_2) $
$ B = b_11 ketbra(a_1) + b_12 ketbra(a_1, a_2) + b_21 ketbra(a_2, a_1) + b_22 ketbra(a_2) = -i ketbra(a_1, a_2) +i ketbra(a_2, a_1) $

נבדוק האם המטריצה המייצגת של הצמוד ההרמיטי של $B$ שווה למטריצה המייצגת של $B$:
$ B_cal(B)^+ = overline(mat(0, -i; i, 0)^T)  = overline(mat(0, i; -i, 0)) = mat(0, -i; i, 0) = B_cal(B) $
#תשובה[
  $ A = ketbra(a_1) - ketbra(a_2), quad B = -i ketbra(a_1, a_2) +i ketbra(a_2, a_1) $
  $ B_cal(B) = mat(0, -i; i, 0), B_cal(B)^+ = B_cal(B) $
  לכן $B$ הוא אופרטור הרמיטי.
]

#סעיף[
  חשבו את פעולת האופרטורים $A,B$ על המצב $ps$. מה ניתן להסיק על המצב $ps$?
]
$ A ps =  1/sqrt(2)(A e1k + i A e2k) = 1/sqrt(2)(e1k - i e2k) $
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
$ B ket(b_1) = lambda_1 ket(b_1) => mat(0, -i; i, 0) vec(x, y) = 1 dot vec(x, y) => vec(-i y, i x) = vec(x,y) => vec(x, y) = vec(1, i) $
עבור $lambda_2$:
$ B ket(b_2) = lambda_2 ket(b_2) => mat(0, -i; i, 0) vec(x, y) = -1 dot vec(x, y) => vec(-i y, i x) = vec(-x,-y) => vec(x, y) = vec(1, -i) $
ננרמל את הווקטורים העצמיים:
$ norm(ket(b_1)) = sqrt(|1|^2 + |i|^2) = sqrt(2), norm(ket(b_2)) = sqrt(|1|^2 + |-i|^2) = sqrt(2) $
לכן הבסיס המלכסן של $B$ הוא:
#תשובה[
  $ {1/sqrt(2) vec(1, i), 1/sqrt(2) vec(1, -i)} $
]


#שאלה[
  על סמך ההגדרה של אופרטור צמוד הרמיטי
  ($braket(u, T v) = braket(T^+u, v)$)
  הוכיחו את התכונות הבאות:
]
#סעיף[
  $ (T^+)^+ = T $
]
#סעיף[
  $ (T^(-1))^+ = (T^+)^(-1) $
]