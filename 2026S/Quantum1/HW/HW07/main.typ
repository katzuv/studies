#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *

#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "7",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 6, day: 29),
)

#שאלה(כותרת: "פונקציית דלתא שלילית", מזהה: <1>, [
  נתבונן במערכת המתוארת על ידי ההמילטוניאן הבא:
  $ H = P^2 / (2m) - lambda delta(x) $
  כאשר $lambda > 0$.

  מצאו את האנרגיות והפונקציות העצמיות של האנרגיה עבור $E < 0$.
])
נתחיל ממשוואת הערכים העצמיים:
$ H ket(E) = E ket(E) $
נכפול משמאל ב-$bra(x)$:
$ mel(x, H, E) = E braket(x, E) => P^2/(2m) psi_E (x) - lambda delta(x) psi_E (x) = E psi_E (x) $
נשתמש בכך ש-$P^2 = -hbar^2 partial_x^2$:
$ hbar^2/(2m) psi''_E (x) + (lambda delta(x) + E) psi_E (x) = 0 $ <מדר>
נפצל למקרים. לכל $x!=0$ מתקיים $delta(x)=0$. לכן לכל $x!=0$ מתקיים:
$ hbar^2/(2m) psi''_E (x) + E psi_E (x) =0 $
נסמן $kappa^2 = -(2m E)/hbar^2$. משום ש-$E<0$ אז $kappa^2>0$.
$ psi''_E (x) - kappa^2 psi_E (x) =0 $
הפתרון הכללי הוא:
$
  psi_E (x) = cases(
    A e^(kappa x) + B e^(-kappa x) & \, x < 0,
    C e^(kappa x) + D e^(-kappa x) & \, x > 0
  )
$

#let pex = $psi_E (x)$
משום ש-$pex$ פונקציית מצב, נדרוש שהיה תהיה אפשרית לנרמול. לכן נדרוש:
$ lim_(x->pm oo) pex = 0 $
ומכאן נקבל $B = C = 0$.
בנוסף, כפונקציית מצב $pex$ צריכה להיות רציפה, לכן:
$ psi_E (0^-) = psi_E (0^scripts(+)) => A = D $
נקבל את פונקציית המצב:
$ pex = cases(A e^(kappa x)&\, x<0, A &\, x=0, A e^(-kappa x)&\, x>0) $

כעת נראה מה קורה ב-$x=0$. נחשב אינטגרל על @מדר על טווח קטן מסביב לאפס:
$
  -hbar^2/(2m) integral_(-epsilon)^epsilon psi''_E (x) dd(x) - lambda integral_(-epsilon)^epsilon delta(x) pex dd(x) = E integral_(-epsilon)^epsilon pex dd(x) \
  -hbar^2/(2m) (psi'_E (epsilon) - psi'_E (-epsilon)) - lambda psi_E (0) = E integral_(-epsilon)^epsilon pex dd(x)
$
ניקח את הגבול בו $epsilon -> 0$. האינטגרל באגף ימין יתאפס משום שהאינטגרנד רציף בקטע עם רוחב אפס:
$
  -hbar^2/(2m)(psi'_E (0^scripts(+)) - psi'_E (0^-)) - lambda psi_E (0) = 0 => psi'_E (0^scripts(+)) - psi'_E (0^-) = -(2m lambda)/hbar^2 psi_E (0)
$ <מגניבה>
נחשב את הנגזרת של פונקציית המצב:
$
  psi'_E (x) = cases(kappa A e^(kappa x)\, x<0, -kappa A e^(-kappa x)\, x>0) => psi'_E (0^-) = kappa A, space psi'_E (0^scripts(+)) = -kappa A
