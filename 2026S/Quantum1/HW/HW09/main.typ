#import "../../../../typst/templates/hw.typ": *
#import "../../../../typst/consts.typ": *
#import "../../../../typst/utils.typ": *


#show: project.with(
  title: "פיסיקה קוונטית 1",
  number: "9",
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2026, month: 7, day: 11),
)

#שאלה(כותרת: "אוסילטור הרמוני דו־ממדי לא־איזוטרופי", מזהה: <1>, [
  נתון ההמילטוניאן הבא המתאר מערכת דו־ממדית:
  $ H = P_x^2 / (2m) + P_y^2 / (2m) + 1/2 m omega_1^2 X^2 + 1/2 m omega_2^2 Y^2 $
  כאשר $omega_1 != omega_2$. נתון כי לרמת היסוד אנרגיה $E_0$ ולרמה הראשונה אנרגיה $5/3 E_0$.
  מהו הניוון של הרמה המעוררת השנייה?
])
ניתן לרשום את ההמילטוניאן כסכום של שני המילטוניאנים נפרדים:
$ H = H_x + H_y, space H_x = P_x^2/(2m) + 1/2 m omega_1^2 X^2, space H_y = P_y^2/(2m) + 1/2 m omega_2^2 Y^2 $
כמו שראינו בתרגול, נסמן את המצבים העצמיים כך:
$
  H ket(n\, m) = hbar (omega_1 (n+1/2) + omega_2 (m+1/2)) ket(n\, m) = hbar(omega_1 n + omega_2 m + (omega_1 + omega_2)/2) ket(n\, m)
$
כעת נציב את הנתון בשביל למצוא את $omega_1$ ואת $omega_2$. נניח בה"כ כי $omega_1 < omega_2$, כך שרמת האנרגיה הראשונה נמדדת אצל חלקיק במצב $ket(1\, 0)$:
$
  E_0 = hbar(omega_1 dot 0 + omega_2 dot 0 + (omega_1 + omega_2)/2) = hbar (omega_1 + omega_2)/2 space => space omega_1 + omega_2 = (2E_0)/hbar
$
$
  5/3 E_0 = hbar(omega_1 dot 1 + omega_2 dot 0 + (omega_1 + omega_2)/2) = hbar/2 (3 omega_1 + omega_2) = hbar/2 (2 E_0 / hbar + 2 omega_1) = E_0 + hbar omega_1
$
כעת נוכל למצוא את $omega_1$ ואת $omega_2$:
$ omega_1 =(5/3-1)E_0/hbar = 2/3 E_0/hbar space => space omega_2 = (2 - 2/3)E_0/hbar = 4/3 E_0/hbar = 2 omega_1 $
כלומר האנרגיות העצמיות הן:
$ E_(n m) = 2/3 E_0 (n + 2m + 3/2) = E_0(1 + 2/3 (n + 2m)) $
רמת האנרגיה השנייה תימדד במצב $ket(0\, 1)$ או $ket(2\, 0)$:
$ E_(01) = E_0(1 + 2/3(0 + 2 dot 1)) = 7/3 E_0, space E_(20) = E_0(1 + 2/3(2 + 2 dot 0)) = 7/3 E_0 $
#תשובה[
  קיבלנו שני מצבים עצמיים המתאימים לרמת האנרגיה השנייה, לכן הניוון שלה הוא $2$.
]

#שאלה(כותרת: "שני אוסילטורים הרמונים מצומדים", מזהה: <2>, [
  שני חלקיקים מובחנים בעלי מסה $m$ נמצאים בפוטנציאל הרמוני חד-מימדי עם תדירות $omega$. פוטנציאל האינטראקציה ביניהם הוא:
  $ U = 1/4 m Omega^2 (x1 - x2)^2 $
  כאשר $x1, x2$ מיקומים של החלקיק הראשון והשני בהתאמה, ומתקיים $[x1, x2] = 0$.
])

#סעיף(מזהה: <2.א>, [
  רשמו את ההמילטוניאן המלא של המערכת בעזרת מיקום ותנע של החלקיקים.
])

#תשובה[
  $ H = (p_1^2 + p_2^2)/(2m) + 1/2 m omega^2(x1^2 + x2^2) + 1/4 m Omega^2 (x1 - x2)^2 $
]

