#import "@preview/ctheorems:1.1.3": *
#import "@preview/cetz:0.2.0"
#import "../../utils.typ": *
#show: thmrules

#set text(lang: "he", dir: rtl, font: "David")
#set heading(numbering: "1.1")


#let משפט = thmbox(
  "theorem", // This is the unique identifier for the internal counter for theorems
  "משפט", // This is the displayed name of the environment (e.g., "Theorem 1.1")
  fill: rgb("#e8e8f8"), // Optional: adds a light blue background fill to the theorem box
  inset: (x: 1.2em, top: 1em, bottom: 0.8em), // Optional: adds padding inside the theorem box
  radius: 4pt // Optional: rounds the corners of the theorem box
)

#let למה = thmbox(
 "theorem", // identifier - same as that of theorem
 "לֶמה", // head
 fill: rgb("#efe6ff")
)
#let הוכחה = thmproof("proof", "הוכחה")
#let הגדרה = thmbox(
 "definition",
 "הגדרה",
 // base_level: 1, // take only the first level from the base
 stroke: rgb("#68ff68") + 1pt
)
#let דוגמה = thmbox(
 "examples",
 "דוגמה",
 // base_level: 1, // take only the first level from the base
 stroke: rgb("#a86432") + 1pt
)
#let דוגמאות = thmbox(
 "examples",
 "דוגמאות",
 // base_level: 1, // take only the first level from the base
 stroke: rgb("#a86432") + 1pt
)

#set align(center)
  #text(3.5em)[
    חדו"א 1ת -- קיץ תשפ"ה 
  ] \
  \
#שם-מייל

#outline()
#set align(right)
‎#הרצאה("1", "25/08/25", "https://panoptotech.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=ab37c0fb-0517-4540-b13d-b34400d08c31")
== קבוצות
סימון של קבוצה: ${}$. בקבוצה אין חזרות ואין חשיבות לסדר, כלומר ${1,2,3}={3,2,1}={1,1,2,3}$.

נראה כמה סימונים בסיסיים. יהיו $A$ ו-$B$ קבוצות כאשר $A={1,2,7}, B={1,3,7$. כדי לסמן שאף קבוצה לא מכילה את השנייה נסמן $A subset.eq.not B, B subset.eq.not A$. \
את *החיתוך* של הקבוצות, כלומר הקבוצה שמכילים את האיברים המשותפים לשתי הקבוצות, נסמן ב-$A inter B = {1,7}$. *האיחוד* שלהן יכיל את האיברים שקיימים בלפחות קבוצה אחת ויסומן ב-$A union B = {1,3,2,7}$

נראה כמה קבוצות בסיסיות של מספרים.

*המספרים הטבעיים $NN$*:
$NN = {1, 2, 3, 4, ...}, NN_0 = {0, 1, 2, 3, 4, ...}$ 

$ 2 in A = {1, 2, 7} subset.eq NN, 4 in.not A \
 NN_"even" = {2, 4, 6, 8}  = {n in NN | #heb[זוגי] n } = {n in NN | n  = 2k, k in NN } \ 
NN_"even" union NN_"odd" = NN, NN_"even" inter NN_"odd" = {} = emptyset = #text(font: "David", [קבוצה ריקה])
$
\
*המספרים השלמים $ZZ$*: $ZZ={...,-3,-2,-1,0,1,2,3,...}$


*המספרים הרציונליים $QQ$*:
$QQ={m/n| m,n in ZZ, n eq.not 0}$

שבר $m/n$ ייקרא *מצומצם* אם לא קיימים שלמים המקיימים:
$ a,b,k, k > 1, m = k dot a, m = k dot b $
נראה ש-$84/27$ אינו שבר מצומצם:
$ 84/27 = (28 dot cancel(3)) / (9 dot cancel(3))$.
האם כעת קיבלנו שבר מצומצם? $ 28/9 = (7 dot 2^2)/3$, כלומר אין גורם משותף למונה ולמכנה גדול מ-1.

*מספרים ממשיים $RR$:* "כל המספרים שניתן למקם על הציר": $2, -84/27, pi, e, sqrt(2)$. כל שבר עשרוני סופי או אינסופי. \ מתקיים: $ZZ subset QQ subset RR$

== קטעים
נרצה דרך נוחה לסמן קטעים שתחומים בין שני מספרים ממשיים. יהיו $a<b a, b in RR$. נסמן את הקטעים הבאים:
+ *קטע פתוח*: $(a,b)={x in RR | a < x < b}$. אפשר גם לוותר על $x in RR$.
+ *קטע סגור*: $[a,b]={a<=x<=b}$
+ *קטע חצי סגור/פתוח*: $[a,b)={a<=x<b}, (a,b]={a<x<=b}$
ניתן לקחת גם את $infinity$ בתור אחד הקצוות, כאשר קצה זה פתוח: \
     $(a, infinity) = {x in RR | x > a}, (-infinity, a] = { x in RR | x <= a}$
 
 לא נתעסק בקטע מהצורה $[a, infinity]$.
 
 #הגדרה("סביבת-ε / ε-סביבה")[
    סביבת $epsilon$ של $x_0 in RR$ הוא קטע מהצורה $(x_0 - epsilon, x_0 + epsilon)$.
 ]
 #הגדרה("סביבת-ε נקובה / ε-סביבה נקובה")[
    סביבת $epsilon$ *נקובה* של $x_0 in RR$ הוא קטע מהצורה:    
        $ (x_0 - epsilon, x_0 + epsilon) without {x_0} = (x_0 - epsilon, x_0) union (x_0, x_0 + epsilon) $
        ]