$
ובנוסף משום ש-#pex רציפה, $psi_E (0) = psi_E (0^-) = A$. נציב ב@מגניבה:
$ - kappa A - kappa A = -(2m lambda)/hbar^2 A => kappa A = (m lambda) /hbar^2 A => kappa = (m lambda)/hbar^2 $
כאשר השתמשנו בכך ש-$A!=0$ אחרת $pex equiv 0$. נציב חזרה בהגדרת $kappa$:
$ kappa^2 = (m^2 lambda^2)/hbar^4 = -(2m E)/hbar^2 => E = -(m lambda^2)/(2 hbar^2) $
לבסוף, נמצא את קבוע הנרמול $A$:
$
  intoo abs(pex)^2 dd(x) =& integral_(-oo)^0 abs(A e^(kappa x))^2 dd(x) + integral_(0)^oo abs(A e^(-kappa x))^2 dd(x) = |A|^2 intoo e^(-2kappa abs(x)) dd(x) \
  stretch(=)_"אינטגרנד זוגי"& 2 |A|^2 integral_0^oo e^(-2kappa x) dd(x) = evaluated((2|A|^2)/(-2kappa) e^(-2kappa x))_0^oo = (|A|^2)/kappa =^! 1
$
נקבל כי $A = sqrt(kappa) = sqrt(m lambda)/hbar$.
#תשובה[
  קיבלנו כי יש אנרגיה עצמית יחידה שלילית:
  $ E = -(m lambda^2)/(2 hbar^2) $
  והפונקציה העצמית המתאימה היא:
  $ pex = sqrt(m lambda)/hbar e^(-(m lambda)/hbar^2|x|) $
]
#שאלה(כותרת: "מעבדה לחקר מבנים קוונטיים", מזהה: <2>, [
  במעבדה לחקר מבנים קוונטיים מכינים מצב $psi(x)$ המתאר חלקיק בעל מסה $m$ הנמצא בבור פוטנציאל אינסופי:
  $
    psi(x) = cases(
      A sin^2(pi (L-x) / L) & \, 0 <= x <= L,
      0 & \, "else"
    )
  $
])

#סעיף(מזהה: <2.1>, [
  מצאו את קבוע הנרמול $A$.
])
ננרמל את המצב:
$ integral_0^L abs(psi(x))^2 dd(x) = |A|^2 integral_0^L sin^4(pi (L-x)/L) dd(x) = 1 $
נבצע החלפת משתנים $u(x) = pi (L-x)/L$ ונקבל:
$ u= pi (L-x)/L => dd(u) = -pi/L dd(x) => dd(x) = -L/pi dd(u); space space u(x=0) = pi, u(x=L) = 0 $
נציב ונהפוך את גבולות האינטגרל:
$ 1 = L/pi|A|^2 integral_0^pi sin^4 (u) dd(u) $
נפתח את האינטגרנד:
$
  (sin^2(u))^2 & = ((1-cos(2u))/2)^2 = 1/4(1 - 2cos(2u) + cos^2(2u)) \
               & = 1/4(1- 2cos(2u) + (1+cos(4u))/2) = 1/4(3/2 - 2cos(2u) + 1/2cos(4u))
$
נחשב את האינטגרל:
$
  1 &= L/pi (|A|^2)/4 integral_0^pi (3/2 - 2cos(2u) + 1/2cos(4u)) dd(u) = L/pi (|A|^2)/4 evaluated(((3u)/2 - sin(2u) + 1/8 sin(4u)))_0^pi \
  &= L/pi (|A|^2)/4 (3pi)/2 = (3L)/8 |A|^2
$
#תשובה[
  $ A = sqrt(8/(3L)) $ <קבוע_נרמול>
]


#pagebreak()
#סעיף(מזהה: <2.2>, [
  רשמו את $psi(x)$ בבסיס האנרגיה ${ket(phi_i)}_(i=1)^oo$.
])
מצאנו בהרצאה את האנרגיות והמצבים העצמיים בבור פוטנציאל. בשביל למנוע בלבול עם $sqrt(-1)$, נסמן $n$ במקום $i$:
$ phi_n (x) = sqrt(2/L) sin((n pi x)/L), space E_n = (hbar^2 pi^2 n^2)/(2m L^2), space n in NN $
כעת נמצא את מקדמי המצבים העצמיים שיוצרים את $psi(x)$ בסכום
$ket(psi) = sum_(n=1)^oo c_n ket(phi_n)$:
$
  c_n = braket(phi_n, psi) = integral_0^L phi_n(x) psi^*(x) dd(x) = sqrt(2/L) sqrt(8/(3L)) integral_0^L sin((n pi x)/L) sin^2(pi (L-x) / L)
