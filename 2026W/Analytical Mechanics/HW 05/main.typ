#import "../template.typ": *
#import "../consts.typ": *
#import "../utils.typ": *


// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "מכניקה אנליטית",
  number: 5,
  authors: (
    (name: "דן קצוב-פייגין", email: "dan.k@campus.technion.ac.il", id: "323002915"),
  ),
  date: datetime(year: 2025, month: 12, day: 20)
)
#set text(font: "Noto Serif Hebrew", weight: 500, lang: "he", region: "il")

#שאלה(כותרת:"פוטנציאל מרכזי",[
נתון לגרנזי'אן $לגר$ המתאר מערכת של שני חלקיקים עם אינטראקציה שתלויה רק במרחק ביניהם:
$ call = 1/2m1 dx1^2 + 1/2m2 dx2^2 - V(|vx1-vx2|) $
נסמן את המסה הכוללת $M=m1+m2$ ונגדיר:
$ vX = 1/M (m1 vx1 + m2 vx2), space.quad vx = vx2-vx1 $
])
#סעיף[
כתבו את הלגרנזי'אן בקואורדינטות החדשות.]
נמצא ראשית את $vx1$. נקבל מהגדרת $vx$ כי $vx2 = vx+vx1$ ואז:
$ vX = 1/M (m1 vx1 + m2 (vx+vx1)) = 1/M (vx1 (m1+m2) + vx2) = 1/M (M vx1 + m2 vx) = vx1 + m2/M vx => \ vx1 = vX - m2/M vx $
נקבל מהגדרת $vx$:
$ vx2 = vx + vX - m2/M vx = vX + (1- m2/M)vx $
נשים לב כי:
$ 1-m2/M = (M-m2)/M = (cancel(m1)+m2-cancel(m2))/M = m1/M $
ואז:
$ vx2 = vX + m1/M vx $
נחשב את $לגר$:
$ dx1^2 = dX^2 - 2 m2/M dX dot dx + m2^2/M^2 dx^2 \
  dx2^2 = dX^2 + 2 m1/M dX dot dx + m1^2/M^2 dx^2 $
$
T = &1/2 m1 (dX^2 - 2 m2/M dX dot dx + m2^2/M^2 dx^2) + 1/2 m2 (dX^2 + 2 m1/M dX dot x + m1^2/M^2 dx^2) = \
&1/2 (m1 + m2)dX^2 cancel(-(m1 m2)/M dX dx + (m2 m1)/M dX dx) + 1/(2M^2)(m1 m2^2 + m2 m1^2)dx^2
 $
נגדיר את המסה המצומצמת $mu = (m1 m2)/M$ ואז:
$ (m1 m2^2 + m2 m1^2)/(2M^2) = 1/(2M)( (m1 m2)/M m2 + (m2 m1)/M m1) = mu/2 cancel((m2+m1)/M) = mu/2 $
$ T = 1/2 M dX^2 + mu/2 dx^2 $
$ V = V(|vx1-vx2|) = V(|vx2-vx1|) = V(|vx|) $
נקבל כי:
#תשובה[
$ call = T - V = 1/2 M dX^2 + 1/2 mu dx^2 - V(|vx|) $ <מסה>]
#סעיף[
מצאו קואורדינטה ציקלית והסבירו מהו הגודל השמור הנובע ממנה.]
#let pX = $p_X$
ב-$לגר$ לא מופיע $X$ לכן זו קואורדינטה ציקלית. נמצא את $pX$, התנע הצמוד ל-$X$:
$ pX = del(call, dX) = M dX $ <תנע>
ולפי משפט נטר, $pX$ קבוע.
#תשובה[
הפוטנציאל במערכת תלוי רק במרחק בין הגופים, לכן התנע (הקווי) של המערכת כולה, $M dX$, נשמר, והמערכת סימטרית להזזה של המערכת כולה.]


#שאלה(כותרת: "חלקיק במעבר בין שני פוטנציאלים", [
חלקיק עם מסה $m$ הנע במהירות $vv1$ עוזב חצי מרחב בו הפוטנציאל קבוע וערכו $U1$ ועובר לחצי השני בו הפוטנציאל קבוע אך בעל ערך שונה, $U2$.
#figure(
  image("graph2.svg", width: 80%)
, caption: [חלקיק במעבר בין שני פוטנציאלים])
])
#סעיף[באיזה כיוון יש שימור תנע קווי?]

