#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *

#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "5",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 6, day: 14),
)

#שאלה(כותרת: "זהות בקומוטטורים", מזהה: <1>, [
  נתונים שני אופרטורים $A$ ו-$B$ ונתון כי האופרטור $B$ מתחלף עם יחסי החילוף שלהם, כלומר:
  $ [B, [A, B]] = 0 $

  הוכיחו כי לכל פונקציה אנליטית $f(x) = sum_(n=0)^infinity a_n x^n$ מתקיים:
  $ [A, f(B)] = [A, B] f'(B) $

  הסיקו זהות עבור קומוטטור מהצורה $[X, f(P)]$.
])
נוכיח ראשית כי מתקיים
$[A, B^n] = n [A, B] B^(n-1)$.
נוכיח באינדוקציה. עבור $n=1$ מתקיים:
$ [A, B^1] = 1 dot [A, B] B^(1-1) = [A, B] bb(1) = [A,B] space.en #emoji.checkmark $
נניח שהטענה נכונה עבור $n-1$, כלומר שמתקיים:
$ [A, B^(n-1)] = (n-1) [A,B] B^(n-2) $
כעת נוכיח את נכונות הטענה עבור $n$:
$
                    [A, B^n] = & [A, B dot B^(n-1)] = [A, B]B^(n-1) + B[A, B^(n-1)] \
        stretch(=)_"הנחת אינ'" & [A,B]B^(n-1) + B (n-1) [A,B]B^(n-2) \
  stretch(=)_([B, [A, B]] = 0) & [A, B]B^(n-1) + (n-1)B [A, B]B^(n-2) \
                             = & [A, B]B^(n-1) + (n-1)[A, B]B dot B^(n-2) \
                             = & [A, B] B^(n-1) + (n-1)[A, B]B^(n-1) = (1 + n -1)([A, B]B^(n-1)) \
                             = & n[A, B]B^(n-1)
$
כעת נוכיח את המבוקש, ונזכור כי $A$, $B$ ו-$[A, B]$ אופרטורים לינאריים:
$
  [A, f(B)] & = [A, sum_(n=0)^oo a_n B^n] = sum_(n=0)^oo a_n [A, B^n] = sum_(n=0)^oo a_n n[A, B]B^(n-1) \
            & = [A, B] sum_(n=1)^oo n a_n B^(n-1) = [A, B] f'(B)
$
#משל
כעת נעבור לחלק השני. ידוע כי עבור אופרטורי המיקום והתנע מתקיים
$[X, P] = i hbar$.
נסמן $A=X$ ו-$B=P$. אזי:
$ [P, [X, P]] = [P, overbrace(i hbar, "scalar")] = 0 $
לכן לפי הזהות שהוכחנו מתקיים:
#תשובה[$ [X, f(P)] = [X, P] f'(P) = i hbar f'(P) $]

#שאלה(כותרת: "מצבים עצמיים של אופרטורים", מזהה: <2>, [
  נתון אופרטור הרמיטי $W$ כך ש-$W ket(w_i) = w_i ket(w_i)$. כמו כן, נתון כי הספקטרום של האופרטור $W$ הוא דיסקרטי.
])

#סעיף(מזהה: <2.א>, [
  הראו כי בהינתן $ket(psi)$
  תוצאה של מדידת $W$ תהיה תמיד $w_i$ אמ"מ $ket(psi) = ket(w_i)$, או #box[$ket(psi) = sum_n a_n ket(w_i\, n)$] אם $w_i$ מנוון.

  *הערה חשובה:* הכוונה ב"תמיד" היא כאשר חוזרים על הניסוי ושוב ושוב, ולא עבור מערכת שמתפתחת בזמן!
])
נניח כי יש $N$ מצבים עצמיים ל-$w$. נניח ראשית כי $ket(psi)$ שייך למרחב העצמי של $w_i$. לכן, ניתן לרשום את $ket(psi)$ כצירוף לינארי של מצבי בסיס התואמים לערך העצמי $w_i$:
$ ket(psi) = sum_(n=1)^N a_n ket(w_i\, n), space.en sum_(n=1)^N abs(a_n)^2 = 1 $
נחשב את ההסתברות למדוד $w_1$:
#let wi = $w_i$
$
  P(w_i) & = sum_(n=1)^N abs(braket(wi\, n, psi))^2 = sum_(n=1)^N abs(braket(wi\, n, sum_(m=1)^N a_m ket(wi\, m)))^2 \
         & = sum_(n=1)^N abs(sum_(m=1)^N a_m braket(wi\, n, wi\, m))^2 =^* sum_(n=1)^N abs(a_n)^2 = 1
