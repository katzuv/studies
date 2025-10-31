= box

An inline-level container that sizes content.

All elements except inline math, text, and boxes are block-level and cannot occur inside of a #link("/docs/reference/model/par/")[paragraph]. The box function can be used to integrate such elements into a paragraph. Boxes take the size of their contents by default but can also be sized explicitly.

== Example

```typst
Refer to the docs
#box(
  height: 9pt,
  image("docs.svg")
)
for more information.
```

== Parameters

```
box(
  width: auto | relative | fraction,
  height: auto | relative,
  baseline: relative,
  fill: none | color | gradient | tiling,
  stroke: none | length | color | gradient | stroke | tiling | dictionary,
  radius: relative | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  clip: bool,
  body: none | content
) -> content
```

=== `width`: auto | relative | fraction (Settable)

The width of the box.

Boxes can have #link("/docs/reference/layout/fraction/")[fractional] widths, as the example below demonstrates.

_Note:_ Currently, only boxes and only their widths might be fractionally sized within paragraphs. Support for fractionally sized images, shapes, and more might be added in the future.

Default: `auto`

*Example:*
```typst
Line in #box(width: 1fr, line(length: 100%)) between.
```

=== `height`: auto | relative (Settable)

The height of the box.

Default: `auto`

=== `baseline`: relative (Settable)

An amount to shift the box's baseline by.

Default: `0% + 0pt`

*Example:*
```typst
Image: #box(baseline: 40%, image("tiger.jpg", width: 2cm)).
```

=== `fill`: none | color | gradient | tiling (Settable)

The box's background color. See the #link("/docs/reference/visualize/rect/#parameters-fill")[rectangle's documentation] for more details.

Default: `none`

=== `stroke`: none | length | color | gradient | stroke | tiling | dictionary (Settable)

The box's border color. See the #link("/docs/reference/visualize/rect/#parameters-stroke")[rectangle's documentation] for more details.

Default: `(:)`

=== `radius`: relative | dictionary (Settable)

How much to round the box's corners. See the #link("/docs/reference/visualize/rect/#parameters-radius")[rectangle's documentation] for more details.

Default: `(:)`

=== `inset`: relative | dictionary (Settable)

How much to pad the box's content.

_Note:_ When the box contains text, its exact size depends on the current #link("/docs/reference/text/text/#parameters-top-edge")[text edges].

Default: `(:)`

*Example:*
```typst
#rect(inset: 0pt)[Tight]
```

=== `outset`: relative | dictionary (Settable)

How much to expand the box's size without affecting the layout.

This is useful to prevent padding from affecting line layout. For a generalized version of the example below, see the documentation for the #link("/docs/reference/text/raw/#parameters-block")[raw text's block parameter].

Default: `(:)`

*Example:*
```typst
An inline
#box(
  fill: luma(235),
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)[rectangle].
```

=== `clip`: bool (Settable)

Whether to clip the content inside the box.

Clipping is useful when the box's content is larger than the box itself, as any content that exceeds the box's bounds will be hidden.

Default: `false`

*Example:*
```typst
#box(
  width: 50pt,
  height: 50pt,
  clip: true,
  image("tiger.jpg", width: 100pt, height: 100pt)
)
```

=== `body`: none | content (Positional, Settable)

The contents of the box.

Default: `none`