נסמן את הקו המפריד בין חצאי המרחב ב-$a$ ונגדיר את הפוטנציאל במרחב כפונקציית מקרים:
$ U(x,y) = cases(U1 "if" x < a, U2 "if" x > a) $
ברור כי $del(U,y)=0$ וגם $del(T,y)=0$. כלומר, $call=T-U$ לא תלוי ב-$y$, לכן זו קואורדינטה ציקלית. אזי:
#תשובה[
$y$
היא קואורדינטה ציקלית, לכן לפי משפט נטר, התנע הקווי בכיוון האנכי נשמר:
$ (dif p_y)/(dif t) = 0 $]

#let t1 = $theta_1$
#let t2 = $theta_2$
#סעיף[
סמנו ב-$t1$ וב-$t2$ את הזוויות בין המישור בו מתחלפים הפוטנציאל והמהירויות $v1$ ו-$v2$ בהתאמה. בעזרת שימור התנע מסעיף א' מצאו קשר בין הזוויות שתלוי ב-$v1$ וב-$v2$.]
בסעיף א' קיבלנו כי התנע בכיוון האנכי נשמר. נניח שמסת החלקיק נשארת קבועה ואז:
$ v1 sin t1 = v2 sin t2 $
נחלק ונקבל:
#תשובה[
$ (sin t1) / (sin t2) = v2/v1 $]

#סעיף[
בעזרת שימור אנרגיה, כתבו ביטוי עבור $(sin t1) / (sin t2)$ כפונקציה של $U1,U2, v2$ ו-$m$.]
אנרגיית החלקיק היא סכום האנרגיות הקינטית והפוטנציאלית. האנרגיה הכוללת נשמרת בין שני חצאי המרחב, כלומר:
$ T_1 + U1 = T_2 + U2 \
1/2 m v1^2 + U1 = 1/2 m v2^2 + U2 \
v1 = sqrt(v2^2 + 2/m (U2 - U1)) \
 $
נקבל כי:
#תשובה[
$ (sin t1) / (sin t2) = v2 / sqrt(v2^2 + 2/m (U2 - U1)) $]


#שאלה(כותרת: "מסלולים של פוטנציאל דוחה", [עבור בעיית קפלר הנחנו פוטנציאל מושך ומצאנו משוואה המקשרת בין $r$ ו-$theta$.])
#סעיף[
הניחו פוטנציאל מהצורה $V(r)=alpha/r$ עבור $alpha>0$ וחזרו על הפיתוח מהכיתה עבור פוטנציאל זה.]
#let vf = $V_"eff"$
נסמן את הלגרנז'יאן במערכת:
$ call = 1/2 m1 dx1^2 + 1/2 m2 dx^2 - V(|vx2-vx1|) $
נגדיר את מיקום מרכז המסה ב-$vX$, המרחק בין המסות ב-$vx$, סכום המסות ב-$M$, ואת המסה המצומצמת ב-$mu$ כך:
$ vx = x2-x1, space.quad mu = (m1 m2)/(m1 + m2) $
נקבל מ@מסה את $לגר$:
$ call = T - V = 1/2 M dX^2 + 1/2 mu dx^2 - V(|vx|) $

כפי שקיבלנו ב@תנע, מרכז המסה של המערכת נשמר, לכן $1/2 M dX^2$  הוא קבוע ונתעלם ממנו בלגרנז'יאן:
$ call = 1/2 mu dx^2 - V(|vx|) $
הכוח הפועל על כל גוף הוא:
$ F = -del(V(vx),x) = -(dif V)/(dif x) vx $
$לגר$ אינווריאנטי לסיבובים. ממשפט נטר נקבל כי התנע הזוויתי נשמר:
$ arrow(L) := vx times arrow(P) = "const" $
כיוון $arrow(L)$ גם הוא קבוע, לכן התנועה כולה מתבצעת במישור, ונגדיר את כיוון ציר $hat(z)$ בכיוון הנורמל למישור זה (כיוון $arrow(L)$). נעבור לקואורדינטות מעגליות ונקבל:
#let dr = $dot(r)$
$ call = 1/2 mu(dr^2 + r^2 dot(phi)^2) - V(r) $
$phi$
קואורדינטה ציקלית, לכן:
$ L_z = del(L, dot(phi)) = mu r^2 dot(phi) $
נחלץ את $dot(phi)$:
$ dot(phi) = L_z/(mu r^2) $ <דפ>