#let scale = 50pt  // pixels per unit

//#import "@preview/cetz:0.4.1"
//#cetz.canvas({
 // import cetz.draw: *
  //  line((-1, 0), (1, 0))
  //  arc((-1/2,0), start: 225deg, stop: 135deg)
//})

 #משפט("צפיפות המספרים הרציונליים")[
    לכל $x in RR$ ולכל $epsilon > 0$ קיים $q in QQ$ שמקיים $|x-q|<epsilon$.
]

#משפט[$sqrt(2) in.not QQ$]
#הוכחה[
נניח בשלילה שקיים מספר רציונלי מצומצם $r=m/n$ המקיים $r^2=2$. מכאן נקבל:
$ (m/n)^2 = m^2/n^2 => m^2 = 2 dot n^2 $
כלומר $m^2$ מספר זוגי, ולכן $m$ זוגי, כלומר קייחם $a in NN$ המקיים $m=2 dot a$. מכאן:
$ 2n^2= m^2 = (2a)^2 = 4a^2 => n^2 = 2a^2 => n = 2 dot b $
כלומר $m$ וגם $n$ זוגיים ולכן השבר
$r = m/n = (2 dot a)/(2 dot b)$
אינו שבר מצומצם. הגענו לסתירה לנתון כנדרש.
]
קיבלנו גם ש-$QQ subset.eq.not RR$.
#למה[אם $m^2$ זוגי, אז גם $m$ זוגי.]

== חסימות
#הגדרה("חסימות")[
    תהי $A subset.eq RR$. נאמר ש-$A$:
    + *חסומה מלמעלה / מלעיל* אם קיים $M in RR$ שמקיים $forall x in A, x <= M$. $M$ נקרא *חסם מלמעלה / מלעיל*.
    + *חסומה מלמטה / מלרע* Aאם קיים $m in RR$ שמקיים $forall x in A, m <= x$. $m$ נקרא *חסם מלמטה / מלרע*.
    + *חסומה* אם היא חסומה למעלה וגם מלמטה
     $ <=>$ $A subset.eq [m,M] <=> |A| <= d$.
]

#דוגמאות[
+ $(a, b]$
    חסומה על ידי $b$ מלמעלה ועל ידי $a$ מלמטה, אך גם על ידי $b + 1$ מלמעלה ועל ידי $a - 1$ מלמטה.
+ $NN$ חסומה מלמטה על ידי $0$ אך לא חסומה.
]
    #let an = $a_n$; #let bn = $b_n$; #let eps = $epsilon$; #let n0 = $n_0$
