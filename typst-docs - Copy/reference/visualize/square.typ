= square

A square with optional content.

== Example

```typst
// Without content.
#square(size: 40pt)

// With content.
#square[
  Automatically \
  sized to fit.
]
```

== Parameters

```
square(
  size: auto | length,
  width: auto | relative,
  height: auto | relative | fraction,
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  radius: relative | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  body: none | content
) -> content
```

=== `size`: auto | length (Settable)

The square's side length. This is mutually exclusive with `width` and `height`.

Default: `auto`

=== `width`: auto | relative (Settable)

The square's width. This is mutually exclusive with `size` and `height`.

In contrast to `size`, this can be relative to the parent container's width.

Default: `auto`

=== `height`: auto | relative | fraction (Settable)

The square's height. This is mutually exclusive with `size` and `width`.

In contrast to `size`, this can be relative to the parent container's height.

Default: `auto`

=== `fill`: none | color | gradient | tiling (Settable)

How to fill the square. See the #link("/docs/reference/visualize/rect/#parameters-fill")[rectangle's documentation] for more details.

Default: `none`

=== `stroke`: none | auto | length | color | gradient | stroke | tiling | dictionary (Settable)

How to stroke the square. See the #link("/docs/reference/visualize/rect/#parameters-stroke")[rectangle's documentation] for more details.

Default: `auto`

=== `radius`: relative | dictionary (Settable)

How much to round the square's corners. See the #link("/docs/reference/visualize/rect/#parameters-radius")[rectangle's documentation] for more details.

Default: `(:)`

=== `inset`: relative | dictionary (Settable)

How much to pad the square's content. See the #link("/docs/reference/layout/box/#parameters-inset")[box's documentation] for more details.

Default: `0% + 5pt`

=== `outset`: relative | dictionary (Settable)

How much to expand the square's size without affecting the layout. See the #link("/docs/reference/layout/box/#parameters-outset")[box's documentation] for more details.

Default: `(:)`

=== `body`: none | content (Positional, Settable)

The content to place into the square. The square expands to fit this content, keeping the 1-1 aspect ratio.

When this is omitted, the square takes on a default size of at most `30pt`.

Default: `none`