#pagebreak()
#let cm = $c m$
#סעיף(מזהה: <2.ב>, [
  הגדירו את אופרטור המיקום היחסי $x_R = x1 - x2$ ואופרטור מרכז המסה $x_(cm) = 1/2 (x1 + x2)$ והתנע הצמוד להם. הראו כי המיקום החדש והתנע הצמוד לו מקיימים יחסי חילוף קנוניים.
])
#let x1 = $x1$; #let x2 = $x2$; #let p1 = $p_1$; #let p2 = $p_2$
נראה כי מתקיים
$[x_i, p_j] = i hbar delta_(i j)$. נגדיר $p_R = 1/2(p1-p2)$ ונקבל:
$
  [x_R, p_R] & = [x1 - x2, 1/2(p1-p2)] \
             & = 1/2([x1, p1] + underbrace([x1, -p2] + [-x2, p1], 0) + [-x2, -p2]) = 1/2(i hbar + i hbar) = i hbar
$
נגדיר את תנע מרכז המסה, $p_(cm) = p1+p2$ ונקבל:
$
  [x_(cm), p_(cm)] & = [1/2(x1+x2), p1+p2] \
                   & = 1/2([x1, p1] + underbrace([x1, p2] + [x2 , p1], 0) + [x2, p2]) = 1/2 dot 2 i hbar = i hbar
$
בנוסף:
$
  [x_R, p_cm] & = [x1 - x2, p1 + p2] = [x1, p_1] - [x2, p_2] = i hbar - i hbar  & = 0 \
  [x_cm, p_R] & = [1/2 (x1 + x2), 1/2 (p_1 - p_2)] = 1/4([x1, p_1] - [x2, p_2]) & = 0 \
  [x_cm, x_R] & = [1/2(x1 + x2), x1 - x2]                                       & = 0 \
  [p_cm, p_R] & = [p1 + p2, 1/2(p1 - p2)]                                       & = 0
$
#תשובה[
  $ [x_i, p_j] = i hbar delta_(i j) $
]

#pagebreak()
#סעיף(מזהה: <2.ג>, [
  רשמו את ההמילטוניאן בעזרת אופרטורים חדשים. לכסנו את ההמילטוניאן והציגו אותו בעזרת אופרטורי המספר $N_R, N_(c m)$. חשבו את רמות האנרגיה.
])
נתאר את המיקום והתנע של כל אחד מהחלקיקים בעזרת הקואורדינטות החדשות:
$
  x_cm + 1/2 x_R & = 1/2(x1 + cancel(x2) + x1 - cancel(x2)) & = x1 \
  x_cm - 1/2 x_R & = 1/2(cancel(x1) + x2 - cancel(x1) + x2) & = x2 \
  1/2 p_cm + p_R & = 1/2(p1 + cancel(p2) + p1 - cancel(p2)) & = p1 \
  1/2 p_cm - p_R & = 1/2(cancel(p1) + p2 - cancel(p1) + p2) & = p2
$
נחשב את האנרגיות הקינטית והפוטנציאלית:
$
  T & = (1/4 p_cm^2 + cancel(p_cm p_R) + p_R^2 + 1/4 p_cm^2 - cancel(p_cm p_R) + p_R^2)/(2m) = p_cm^2/(4m) + p_R^2/m \
  V & = 1/2 m omega^2(x_cm^2 + cancel(x_cm x_R) + 1/4 x_R^2 + x_cm^2 - cancel(x_cm x_R) + 1/4 x_R^2) + 1/4 m Omega^2 (cancel(x_cm) + 1/2 x_R - cancel(x_cm) + 1/2 x_R)^2 \
  &= m omega^2(x_cm^2 + 1/4 x_R^2) + 1/4 m Omega^2 x_R^2 = m omega^2 x_cm^2 + 1/4 m (omega^2 + Omega^2) x_R^2
$
נוכל כעת לפרק את $H$ לרכיב של מרכז המסה ולרכיב של התנועה היחסית:
$ H_cm = p_cm^2/(4m) + m omega^2 x_cm^2, space H_R = p_R^2/m + 1/4 m (omega^2 + Omega^2) x_R^2 $
נבחין כי כל אחד מההמילטוניאנים מתאים להמילטוניאן של מתנד הרמוני:
$ H = p^2/(2m) + 1/2 m omega^2 x^2 = hbar omega (N + 1/2) $
מכאן:
$
  m_cm = 2m, space.thin omega_cm = omega space.thin => space.thin H_cm &= hbar omega(N_cm + 1/2) \
  m_R = 1/2 m, space.thin omega_R = sqrt(omega^2 + Omega^2) space.thin => space.thin H_R &= hbar sqrt(omega^2 + Omega^2) (N_R + 1/2)
