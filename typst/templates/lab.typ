#import "@preview/showybox:2.0.4": showybox
#import "@preview/physica:0.9.8": *

#import "../utils.typ": codly-setup, equation-setup, משל, typst_evangelist
#import "../consts.typ": *

#let project(
  experiment_name,
  instructor,
  course_name,
  experiment_id: "",
  report_title: "",
  abstract: [],
  authors: (),
  date: none,
  logo: none,
  lab_info: "מעבדה 4מח 114037 – מעבדה 331, מסלול 1",
  bibliography_file: none,
  scientific_theme: false,
  body,
) = {
  show "--": "–"
  // Set the document's basic properties.
  let doc_title = if experiment_id != "" [#experiment_id: #experiment_name] else [#experiment_name]
  set document(author: authors.map(a => a.name), title: doc_title)

  // Font stack: Consistent Sans-serif as per user preference
  let main_font = ("Noto Sans Hebrew", "Noto Sans", "Arial", "David")

  set text(font: main_font, lang: "he")
  show heading: set text(font: main_font)

  show strong: set text(weight: 700)
  set heading(numbering: "1.1")
  // math equation numbering set via equation-setup

  show: super-T-as-transpose // Render "..^T" as transposed matrix
  show: super-plus-as-dagger // Render "..^+" as dagger

  // Style links and references
  show link: underline.with(stroke: 0.6pt + gray.darken(20%), offset: 2pt)
  show ref: underline.with(stroke: 0.6pt + gray.darken(20%), offset: 2pt)

  // Table styling: Captions at the top
  show figure.where(kind: table): set figure.caption(position: top)

  // Layout settings
  let margin_settings = (right: 2.5cm, left: 2.5cm, top: 2.5cm, bottom: 2.5cm)

  set page(
    margin: margin_settings,
    numbering: "1",
    number-align: center,
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 0.9em, fill: gray.darken(30%))
        grid(
          columns: (1fr, 1fr),
          align(right, course_name), align(left, experiment_name),
        )
        v(-0.6em)
        line(length: 100%, stroke: 0.5pt + gray)
      }
    },
  )

  // Typst credit footnote

  // Title page.
  v(4fr) // Significantly lower the title
  if logo != none {
    align(right, image(logo, width: 26%))
  }
  v(6.2fr)

  v(1.2em, weak: true)
  text(3.5em, weight: 700, experiment_name)

  v(0em)

  if date != none {
    text(size: 1.8em)[תאריך הניסוי: #date.display("[day]/[month]/[year]")]
  }

  v(1em)
  text(1.4em)[#instructor]
  linebreak()
  v(0.2em)
  text(1.1em, lab_info)

  // Author information.
  pad(
    top: 0.8em,
    right: 0%,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1.5em,
      ..authors.map(author => align(start)[
        #text(1.2em)[*#author.name*] \
        #text(1.1em)[#author.id] \
        #text(1.1em)[#author.email]
      ]),
    ),
  )

  v(2.4fr)
  typst_evangelist()
  pagebreak()

  // Abstract & Title
  if report_title != "" {
    align(center)[#text(2em, weight: 700, report_title)]
    v(1.5em)
  }

  if abstract != [] {
    align(center)[
      #heading(
        outlined: false,
        numbering: none,
        text(1em, "תקציר"),
      )
      #abstract
    ]
    v(3em)
  }

  pagebreak()

  // Main body.
  set par(justify: true)
  show: codly-setup
  show: equation-setup

  body

  // Bibliography
  if bibliography_file != none {
    pagebreak()
    bibliography(bibliography_file, full: true)
  }
}

// --- Common Utilities ---

#let בולד(טקסט) = strong(טקסט)

#let smart-breakable(it) = context {
  let m = measure(it)
  if m.height < 24cm {
    block(breakable: false, width: 100%, it)
  } else {
    it
  }
}

// Callout box helper
#let callout(title: none, color: blue, body) = {
  showybox(
    title: title,
    frame: (
      border-color: color.darken(20%),
      title-color: color.lighten(80%),
      body-color: color.lighten(95%),
      thickness: 1pt,
      radius: 4pt,
    ),
    title-style: (
      color: black,
      weight: "bold",
    ),
    body,
  )
}
#let דגש = callout

// --- Physics & Math Aliases ---

#let פמ = $plus.minus$
#let pm = $plus.minus$

// Measurement formatter: (value ± error) unit
#let qty(val, err, u) = $lr((#val פמ #err)) #u$
#let כמות = qty

// Time derivatives
#let dx = $dot(x)$
#let ddx = $accent(x, diaer)$
#let dy = $dot(y)$
#let ddy = $accent(y, diaer)$
#let dth = $dot(theta)$
#let ddth = $accent(theta, diaer)$

// Greek letters as Hebrew names
#let או = $omega$
#let או0 = $omega_0$
#let אומ = $omega_m$
#let פי = $phi$
#let תטא = $theta$
#let אלפא = $alpha$
#let למדא = $lambda$

// Sets
#let NN = $bb(N)$
#let RR = $bb(R)$

// Units (upright in math mode)
#let nm = $"nm"$
#let um = $upright(mu m)$
#let mm = $"mm"$
#let cm = $"cm"$
#let mps = $"m/s"$
#let ev = "eV"
#let Hz = $"Hz"$
#let mHz = $"mHz"$
#let rad = $"rad"$
#let sec = $"sec"$
#let Pa = $"Pa"$
#let torr = $"torr"$
#let מעלה = $degree$

// --- Structural Helpers ---

// Appendix helper
#let נספח(title, body) = {
  pagebreak()
  [#heading(level: 1, numbering: none)[נספח: #title] <נספח>]
  body
}

// Subfigures helper (side-by-side images)
#let subfigures(..figs, columns: 2, gutter: 1em, caption: none) = {
  figure(
    grid(
      columns: (1fr,) * columns,
      gutter: gutter,
      ..figs
    ),
    caption: caption,
  )
}

// Table of constants helper
#let table-from-file(..args) = {
  let constants = json(..args)
  table(
    columns: (3.5fr, 1.2fr, 2.5fr),
    align: center + horizon,
    stroke: 0.5pt,
    fill: (col, row) => if row == 0 { luma(240) } else { white },
    [*שם הקבוע*], [*סימון*], [*ערך מחושב*],
    ..constants
      .map(c => (
        align(
          right,
          if c.units != "" [
            #c.hebrew_name [#text(dir: ltr)[#eval(c.units, mode: "math", scope: (dd: dd, sec: sec))]]
          ] else [
            #c.hebrew_name
          ],
        ),
        eval(c.symbol, mode: "math", scope: (dd: dd, sec: sec)),
        eval(c.formatted_value, mode: "math", scope: (dd: dd, sec: sec, pm: pm)),
      ))
      .flatten(),
  )
}
