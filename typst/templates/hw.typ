#import "@preview/showybox:2.0.4": showybox
#import "@preview/physica:0.9.8": *

#import "../utils.typ": משל

// Helper to add geresh to single Hebrew letters (e.g., א -> א')
#let fix-geresh(s) = {
  let parts = s.split(".")
  let last = parts.last()
  if last.clusters().len() == 1 and last >= "א" and last <= "ת" {
    s + "'"
  } else {
    s
  }
}

#let project(
  title: "",
  number: 0,
  authors: (),
  date: none,
  logo: none,
  body,
) = {
  show "--": "–"
  // Set the document's basic properties.
  set document(author: authors.map(a => a.name), title: title + " – גיליון " + str(number))
  set text(font: ("Noto Sans Hebrew", "Noto Sans", "Noto Serif Hebrew", "David", "Arial"), lang: "he")

  show strong: set text(weight: 700)

  // show math.equation: set text(weight: 400) // Removed to allow bold in math
  set heading(numbering: "1.1")
  set math.equation(numbering: "(1)")

  show: super-T-as-transpose // Render "..^T" as transposed matrix
  show: super-plus-as-dagger // Render "..^+" as dagger

  show heading: none

  // Title page.
  // The page can contain a logo if you pass one with `logo: "logo.png"`.
  v(0.6fr)
  if logo != none {
    align(right, image(logo, width: 26%))
  }
  v(9.6fr)

  text(2em, weight: 700, title + " – גיליון " + str(number))
  v(1.2em, weak: true)
  text(size: 1.5em)[#date.display("[day]/[month]/[year]")]

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
  align(center)[#text(1.8em, weight: 700)[תוכן עניינים]]
  v(1.5em)

  show outline.entry: it => {
    show link: it => it
    let el = it.element
    if el.func() != heading { return it }

    let loc = el.location()
    let num-parts = counter(heading).at(loc)

    if el.level == 1 {
      let num = numbering(el.numbering, ..num-parts)
      let body = el.body
      let txt = [*שאלה #num*]
      if body != [] {
        txt = [*שאלה #num: #body*]
      }

      let entry = link(loc, block(width: 100%, {
        txt
        box(width: 1fr, it.fill)
        it.page()
      }))

      if num-parts.at(0, default: 0) > 1 {
        stack(dir: ttb, v(0.65em), entry)
      } else {
        entry
      }
    } else if el.level == 2 {
      let last-num = numbering("1", num-parts.last())
      link(loc, block({
        h(1.2em)
        [סעיף #last-num]
        box(width: 1fr, it.fill)
        it.page()
      }))
    } else {
      it
    }
  }
  outline(title: none, depth: 2)

  set page(
    numbering: "1",
    number-align: center,
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 0.9em, fill: gray.darken(30%))
        grid(
          columns: (1fr, 1fr),
          align(right, title + " – גיליון " + str(number)), align(left, authors.at(0).name),
        )
        v(-0.6em)
        line(length: 100%, stroke: 0.5pt + gray)
      }
    },
  )

  show link: underline.with(stroke: 0.6pt + gray.darken(20%), offset: 2pt)
  show ref: underline.with(stroke: 0.6pt + gray.darken(20%), offset: 2pt)

  show ref: it => {
    let el = it.element
    if el != none and el.func() == heading {
      let loc = el.location()
      let num = counter(heading).at(loc)
      let content = if el.level == 1 {
        [שאלה #numbering("1", ..num)]
      } else if el.level == 2 {
        context {
          let curr = counter(heading).get()
          if curr.len() > 0 and curr.first() == num.first() {
            [סעיף #numbering("1", num.last())]
          } else {
            [שאלה #numbering("1", num.first()) סעיף #numbering("1", num.last())]
          }
        }
      } else {
        it
      }
      underline(stroke: 0.6pt + gray.darken(20%), offset: 2pt, link(loc, content))
    } else {
      underline(stroke: 0.6pt + gray.darken(20%), offset: 2pt, it)
    }
  }

  // Main body.
  set par(justify: true)

  body
}

#let בולד(טקסט) = strong(טקסט)

#let frame-darken = 50%
#let title-lighten = 55%
#let body-lighten = 80%

#let smart-breakable(it) = context {
  let m = measure(it)
  if m.height < 24cm {
    block(breakable: false, width: 100%, it)
  } else {
    it
  }
}

#let שאלה(כותרת: "", מזהה: none, טקסט) = {
  pagebreak()
  [#heading(level: 1, supplement: [שאלה])[#כותרת] #מזהה]

  let color = rgb("#1a5fb4") // Deep Navy Blue
  
  // Split intro text from clauses
  let children = if טקסט.has("children") { טקסט.children } else { (טקסט,) }
  let idx = children.position(c => (c.func() == heading and c.level == 2) or (c.has("label") and str(c.label) == "is-clause"))
  
  let intro = if idx == none { טקסט } else { children.slice(0, idx).join() }
  let rest = if idx == none { [] } else { children.slice(idx).join() }

  smart-breakable(showybox(
    title-style: (
      boxed-style: (
        anchor: (x: center, y: horizon),
        radius: (top-right: 10pt, bottom-left: 10pt, rest: 0pt),
      ),
      color: rgb("#FFFFFF"),
      weight: 600,
      align: center,
    ),
    frame: (
      border-color: color.darken(frame-darken),
      title-color: rgb("#2e62da"),
      body-color: color.lighten(body-lighten),
    ),
    shadow: (
      offset: 2pt,
    ),
    title: context counter(heading).display((..nums) => {
      let n = nums.pos().at(0)
      [שאלה #n – #כותרת]
    }),
    intro
  ))

  rest
}

#let סעיף(מזהה: none, טקסט) = {
  [#metadata("is-clause") <is-clause>]
  [#heading(level: 2, supplement: [סעיף])[] #מזהה]
  let color = rgb("#26a269") // Deep Emerald Green
  smart-breakable(showybox(
    frame: (
      border-color: color.darken(frame-darken),
      title-color: color.lighten(title-lighten),
      body-color: color.lighten(body-lighten),
    ),
    title-style: (
      color: black,
      weight: "bold",
      align: right,
    ),
    shadow: (
      offset: 2pt,
    ),
    title: context counter(heading).display((..nums) => {
      let n = nums.pos().at(1, default: 1)
      [סעיף #n]
    }),
    {
      set math.equation(numbering: none)
      טקסט
    },
  ))
}

#let תשובה(טקסט) = {
  let color = rgb("#e66100") // Deep Vermilion (Orange-Red)
  smart-breakable(showybox(
    breakable: true, 
    title: [תשובה סופית],
    frame: (
      border-color: color.darken(frame-darken - 10%),
      title-color: color.lighten(title-lighten - 5%),
      body-color: color.lighten(body-lighten),
    ),
    title-style: (
      color: black,
      weight: "bold",
      align: right,
    ),
    [#טקסט #משל],
  ))
}