בנוסף, $del(call,t) = 0$, לכן לפי משפט נטר האנרגיה נשמרת, ונסמנה:
$ E = 1/2 mu(dr^2 + r^2 dot(phi)^2) + V(r) = 1/2 mu dr^2 + vf(r) = "const" $ <אנרגיה>
כאשר את הפוטנציאל האפקטיבי סימנו ב-$vf$ שגודלו:
$ vf = 1/2 mu r^2 dot(phi)^2 + V(r) = 1/2 mu r^2 L_z^2/(mu^2 r^4) + alpha/r =
 L_z^2 / (2 mu r^2) + alpha/r $ <ופ>

נקבל מ@אנרגיה ביטוי עבור $dif t$:
$ dif r = sqrt(2/mu (E - vf(r))) space.quad slash dot dif t $
$ (dif r) /sqrt(2/mu (E - vf(r))) = dif t $
מ@דפ נקבל:
$ dot(phi) = (dif phi)/(dif t) = L_z/(mu r^2) => dif phi = L_z / (mu r^2) dif t = L_z / (mu r^2) dot (dif r) /sqrt(2/mu (E - vf(r))) = L_z/r^2 (dif r)/sqrt(2 mu (E-vf(r))) $
נבצע אינטגרציה על שני האגפים מ-$t_0$ ל-$t$ ונקבל:
$ phi(t) - phi(t_0) = integral_(r(t_0))^r(t) (L_z dif r)/(r^2 sqrt(2 mu (E-vf(r)))) $

נסמן $u = 1/r$, ואז:
$ dif u = -1/r^2 dif r => (dif r)/r^2 = -dif u $
נבטא את $vf$ עם המשתנה החדש. לפי @ופ:
$ vf(r) = L_z^2 / (2 mu r^2) + alpha/r => vf(u) = L_z^2/(2mu) u^2 + alpha u $

נחליף את המשתנה באינטגרל ונקבל:
$ phi - phi_0 = integral -(L_z dif u)/sqrt(2 mu (E-vf(u))) $
נסדר את הביטוי בתוך השורש:
$ 2 mu (E-vf(u)) =& 2mu E-2 mu (L_z^2/(2mu) u^2 + alpha u) = \ &2mu E - L_z^2u^2 - 2 mu alpha u = L_z^2((2 mu E)/L_z^2 - (2mu alpha)/L_z^2 u - u^2) $
נמשיך לסדר את הביטוי באמצעות השלמה לריבוע:
$ B = (2 mu alpha)/L_z^2, C = (2 mu E)/L_z^2 =>  -u^2 - B u = &-(u^2 + B u + B^2/4 - B^2/4) = -((u + B/2)^2 - (B/2)^2) =\ & (B/2)^2 -(u + B/2)^2 => (2 mu E)/L_z^2 - (2mu alpha)/L_z^2 u - u^2 = (2 mu E)/L_z^2 + ((mu alpha)/L_z^2)^2 - (u +(mu alpha)/L_z^2)^2 $
נסמן קבוע נוסף, $Lambda^2$, להיות הקבוע בביטוי הקודם:
$ Lambda^2 = (2 mu E)/L_z^2 + ((mu alpha)/L_z^2)^2 = ((mu alpha)/L_z^2)^2(1+(2 E L_z^2)/(mu alpha^2)) $
נציב באינטגרל:
$ phi - phi_0 = integral (-L_z dif u)/sqrt(2 mu (E-vf(u))) = integral (-L_z dif u)/(L_z sqrt(Lambda^2-(u +(mu alpha)/L_z^2)^2)) $
זהו אינטרגל מיידי של $arccos$:
$ phi - phi_0 = arccos((u + (mu alpha)/L_z^2) slash Lambda) $
מכאן נקבל:
$ cos(phi-phi_0) = (u + (mu alpha)/L_z^2) slash Lambda => u = -(mu alpha)/L_z^2 + Lambda cos(phi-phi_0) $
נסמן:
$ P = L_z^2/(mu alpha), e = P Lambda = sqrt(1+ (2 E L_z^2)/(mu alpha^2)) $ <אי>
נחליף חזרה $u = 1 slash r$ ונקבל:
#תשובה[
$ P/r = -1 + e cos(phi-phi_0) $]
#סעיף[
זכרו כי $r$ מוגדר כך שהוא תמיד חיובי. איזה תנאי זה גורר על האקסצנטריות $e$? האם מקבלים מסלולים סגורים בפוטנציאל זה?]
נזכור כי $r,alpha>0$ ולכן $V>0$ לכל $r$. כלומר, הפוטניצאל דוחה במקום מושך בבעיית שני הגופים הקלאסית.
האנרגיה הקינטית חיובית תמיד וכך גם הפוטנציאלית, לכן האנרגיה הכוללת תמיד חיובית. לכן מ@אי נקבל:
$ e = sqrt(1+ (2 E L_z^2)/(mu alpha^2)) > sqrt(1+0) = 1 $
#תשובה[
התנאי על האקסצנטריות הוא $e > 1$, כלומר כל המסלולים האפשריים הם היפרבוליים, לכן אין מסלולים סגורים בפוטנציאל זה.]