$
קיבלנו כי ההסתברות למדוד $wi$ היא $1$, כאשר ב-$*$ השתמשנו בכך שמצבים עצמיים שונים המתאימים לאותו ערך עצמי הם אורותוגנוליים, תוך הנחה שהבסיס העצמי מנורמל. $qed$

#linebreak()
כעת נניח כי $p(wi) = 1$. נרשום את $ket(psi)$ כצירוף לינארי של כלל מצבי הבסיס האורתונורמליים של $W$ בספקטרום שלו. נניח כי יש $M$ ערכים עצמיים שונים ל-$W$:
$ ket(psi) = sum_(m=1)^M sum_(n=1)^(N_m) a_(m,n) ket(w_m\, n), space.en sum_(m=1)^M sum_(n=1)^(N_m) abs(a_(m,n))^2 = 1 $
נחשב מפורשות את $p(wi)$:
$
  p(wi) &= sum_(j=1)^(N_i) abs(braket(w_i\,j, psi))^2 = sum_(j=1)^N_i abs(sum_(m=1)^M sum_(n=1)^N a_(m,n)braket(wi\, j, w_m\, n))^2 \
  &= sum_(j=1)^(N_i) abs(a_(i,j) braket(wi\, j, wi, j))^2 = sum_(j=1)^(N_i) abs(a_(i,j))^2 = 1
$
כלומר מתקיים:
$
  1 stretch(=)_"תנאי נרמול" sum_(m=1)^M sum_(n=1)^N_m abs(a_(m,n))^2 = sum_(n=1)^N_i abs(a_(i,n))^2 + sum_(i!=m=1)^M sum_(n=1)^N_m abs(a_(m,n))^2 = 1 + sum_(i!=m=1)^M sum_(n=1)^N_m abs(a_(m,n))^2 \
  => sum_(i!=m=1)^M sum_(n=1)^N_m abs(a_(m,n))^2 = 0
$
כלומר $ket(psi)$ מורכב אך ורק ממצבי הבסיס העצמי של הערך העצמי $wi$. $qed$

#סעיף(מזהה: <2.ב>, [
  נתון $Lambda ket(lambda_i) = lambda_i ket(lambda_i)$. מודדים את $W$ ומקבלים ערך $w_j$. לאחר מכן, מודדים את $Lambda$, ואחר כך מודדים שוב את $W$.
])

#תתסעיף(מזהה: <2.ב.1>, [
  הראו שלכל $w_j$, מדידת $W$ בפעם השנייה תיתן בוודאות $w_j$ אמ"מ $[W, Lambda] = 0$.
])
נניח ראשית כי $[W, Lambda] = 0$. אזי שני האופרטורים חולקים בסיס משותף של מצבים עצמיים, שנסמנם
$ket(w_j\, lambda_i\, n)$.
כלומר, זהו מצב עצמי המתאים לערך עצמי $w_j$ של $W$, לערך עצמי $lambda_i$ של $Lambda$, בתוספת אינדקס למקרה שיש ניוון.

אחרי המדידה הראשונה המצב הוא סופרפוזיציה של מצבים $ket(w_j\, lambda_i\, n)$. נסמן את המצב $ket(psi)$:
$ ket(psi) = sum_i sum_n c_(i,n) ket(w_j\, lambda_i\, n) $

