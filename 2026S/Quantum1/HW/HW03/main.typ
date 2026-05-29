#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *

#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "3",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 5, day: 27),
)

#שאלה(כותרת: "תכונות פונקציית דלתא", [
  בשאלה זו נתעסק בתכונות פונקציית דלתא של דיראק.
])

#סעיף[
  חשבו:
  $ integral_(-oo)^oo delta(x^2 - 4) f(x) dd(x) $
]
נסמן
$g(x)=x^2-4$.
ששורשיה הם
$x = pm 2$.
נשתמש בזהות:
$
  delta(g(x)) = sum_i delta(x-x_i) / abs(g'(x_i)) = delta(x-2)/abs(evaluated(2x)_(x=2)) + delta(x+2)/abs(evaluated(2x)_(x=-2)) = (delta(x-2) + delta(x+2))/4
$
נציב חזרה באינטגרל ונקבל:
$
  integral_(-oo)^oo delta(x^2 - 4) f(x) dd(x) &= 1/4 integral_(-oo)^oo (delta(x-2) + delta(x+2)) f(x) dd(x) \
  &= 1/4 (integral_(-oo)^oo delta(x-2) f(x) dd(x) + integral_(-oo)^oo delta(x+2) f(x) dd(x)) \
  &= 1/4(f(2) + f(-2))
$
#תשובה[
  $ integral_(-oo)^oo delta(x^2 - 4) f(x) dd(x) = (f(2) + f(-2))/4 $
]
#pagebreak()
#סעיף[
  בהרצאה הראינו כי:
  $ integral pdv(, x) delta(x-y) f(y) dd(y) = f'(x) $
  הראו כי (עבור פונקציה שמתאפסת בקצה תחום האינטגרציה) מתקיים:
  $ integral pdv(, y) delta(x-y) f(y) dd(y) = -f'(x) $
]
נשתמש באינטגרציה בחלקים. נסמן:
#[ #set math.cases(gap: 0.6em)
  $
    cases(
      u = f(y) \, space dd(u) = f'(y),
      dd(v) = pdv(, y) delta(x-y)\, space v = delta(x-y),
    )
  $ ]
נחשב את האינטגרל:
$
  integral_a^b pdv(, y) delta(x-y) f(y) dd(y) &= evaluated(f(y)delta(x-y))_a^b - integral delta(x-y) f'(y) dd(y) \
  &= underbrace(cancel(f(b) delta(x-b) - f(a) delta(x-a)), f(a)=f(b)=0) - integral_a^b underbrace(delta(x-y), =delta(y-x)) f'(y) dd(y) \
  &= - integral_a^b delta(y-x) f'(y) dd(y) \
  &= -f'(x)
$

#תשובה[
  $ integral_a^b pdv(, y) delta(x-y) f(y) dd(y) = -f'(x) $
]

#שאלה(כותרת: "כתיב דיראק", [
  תרגמו את הביטויים הבאים לכתיב דיראק עבור פונקציות מצב $f, g$.

  יש לזכור כי
  $braket(x, psi) = psi(x)$.
])

#סעיף[
  $ f(x) = g(x) $
]
לפי התזכורת, $f(x) = braket(x, f)$ ו- $g(x) = braket(x, g)$. לכן:
$ f(x) = g(x) => braket(x, f) = braket(x, g) $
משום שזה נכון לכל $x$, נקבל:
#תשובה[
  $ ket(f) = ket(g) $
]

