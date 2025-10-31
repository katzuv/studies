= target

Returns the current export target.

This function returns either

- `"paged"` (for PDF, PNG, and SVG export), or
- `"html"` (for HTML export).

The design of this function is not yet finalized and for this reason it is guarded behind the `html` feature. Visit the #link("/docs/reference/html/")[HTML documentation page] for more details.

== When to use it

This function allows you to format your document properly across both HTML and paged export targets. It should primarily be used in templates and show rules, rather than directly in content. This way, the document's contents can be fully agnostic to the export target and content can be shared between PDF and HTML export.

== Varying targets

This function is #link("/docs/reference/context/")[contextual] as the target can vary within a single compilation: When exporting to HTML, the target will be `"paged"` while within an #link("/docs/reference/html/frame/")[html.frame].

== Example

```typst
#let kbd(it) = context {
  if target() == "html" {
    html.elem("kbd", it)
  } else {
    set text(fill: rgb("#1f2328"))
    let r = 3pt
    box(
      fill: rgb("#f6f8fa"),
      stroke: rgb("#d1d9e0b3"),
      outset: (y: r),
      inset: (x: r),
      radius: r,
      raw(it)
    )
  }
}

Press #kbd("F1") for help.
```

== Parameters

```
target(
  
) -> str
```
