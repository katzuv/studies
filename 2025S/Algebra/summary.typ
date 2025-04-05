#import "../../utils.typ": שם-מייל, הרצאה, innerp, Rn, Cn, Rnn, Cnn
#set text(lang: "he", dir: rtl)

#align(center)[= אלגברה 2מ 104038 -- סיכום קורס
== סמסטר אביב תשפ"ה
#שם-מייל]

#הרצאה(1, "30/03/2025", "https://web.goodnotes.com/s/SWHvZzqOHp21yQNfF3nLUN")

==== מכפלה סקלרית
#let av = math.arrow("a")
#let bv = math.arrow("b")
$ av = vec(a_1, a_2), bv = vec(b_1, b_2), a_a dot bv = a_1b_1 + a_2b_2  \
 av dot bv = (a_1)^2 + (a_2)^2 = ||av|| => ||av|| = sqrt(av dot av)
$
יש הגדרה אחרת: $av dot bv = ||av|| dot ||bv||cos(alpha)$ \
מכפלה סקלרית מוגדרת גם ב-$Rn$ לכל $n$: 
$av dot bv = sum_(j=1)^n a_j dot b_j$ \ \

==== מכפלה פנימית
יהי $V$ מרחב וקטורי (ממימד סופי). מכפלה פנימית ב-$V$ היא פונקציה $innerp(dot,dot): V times V -> bb(R)$.
כלומר, לכל $u, v$ קיימת $innerp(u,v) in bb(R)$ המקיימת:
1. *אי-שליליות "חזקה"*: לכל $u in V$, $innerp(u,u) >= 0$ אם"ם $u=arrow(0)$ (וקטור האפס).
2. *סימטריות*:
    $innerp(u,v)=innerp(v,u)$
3. *לינאריות ברכיב הראשון*:
    $innerp(alpha u + beta v, w) = alpha innerp(u, w) + beta innerp(v, w)$

4. לינאריות ברכיב השני נובעת מתכונות (2), (3).
מרחב וקטורי $V$ המצויד במכפלה פנימית $innerp(dot,dot)$ נראה #underline("מרחב מכפלה פנימית (ממ\"פ)").

עבור מטריצות ריבועיות:
$V = Rnn = M_n (bb(R)), dim(V) = n^2$.
    לכל $A, B in V$ נגדיר:
$ innerp(A, B) = sum_(i,j=1)^n a_(i j) b_"ij" = sum_(i=1)^n sum_(j=1)^n a $
בנוסף מתקיים:
$innerp(A,B) = tr(B^(t) A)$ \ \

תנאי מכפלה פנימית ב-$Cn$ הם כמו ב-$Rn$, למעט סימטריות עד כדי הצמדה:
$innerp(u,v) = overline(innerp(v,u))$ \ \

==== אפיון כל המכפלות הפנימיות ב-$Rn$ וב-$Cn$
$A in Rnn$
היא מטריצה #underline("מטריצה מוגדרת חיובית") אם היא סימטרית ($A^t=A$) ומתקיים:
$ x^T A x = x dot A x = innerp(x, A x) = sum_(i,j=1)^n a_(i j) x_i x_j >= 0 $
אי השוויון חד אלא אם $x = 0$. \ \ 

==== משפט: אפיון מכפלה פנימית ב-$Rn$
1. אם $A in Rnn$ מוגדרת חיובית, אז
    $innerp(x,y)_A: y^T A x = innerp(A x, y) = sum(i,j=1)^n a_(i j) x_i y_j$
2. אם $innerp(x,y)$ מכפלה פנימית ב-$Rn$ אז קיימת מטריצה מוגדרת חיובית $A$ כך ש: $innerp(x,y)=innerp(x,y)_A$.