#סעיף(מזהה: <2.2>, [
  $ c = integral g^*(x') h(x') dd(x') $
])
נשתמש באופרטור הזהות:
$
  integral g^*(x') h(x') dd(x') = integral (braket(x', g))^* braket(x', h) dd(x') = integral braket(g, x') braket(x', h) dd(x')
$
$bra(g)$ ו-$bra(h)$ לא תלויים ב-$x'$, ולכן ניתן להוציא אותם מהאינטגרל:
$braket(x', h) dd(x')$
$
  integral braket(g, x') braket(x', h) dd(x') = bra(g) (integral ketbra(x') dd(x')) ket(h) = mel(g, II, h) = braket(g, h)
$
#תשובה[
  $ c = integral g^*(x') h(x') dd(x') = braket(g, h) $
]

#סעיף[
  $ f(x) = sum_n phi_n (x) integral phi_n^*(x') f(x') dd(x') $
]
נטפל ראשית באינטגרל כמו בסעיף הקודם:
$
  integral phi_n^*(x') f(x') dd(x') = integral braket(phi_n, x') braket(x', f) dd(x') = mel(phi_n, II, f) = braket(phi_n, f)
$
נציב חזרה לסכום:
$ f(x) = braket(x, f) = sum_n braket(x, phi_n) braket(phi_n, f) $
זה נכון לכל $bra(x)$, לכן:
$ ket(f) = sum_n ket(phi_n) braket(phi_n, f) $
#תשובה[
  $ ket(f) = sum_n ket(phi_n) braket(phi_n, f), quad braket(x, f) = sum_n braket(x, phi_n) braket(phi_n, f) $
]

#סעיף[
  $ pdv(, x) f(x) = h(x) integral h^*(x') g(x') dd(x') $
]
נשתמש בפיתוח האינטגרל מ@2.2:
$ h(x) integral h^*(x') g(x') dd(x') = braket(x, h) braket(h, g) $
נשתמש באופרטור הנגזרת שראינו בתרגול:
$ pdv(, x) f(x) = mel(x, upright(D), f) $
משום שהשוויון נכון לכל $bra(x)$, נקבל:
$ "D"ket(f) = ket(h) braket(h, g) $
#תשובה[
  $ "D"ket(f) = ket(h) braket(h, g), quad mel(x, "D", f) = braket(x, h) braket(h, g) $

]


#שאלה(כותרת: "אופרטורים הרמיטיים וזוגיות", [
  נסתכל על האופרטור:
  $ Omega = K (L^2 - X^2) K $
  הפועל על פונקציות סופיות בקטע $[-L, L]$.
])

#סעיף[
  הראו כי במרחב זה האופרטור $K$ אינו הרמיטי.
]
נראה כי $K$ אינו הרמיטי על ידי כך שנראה שבאופן כללי לא מתקיים:
$mel(g, K, f) = mel(f, K^+, g)$. נחשב לפי הגדרה, כאשר נזכור כי $K=-i"D"$:
$ mel(g, K, f) = integral_(-L)^L g^*(x) (-i) pdv(, x) f(x) dd(x) = -i integral_(-L)^L g^*(x) pdv(f, x) (x) dd(x) $
נשתמש באינטגרציה בחלקים:
#[ #set math.cases(gap: 0.6em)
  $
    cases(
      u = g^*(x) \, space dd(u) = pdv(, x) g^*(x),
      dd(v) = pdv(, x) f(x) \, space v = f(x),
    ) => \ mel(g, K, f) = -i evaluated(g^*(x) f(x))_(-L)^L + i integral_(-L)^L f(x) (pdv(g, x))^*(x) dd(x)
  $ ]
כעת נחשב את $mel(g, K^+, f)$:
$
  mel(g, K^+, f) &= mel(f, K, g)^* = (integral_(-L)^L f^*(x) (-i) pdv(, x) g(x) dd(x))^* = i integral_(-L)^L f(x) pdv(, x) g^*(x) dd(x) \
  &= i evaluated(g^*(x) f(x))_(-L)^L + mel(g, K, f)
$
השוויון לא יתקיים לכל צמד פונקציות $f(x), g(x)$, אלא רק אם $evaluated(g^*(x) f(x))_(-L)^L = 0$.
#תשובה[
  קיבלנו כי באופן כללי לא מתקיים:
  $ mel(g, K, f) = mel(g, K^+, f) $
  ולכן $K$ אינו הרמיטי.
]