$
נמצא את רמות האנרגיה:
#תשובה[
  $
    H = hbar omega (N_cm + 1/2) + hbar sqrt(omega^2 + Omega^2) (N_R + 1/2)
  $
  $ E_(n_cm, n_R) = hbar (omega(n_cm + 1/2) + sqrt(omega^2 + Omega^2) (n_R + 1/2)), space n_cm, n_R in NN union {0} $
]

#שאלה(כותרת: "דרגת חופש נוספת", מזהה: <3>, [
  נתון חלקיק במימד אחד עם דרגת חופש של צבע שיכולה לקבל ערכים $b$ ו־$g$. נתון המילטוניאן (הרמיטי):
  $
    H = P^2 / (2m) + 1/2 m omega^2 X^2 (ket(g)bra(g) + i alpha ket(g)bra(b) - i sqrt(5)/2 ket(b)bra(g) + 3 ket(b)bra(b))
  $
  נתון כי $m, alpha, omega$ ממשיים וחיוביים.
])

#סעיף(מזהה: <3.א>, [
  מהו $alpha$?
])
נסמן את אופרטור הצבע:
$
  C = ket(g)bra(g) + i alpha ket(g)bra(b) - i sqrt(5)/2 ket(b)bra(g) + 3 ket(b)bra(b)
$
$H$, $P$ ו־$X$ הם אופרטורים הרמיטיים, לכן גם $C$ צריך להיות הרמיטי, כלומר נדרוש $C=C^+$:
$
  C^+ = ketbra(g) - i alpha ketbra(b, g) + i sqrt(5)/2 ketbra(g, b) + 3 ketbra(b)
$
כאשר $alpha$ ממשי ולכן $alpha^* = alpha$. נדרוש שהמקדמים של $ketbra(g, b)$ ב־$C$ וב־$C^+$ יהיו שווים ונקבל:
#תשובה[
  $ alpha = sqrt(5)/2 $
]

#סעיף(מזהה: <3.ב>, [
  מהן רמות האנרגיה?
])
נבטא את $H$ באופן מפורש כסכום מכפלה טנזורית:
$
  H = P^2/(2m) tp II + 1/2 m omega^2 X^2 tp C = dmat(P^2/(2m), P^2/(2m), fill: 0) + 1/2 m omega^2 X^2 dmat(lambda_1, lambda_2, fill: 0) => \
  H = dmat(P^2/(2m) + 1/2 m (lambda_1 omega^2) X^2, P^2/(2m) + 1/2 m (lambda_2 omega^2) X^2, fill: 0)
$
כלומר ההמילטוניאן מורכב משני המילטוניאנים של מתנדים הרמוניים. נלכסן את $C$. המטריצה המייצגת שלו היא:
$ A = mat(1, sqrt(5)/2 i; -sqrt(5)/2 i, 3) $
נפתור את הפולינום האופייני:
$
  p(lambda) & = abs(A - lambda I) = det(1-lambda, sqrt(5)/2 i; -sqrt(5)/2 i, 3-lambda) = (1-lambda)(3-lambda) - 5/4 \
            & = 3 - lambda - 3lambda + lambda^2 - 5/4 = lambda^2 - 4lambda + 7/4 = 0
$
$
  lambda_(1,2) = (4 pm sqrt(16-7))/2 = (4 pm 3)/2 => lambda_1 = 1/2, lambda_2 = 7/2
$
כלומר:
$
  m_1 & = m, space omega_1 = 1/sqrt(2) omega \
  m_2 & = m, space omega_2 = sqrt(7/2) omega
$
#תשובה[
  $
    E_n = 1/sqrt(2) hbar omega (n + 1/2), space E_m = sqrt(7/2) hbar omega (m + 1/2) , space m, n in {0, 1, 2, ...}
  $
]

