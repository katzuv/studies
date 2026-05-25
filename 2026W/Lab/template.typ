// The project function defines how your document looks.
// It takes your content and some metadata and formats it.
// Go ahead and customize it to your liking!
#let project(
  experiment_name: "",
  report_title: "",
  abstract: [],
  authors: (),
  date: none,
  logo: none,
  body,
) = {
  // Set the document's basic properties.
  set text(lang: "he", font: "Noto Sans Hebrew")
  set math.equation(numbering: "(1)")
  let name = [ניסוי #experiment_name]
  set document(author: authors.map(a => a.name), title: name)
  show math.equation: set text(weight: 400)
  set heading(numbering: "1.1")
//   show ref: it => {
//   underline(link(it.target, it))
// }

  let typst_evangelist(body) = {
    footnote(numbering: _ => [])[#body]
    counter(footnote).update(n => n - 1)
  }
  typst_evangelist[דו"ח זה נכתב ב-#link("https://typst.app/")[#underline[Typst]], שפה לכתיבת מסמכים. ניתן לראות את קוד המקור #link("https://typst.app/project/ryNVs59Kpm1qxphJr4NmSd")[#underline[כאן]].]

  // Title page.
  // The page can contain a logo if you pass one with `logo: "logo.png"`.
  v(0.6fr)
  if logo != none {
    align(right, image(logo, width: 26%))
  }
  v(9.6fr)

  v(1.2em, weak: true)
  text(2em, weight: 700, name)
  text(size: 1.5em)[ #date.display(" [day]/[month]/[year]")]
  linebreak()
  linebreak()
  text(1.2em, "מדריך: אברהם איתן")
  linebreak()
  text(0.95em, "קבוצה 2, עמדה 2")

  // Author information.
  pad(
    top: 0.7em,
    right: 0%,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter:1em,
      ..authors.map(author => align(start)[
        *#author.name* #author.id \
        // #link("mailto:#author.mail")[#author.email]
        #author.email
      ]),
    ),
  )

  v(2.4fr)
  pagebreak()

  title(report_title)
  
  // Abstract page.
    align(center)[
    #heading(
      outlined: false,
      numbering: none,
      text(0.85em, "תקציר"),
    )
    #abstract
  ]
  v(6em, weak: true)

  // Table of contents.
  outline(depth: 2, indent: auto)
  pagebreak()
  set page(numbering: "1", number-align: center)


  // Main body.
  set par(justify: true)

  body
}