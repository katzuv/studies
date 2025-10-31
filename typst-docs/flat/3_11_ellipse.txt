= ellipse

An ellipse with optional content.

== Example

```typst
// Without content.
#ellipse(width: 35%, height: 30pt)

// With content.
#ellipse[
  #set align(center)
  Automatically sized \
  to fit the content.
]
```

== Parameters

```
ellipse(
  width: auto | relative,
  height: auto | relative | fraction,
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  body: none | content
) -> content
```

=== `width`: auto | relative (Settable)

The ellipse's width, relative to its parent container.

Default: `auto`

=== `height`: auto | relative | fraction (Settable)

The ellipse's height, relative to its parent container.

Default: `auto`

=== `fill`: none | color | gradient | tiling (Settable)

How to fill the ellipse. See the #link("/docs/reference/visualize/rect/#parameters-fill")[rectangle's documentation] for more details.

Default: `none`

=== `stroke`: none | auto | length | color | gradient | stroke | tiling | dictionary (Settable)

How to stroke the ellipse. See the #link("/docs/reference/visualize/rect/#parameters-stroke")[rectangle's documentation] for more details.

Default: `auto`

=== `inset`: relative | dictionary (Settable)

How much to pad the ellipse's content. See the #link("/docs/reference/layout/box/#parameters-inset")[box's documentation] for more details.

Default: `0% + 5pt`

=== `outset`: relative | dictionary (Settable)

How much to expand the ellipse's size without affecting the layout. See the #link("/docs/reference/layout/box/#parameters-outset")[box's documentation] for more details.

Default: `(:)`

=== `body`: none | content (Positional, Settable)

The content to place into the ellipse.

When this is omitted, the ellipse takes on a default size of at most `45pt` by `30pt`.

Default: `none`