#סעיף(מזהה: <3.ג>, [
  אילו רמות אנרגיה מנוונות?
])
כפי שראינו בעבר, רמות אנרגיה של מתנד הרמוני יחיד לעולם אינן מנוונות. כלומר אין שני מצבים $ket(i)$ המתאימים לאותה אנרגיה $E_i$ כאשר $i in {n, m}$. נבדוק האם קיימים $n$ ו־$m$ כך ש־$E_n = E_m$:
$
  1/sqrt(2) hbar omega (n + 1/2) = sqrt(7/2) hbar omega (m + 1/2) space slash.big dot sqrt(2)/(hbar omega) \
  n + 1/2 = sqrt(7) (m + 1/2) space.thin => space.thin (2n+1)/(2m+1) = sqrt(7)
$
משום ש־$n$ ו־$m$ מספרים שלמים, בצד שמאל של המשוואה יש לנו מספר רציונלי, אך באגף ימין יש #box[מספר אי־רציונלי]. לכן השוויון לא מתקיים לאף $n$ ו־$m$.
#תשובה[
  אין ניוון ברמות האנרגיה.
]

#שאלה(כותרת: "אבולוציה בזמן במערכת מרובת חלקים ללא אינטראקציה", מזהה: <4>, [
  נתבונן בשני חלקיקים שונים ומובחנים, 1 ו־2, כאשר אין אינטראקציה ביניהם. ההמילטוניאנים של החלקיקים הבודדים הם $h(1)$ ו־$h(2)$ (כל אחד פועל רק על מרחב הילברט של החלקיק המתאים). ההמילטוניאן הכולל הוא:
  $ H = h(1) tp bb(1)(2) + bb(1)(1) tp h(2) $
])

#סעיף(מזהה: <4.א>, [
  הוכיחו כי מתקיים יחס החילוף הבא:
  $[h(1) tp bb(1)(2), bb(1)(1) tp h(2)] = 0$.
])

נשתמש בזהות הבאה:
$ (A tp B)(C tp D) = (A C) tp (B D) $ <פירוק>
$
  [h(1) tp bb(1)(2), bb(1)(1) tp h(2)] & = (h(1) tp bb(1)(2))(bb(1)(1) tp h(2)) - (bb(1)(1) tp h(2))(h(1) tp bb(1)(2)) \
                                       & = (h(1)bb(1)(1)) tp (bb(1)(2)h(2)) - (bb(1)(1)h(1)) tp (h(2)bb(1)(2)) \
                                       & = h(1) tp h(2) - h(1) tp h(2) = 0 space.quad qed
$

#סעיף(מזהה: <4.ב>, [
  היעזרו בתוצאה מ@4.א ובנוסחת בייקר־קמפבל־האוסדורף כדי להראות:
  $ U(t) = e^(-i/hbar H t) = e^(-i/hbar h(1) t) tp e^(-i/hbar h(2) t) $
])
מנוסחת BCH נקבל כי אם שני אופרטורים, $A$ ו-$B$ מתחלפים, אז $e^(A+B) = e^A e^B$. מכאן:
$
  U(t) = e^(-i/hbar H t) = e^(-i/hbar (h(1) tp bb(1)(2) + bb(1)(1) tp h(2)) t) = e^(-i/hbar h(1) tp bb(1)(2)t) dot e^(-i/hbar bb(1)(1) tp h(2) t)
$
נוכיח את הזהות $e^(A tp bb(1)) = e^A tp bb(1)$:
$ e^(A tp bb(1)) = sum_(k=0)^oo (A^k tp bb(1))/k! = (sum_(k=0)^oo A^k/k!) tp bb(1) = e^A tp bb(1) $
ההוכחה עבור $e^(bb(1) tp A)$ אנלוגית. נציב חזרה:
$
  U(t) &= (e^(-i/hbar h(1)t) tp bb(1)(2)) dot (bb(1)(1) tp e^(-i/hbar h(2) t)) \
  &= (e^(-i/hbar h(1)t) bb(1)(1)) tp (bb(1)(2) e^(-i/hbar h(2) t)) = e^(-i/hbar h(1)t) tp e^(-i/hbar h(2) t) space.quad qed
$

#pagebreak()
#סעיף(מזהה: <4.ג>, [
  יהי המצב ההתחלתי $ket(Psi(0)) = ket(phi.alt(1)) tp ket(chi(2))$. חשבו את $ket(Psi(t)) = U(t)ket(Psi(0))$. הראו במפורש שהמצב נשאר מצב מכפלה בכל זמן $t$. מה משמעות תוצאה זו?
])
נשתמש בזהות הנתונה ב@פירוק:
$
  ket(Psi(t)) & = U(t) ket(Psi(0)) = (e^(-i/hbar h(1)t) tp e^(-i/hbar h(2) t))(ket(phi(1)) tp ket(chi(2))) \
              & = (e^(-i/hbar h(1)t) ket(phi(1))) tp (e^(-i/hbar h(2) t) ket(chi(2)))