נניח שבמדידה השנייה מקבלים ערך $lambda_k$. זה אומר שכעת מצב המערכת מורכב רק ממצבים עצמיים של $Lambda$ בעלי הערך העצמי $lambda_k$. לכן, מצב המערכת כעת הוא:
$ ket(psi') = sum_n c_(k,n) ket(w_j\, lambda_k\, n) $
משום שכל המצבים העצמיים המרכיבים את $ket(psi')$ מתאימים לערך העצמי $w_j$, אזי מדידה חוזרת של $W$ תיתן בוודאות $w_j$. $qed$

#linebreak()
כעת נניח כי בוודאות המדידה הראשונה והשלישית תתנה $w_j$ והמדידה השנייה תיתן $lambda_k$.
נסמן ב-$ket(psi_i)$ את המצב אחרי המדידה ה-$i$.
מההנחה נקבל כי $ket(psi_1)$ ו-$ket(psi_3)$ הם מצבים עצמיים של $W$ עם #box[ערך עצמי $w_j$].
בנוסף, $ket(psi_2)$ הוא מצב עצמי של $Lambda$ עם $lambda_k$.

מדידת $W$ על $ket(psi_2)$ תחזיר בוודאות $w_j$, לכן $ket(psi_2)$ הוא גם מצב עצמי של $W$ עם ערך עצמי $w_j$. כלומר:
$ W ket(psi_2) = w_j ket(psi_2), space Lambda ket(psi_2) =lambda_k ket(psi_2) $
משום שזה נכון לכל $w_j$ ולכל $lambda_k$, נוכל לבנות בסיס מלא למרחב המורכב ממצבים עצמיים של $W$ וגם של $Lambda$.
לכן האופרטורים מתחלפים. $qed$

#pagebreak()
#תתסעיף(מזהה: <2.ב.2>, [
  הראו כי אם $[W, Lambda] = i Gamma$ וגם ל-$Gamma$ אין ערך עצמי אפס, אז לכל $w_j$ לא ניתן לדעת בוודאות מהי תוצאת מדידת $W$ בפעם השנייה.
])
נניח בשלילה שקיימים $w_j$ ו-$lambda_k$ כך שניתן לדעת בוודאות שהמדידה השנייה תיתן $w_j$. כפי שראינו #box[ב@2.ב.1], זה אומר ש-$ket(psi_2)$ הוא מצב עצמי של $Lambda$ וגם של $W$, כלומר:
$ W ket(psi_2) = w_j ket(psi_2), space Lambda ket(psi_2) =lambda_k ket(psi_2) $
נפעיל את הקומטטור על $ket(psi_2)$:
$
  [W, Lambda] ket(psi_2) = (W Lambda - Lambda W) ket(psi_2) = W lambda_k ket(psi_2) - Lambda w_j ket(psi_2) =
  (lambda_k w_j - w_j lambda_k) ket(psi_2) = 0
$
משום ש-$[W, Lambda] = i Gamma$, נקבל:
$ i Gamma ket(psi_2) = 0 = 0 ket(psi_2) => Gamma ket(psi_2) = 0 ket(psi_2) $
$ket(psi_2)$ הוא מצב מנורמל, לכן שונה מאפס. לכן,
קיבלנו ש-$ket(psi_2)$ הוא מצב עצמי של $Gamma$ עם ערך עצמי אפס, בסתירה לנתון של-$Gamma$ אין ערך עצמי אפס. $qed$


#שאלה(כותרת: "פונקציית גל לורנציאנית", מזהה: <3>, [
  מערכת מתוארת על ידי פונקציית גל:
  $ psi(x) = sqrt(a^3) 1/(x^2 + a^2) $
  כאשר $a$ פרמטר ממשי.
])

