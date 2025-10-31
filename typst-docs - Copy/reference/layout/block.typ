= block

A block-level container.

Such a container can be used to separate content, size it, and give it a background or border.

Blocks are also the primary way to control whether text becomes part of a paragraph or not. See #link("/docs/reference/model/par/#what-becomes-a-paragraph")[the paragraph documentation] for more details.

== Examples

With a block, you can give a background to content while still allowing it to break across multiple pages.

```typst
#set page(height: 100pt)
#block(
  fill: luma(230),
  inset: 8pt,
  radius: 4pt,
  lorem(30),
)
```

Blocks are also useful to force elements that would otherwise be inline to become block-level, especially when writing show rules.

```typst
#show heading: it => it.body
= Blockless
More text.

#show heading: it => block(it.body)
= Blocky
More text.
```

== Parameters

```
block(
  width: auto | relative,
  height: auto | relative | fraction,
  breakable: bool,
  fill: none | color | gradient | tiling,
  stroke: none | length | color | gradient | stroke | tiling | dictionary,
  radius: relative | dictionary,
  inset: relative | dictionary,
  outset: relative | dictionary,
  spacing: relative | fraction,
  above: auto | relative | fraction,
  below: auto | relative | fraction,
  clip: bool,
  sticky: bool,
  body: none | content
) -> content
```

=== `width`: auto | relative (Settable)

The block's width.

Default: `auto`

*Example:*
```typst
#set align(center)
#block(
  width: 60%,
  inset: 8pt,
  fill: silver,
  lorem(10),
)
```

=== `height`: auto | relative | fraction (Settable)

The block's height. When the height is larger than the remaining space on a page and #link("/docs/reference/layout/block/#parameters-breakable")[breakable] is `true`, the block will continue on the next page with the remaining height.

Default: `auto`

*Example:*
```typst
#set page(height: 80pt)
#set align(center)
#block(
  width: 80%,
  height: 150%,
  fill: aqua,
)
```

=== `breakable`: bool (Settable)

Whether the block can be broken and continue on the next page.

Default: `true`

*Example:*
```typst
#set page(height: 80pt)
The following block will
jump to its own page.
#block(
  breakable: false,
  lorem(15),
)
```

=== `fill`: none | color | gradient | tiling (Settable)

The block's background color. See the #link("/docs/reference/visualize/rect/#parameters-fill")[rectangle's documentation] for more details.

Default: `none`

=== `stroke`: none | length | color | gradient | stroke | tiling | dictionary (Settable)

The block's border color. See the #link("/docs/reference/visualize/rect/#parameters-stroke")[rectangle's documentation] for more details.

Default: `(:)`

=== `radius`: relative | dictionary (Settable)

How much to round the block's corners. See the #link("/docs/reference/visualize/rect/#parameters-radius")[rectangle's documentation] for more details.

Default: `(:)`

=== `inset`: relative | dictionary (Settable)

How much to pad the block's content. See the #link("/docs/reference/layout/box/#parameters-inset")[box's documentation] for more details.

Default: `(:)`

=== `outset`: relative | dictionary (Settable)

How much to expand the block's size without affecting the layout. See the #link("/docs/reference/layout/box/#parameters-outset")[box's documentation] for more details.

Default: `(:)`

=== `spacing`: relative | fraction (Settable)

The spacing around the block. When `auto`, inherits the paragraph #link("/docs/reference/model/par/#parameters-spacing")[spacing].

For two adjacent blocks, the larger of the first block's `above` and the second block's `below` spacing wins. Moreover, block spacing takes precedence over paragraph #link("/docs/reference/model/par/#parameters-spacing")[spacing].

Note that this is only a shorthand to set `above` and `below` to the same value. Since the values for `above` and `below` might differ, a #link("/docs/reference/context/")[context] block only provides access to `block.above` and `block.below`, not to `block.spacing` directly.

This property can be used in combination with a show rule to adjust the spacing around arbitrary block-level elements.

Default: `1.2em`

*Example:*
```typst
#set align(center)
#show math.equation: set block(above: 8pt, below: 16pt)

This sum of $x$ and $y$:
$ x + y = z $
A second paragraph.
```

=== `above`: auto | relative | fraction (Settable)

The spacing between this block and its predecessor.

Default: `auto`

=== `below`: auto | relative | fraction (Settable)

The spacing between this block and its successor.

Default: `auto`

=== `clip`: bool (Settable)

Whether to clip the content inside the block.

Clipping is useful when the block's content is larger than the block itself, as any content that exceeds the block's bounds will be hidden.

Default: `false`

*Example:*
```typst
#block(
  width: 50pt,
  height: 50pt,
  clip: true,
  image("tiger.jpg", width: 100pt, height: 100pt)
)
```

=== `sticky`: bool (Settable)

Whether this block must stick to the following one, with no break in between.

This is, by default, set on heading blocks to prevent orphaned headings at the bottom of the page.

Default: `false`

*Example:*
```typst
// Disable stickiness of headings.
#show heading: set block(sticky: false)
#lorem(20)

= Chapter
#lorem(10)
```

=== `body`: none | content (Positional, Settable)

The contents of the block.

Default: `none`