$
קיבלנו כנדרש מצב מכפלה בכל זמן $t$.
#תשובה[
  משמעות התוצאה היא שאין שום תלות בין שני החלקיקים -- ניתן למדוד כל אחד מהם ללא השפעה על החלקיק השני.
]

#סעיף(מזהה: <4.ד>, [
  יהיו $A(1) = A tp bb(1)$ ו־$B(2) = bb(1) tp B$ אופרטורים הפועלים רק על החלקיק הראשון והשני, בהתאמה. הראו כי:
  $ expval(A(1) B(2))_(Psi(t)) = expval(A(1))_(Psi(t)) expval(B(2))_(Psi(t)) $
  כאשר $A(1) B(2) equiv A tp B$.
])
נסמן
$ket(Psi(t)) = ket(phi.alt(t, 1)) tp ket(chi(t, 2))$. נפתח את אגף שמאל של המשוואה:
$
  expval(A(1) B(2))_Psi(t) & = expval(A(1) B(2), Psi(t)) \
                           & = (bra(phi.alt(t, 1)) tp bra(chi(t, 2))) (A tp B) (ket(phi.alt(t, 1)) tp ket(chi(t, 2))) \
                           & = expval(A, phi.alt(t, 1))dot expval(B, chi(t, 2))
$
כעת נפתח את כל אחת מהתוחלות באגף ימין:
$
  expval(A(1))_Psi(t) & = expval(A(1), Psi(t)) = (bra(phi.alt(t, 1)) tp bra(chi(t, 2))) (A tp bb(1)) (ket(phi.alt(t, 1)) tp ket(chi(t, 2))) \
  & = expval(A, phi.alt(t, 1)) dot braket(chi(t, 2), chi(t, 2)) = expval(A, phi.alt(t, 1)) \
  expval(B(2))_Psi(t) & = expval(B(2), Psi(t)) = (bra(phi.alt(t, 1)) tp bra(chi(t, 2))) (bb(1) tp B) (ket(phi.alt(t, 1)) tp ket(chi(t, 2))) \
  & = braket(phi.alt(t, 1), phi.alt(t, 1)) dot expval(B, chi(t, 2)) = expval(B, chi(t, 2))
$
#תשובה[
  $ expval(A(1) B(2))_(Psi(t)) = expval(A(1))_(Psi(t)) expval(B(2))_(Psi(t)) $
]

#סעיף(מזהה: <4.ה>, [
  אם במקום המצב ההתחלתי $ket(Psi)$ המערכת הייתה במצב התחלתי שזור, האם תוצאת סעיף ד' הייתה נכונה? נמקו בקצרה.
])
#תשובה[
  באופן כללי תוצאת @4.ד הייתה שגויה. בפיתוח התבססנו על כך שיכולנו לכתוב את $ket(Psi)$ כמכפלה של שני מצבים, ואז יכולנו לפצל את $expval(A(1)B(2))_Psi(t)$ למכפלה של שתי תוחלות. בלי האפשרות לכתוב את $ket(Psi)$ כמצב מכפלה לא היינו יכולים לעשות זאת.
]

#שאלה(כותרת: "התפתחות בזמן וערכי תצפית במערכת שני חלקיקים", מזהה: <5>, [
  שני חלקיקים שונים (ומובחנים) בעלי אותה המסה וללא אינטראקציה ביניהם נמצאים בבור פוטנציאל כלשהו. לכל חלקיק המילטוניאן $h(i)$ (עם $i=1,2$) עם ספקטרום בדיד של מצבים קשורים, ${E_n}_(n=1)^oo$, הזהה לשני החלקיקים. המצבים העצמיים המתאימים מסומנים ב־$ket(psi_n (i))$.
  ההמילטוניאן המתאר את שני החלקיקים יחדיו הוא:
  $ H(1,2) = h(1) + h(2) = h(1) tp bb(1)(2) + bb(1)(1) tp h(2) $
  המצבים העצמיים שלו מתקבלים ממכפלות טנזוריות מהצורה:
  $ ket(psi_n (1)) tp ket(psi_m (2)) = ket(psi_n psi_m) $
])