#סעיף(מזהה: <3.א>, [
  נרמלו את $psi(x)$.

  *הדרכה:* השתמשו באינטגרל $integral_(-infinity)^infinity 1/(x^2+a^2) dd(x) = pi (a^2)^(-1/2)$ ובגזירה לפי $a^2$.
])
נמצא $n >0$ כך שיתקיים:
$ 1 = integral_(-oo)^oo abs(n psi(x))^2 dd(x) = n^2 integral_(-oo)^oo (a^3)/(x^2 + a^2)^2 dd(x) $
נשים לב כי
$pi(a^2)^(-1/2)=pi/a$ ונגזור את הנתון לפי $a$:
$
  dv(, a) integral_(-oo)^(oo) 1/(x^2 + a^2) dd(x) = integral_(-oo)^(oo) dv(, a) (1/(x^2 + a^2)) dd(x) = integral_(-oo)^oo (-2a)/(x^2+a^2)^2 dd(x) = -pi/a^2
$
נציב חזרה:
$
  n^2 integral_(-oo)^oo (a^3)/(x^2 + a^2)^2 dd(x) & = -(a^2 n^2)/2 integral_(-oo)^oo (-2a)/(x^2+a^2)^2 dd(x) \
                                                  & = -(a^2 n^2)/2 dot (-pi/a^2) = (pi n^2)/2 = 1 => n = sqrt(2/pi)
$
#תשובה[
  $ psi(x) = sqrt((2a^3)/pi)1/(x^2+a^2) $
]

#סעיף(מזהה: <3.ב>, [
  חשבו את $expval(X), expval(X^2), Delta X$ וגם את $expval(P), expval(P^2), Delta P$.
])
$ expval(X) = integral_(-oo)^oo x |psi(x)|^2 dd(x) $
$psi(x)$ פונקציה ממשית זוגית, לכן גם $|psi(x)|^2$ זוגית. $x$ פונקציה אי-זוגית ולכן האינטגרל מתאפס ונקבל $expval(X)=0$.
נשים לב כי משום ש-$a^3$ נמצא מתחת לשורש ושאר הגורמים חיוביים, נדרוש $a>0$.
$
  expval(X^2) &= integral_(-oo)^oo x^2 |psi(x)|^2 dd(x) = integral_(-oo)^oo x^2 abs((2a^3)/pi 1/(x^2+a^2)^2) dd(x) \
  &= integral_(-oo)^oo (x^2 + a^2 - a^2)(2a^3)/(pi(x^2+a^2)^2) dd(x) = (2a^3)/pi ( integral_(-oo)^oo 1/(x^2+a^2) dd(x) - a^2 integral_(-oo)^oo 1/(x^2+a^2)^2 dd(x)) \
  &= (2a^3)/pi (pi/a - pi/(2a)) = (2a^3)/pi pi/(2a) = a^2
$
נחשב את השונות:
$ Delta X = sqrt(expval(X^2) - expval(X)^2) = sqrt(a^2 - 0) = a $

#linebreak()
כעת נחשב עבור $P$:
$
  expval(P) &= expval(P, psi(x)) = integral_(-oo)^oo (-i hbar) psi^*(x) dv(psi, x) dd(x) = -1/2 i hbar integral_(-oo)^oo 2 psi(x) dv(psi, x) dd(x) \
  &= -(i hbar)/2 integral_(-oo)^oo dv(psi^2, x) dd(x) = -(i hbar)/2 evaluated(psi^2(x))_(-oo)^oo = 0
$
משום שזו פונקציית גל, עליה לשאוף לאפס ב-$pm oo$.

נמצא את $P^2$:
$ P^2 psi(x) = (-i hbar)^2 dv(psi, x, 2) = -hbar^2 dv(psi, x, 2) $
נחשב את התוחלת:
$ expval(P^2) = -hbar^2 integral_(-oo)^oo psi(x) dv(psi, x, 2) dd(x) $
נשתמש באינטגרציה בחלקים. נסמן:
#[ #set math.cases(gap: 0.6em)
  $
    cases(
      u = psi(x) \, space dd(u) = dv(psi, x),
      dd(v) = dv(psi, x, 2) \, space v = dv(psi, x),
    )
  $ ]