$
ראשית נפשט את פונקציית המצב. ידוע כי $sin x =sin(pi-x)$, לכן:
$ sin^2(pi - pi (L-x)/L) = sin^2(pi - (pi - pi x / L)) = sin^2((pi x)/L) = 1/2(1-cos((2pi x)/L)) $ <מפושט>
נציב חזרה באינטגרל:
$
  c_n & = 2/(sqrt(3) L) integral_0^L sin((n pi x)/L) (1-cos((2pi x)/L)) dd(x) \
      & = 2/(sqrt(3) L) (integral_0^L sin((n pi x)/L) dd(x) - integral_0^L sin((n pi x)/L) cos((2pi x)/L) dd(x))
$
נחשב כל אינטגרל בנפרד:
$
  I_1 = integral_0^L sin((n pi x)/L) dd(x) = evaluated(- L/(n pi) cos((n pi x)/L))_0^L = -L/(n pi) (cos(n pi)-1) = L/(n pi)(1-(-1)^n)
$
נקבל כי לכל $n$ זוגי האינטגרל מתאפס.

באינטגרל השני נשתמש בזהות הטריגונומטרית הבאה:
$ sin(alpha)cos(beta) = 1/2(sin(alpha+beta)+sin(alpha-beta)) $
נציב ונקבל:
$ sin((n pi x)/L) cos((2pi x)/L) = 1/2(sin(((n+2) pi x)/L) + sin(((n-2) pi x)/L)) $
נחשב את האינטגרל:
$
                      I_2 = & 1/2 integral_0^L (sin(((n+2) pi x)/L) + sin(((n-2) pi x)/L)) dd(x) \
  stretch(=)_(forall n!= 2) & -L/(2pi) evaluated((1/(n+2) cos(((n+2) pi x)/L) + 1/(n-2) cos(((n-2) pi x)/L)))_0^L \
                          = & -L/(2pi)(1/(n+2) (cos((n+2)pi)-1) + 1/(n-2) (cos((n-2)pi)-1)) \
                          = & -L/(2pi) ((-1)^n-1) (1/(n-2) + 1/(n+2)) = -L/(pi) (n)/(n^2-4) ((-1)^n-1)
$
עבור $n=2$:
$
  I_2 & = integral_0^L (sin(((2+2)pi x)/L) + sin 0) dd(x) = integral_0^L sin((4pi x)/L) dd(x) \
      & = evaluated(L/(4pi) cos((4pi x)/L))_L^0 = L/(4pi)(1-1) = 0
$
נקבל כי לכל $n$ זוגי האינטגרל מתאפס.

קיבלנו בסך הכל כי לכל $n$ זוגי, $c_n=0$. לכן נסמן $k=2n+1$ ונקבל:
$
  c_k = 2/(sqrt(3) L) L/pi underbrace(((-1)^k-1), k in"odds" => =2) (1/k - k/(k^2-4)) = 4/(sqrt(3) pi) (k^2 - 4 -k^2)/(k(k^2-4)) = (-16)/(sqrt(3) pi k(k^2-4))
$
נציב חזרה $k = 2n+1$:
$
  k(k^2-4) = (2n+1)((2n+1)^2-4)
$
#תשובה[
  $ ket(psi) = sum_(n=0)^oo (-16)/(sqrt(3)pi(2n+1)((2n+1)^2-4)) ket(phi_(2n+1)) $
]

#סעיף(מזהה: <2.3>, [
  מה ההסתברות למצוא חלקיק במצב האנרגיה $ket(phi_1)$?
])
$ P("Particle at" ket(phi_1)) = |c_0|^2 = (-16/(sqrt(3) pi(0+1)((2(0)+1)^2-4)))^2 = (16/(sqrt(3) pi (-3)))^2 $
#תשובה[
  ההסתברות למצוא חלקיק במצב האנרגיה $ket(phi_1)$ היא:
  $ 256/(27 pi^2) $
]
#let ee = $overline(E)$
#סעיף(מזהה: <2.4>, [
  חשבו את ערך התוחלת של אופרטור ההמילטוניאן $H$ במצב $ket(psi)$ בשתי דרכים.
  נסמן את ערך התוחלת ב-$ee$.

  *הערה:* ניתן להשתמש בזהות הבאה (יש מספר דרכים לפתרון ולא בכולן צריך את זה):
  $ sum_(n in"odds") 1 / (n^2 - 4)^2 = sum_(n=0)^oo 1 / ((2n+1)^2-4)^2 = pi^2 / 64 $
])
#תתסעיף(מזהה: <2.4.א>, [
  על ידי חישוב פעולת ההמילטוניאן על המצב (כלומר, העזרו בחישוב אלמנט המטריצה $mel(x, H, psi)$).
])
$
  ee = expval(H, psi) = expval(H I, psi) = intoo mel(psi, H, x)braket(x, psi) dd(x) = intoo (H psi(x))^* psi(x) dd(x)
