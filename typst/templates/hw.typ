#import "@preview/showybox:2.0.4": showybox
#import "@preview/physica:0.9.8": *

#import "../utils.typ": משל

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
  // show math.equation: set text(weight: 400) // Removed to allow bold in math
  set heading(numbering: "1.1")
  set math.equation(numbering: "(1)")

  show: super-T-as-transpose // Render "..^T" as transposed matrix
  show: super-plus-as-dagger // Render "..^+" as dagger

  show heading: none

  show ref: it => {
    let el = it.element
    if el != none and el.func() == heading {
      let loc = el.location()
      let num = counter(heading).at(loc)
      if el.level == 1 {
        link(loc, [שאלה #numbering("1", ..num)])
      } else if el.level == 2 {
        context {
          let curr = counter(heading).get()
          if curr.len() > 0 and curr.first() == num.first() {
            link(loc, [סעיף #numbering("1", num.last())])
          } else {
            link(loc, [שאלה #numbering("1", num.first()) סעיף #numbering("1", num.last())])
          }
        }
      } else {
        it
      }
    } else {
      it
    }
  }
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

#let שאלה(כותרת: "", מזהה: none, טקסט) = {
  pagebreak()
  [#heading(level: 1, supplement: [שאלה])[שאלה] #מזהה]

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
    {
      set math.equation(numbering: none)
      טקסט
    }
  )
}

#let סעיף(מזהה: none, טקסט) = {
  [#heading(level: 2, supplement: [סעיף])[סעיף] #מזהה]
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
    {
      set math.equation(numbering: none)
      טקסט
    }
  )
}

#let תשובה(טקסט) = {
  showybox[#טקסט #משל]
}