$
  expval(P^2) = -hbar^2(cancel(evaluated(psi'(x)psi(x))_(-oo)^oo) - integral_(-oo)^oo (psi'(x))^2 dd(x)) = hbar^2 integral_(-oo)^oo (psi'(x))^2 dd(x)
$
נחשב את הנגזרת:
$ dv(psi, x) = sqrt((2a^3)/pi) (-2x)/(x^2+a^2)^2 $
$ (psi'(x))^2 = (2a^3)/pi (4x^2)/(x^2+a^2)^4 = (8a^3 x^2)/(pi (x^2+a^2)^4) $
לאחר חישוב האינטגרל נקבל כי:
$ expval(P^2) = hbar^2/(2a^2) $
נחשב את השונות:
$ Delta P = sqrt(expval(P^2) - expval(P)^2) = sqrt(hbar^2/(2a^2) - 0) = hbar/(sqrt(2)a) $
#תשובה[
  $
    & expval(x) = 0, space.en expval(X^2) = a^2,                    && Delta X = a \
    & expval(P) = 0, space.en expval(P^2) = hbar^2/(2a^2), space.en && Delta P = hbar/(sqrt(2)a)
  $
]
#סעיף(מזהה: <3.ג>, [
  חשבו את $Delta X Delta P$.
])
#תשובה[
  $ Delta X Delta P = hbar/sqrt(2) $
]

#שאלה(כותרת: "המילטוניאן במרחב הדואלי (תרגיל בונוס)", מזהה: <4>, [
  חשבו את $bra(psi(t)) H$.
])
נצטט את משוואת שרדינגר:
$ i hbar dv(, t)ket(psi(t)) = H ket(psi(t)) $
ניקח את הצמוד למשוואה, ונזכור כי $H$ הרמיטי:
$ -i hbar dv(, t)bra(psi(t)) = (H ket(psi(t)))^+ = bra(psi(t)) H $
#תשובה[
  $ bra(psi(t)) H = -i hbar dv(, t)bra(psi(t)) $
]

#שאלה(כותרת: "ניוון במצבים (תרגיל בונוס)", מזהה: <5>, [
  נתון כי חלקיק יכול להימדד בצבעים $ket(r), ket(g), ket(b)$. נתון גם כי הוא יכול להימדד במצב קשה $ket(h)$ או רך $ket(s)$ בלבד.
  הסבירו מדוע לפחות אחד מהמצבים $ket(h)$ או $ket(s)$ מנוון.
])
לפי הנתון על הצבעים נסיק שהמימד של המרחב הוא $3$ או יותר אם אחד ממצבי הצבע מנוון. משום שאופרטור הקושי הרמיטי, המצבים העצמיים שלו חייבים לפרוס את המרחב כולו. משום שיש שני ערכים עצמיים בלבד, חייב להתקיים שלפחות אחד מהמצבים העצמיים מנוון. נראה בחישוב. נסמן את מימד המרחב כולו ב-$n >= 3$, ואז:
$
  & dim(ker(H-h I)) + dim(ker(H-s I)) = n => \
  & dim(ker(H-h I)) = n - dim(ker(H-s I))
$
נניח בה"כ כי $dim(ker(H- s I)) = 1$, אז $dim(ker(H-h I)) = n-1 >= 2$ ולכן הוא מנוון.

#שאלה(כותרת: "מדידות במרחב רציף", מזהה: <6>, [
  נתון כי מדידת טמפרטורה $T$ יכולה לקבל כל ערך בין $0$ ל-$1$. נסמן את הערכים העצמיים והווקטורים העצמיים של $T$ ב-$ket(t)$, וננרמל: $braket(t, t') = delta(t-t')$.
  נתון כי:
  $ ket(psi) = integral_(1/2)^1 c ket(t') dd(t') $
  כאשר $c$ הוא קבוע כלשהו (כלומר אינו תלוי ב-$t$).
])