#סעיף(מזהה: <4.2>, [
  הראו כי $Omega$ הוא אופרטור הרמיטי.
])
נפתור בצורה דומה:
$
  mel(g, Omega, f) = integral_(-L)^L g^*(x) K (L^2-X^2) K f(x) dd(x) = integral_(-L)^L g^*(x) (-i) pdv(, x) ((L^2-X^2) K f(x)) dd(x)
$
נחשב את $X^2 h(x)$:
$ X^2 h(x) = X (x h(x)) = x^2 h(x) $
ולכן:
$ mel(g, Omega, f) = -i integral_(-L)^L g^*(x) pdv(, x) ((L^2-x^2) K f(x)) dd(x) $

נשתמש באינטגרציה בחלקים:
#[ #set math.cases(gap: 0.6em)
  $
    cases(
      u = g^*(x) \, space dd(u) = pdv(, x) g^*(x),
      dd(v) = pdv(, x) ((L^2-x^2) K f(x)) \, space v = (L^2-x^2) K f(x),
    ) => \ mel(g, Omega, f) = -i evaluated(g^*(x) (L^2-x^2) K f(x))_(-L)^L + i integral_(-L)^L (pdv(g, x))^*(x) (L^2-x^2) K f(x) dd(x)
  $ ]
משום ש-$L^2-x^2$ מתאפס בקצוות $x = pm L$, נקבל:
$
  mel(g, Omega, f) = i integral_(-L)^L (pdv(g, x))^*(x) (L^2-x^2) K f(x) dd(x) = integral_(-L)^L (pdv(g, x))^*(x) (L^2-x^2) pdv(f, x)(x) dd(x)
$
נחשב את $mel(g, Omega^+, f)$:
$
  mel(g, Omega^+, f) & = mel(f, Omega, g)^* = (integral_(-L)^L f^*(x) (-i) pdv(, x) ((L^2-x^2) K g(x)) dd(x))^* \
                     & = i integral_(-L)^L f(x) pdv(, x) [(L^2-x^2) (K g(x))^*] dd(x)
$

נשתמש באינטגרציה בחלקים:
#[ #set math.cases(gap: 0.6em)
  $
    &cases(
      u = f(x) \, space dd(u) = pdv(, x) f(x),
      dd(v) = pdv(, x) [(L^2-x^2) (K g(x))^*] \, space v = (L^2-x^2) (K g(x))^*,
    ) => \ mel(g, Omega^+, f) &= i evaluated(f(x) (L^2-x^2) (K g(x))^*)_(-L)^L - i integral_(-L)^L pdv(, x) f(x) (L^2-x^2) (K g(x))^* dd(x) \
    &= integral_(-L)^L -i pdv(, x) f(x) (L^2-x^2) (K g(x))^* dd(x) \
    &= integral_(-L)^L (-i pdv(, x) f(x)) (L^2-x^2)i pdv(, x) g^*(x) dd(x) = integral_(-L)^L pdv(, x) f(x) (L^2-x^2) pdv(, x) g^*(x) dd(x)
  $ ]

#תשובה[
  קיבלנו כי
  $mel(g, Omega, f) = mel(g, Omega^+, f)$
  ולכן $Omega$ הוא אופרטור הרמיטי.
]