== סדרות
#הגדרה("סדרה")[
    אוסף אינסופי ממוספר (סדור) של מספרים: $a_1, a_2, a_3, ..., a_n, ...$. מסמנים סדרה ב-${a_n}_(n=1)^infinity$, $(a_n)_(n=1)^infinity$, או $(a_1, a_2, a_3, ...)$.
]
 #דוגמאות[
 + $an=7$: $7,7,7,...$
 + $ an=sin(n^2+1)/(n^2+1) $
 + $p_n$ = המספר הראשוני ה-$n$-י: $(2,3,5,7,11,...)$
 + $d_n = sqrt(2)$ = הספרה ה-$n$-ית אחרי הנקודה של $sqrt(2)$: 
 $sqrt(2) = 1.d_1 d_2 d_3... => an = 1.d_1d_2...d_n$
 + נוסחאות נסיגה / רקורסיה:
    + $a_1 = 1, n>=1, a_(n+1) = (n+1) dot an$.
     זאת נוסחת העצרת: $an=n!$.
    + $ b_1 = sqrt(2), n>=1, b_(n+1) = sqrt(2+bn) => b_1=sqrt(2), b_2=sqrt(2+sqrt(2)), b_3=sqrt(2+sqrt(2+sqrt(2))), ... $
 ]
=== פעולות על סדרות
- חיבור/חיסור: $c_n = an plus.minus bn$
- ערך מוחלט: $x_n = |an|$
- כפל: $c_n = an dot bn$
- חילוק: $c_n = an/bn$

== גבול של סדרה
$sqrt(2)$  הוא הגבול של סדרת הקירובים $1.4, 1.41, 1.414, dots$. מה זה אומר?
#הגדרה("גבול של סדרה")[
    נאמר ש-$L in RR$ הוא *גבול של סדרה* ${a_n}_(n=1)^infinity$ אם מתקיים:
    $ forall eps > 0, exists n_0, forall n>= n_0, |a_n-L|<eps $
    במקרה זה מסמנים:
    $ lim_(n->infinity)an = lim an = L <=> an stretch(->)^(n->infinity) L $
]
המשמעות היא שלכל $eps > 0$, כל איברי הסדרה למעט מספר סופי ("כמעט כל איברי הסדרה") נמצאים בסביבת-$eps$ של $L$.

#דוגמאות[
+ $an = 1.d_1d_2...d_n -> #heb[שבר עשרוני של שורש 2 עד המקום ה-n-י]$.
#הוכחה[
יהי $eps > 0$. קיים $n0$ כך ש-$eps > 10^(-n0) <=> 10^n0> 1/eps$. מתקיים לכל $n>=n0$:
$ |an - sqrt(2)| = |1.d_1d_2...d_n - 1.d_1d_2d_3...| = 0.underbrace(0...0, "n times")d_(n+1)d_(n+2)... < 10^(-n) < eps $]
2. $a_n = 1 + (-1)^n/n$: \
    #range(1, 7).map(it => calc.round(1 + calc.pow(-1, it) / it, digits: 2)).enumerate().map(it => $a_(it.first()) = it.last()$).join(", ") $display(lim_(n->infinity)) = 1, $.
    #הוכחה[
        יהי $eps > 0$. נבחר $n0 > 1/eps$ ואז לכל $n >= n0$:
        $ |an - 1| = |1 + (-1)^n/n - 1|  = 1/n <= 1/n0 < eps $
        לכן $display(lim_(n->infinity)) = 1$.
    ]
]

#הגדרה("סדרה מתכנסת")[
    נאמר שסדרה ${a_n}_(n=1)^infinity$ *מתכנסת* אם קיים הגבול $display(lim_(n->infinity))an$. אחרת, אומרים שהסדרה *מתבדרת*.
]

#דוגמאות[
    + $n!, (-1)^n n!$ מתבדרות.
    2. $(-1)^n$
     מתבדרת: למשל עבור $eps = 1/2$ נקבל לכל $n$ שכבר $a_(n+1)$ לא מקיים את הגדרת הגבול.
]

#הגדרה("חסימות של סדרה")[
    סדרה נקראת *חסומה* אם הקבוצה של איברי הסדרה היא חסומה.
]
#דוגמאות[
    1. $a_n = 7$: ${7}$
    2. $a_n = (-1)^n$: ${1, -1}$
]

#הגדרה("מונוטוניות של סדרה")[
    סדרה נקראת:
    + *מונוטונית עולה* אם לכל $n$ מתקיים $a_(n+1) >= an$, או *עולה ממש* אם  $a_(n+1) > an$.
    + *מונוטונית יורדת* אם לכל $n$ מתקיים $an >= a_(n+1)$, או *יורדת ממש* אם  $an > a_(n+1)$.
    + *מונוטונית* אם היא מונוטונית עולה או מונוטונית יורדת.
]