#שאלה(כותרת: "פיזור מפוטנציאל", [
נתון פוטנציאל: 
$ V = alpha/r^2, alpha>0 $
])
#סעיף[
מצאו את זווית הפיזור של חלקיק עם מסה $m$ ואנרגיה $1/2 m v_0^2$ כפונקציה של פרמטר הפגיעה $b$.]
ראינו בתרגול כי:
$ phi = integral_(r_min)^infinity (l dif r)/(r^2 sqrt(2 m l eps - V(r) - (l^2)/(2 m r^2))) $
נציב $V(r)=alpha/r^2,eps=1/2 m v_0^2, l=m v_0 b$ ונקבל:
#let v0 = $v_0$
#let mv0 = $m v0$
$ phi = integral_(r_min)^infinity (mv0 b dif r)/(r^2 sqrt(m^2v0^2- (2m alpha)/r^2 - (m^2b^2v_0^2)/r^2)) =  
integral_(r_min)^infinity (b dif r)/(r^2 sqrt(1-1/r^2(b^2+(2 alpha)/(m v_0^2))) $
נבצע החלפת משתנים:
$ u = 1/r, dif u = -1/r^2 \
  r -> inf => u = 0, space.en r = r_min -> u = u_max => $

$ phi = integral_0^u_max (b dif u)/sqrt(1-u^2(b^2+(2 alpha)/(mv0))) $
נסמן 
$c^2 = b^2+(2 alpha) slash mv0$. 
נמצא את $u_max$. $r_min$ מתקבל כאשר מהירות החלקיק מתאפסת ויש לו רק אנרגיה פוטנציאלית. בביטוי שלנו זה מתרחש כאשר המכנה מתאפס, כלומר:
$ 1 - c^2 u^2 = 0 => u_max  =1/c $
נחשב את האינטגרל:
$ phi = b 1/c arcsin(c u)|_0^(1/c) = b/c (arcsin 1 - arcsin 0) = (pi b)/(2 c) $
לכן זווית הפיזור תהיה:
$ chi = pi - 2 phi = pi - (pi b)/c $
נציב את $c$ ונקבל:
#תשובה[
$ chi(b) = pi (1- b/sqrt(b^2+(2 alpha)/mv0)) $
]
#סעיף[
מצאו את חתך הפעולה הדיפרנציאלי
 $(dif sigma)/(dif Omega)$ של הפיזור.]

כפי שראינו בתרגול:
$ (dif sigma)/(dif Omega) = b/(sin chi) dot abs((dif b)/(dif chi)) = 1/(2 sin chi) abs((dif (b^2))/(dif chi)) $
נמצא חילוץ ל-$b(chi)$:
$ chi = pi(1- b/sqrt(1 + (2 alpha)/mv0 dot 1/b^2)) => pi/(pi-chi) = 
sqrt(1+(2 alpha)/mv0 1/b^2) $
$ pi^2/(pi-chi)^2 = 1 + (2 alpha)/mv0 1/b^2 => (pi^2 - (pi-chi)^2)/(pi-chi)^2 = (2 alpha)/mv0 1/b^2
 $
$ b^2(chi)=((pi-chi)^2 2alpha)/((2pi chi-chi^2)mv0) $

$ dif(b^2)/(dif chi) = &(2 alpha)/(mv0)((-2(pi-chi)(2pi chi-chi^2)-(2pi-2chi)(pi-chi^2))/(2pi chi-chi^2)^2)=\
& (2alpha)/mv0 (-2(pi-chi))((2pi chi - chi^2 + pi^2 - 2pi chi + chi^2)/(2pi chi - chi^2)^2) $
כעת נציב בנוסחה לחתך הפעולה:
#תשובה[
$ (dif sigma)/(dif Omega) =alpha/mv0 (2pi^2(pi-chi))/(sin (chi) chi^2(2pi - chi)^2) $
]

