#סעיף(מזהה: <4.3>, [
  נסמן את הווקטורים העצמיים של $Omega$ ב-$ket(n)$. נתון כי הווקטורים העצמיים אינם מנוונים. השתמשו בשאלה על אופרטור הזוגיות מתרגול 3, כדי להראות ש- $p_n (x)$, המוגדר על ידי:
  $ p_n (x) = braket(x, n) $
  מקיים:
  $ p_n (x) = p_n (-x) quad "or" quad p_n (x) = -p_n (-x) $
])
ב@4.2 מצאנו ש-$Omega$ הרמיטי, לכן הווקטורים העצמיים שלו יוצרים בסיס למרחב כולו. בתרגול ראינו כי גם $Pi$ הרמיטי. לכן שניהם לכסינים אורתוגונלית. נראה כי הם מתחלפים. תהי $f(x)$ פונקציה במרחב:
$
  Omega Pi f(x) & = Omega f(-x) = -i pdv(, x) [(L^2 - (-x)^2) (-i) pdv(, x) f(-x)] \
                & = -pdv(, x)[(L^2 - x^2) (-f'(-x))] = pdv(, x)[(L^2-x^2)f'(-x)]
$
ומצד שני:
$
  Pi Omega f(x) & = Pi[K(L^2-X^2) K f(x)] = Pi[-i pdv(, x)((L^2-X^2) (-i) pdv(, x) f(x))] \
                & = -Pi[pdv(, x)((L^2-x^2)f'(x))] = -pdv(, (-x))((L^2-(-x)^2)f'(-x)) \
                & = pdv(, x)((L^2-x^2)f'(-x))
$
כלומר:
$ Omega Pi f(x) = Pi Omega f(x) => [Omega, Pi] = 0 $
כעת, ראינו בהרצאה כי אם ורק אם אופרטורים לכסינים אורתוגונלית מתחלפים, יש להם סט משותף של וקטורים עצמיים. לכן, כל וקטור עצמי $ket(n)$ של $Omega$ הוא גם וקטור עצמי של $Pi$. נסמן את הערכים העצמיים של $Pi$ ב-$pi_n$:
$ Pi ket(n) = pi_n ket(n) $
לכן:
$ braket(-x, n) = mel(x, Pi, n) = braket(x, pi_n n) = pi_n braket(x, n) $
נציב את ההגדרה של $p_n (x) = braket(x, n)$:
$ p_n (-x) = pi_n p_n (x) $
ראינו בתרגול כי $pi_n = pm 1$:
#תשובה[
  $ p_n (x) = pm p_n (-x) quad => quad p_n (x) = p_n (-x) "or" p_n (x) = -p_n (-x) $
]

#סעיף(מזהה: <4.4>, [
  נתון כי הערכים העצמיים של $Omega$ הם $n(n+1)$, עבור $n = 0, 1, 2, ...$, כלומר:
  $ Omega ket(n) = n(n+1) ket(n) $
  נתון גם כי $p_n (x) = braket(x, n)$ הם פולינומים מסדר $n$. מצאו את $ket(0), ket(1), ket(2), ket(3)$ עד כדי קבוע נרמול בהצגת המקום.
])
נחשב תחילה את $p_0(x) = braket(x, 0)$. נתון לנו שהוא פולינום מסדר $n=0$, לכן, עד כדי קבוע נרמול מתאים,
$p_0 (x) = 1$.

בשביל לחשב את שאר הווקטורים, נשתמש בשתי תכונות:
1. ב@4.3 מצאנו כי $p_n (x) = pm p_n (-x)$. כעת, נתון כי $p_n (x)$ הם פולינומים מסדר $n$. לכן, כל פולינום ממעלה זוגית חייב להכיל חזקות זוגיות בלבד, וכל פולינום ממעלה אי-זוגית מכיל חזקות אי-זוגיות בלבד.
מכאן כבר נקבל ש-$p_1 (x) = x$,
ביחס לקבוע נרמול מתאים.

2. ב@4.2 הראינו כי $Omega$ אופרטור הרמיטי. ידוע לפי משפט הפירוק הספקטרלי שווקטורים עצמיים של ערכים עצמיים שונים אורתוגונליים זה לזה, ומשום שנתון כי הם אינם מנוונים, כל וקטור עצמי אורתוגונלי לווקטור אחר. במונחי המכפלה הפנימית נקבל:
$ forall n!=m, space integral_(-L)^L p_n (x) p_m (x) dd(x) = 0 $
נחשב את $p_2 (x)$. ידוע לנו שהוא מהצורה
$p_2 (x) = x^2 + a$.
נחשב את המכפלה הפנימית שלו עם
#box[$p_0 (x) = 1$]:
$ integral_(-L)^L (x^2 + a) dd(x) = evaluated(1/3 x^3 + a x)_(-L)^L = 2/3 L^3 + 2 a L = 2 L(L^2/3 + a) = 0 $
$L!=0$,
לכן נקבל
$a = -L^2/3$
ומכאן
$p_2 (x) = x^2 - L^2/3$
עד כדי קבוע נרמול מתאים.