#דוגמה[
    $b_1=sqrt(2), n>=1, b_(n+1)=sqrt(2+b_n)$
    נוכיח באינדוקציה שהסדרה עולה ממש.
    - #קותח("בסיס"):
        $checkmark space b_2 = sqrt(2+sqrt(2)) > sqrt(2) = b_1$
    - #קותח("צעד"): נניח כי $b_(n+1) >= b_n$ עבור $n$ כלשהו.
    - #קותח("הוכחה"): נוכיח כי $b_(n+2)>=b_(n+1)$: \
        $ b_(n+2) = sqrt(2 + b_(n+1)) >= sqrt(2+b_n) = b_(n+1) space qed$

האם הסדרה חסומה?
$ b_1 = sqrt(2) = #calc.round(calc.sqrt(2), digits: 3),  b_2 = sqrt(2+sqrt(2)) = #calc.round(calc.sqrt(2+calc.sqrt(2)), digits: 3),  b_3 = sqrt(2+sqrt(2+sqrt(2))) = #calc.round(calc.sqrt(2+calc.sqrt(2 + calc.sqrt(2))), digits: 3), b_4 = #calc.round(calc.sqrt(2+calc.sqrt(2+calc.sqrt(2 + calc.sqrt(2)))), digits: 3), b_5 = #calc.round(calc.sqrt(2+calc.sqrt(2+calc.sqrt(2 + calc.sqrt(2 + calc.sqrt(2))))), digits: 3), ... $
נוכיח באינדוקציה כי $bn<=2$.
    - #קותח("בסיס"): $ checkmark space b_1 = sqrt(2) < 2$
    - #קותח("צעד"): נניח כי $bn<=2$ עבור $n$ כלשהו.
    - #קותח("הוכחה"): נוכיח כי $b_(n+1)<=2$:   \
        $b_(n+1) = sqrt(2 + bn) <= sqrt(2+bn)<=sqrt(2+2) = 2 space qed$

נניח שאנחנו יודעים כי $display(lim_(n->infinity)bn = L)$. נמצא את $L$:
$ b_(n+1) = sqrt(2+bn) => limn(b_(n+1)) = limn(sqrt(2+bn)) stretch(=)_(lim bn=lim b_(n+1)) limn(bn) = \ 
L = sqrt(limn(2+bn)) = sqrt(2+limn(bn)) = sqrt(2+L) \
L = sqrt(2+L) => L^2 = 2 + L  => L^2 - L - 2 = (L-2)(L+1) = 0 => \
    cancel(L = -1) => L = 2
  $
  כפי שציפינו.
]

#let L1=$L_1$;#let L2=$L_2$
#משפט("יחידות הגבול")[אם $an->L1, an->L2$, אז $L_1=L2$.]
#הוכחה[
    יהי $eps>0$. קיימים $,N_2N_1$ עבורם ניקח $n_0 = max{N_1,N_2}$ שמקיים
     $ forall n>=N_1, |an-L1|<eps,forall n>=N_2, |an-L2|<eps $
     ואז לכל $n>=n_0$:
     $ |L1-L2| = |L1 - an + an - L2] <=_#heb[אי-שוויון המשולש] |L1-an| + |an-L2| < 2 eps $
     הוכחנו שלכל $eps > 0$ מתקיים $|L1-L2|<eps$. כלומר ההפרש קטן ממספר חיובי קטן כרצוננו, ולכן $L1=L2$.
]

#משפט[
    אם סדרה ${a_n}_(n=1)^infinity$ מתכנסת, אזי היא חסומה.
]
#הוכחה[
    עבור $eps=1$ קיים $n0$ כך שלכל $n >= n0$ מתקיים $L-1<=an<=L+1$.\
    נגדיר $M = max{a_1,...,a_(n-1)}$ ו-$m=min{a_1,...,a_(n-1)}$ ואז לכל $n in NN$ מתקיים:
$ min{L-1,m}<=a_n<=max{L+1,M} $
]
יש לשים לב שההפך אינו נכון: חסומה $arrow.l.double.not$ מתכנסת. לדוגמה $(-1)^n$.
באופן כללי,
$A => B cancel(=>) B => A $.
אך כן מתקיים $A => B => not B => not A $ כאשר $not$ מסמל שלילה. \
במקרה שלנו למשל, אם סדרה חסומה, זה לא אומר בהכרח שהיא מתכנסת. אולם, מתקיים שאם הסדרה _לא_ חסומה, היא בוודאי לא מתכנסת! אם הייתה מתכנסת, הייתה חייבת להיות חסומה לפי המשפט שהוכחנו.