$
נציב את הגרסה המפושטת שמצאנו ל-$psi(x)$ ב@מפושט:
$
  H psi(x) & = (-hbar^2)/(2m) pdv(, x, 2) (A/2 (1-cos((2pi x)/L))) = (-hbar^2)/(4m) A pdv(, x)((2pi)/L sin((2pi x)/L)) \
           & = (-hbar^2)/(2m) A pi/L (2pi)/L cos((2pi x)/L) = -(hbar^2 pi^2)/(m L^2) A cos((2pi x)/L)
$ <הפסי>
אחרי הפעלת צמוד נקבל אותה תוצאה. כעת נציב:
$ ee & = -(hbar^2 pi^2)/(m L^2) A A/2 integral_0^L (1-cos((2pi x)/L))cos((2pi x)/L) dd(x) $
נחשב את  האינטגרל בנפרד:
$ I = integral_0^L (cos((2pi x)/L) - cos^2((2pi x)/L)) dd(x) $

נבצע החלפת משתנים:
$ u = (2pi x)/L => dd(u) = (2pi)/L dd(x) => dd(x) = L/(2pi) dd(u); space space u(x=0) = 0, u(x=L) = 2pi $
נציב ונקבל:
$
  I = L/(2pi) integral_0^(2pi) (cos u - cos^2(u)) dd(u) = L/(2pi) (0 - 1/2 integral_0^(2pi) 1+cos(2u) dd(u)) = -L/2
$ <תוצאת_אינטגרל>
וזאת משום ש-$0->2pi$ הוא מחזור שלם של $cos x$ ושל $cos(2x)$. נציב חזרה:
$ ee = -(A^2 hbar^2 pi^2)/(2 m L^2) (-L/2) = (A^2 hbar^2 pi^2)/(4 m L) $
#תשובה[
  התוחלת היא:
  $ ee = (2 hbar^2 pi^2)/(3 m L^2) $
]

#תתסעיף(מזהה: <2.4.ב>, [
  על ידי סכימה של הסתברויות מדידת האנרגיות השונות עבור מצב $ket(psi)$.
])
$
  ee &= sum_(n=0)^oo P(E_(2n+1)) E_(2n+1) = sum_(n=0)^oo |c_(2n+1)|^2E_(2n+1) \
  &= sum_(n=0)^oo ((-16)/(sqrt(3)pi cancel((2n+1))[(2n+1)^2-4]))^2 (hbar^2 pi^2 cancel((2n+1)^2))/(2m L^2) = (128 hbar^2)/(3m L^2) sum_(n=0)^oo 1/((2n+1)^2-4)^2 \
  &= (128 hbar^2)/(3m L^2) (pi^2)/(64) = (2 hbar^2 pi^2)/(3m L^2)
$
#תשובה[
  התוחלת היא
  $ee = (2 hbar^2 pi^2)/(3 m L^2)$. כצפוי, קיבלנו אותה תוצאה.
]
#let eee = $overline(E^2)$
#סעיף(מזהה: <2.5>, [
  חשבו את $eee$ ואת $Delta E$ בשלוש דרכים.

  *הערה:* ניתן להשתמש בזהות הבאה (יש מספר דרכים לפתרון ולא בכולן צריך את זה):
  $ sum_(n in"odds") n^2 / (n^2 - 4)^2 = sum_(n=0)^oo (2n+1)^2 / (((2n+1)^2-4)^2) = pi^2 / 16 $
])

