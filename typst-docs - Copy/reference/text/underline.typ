= underline

Underlines text.

== Example

```typst
This is #underline[important].
```

== Parameters

```
underline(
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
Take #underline(
  stroke: 1.5pt + red,
  offset: 2pt,
  [care],
)
```

=== `offset`: auto | length (Settable)

The position of the line relative to the baseline, read from the font tables if `auto`.

Default: `auto`

*Example:*
```typst
#underline(offset: 5pt)[
  The Tale Of A Faraway Line I
]
```

=== `extent`: length (Settable)

The amount by which to extend the line beyond (or within if negative) the content.

Default: `0pt`

*Example:*
```typst
#align(center,
  underline(extent: 2pt)[Chapter 1]
)
```

=== `evade`: bool (Settable)

Whether the line skips sections in which it would collide with the glyphs.

Default: `true`

*Example:*
```typst
This #underline(evade: true)[is great].
This #underline(evade: false)[is less great].
```

=== `background`: bool (Settable)

Whether the line is placed behind the content it underlines.

Default: `false`

*Example:*
```typst
#set underline(stroke: (thickness: 1em, paint: maroon, cap: "round"))
#underline(background: true)[This is stylized.] \
#underline(background: false)[This is partially hidden.]
```

=== `body`: content (Required, Positional)

The content to underline.