לבסוף, נחשב את $p_3 (x)$. ידוע לנו שהוא מהצורה
$p_3 (x) = x^3 + b x$.
נחשב את המכפלה הפנימית שלו עם $p_1 (x)$:
$
  integral_(-L)^L (x^3 + b x)x dd(x) = integral_(-L)^L (x^4 + b x^2) dd(x) = evaluated(1/5 x^5 + (b x^3)/3)_(-L)^L = 2(L^5/5 + (b L^3)/3) = 0
$
מכאן נקבל כי
$b = -(3 L^2)/5$
ולכן
$p_3 (x) = x^3 - (3 L^2)/5 x$
עד כדי קבוע נרמול מתאים.
#תשובה[
  עד כדי קבועי נרמול מתאימים:
  $ braket(x, 0) = 1, space braket(x, 1) = x, space braket(x, 2) = x^2 - L^2/3, space braket(x, 3) = x^3 - (3 L^2)/5 x $
]

#סעיף[
  הראו כי $braket(n, m) prop delta_(n m)$ עבור כל המצבים ${ket(n)}_(n=0)^3$ מהסעיף הקודם.
]
כפי שראינו בסעיף הקודם, לכל $m!=n$ מתקיים
$braket(n, m)=0$.

לכל $n=m$, מתקיים:
$braket(n, m)=braket(n)=norm(n)^2$.
משום ש-$ket(n)!=0$, גם הנורמה שלהם היא מספר ממשי חיובי שכמובן פרופורציונלי ל-$1$.
#תשובה[
  קיבלנו כי:
  $ forall m, n in {0,1,2,3}, braket(n, m) = cases(0 \, m!=n, ||n||^2\, m=n) prop delta_(n m) $
]

#סעיף[
  מצאו נרמול כך ש- $braket(n, m) = delta_(n m)$ עבור האיברים מהסעיף הקודם.
]
נחשב את הנורמה של כל אחד מהווקטורים העצמיים שמצאנו:
$ ||ket(0)||^2 = integral_(-L)^L 1 dot 1 dd(x) = 2L => ||ket(0)|| = sqrt(2L) $
$
  ||ket(1)||^2 = integral_(-L)^L x dot x dd(x) = integral_(-L)^L x^2 dd(x) = evaluated(1/3 x^3)_(-L)^L = (2L^3)/3 => ||ket(1)|| = sqrt((2L^3)/3)
$
$
  &||ket(2)||^2 = integral_(-L)^L (x^2 - L^2/3) dot (x^2 - L^2/3) dd(x) = integral_(-L)^L (x^4 - (2L^2)/3 x^2 + L^4/9) dd(x) \ &= evaluated(1/5 x^5 - (2L^2)/9 x^3 + L^4/9 x)_(-L)^L = (8L^5)/45 => ||ket(2)|| = sqrt((8L^5)/45)
$
$
  &||ket(3)||^2 = integral_(-L)^L (x^3 - (3L^2)/5 x) dot (x^3 - (3L^2)/5 x) dd(x) = integral_(-L)^L (x^6 - (6L^2)/5 x^4 + (9L^4)/25 x^2) dd(x) \ &= evaluated(1/7 x^7 - (6L^2)/25 x^5 + (9L^4)/75 x^3)_(-L)^L = (8L^7)/175 => ||ket(3)|| = sqrt((8L^7)/175)
$
#תשובה[
  עבור הווקטורים המנורמלים הבאים יתקיים
  לכל $n in {0,1,2,3}$ כי $braket(tilde(n), tilde(m)) = delta_(n m)$:
  $
    ket(tilde(0)) = 1/sqrt(2L) ket(0), space ket(tilde(1)) = sqrt(3/(2L^3)) ket(1), space ket(tilde(2)) = sqrt(45/(8L^5)) ket(2), space ket(tilde(3)) = sqrt(175/(8L^7)) ket(3)
  $
]