#הרצאה("2", "27/08/25", "https://panoptotech.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=d4caa20f-c21d-4791-8bb9-b34600ca2e29")
תזכורת: הסדרה ${an}_(n=1)^infinity$ מתכנסת אם לכל $epsilon > 0$ קיים $n_0$ כך שלכל $n>=n_0$ מתקיים $|an-L|<epsilon$. במקרה זה נאמר ש-L הוא *הגבול* של ${an}$ ונסמן $display(lim_(n->infinity)an = L)$ או $an stretch(->)_(n->infinity)L$.
== יחס סדר בין גבולות
#משפט("סדר בין גבולות")[
    תהיינה $an,bn$ סדרות כך ש-
    $display(lim_(n->infinity)an = L), display(lim_(n->infinity)bn = M, )$. אזי:
    + אם $an >= b_n$ כמעט לכל $n$ אזי $L >= M$.
    + אם $L > M$ אזי $an > bn$ החל ממקום מסוים $<=>$ 
        $exists n_0, forall n >= n_0, an > bn$.
] <סדר-בין-גבולות>
#let na = $n_a$; #let nb = $n_b$
#הוכחה[
    + יהי $eps > 0$. קיים $na$ כך שלכל $n>=na$ מתקיים 
        $L - eps < an < L + eps$.
        באופן דומה, קיים $nb$ כך שלכל $n>=nb$ מתקיים
        $M - eps < bn < M + eps $. \
        ניקח $n0=max{na,nb}$ ואז לכל $n>=n0$ מתקיים $M-eps<bn<=an<L+eps$ ומכאן \ $M-L<2eps$. זה נכון לכל $eps>0$ ולכן $M-L<=0$ $M<=L<=>$.
        
    + עבור $eps=(L-M)/2$ קיים $n0$ כך שלכל $n>=n0$ מתקיים 
     $an in (L - eps, L + eps), bn in (M - eps, M + eps)$.
     לפי הגדרת הגבול, לכל $n>=n0$ מתקיים:
     $ bn < M + eps = M + (L - M)/2 = (2M + L - M)/2 = (M + L)/2 = (M + L + L - L)/2  = L - eps < an $
]
הערות:
+ אם $an>bn$ לכל $n$, לא ניתן להסיק כי $L>M$. למשל $an=1/n,bn=1/n$ אך $limn(an)=limn(bn)=0$.
+ אם $L>=M$ לא ניתן להסיק ש-$an<=bn$ החל ממקום מסוים. למשל $an=bn=0$.
מסקנות:
+ אם $an>=0$, אז $limn(an)>=0$. ניקח $bn=0$ אז $limn(bn)=0$ ואז נשתמש בסעיף 1 של @סדר-בין-גבולות.
+ אם $a<=an<=b$ כמעט לכל $n$, אז $limn(an) in [a,b]$.
+ אם $limn(an)>0$ אז $an>0$ כמעט לכל $n.$

#למה("אי שוויון המשולש")[
    $|a-b|<=|a|+|b|, ||a|-|b||<=|a-b|, |b|-|a|<=|a-b|$
]
#משפט[
    תהי ${an}_(n=1)^infinity$ סדרה ו-${|an|}_(n=1)^infinity$ סדרת הערכים המוחלטים. אם
     $an stretch(->)_(n->infinity)L$ אז $|an|stretch(->)_(n->infinity)|L|$
      ובפרט 
        $|an| stretch(->)_(n->infinity) 0<=> an stretch(->)_(n->infinity) 0$.
]
#הוכחה[
    יהי $eps>0$. ניקח $n_0$ כך שלכל $n>n_0$ מתקיים $|an-L|<eps$. ואז לפי אי-שוויון המשולש, 
    $ ||an|-|L|| <=_(forall n>=n_0) |an-L| < eps $
 ]
 #למה[
    $|an-L| stretch(->)_(n->infinity) L<=> an stretch(->)_(n->infinity) L$.
 ]
 #הוכחה[
    $||an-L| - 0| = |an-L| < eps$ ואז לפי הגדרת הגבול.
 ]
 #let cn = $c_n$
 #משפט("סנדוויץ'")[
    תהיינה $an,bn,cn$ סדרות כאשר $an<=bn<=cn$ לכל $n$. \ 
    אם $limn(an) = limn(cn) = L$ אז $limn(bn) = L$.
 ]
 #הוכחה[
        יהי $eps>0$. נמצא $n_0$ כזה שמתאים ל-$eps$ עבור שתי הסדרות, $an$ ו-$cn$. נשתמש בנוסף בנתון ונקבל:
        $ forall n >= n_0, L-eps < an <= bn <= cn < L + eps => forall n >= n_0, bn in (L-eps,L+eps) => display(lim_(n->infinity)bn) = L $
]
     
