= overline

Adds a line over text.

== Example

```typst
#overline[A line over text.]
```

== Parameters

```
overline(
  stroke: auto | length | color | gradient | stroke | tiling | dictionary,
  offset: auto | length,
  extent: length,
  evade: bool,
  background: bool,
  content: content
) -> content
```

=== `stroke`: auto | length | color | gradient | stroke | tiling | dictionary (Settable)

How to #link("/docs/reference/visualize/stroke/")[stroke] the line.

If set to `auto`, takes on the text's color and a thickness defined in the current font.

Default: `auto`

*Example:*
```typst
#set text(fill: olive)
#overline(
  stroke: green.darken(20%),
  offset: -12pt,
  [The Forest Theme],
)
```

=== `offset`: auto | length (Settable)

The position of the line relative to the baseline. Read from the font tables if `auto`.

Default: `auto`

*Example:*
```typst
#overline(offset: -1.2em)[
  The Tale Of A Faraway Line II
]
```

=== `extent`: length (Settable)

The amount by which to extend the line beyond (or within if negative) the content.

Default: `0pt`

*Example:*
```typst
#set overline(extent: 4pt)
#set underline(extent: 4pt)
#overline(underline[Typography Today])
```

=== `evade`: bool (Settable)

Whether the line skips sections in which it would collide with the glyphs.

Default: `true`

*Example:*
```typst
#overline(
  evade: false,
  offset: -7.5pt,
  stroke: 1pt,
  extent: 3pt,
  [Temple],
)
```

=== `background`: bool (Settable)

Whether the line is placed behind the content it overlines.

Default: `false`

*Example:*
```typst
#set overline(stroke: (thickness: 1em, paint: maroon, cap: "round"))
#overline(background: true)[This is stylized.] \
#overline(background: false)[This is partially hidden.]
```

=== `body`: content (Required, Positional)

The content to add a line over.