#שאלה(כותרת: "אופרטורים אוניטריים", [
  נסתכל על האופרטור
  $"D"_a$
  המוגדר על ידי:
  $ braket(x, "D"_a f) = e^(a/2) f(e^a x) $
])

#סעיף[
  הראו כי
  $"D"_a$
  אופרטור אוניטרי.
  רמז: התבוננו באופרטור
  $"D"_(-a)$.
]

#let da = $"D"_a$
בשביל להראות ש-$da$ אוניטרי, נראה שהצמוד שלו הוא גם ההופכי שלו. נתחיל בלהשתמש בהגדרת הצמוד:
$ braket(g, da f) = braket(da^+ g, f) $ <צמוד>
ראשית, נמצא את
$"D"_a^+$:
$ braket(g, da f) = integral_(-oo)^(oo) g^*(x) e^(a/2) f(e^a x) dd(x) $
נבצע החלפת משתנים $u(x) = e^a x$ ונקבל:
$ dd(u) = e^a dd(x) => dd(x) = e^(-a) dd(u); space x = e^(-a) u; space u(x=oo) = oo, u(x=-oo) = -oo $
נציב חזרה באינטגרל:
#let dma = $"D"_(-a)$
$
  braket(g, da f) = integral_(-oo)^(oo) g^*(e^(-a) u) e^(a/2) f(u) e^(-a) dd(u) = integral_(-oo)^(oo) [g(e^(-a) u) e^(-a/2)]^* f(u) dd(u) = braket(dma g, f)
$
מ@צמוד נקבל כי:
$ da^+ = dma $
כעת נראה שמתקיים גם
$da^(-1) = dma$:
$ mel(x, da dma, f) = da [e^(-a/2) f(e^(-a) x)] = e^(a/2)e^(-a/2) f(e^a e^(-a) x) = f(x) = braket(x, f) $
כלומר קיבלנו:
#תשובה[
  $ da dma = da da^+ = II $
  לכן $da$ אופרטור אוניטרי.
]

#pagebreak()
#סעיף[
  חשבו את
  $"D"_a^+ X "D"_a$.
]
נשתמש בכך שמצאנו כי
$da^+ = dma$:
$
  mel(x, da^+ X da, f) & = mel(x, dma X da, f) = (dma X)e^(a/2) f(e^a x) = dma(x dot e^(a/2) f(e^a x)) \
                       & = e^(-a/2) dot e^(a/2) (e^(-a) x) f(e^a (e^(-a) x)) = e^(-a) x f(x) = e^(-a) mel(x, X, f)
$
משום שזה נכון לכל $ket(f)$:
#תשובה[
  $ da^+ X da = e^(-a) X $
]

#סעיף[
  חשבו את יחסי החילוף $["D"_a, S_b]$, כאשר $S_b$ הוא אופרטור ההזזה (העתקה) שהוגדר בתרגול.
]
נחשב לפי הגדרה.
#let sb = $S_b$
$ mel(x, da sb, f) = (da sb)f(x) = da f(x-b) = e^(a/2) f(e^a x - b) $
מצד שני:
$ mel(x, sb da, f) = (sb da)f(x) = sb (e^(a/2)f(e^a x)) = e^(a/2) f(e^a (x - b)) $
נמצא את ההפרש בין שני הביטויים:
$
  & mel(x, da sb - sb da, f) = e^(a/2)[f(e^a x - b) - f(e^a (x - b))] \
  & = e^(a/2)f(e^a (x - b e^(-a))) - e^(a/2)f(e^a (x - b)) = e^(a/2)S_(b e^(-a)) f(e^a x) - e^(a/2) sb f(e^a x) \
  & = S_(b e^(-a)) da f(x) - sb da f(x) = (S_(b e^(-a)) - S_b) da f(x) = mel(x, (S_(b e^(-a)) - S_b) da, f)
$

#תשובה[
  $ [da, sb] = (S_(b e^(-a)) - S_b) da $
]