#סעיף(מזהה: <6.א>, [
  מהם ערכי הטמפרטורה האפשריים שנמדוד עבור $ket(psi)$?
])
נחשב את ההסתברות למדוד ערך $t$ כלשהו:
#set math.cases(gap: .5em)
$
  braket(t, psi) = bra(t) integral_(1/2)^1 c ket(t') dd(t') = c integral_(1/2)^1braket(t, t') dd(t') = c integral_(1/2)^1 delta(t-t') dd(t') = cases(c\, 1/2<=t<=1, 0\, "else")
$
#תשובה[
  ערכי הטמפרטורה האפשריים למדידה הם בקטע $[1/2, 1]$.
]

#סעיף(מזהה: <6.ב>, [
  נניח:
  $ ket(psi) = integral_(1/2)^1 c(t') ket(t') d t' $
  כאשר $c(t') != 0$ פונקציה חלקה וסופית כלשהי. מהם ערכי הטמפרטורה האפשריים כעת?
])
נחשב את ההסתברות למדוד ערך $t$ כלשהו:
#set math.cases(gap: .5em)
$
  braket(t, psi) = bra(t) integral_(1/2)^1 c(t') ket(t') dd(t') = integral_(1/2)^1 c(t') braket(t, t') dd(t') = integral_(1/2)^1 c(t') delta(t-t') dd(t') = cases(c(t)\, 1/2<=t<=1, 0\, "else")
$
זאת כי מתקיים:
$ c(t)!=0, delta(t-t')=0 <=> t=t' $
#תשובה[
  ערכי הטמפרטורה האפשריים למדידה הם בקטע $[1/2, 1]$.
]

#שאלה(כותרת: "המילטוניאן תלוי בזמן", מזהה: <7>, [
  נתונה מערכת עם 2 מצבים, $ket(1)$ ו-$ket(2)$, והההמילטוניאן הבא:
  $ H(t) = A ketbra(1) + B cos(omega t) ketbra(1, 2) + B cos(omega t) ketbra(2, 1) - A ketbra(2) $
])

#סעיף(מזהה: <7.א>, [
  מהם ערכי האנרגיה שניתן למדוד?
])
ערכי האנרגיה שניתן למדוד הם הערכים העצמיים של $H(t)$, נרשום את המטריצה המייצגת שלו:
$ M = mat(A, B cos(omega t); B cos(omega t), -A) $
נסמן את הערכים העצמיים ב-$E_(1,2)$. נפתור את הפולינום האופייני:
$ p(E) = abs(A - lambda I) = mdet(A - E, B cos(omega t); B cos(omega t), -A - E) = E^2 - A^2 - B^2 cos^2(omega t) = 0 $
#תשובה[
  ערכי האנרגיה האפשריים למדידה הם:
  $ E_(1,2) = pm sqrt(A^2 + B^2 cos^2 (omega t)) $
]
#סעיף(מזהה: <7.ב>, [
  מהו $[H(t), H(t')]$?
])

$
  H(t) H(t') &= mat(A, B cos(omega t); B cos(omega t), -A) mat(A, B cos(omega t'); B cos(omega t'), -A) \ &= mat(A^2 + B^2 cos(omega t)cos(omega t'), A B cos(omega t') - A B cos(omega t); B A cos(omega t) - B A cos(omega t'), -A^2 + B^2 cos(omega t)cos(omega t'))
$
$
  H(t') H(t) &= mat(A, B cos(omega t'); B cos(omega t'), -A) mat(A, B cos(omega t); B cos(omega t), -A) \ &= mat(A^2 + B^2 cos(omega t')cos(omega t), A B cos(omega t) - A B cos(omega t'); B A cos(omega t') - B A cos(omega t), -A^2 + B^2 cos(omega t')cos(omega t))
$
$
  [H(t), H(t')] & = H(t) H(t') - H(t') H(t) \
                & = mat(0, 2 A B(cos(omega t') - cos(omega t)); -2 A B(-cos(omega t) + cos(omega t')), 0)
$
#תשובה[
  $ [H(t), H(t')] = 2A B(cos(omega t') - cos(omega t))(ketbra(1, 2) - ketbra(2, 1)) $
]