מסקנה ממשפט הסנדוויץ: אם
$0<=an<=bn --> 0$
אז $limn(an)=0$.
     
 #משפט("חשבון גבולות")[
    תהיינה $an,bn$ סדרות כך ש-
    $display(lim_(n->infinity)an = L), display(lim_(n->infinity)bn = M, )$. אזי:
    + $an+bn-->L+M$
    + $an dot bn --> L dot M$ 
    + $an/bn --> L/M$, אם $M eq.not 0$
    + $an^bn --> L^m$, אם $L eq.not 0$
 ]
#הוכחה[
+ יהי $eps>0$ ו-$n0$ כזה שלכל $n>=n0$ מתקיים $|an-L|,|bn-M|<eps/2$. כעת מתקיים לכל $n>=n0$:
    $ |an+bn-(L+M)| <= |an-L|+|bn-M|<eps/2+eps/2=eps space $
+ ידוע ש-$an$ חסומה (כי היא מתכנסת). יהי $c$ כך ש- $|an|<=c$ לכל $n$. נבחר $na$ כך ש-$|an-L|<=eps/(2|M|)$ לכל $n>na$ ו-
        $nb$ כך ש-$|bn-M|<=eps/(2c)$ לכל $n>=nb$.
        יהי $n0=max{na,nb}$ ואז לכל $n>=n0$ מתקיים:
        $ |an dot bn - M dot L|= |an bn - an M + an M - L M| <=_#heb[אי-שוויון המשולש] 
        |an bn - an M| + |an M - L M| = \ =  |an||bn - M| + |an - L||M| <= c|bn - M| + |an -L||M| <= c dot eps/(2c) + eps/(2|M|) dot |M| = eps/2 + eps/2 = eps $
+ ראינו בתרגול ש-
    $limn(1/bn)=M^(-1)$
    ואז
     $ an/bn = an dot 1/bn = L dot 1/M = L/M $
]

 #משפט("חסומה כפול אפסה")[
    אם $an$ סדרה חסומה ו-$limn(bn)=0$ אז $limn(an dot bn)=0$.
 ]
 #הוכחה[
    אם $|an|<=c$ לכל $n$ אז:
    $ 0<= |an bn| <= c|bn| --> 0 => |an bn| --> 0 $
 ]
 #דוגמאות("חסומה כפול אפסה")[
+ את הסדרה $sin(n) slash n$ נפרק למכפלת שתי סדרות, $an = sin(n)$ ו-$bn = 1 slash n$. $|an|<=1$ לכן הסדרה שואפת לאפס.
+ ניתן להוכיח את $an dot bn --> M L$ בקלות עם משפט זה:
$  |an bn - L M| <= limits(|an|)^(<=c) limits(|bn-M|)^(->0) + limits(|an-L|)^(->0)limits(|M|)^(#heb[קבוע חסום]) --> 0 $
 ]
 
 == סדרת ממוצעים
 תהי ${an}_(n=1)^infinity$ סדרה. נייצר את *סדרות הממוצעים*:
 + חשבוני: $m_n = (a_1 + a_2 + dots.h.c + an) slash n = 1/n sum_(k=1)^n a_k$
 
 + הנדסי:
    $g_n = root(n, a_1 dot a_2 space dots.h.c space an) = root(n, product_(k=1)^n a_k)$
    
 + הרמוני:
    $h_n = (1/n (1/a_1 + 1/a_2 + dots.h.c + 1/an))^(-1) = n slash (1/a_1 + 1/a_2 + dots.h.c + 1/an) $
#משפט("אי-שוויון הממוצעים")[
    $m_n >= g_n >= h_n$
    ]
    
