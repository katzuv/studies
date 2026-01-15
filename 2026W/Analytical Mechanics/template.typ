#import "@preview/showybox:2.0.4": showybox

#let project(
  title: "",
  number: 0,
  authors: (),
  date: none,
  logo: none,
  body,
) = {
  // Set the document's basic properties.
  set document(author: authors.map(a => a.name), title: title)
  set text(font: "Noto Sans Hebrew", lang: "he")
  show math.equation: set text(weight: 400)
  set heading(numbering: "1.1")
  set math.equation(numbering: "(1)")
  show heading: none 
  // Title page.
  // The page can contain a logo if you pass one with `logo: "logo.png"`.
  v(0.6fr)
  if logo != none {
    align(right, image(logo, width: 26%))
  }
  v(9.6fr)

  text(2em, weight: 700, title)
  v(1.2em, weak: true)
  text(size: 1.5em)[גיליון #number #date.display(" [day]/[month]/[year]")]

  // Author information.
  pad(
    top: 0.7em,
    right: 0%,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1em,
      ..authors.map(author => align(start)[
        *#author.name* \
        #author.id \
        #author.email
      ]),
    ),
  )

  v(2.4fr)
  pagebreak()

  // Table of contents.
  show outline.entry: it => link(
    it.element.location(),
    block({
      it.element.body
      [ ]
      numbering(it.element.numbering, ..counter(it.element.func()).at(it.element.location()))
      box(width: 1fr, it.fill)
      [ ]
      it.page()
    })
  )
  outline(depth: 1)
  
  set page(numbering: "1", number-align: center)


  // Main body.
  set par(justify: true)

  body
}

#let שאלה(כותרת: "", טקסט) = {
  pagebreak()
  let text = טקסט
  heading[#כותרת – שאלה]

  let color = blue
  showybox(
    frame: (
      border-color: color.darken(50%),
      title-color: color.lighten(60%),
      body-color: color.lighten(80%)
    ),
    title-style: (
      color: black,
      weight: "regular",
      align: center
    ),
    shadow: (
      offset: 2pt,
    ),
    title: [שאלה #context counter(heading).display() – #כותרת],
    text
  )
}

#let סעיף(טקסט) = {
  let text = טקסט
  heading(level: 2)[סעיף]
  let color = green
  showybox(
    frame: (
      border-color: color.darken(50%),
      title-color: color.lighten(60%),
      body-color: color.lighten(80%)
    ),
    title-style: (
      color: black,
      weight: "regular",
      align: right
    ),
    shadow: (
      offset: 2pt,
    ),
    title: [סעיף #context counter(heading).display().at(-1)],
    text
  )
}

#let תשובה(טקסט) = {
  showybox[#טקסט]
}