#סעיף(מזהה: <5.א>, [
  מכינים את המערכת בזמן $t=0$ במצב:
  $
    ket(Psi_s (0)) = 1/sqrt(2) (ket(psi_1(1)) + ket(psi_2(1))) tp 1/sqrt(3) (ket(psi_1(2)) + sqrt(2) ket(psi_2(2)))
  $
  מצאו את המצב $ket(Psi_s(t))$ בזמן $t$.
])
מכיוון שהמערכת אינה מצומדת, מצב המערכת בזמן $t$ הוא מכפלת מצבי החלקיקים בזמן $t$:
$
  ket(Psi_s (t)) & = U(t) ket(Psi_s (0)) \
  & = 1/sqrt(2) (e^(-i/hbar E_1 t) ket(psi_1(1)) + e^(-i/hbar E_2 t) ket(psi_2(1))) tp 1/sqrt(3) (e^(-i/hbar E_1 t) ket(psi_1(2)) + sqrt(2) e^(-i/hbar E_2 t) ket(psi_2(2))) \
$
#תשובה[
  $
    ket(Psi_s (t)) = 1/sqrt(6) (e^(-2i/hbar E_1 t) ket(psi_1 psi_1) + sqrt(2) e^(-i/hbar (E_1 + E_2)t) ket(psi_1 psi_2) + e^(-i/hbar (E_1 + E_2)t) ket(psi_2 psi_1) + sqrt(2) e^(-2i/hbar E_2 t) ket(psi_2 psi_2))
  $
]

#סעיף(מזהה: <5.ב>, [
  בזמן $t > 0$ כלשהו מודדים את האנרגיה הכוללת של המערכת. מהן תוצאות המדידה האפשריות וההסתברויות המתאימות להן?
])

מצב המערכת בזמן $t$ מורכב מארבעה מצבים עצמיים של ההמילטוניאן הכולל $H(1,2)$, כאשר לכל מצב מתאימה אנרגיה כוללת שהיא סכום האנרגיות של כל חלקיק בנפרד:
- עבור המצב $ket(psi_1 psi_1)$, האנרגיה היא $2 E_1$ וההסתברות היא:
  $ P(2E_1) = abs(1/sqrt(6) e^(-2i/hbar E_1 t))^2 = 1/6 $
- עבור המצבים $ket(psi_1 psi_2)$ ו־$ket(psi_2 psi_1)$, האנרגיה היא $E_1 + E_2$ וההסתברות היא סכום ההסתברויות שלהם (שכן שני המצבים הללו מתאימים לאותה אנרגיה):
  $
    P(E_1 + E_2) = abs(sqrt(2)/sqrt(6) e^(-i/hbar (E_1+E_2) t))^2 + abs(1/sqrt(6) e^(-i/hbar (E_1+E_2) t))^2 = 2/6 + 1/6 = 1/2
  $
- עבור המצב $ket(psi_2 psi_2)$, האנרגיה היא $2 E_2$ וההסתברות היא:
  $ P(2E_2) = abs(sqrt(2)/sqrt(6) e^(-2i/hbar E_2 t))^2 = 2/6 = 1/3 $
#תשובה[
  $ P(2E_1) = 1/6, space P(E_1 + E_2) = 1/2, space P(2E_2) = 1/3 $
]
#סעיף(מזהה: <5.ג>, [
  חשבו את ערכי התצפית $expval(h(1))$, $expval(h(2))$ ואת ערך התצפית של המכפלה $expval(h(1) h(2))$. האם מתקיים השוויון $expval(h(1) h(2)) = expval(h(1)) expval(h(2))$ במצב $ket(Psi_s (t))$?
])
נחשב את ערכי התצפית של האנרגיות של החלקיקים הבודדים. מאחר שהמצב הוא מצב מכפלה $ket(Psi_s (t)) = ket(phi_1(t)) tp ket(phi_2(t))$, נקבל עבור החלקיק הראשון:
$
  expval(h(1))_Psi(t) & = braket(Psi_s (t), (h(1) tp bb(1)) Psi_s (t)) \
  & = (bra(phi_1(t)) tp bra(phi_2(t))) (h(1) tp bb(1)) (ket(phi_1(t)) tp ket(phi_2(t))) \
  & = bra(phi_1(t)) h(1) ket(phi_1(t)) dot underbrace(braket(phi_2(t), phi_2(t)), 1) \
  & = 1/2 (e^(i/hbar E_1 t) bra(psi_1) + e^(i/hbar E_2 t) bra(psi_2)) h(1) (e^(-i/hbar E_1 t) ket(psi_1) + e^(-i/hbar E_2 t) ket(psi_2)) \
  & = 1/2 (e^(i/hbar E_1 t) bra(psi_1) + e^(i/hbar E_2 t) bra(psi_2)) (E_1 e^(-i/hbar E_1 t) ket(psi_1) + E_2 e^(-i/hbar E_2 t) ket(psi_2)) \
  & = 1/2 (E_1 braket(psi_1, psi_1) + E_2 e^(i/hbar (E_1 - E_2) t) braket(psi_1, psi_2) + E_1 e^(-i/hbar (E_1 - E_2) t) braket(psi_2, psi_1) + E_2 braket(psi_2, psi_2)) \
  & = 1/2 E_1 + 1/2 E_2
