= circle

A circle with optional content.

== Example

```typst
// Without content.
#circle(radius: 25pt)

// With content.
#circle[
  #set align(center + horizon)
  Automatically \
  sized to fit.
]
```

== Parameters

```
circle(
  radius: length,
  width: auto | relative,
  height: auto | relative | fraction,
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  body: none | content
) -> content
```

=== `radius`: length (Settable)

The circle's radius. This is mutually exclusive with `width` and `height`.

Default: `0pt`

=== `width`: auto | relative (Settable)

The circle's width. This is mutually exclusive with `radius` and `height`.

In contrast to `radius`, this can be relative to the parent container's width.

Default: `auto`

=== `height`: auto | relative | fraction (Settable)

The circle's height. This is mutually exclusive with `radius` and `width`.

In contrast to `radius`, this can be relative to the parent container's height.

Default: `auto`

=== `fill`: none | color | gradient | tiling (Settable)

How to fill the circle. See the #link("/docs/reference/visualize/rect/#parameters-fill")[rectangle's documentation] for more details.

Default: `none`

=== `stroke`: none | auto | length | color | gradient | stroke | tiling | dictionary (Settable)

How to stroke the circle. See the #link("/docs/reference/visualize/rect/#parameters-stroke")[rectangle's documentation] for more details.

Default: `auto`

=== `inset`: relative | dictionary (Settable)

How much to pad the circle's content. See the #link("/docs/reference/layout/box/#parameters-inset")[box's documentation] for more details.

Default: `0% + 5pt`

=== `outset`: relative | dictionary (Settable)

How much to expand the circle's size without affecting the layout. See the #link("/docs/reference/layout/box/#parameters-outset")[box's documentation] for more details.

Default: `(:)`

=== `body`: none | content (Positional, Settable)

The content to place into the circle. The circle expands to fit this content, keeping the 1-1 aspect ratio.

Default: `none`