#תתסעיף(מזהה: <2.5.א>, [
  על ידי חישוב הנורמה $||H psi||$.
])
$ eee = expval(H^2, psi) = mel(psi, H^+ H, psi) = braket(H psi) = norm(H psi)^2 $
לפי @הפסי:
$
  norm(h psi)^2 = norm(-(hbar^2 pi^2 A)/(m L^2) cos((2pi x)/L))^2 = (hbar^4 pi^4 A^2)/(m^2 L^4) integral_0^L cos^2((2pi x)/L) dd(x)
$
לפי @קבוע_נרמול ו@תוצאת_אינטגרל:
$ eee = norm(h psi)^2 = (hbar^4 pi^4)/(m^2 L^4) 8/(3L) L/2 = (4 hbar^4 pi^4)/(3 m^2 L^4) $ <מומנט_שני>
נחשב את סטיית התקן לפי הגדרה:
$
  Delta E = sqrt(eee - (ee)^2) = sqrt((4 hbar^4 pi^4)/(3 m^2 L^4) - (4 hbar^4 pi^4)/(9 m^2 L^4)) = (2 sqrt(2) hbar^2 pi^2)/(3 m L^2)
$
#תשובה[
  $ eee = (4 hbar^4 pi^4)/(3 m^2 L^4), space Delta E = (2 sqrt(2) hbar^2 pi^2)/(3 m L^2) $
]
#תתסעיף(מזהה: <2.5.ב>, [
  על ידי הפעלה של האופרטור $H^2$ על המצב $ket(psi)$.
])
נפעיל את האופרטור על המצב:
$
  mel(x, H^2, psi) &= H^2 psi(x) = H(H psi(x)) = H(-(hbar^2 pi^2)/(m L^2) A cos((2pi x)/L)) \
  &= (hbar^4 pi^2 A)/(2 m^2 L^2) pdv(, x, 2)(cos((2pi x)/L)) = -(2hbar^4 pi^4 A)/(m^2 L^4) cos((2pi x)/L)
$
נחשב את #eee:
$
  eee &= integral_0^L psi(x) mel(x, H^2, psi) dd(x) = -(2hbar^4 pi^4 A)/(m^2 L^4) dot 1/2 A integral_0^L (1-cos((2pi x)/L)) cos((2pi x)/L) dd(x) \
  &= -(hbar^4 pi^4 A^2)/(m^2 L^4) dot (-L/2) = (hbar^4 pi^4 A^2)/(2 m^2 L^3)
$
כאשר השתמשנו בתוצאת האינטגרל מ@תוצאת_אינטגרל.
#תשובה[
  קיבלנו ערך זהה של #eee כפי שקיבלנו ב@מומנט_שני, לכן גם השונות, $Delta E$, זהה.
]
#pagebreak()
#תתסעיף(מזהה: <2.5.ג>, [
  על ידי סכימה של הסתברויות מדידת האנרגיות השונות עבור מצב $ket(psi)$.
])
$
  eee &= sum_(n=0)^oo P(E_(2n+1)) (E_(2n+1))^2 = sum_(n=0)^oo abs(c_(2n+1))^2(E_(2n+1))^2 \
  &= 256/(3pi^2) (hbar^4 pi^4)/(4 m^2 L^4) sum_(n=0)^oo (2n+1)^(cancel(4) text(space.thin "2", fill: #red, style: "italic"))/(cancel((2n+1)^2)((2n+1)^2-4)^2) = (64hbar^4 pi^2)/(3 m^2 L^4) sum_(n=0)^oo (2n+1)^2/((2n+1)^2-4)^2 \
  &= (64hbar^4 pi^2)/(3 m^2 L^4) dot pi^2/16 = (4hbar^4 pi^4)/(3 m^2 L^4)
$
#תשובה[
  קיבלנו ערך זהה של #eee כפי שקיבלנו ב@מומנט_שני, לכן גם השונות, $Delta E$, זהה.
]
#שאלה(כותרת: "התפתחות בזמן בבור פוטנציאל אינסופי", מזהה: <3>, [
  מצאו את $psi(x, t)$ ואת הההסתברות למדוד את ערכי האנרגיה האפשריים $P(E_n)$ עבור $t > 0$ עבור חלקיק בבור פוטנציאל אינסופי $[0, L]$ עבור כל אחד ממצבי ההתחלה הבאים:
])