$
באופן אנלוגי עבור החלקיק השני:
$ expval(h(2))_Psi(t) = 1/3 E_1 + 2/3 E_2 $

כעת נחשב את ערך התצפית של המכפלה $h(1)h(2)$ באמצעות ההסתברויות שמצאנו ב@5.ב:
$
  expval(h(1) h(2)) & = P(2E_1) E_1^2 + P(E_1 + E_2) E_1 E_2 + P(2E_2) E_2^2 \
                    & = 1/6 E_1^2 + 1/2 E_1 E_2 + 1/3 E_2^2
$

נבדוק האם מתקיים השוויון:
$
  expval(h(1)) expval(h(2)) & = (1/2 E_1 + 1/2 E_2)(1/3 E_1 + 2/3 E_2) \
                            & = 1/6 E_1^2 + 2/6 E_1 E_2 + 1/6 E_1 E_2 + 2/6 E_2^2 \
                            & = 1/6 E_1^2 + 1/2 E_1 E_2 + 1/3 E_2^2
$
#תשובה[
  $ expval(h(1)) = 1/2 E_1 + 1/2 E_2, space expval(h(2)) = 1/3 E_1 + 2/3 E_2 $
  $ expval(h(1) h(2)) = 1/6 E_1^2 + 1/2 E_1 E_2 + 1/3 E_2^2 $
  מתקיים השוויון $expval(h(1) h(2)) = expval(h(1)) expval(h(2))$ כפי שצפוי עבור מצב מכפלה.
]

#סעיף(מזהה: <5.ד>, [
  כעת מכינים את המערכת במצב:
  $ ket(Psi_i (0)) = 1/sqrt(5) ket(psi_1 psi_1) + sqrt(3/5) ket(psi_1 psi_2) + 1/sqrt(5) ket(psi_2 psi_1) $
  במצב זה חשבו את ערכי התצפית $expval(h(1))$, $expval(h(2))$, $expval(h(1) h(2))$. \ האם מתקיים השוויון $expval(h(1) h(2)) = expval(h(1)) expval(h(2))$?
])

נחשב את ערכי התצפית עבור המצב השזור הנתון $ket(Psi_i (0))$:
$
  expval(h(1)) & = 1/5 E_1 + 3/5 E_1 + 1/5 E_2 = 4/5 E_1 + 1/5 E_2 \
  expval(h(2)) & = 1/5 E_1 + 3/5 E_2 + 1/5 E_1 = 2/5 E_1 + 3/5 E_2
$
ערך התצפית של המכפלה הוא:
$
  expval(h(1) h(2)) & = 1/5 E_1^2 + 3/5 E_1 E_2 + 1/5 E_2 E_1 = 1/5 E_1^2 + 4/5 E_1 E_2
$

נחשב את מכפלת התוחלות:
$
  expval(h(1)) expval(h(2)) & = (4/5 E_1 + 1/5 E_2)(2/5 E_1 + 3/5 E_2) \
                            & = 8/25 E_1^2 + 14/25 E_1 E_2 + 3/25 E_2^2
$
#תשובה[
  $ expval(h(1)) = 4/5 E_1 + 1/5 E_2, space expval(h(2)) = 2/5 E_1 + 3/5 E_2 $
  $ expval(h(1) h(2)) = 1/5 E_1^2 + 4/5 E_1 E_2 $
  מתקיים $expval(h(1) h(2)) != expval(h(1)) expval(h(2))$, כלומר השוויון *אינו* מתקיים במצב שזור זה.
]