#למה("גבולות של סדרות ממוצעים")[
אם $0 < an --> L$ אז $m_n, g_n, h_n --> L$.
]
#הוכחה[
- ממוצע חשבוני:
#הוכחה[
יהי $eps > 0$.
$ abs((a_1 + a_2 + dots.h.c + an)/n - L) 
= abs((a_1 + a_2 + dots.h.c + an -n L)/n) =
abs(((a_1 - L) + (a_2 - L) + dots.h.c + (an -L))/n) = \
abs(((a_1 - L) + dots.h.c (an_0 - L))/n) + abs(((a_(n_0+1) - L) + dots.h.c + (an - L))/n) = A $ 

הסדרה $an$ חסומה. נסמן $|an|<=c$ לכל $n$. מכאן $|L|<=c$ (אחרת היינו יכולים לקחת $eps = (|L|-c)/3$ ולהראות שקיימים $an>c$) ולכן $|an-L|<=2c$ ומכאן:
$ A <= n0 (2c)/n + (n - n0) eps/n $
בהנחה שבחרנו $n0$ כך ש-$forall k>=n0, |a_k-L|<eps$. נבחר $n_1>=n0$ שיקיים $n0 (2c)/n < eps$. מתקיים גם כי:
    $ (n-n0)/n < 1 => (n-n0) e/n < eps $
  ואז לכל $n >= n_1$ 
    $A < eps + eps = 2 eps $
ולכן
$limn(m_n) = L$.
]
 
\
 - ממוצע הרמוני:
 #הוכחה[
    מאריתמטיקה של גבולות מספיק להוכיח $1/h_n --> 1/L$. נסמן סדרה חדשה $b_n=1/a_n --> 1/L$.
    $ 1/h_n = 1/n (1/a_1 + 1/a_2 + dots.c.h + 1/an) = underbrace(b_1 + b_2 + dots.c.h + b_n, #heb[סדרת הממוצעים החשבוניים]) stretch(->)^#heb[המשפט הקודם] 1/L $
    ולכן $h_n --> L$.
     ]
 - ממוצע הנדסי:
 #הוכחה[
    לפי סנדוויץ' ואי-שוויון הממוצעים.
 ]
]


#דוגמה[
תהי סדרה $an = root(n,n)$. נרצה להוכיח שגבולה $1$.
 
 #קותח[דרך א']: נגדיר $b_n = n^(1 slash n) - 1$ ומכאן:
 $ n = (1+b_n)^n =_#heb[בינום] sum_(k=0)^n binom(n, k)(b_n)^k >= n(n-1)/2 (b_n)^2 $
 כאשר התבססנו על כך הסכום הוא סכום של איברים חיוביים אי-שליליים, ולכן הסכום גדול מכל אחד מהאיברים, בפרט מהאיבר השני. נזכיר את נוסחת הבינום,
 $ binom(n, k) = n!/((n-k)!k!)$. נעביר אגפים ונקבל:
 $ b_n <= sqrt((2 cancel(n))/cancel(n)(n-1)) --> 0 => an --> 1 space qed
 $
 #קותח[דרך ב']: ראשית ננסח טענה שימושית:
 #למה[
    תהי $an$ סדרת חיוביים. אם $an/a_(n-1) --> L$ אז $root(n,an) --> L$.
 ]
 #הוכחה[
    נגדיר $q_1=a_1, q_n=an/(a_(n-1)), n>=2$. ואז נקבל:
    $ an = a_1 dot a_2/a_1 dot a_3/a_2 space dots.h.c space an/a_(n-1) = q_1 space dots.h.c space q_n \
 root(n, an) = root(n, q_1 space dots.h.c space q_n) stretch(->)^#text(font: "David", [כי זו סדרת])_#text(font: "David", [הממוצעים ההנדסיים]) L
 $
 ]
 בדוגמה שלנו נגדיר $bn=n$ ואז:
 $ bn/b_(n-1) = n/(n-1) --> 1 => root(n,n)=root(n,bn) --> 1 $
]
\ \ \ #משפט[
    אם $0<c in RR$ אז $root(n,c) --> 1$.
 ]
 #הוכחה[נחלק למקרים:
    1. $underline(c>=1)$:     
        החל מ-$n0 = ceil(c)$ מתקיים $1 <= root(n,c) <= root(n,n)$. נפעיל את משפט הסנדוויץ' וסיימנו.
    2. $underline(c<1)$:
    $ c^(1 slash n) = (1/c)^(-1 slash n) = 1/ (1/c)^(1 slash n) --> 1/1 = 1 $
    אפשר גם:
    $limn(c^(1/n)) = c^((limn(1/n))) = c^0 = 1$
 ]
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 