#סעיף(מזהה: <3.1>, [
  $ psi(x, 0) = A_1 sin(3 pi x / L) cos((pi x) / L) $
])

#סעיף(מזהה: <3.2>, [
  $ psi(x, 0) = A_2 x^2 (x - L)^2 $
])

#שאלה(כותרת: "התפתחות בזמן של צפיפות הסתברות (תרגיל נומרי)", מזהה: <4>, [
])

#סעיף(מזהה: <4.1>, [
  נתון חלקיק חופשי. נניח שבזמן $t = 0$ החלקיק מתואר על ידי $braket(p, psi_0) = psi_0(p)$. רשמו ביטוי אינטגרלי ל-$psi(x, t)$.
])

#סעיף(מזהה: <4.2>, [
  נרצה לפתור אינטגרל זה נומרית.
])

#תתסעיף(מזהה: <4.2.1>, [
  רשמו פונקציה שמקבלת פונקציה $f(y)$ ומחזירה את האינטגרל שלה בין $x = -10$ ל-$x = 10$. ניתן לקבל את הפונקציה כרשימה של ערכים באינטרוולים $Delta y$ ולבצע את האינטגרל כסכום רימן או בכל דרך אחרת.
])

#תתסעיף(מזהה: <4.2.2>, [
  נניח ש:
  $ psi_0(p) = N e^(- (p-p_0)^2 / (2 Delta^2)) e^(- i p x_0 / hbar) $
  כאשר $L = 1$, קבוע נרמול לא ידוע $N$, $x_0 = -5L$, $m = hbar$, $Delta = hbar / L$, $p_0 = hbar / L$.
  חשבו את $psi(0, 0)$ באופן נומרי. ניתן לקטום את האינטגרל ב-$p = 10 p_0$. ניתן לקבל את $N$ עד כדי קבוע כפלי.
])

#תתסעיף(מזהה: <4.2.3>, [
  חשבו את $psi(x, 0)$ עבור $x$ בין $-10$ ל-$10$ בקפיצות של $0.1$.
])

#תתסעיף(מזהה: <4.2.4>, [
  חשבו באופן נומרי את קבוע הנרמול $N$ מתוך הסעיף הקודם.
])

#תתסעיף(מזהה: <4.2.5>, [
  חשבו את $psi(x, t)$ עבור $x$ בין $-10$ ל-$10$ ו-$t$ בין $0$ ל-$10$ בקפיצות של $0.1$, בהינתן הקבוע מהסעיף הקודם.
])

#תתסעיף(מזהה: <4.2.6>, [
  צרו אנימציה של צפיפות ההסתברות המשויכת ל-$psi(x, t)$.
])

#תתסעיף(מזהה: <4.2.7>, [
  נניח ש:
  $ psi_0(x) = N Delta e^(i p_0 x / hbar) / ((x - x_0)^2 + Delta^2) $
  כאשר $L = 1$, $N$ קבוע נרמול לא ידוע, $x_0 = -5L$, $m = hbar/L$, $Delta = L$, $p_0 = hbar / L$.
  צרו אנימציה של צפיפות ההסתברות המשויכת ל-$psi(x, t)$.
])

#סעיף(מזהה: <4.3>, [
  כעת נסתכל על מחסום פוטנציאל:
  $ V = V_0 Theta(x) $
  כאשר
  $
    Theta(x) = cases(
      0 \, x < 0,
      1 \, x > 0
    )
  $

  השתמשו בביטויים שפיתחנו בכיתה כדי ליצור אנימציה המתארת פונקציית גל עם תמיכה משמאל למחסום, ונעה ימינה, כאשר:
])

#תתסעיף(מזהה: <4.3.1>, [
  פונקציית הגל ההתחלתית בנויה רק מווקטורים עצמיים עם ערכים עצמיים $E < V_0$.
])

#תתסעיף(מזהה: <4.3.2>, [
  פונקציית הגל ההתחלתית בנויה רק מווקטורים עצמיים עם ערכים עצמיים $E > V_0$.
])

#תתסעיף(מזהה: <4.3.3>, [
  פונקציית הגל ההתחלתית בנויה מווקטורים עצמיים עם ערכים עצמיים בסביבות $V_0$ (גם מעל וגם מתחת).
])

