#import "../../../utils.typ": גיליון
#set text(lang: "he", dir: rtl)

#גיליון("פיזיקה 2פ", "אביב תשפ\"ה", 1, "11/04/2025")
  #set align(right) 

== שאלה 1.3
=== סעיף a
התפלגות המטען בחרוט אחידה. הכוח החשמלי בין $q$ לכל מטען אינפיניטיסמלי בחרוט (נסמן זאת $d q$) הוא בכיוון הווקטור המחבר ביניהם. מכיוון שגודל המטען של כל $d q$ בחרוט זהה, ומשיקולי סימטריה, שקול הכוח האופקי על $q$ הוא אפס -- לכל מטען יש מטען בצד השני של החרוט שמבטלים את רכיבי הכוחות האופקיים זה של זה. לכן, שקול הכוח על $q$ הוא אופקית מעלה.

נחשב את גודל הכוח השקול על $q$. ניקח דיסקה עגולה דקה שהיא חתך החרוט במרחק $x$ מהמטען $q$. רדיוס דסקה זו הוא $x sin theta$, לכן מטענה בסך הכל הוא:
$ Q_x = d q dot "היקף" = 2 pi sigma x sin theta space d x $
נחשב את הכוח שמפעילה הדסקה על $q$. כזכור, ניקח רק את הרכיב האנכי של הכוח, כלומר נכפיל את הכוח ב-$cos theta$ ונקבל:
$ F_x = k_e (q dot 2 pi sigma x sin theta cos theta space d x) / x^2 =_(sin theta cos theta = sin(2theta)/2) k_e (q dot pi sigma x sin(2theta) space d x) / x^2 $
נחשב אינטגרל על כלל החרוט, ממרחק $0$ למרחק $L$ כדי למצוא את הכוח הכולל על $q$:
$ F_"tot" = integral_0^L k_e (q dot pi sigma x sin(2theta)) / x^2 d x =
k_e q 2 pi sigma sin(2theta) integral_0^L  1 / x d x = \
k_e = 2 pi sigma k_e q sin(2theta) space [ln x]_0^L =
2 pi sigma k_e q sin(2theta) (ln L - ln 0) $
משום ש-
    $(-ln 0) -> infinity$
אנחנו מקבלים שהכוח מתבדר לאינסוף.

=== סעיף b
נחשב את אותו אינטגרל אך מ-$L/2$ ל-$L$:
$ F_"tot" = 2 pi sigma k_e q sin(2theta) space [ln x]_(L/2)^L = 
2 pi sigma k_e q sin(2theta) (ln L - ln L/2) = 
2 pi sigma k_e q sin(2theta) ln 2 $
מכאן רואים שהכוח יהיה מקסימלי כאשר $sin(2theta)$ מקסימלי, כלומר כאשר
    $ 2theta = 90 deg => theta = 45 deg$.