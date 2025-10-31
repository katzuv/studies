= alignment

Where to #link("/docs/reference/layout/align/")[align] something along an axis.

Possible values are:

- `start`: Aligns at the #link("/docs/reference/layout/direction/#definitions-start")[start] of the #link("/docs/reference/text/text/#parameters-dir")[text direction].
- `end`: Aligns at the #link("/docs/reference/layout/direction/#definitions-end")[end] of the #link("/docs/reference/text/text/#parameters-dir")[text direction].
- `left`: Align at the left.
- `center`: Aligns in the middle, horizontally.
- `right`: Aligns at the right.
- `top`: Aligns at the top.
- `horizon`: Aligns in the middle, vertically.
- `bottom`: Align at the bottom.

These values are available globally and also in the alignment type's scope, so you can write either of the following two:

```typst
#align(center)[Hi]
#align(alignment.center)[Hi]
```

== 2D alignments

To align along both axes at the same time, add the two alignments using the `+` operator. For example, `top + right` aligns the content to the top right corner.

```typst
#set page(height: 3cm)
#align(center + bottom)[Hi]
```

== Fields

The `x` and `y` fields hold the alignment's horizontal and vertical components, respectively (as yet another `alignment`). They may be `none`.

```typst
#(top + right).x \
#left.x \
#left.y (none)
```

== Definitions

=== `axis`

The axis this alignment belongs to.

- `"horizontal"` for `start`, `left`, `center`, `right`, and `end`
- `"vertical"` for `top`, `horizon`, and `bottom`
- `none` for 2-dimensional alignments

```
axis(
  
) -> str
```

```typst
#left.axis() \
#bottom.axis()
```

=== `inv`

The inverse alignment.

```
inv(
  
) -> alignment
```

```typst
#top.inv() \
#left.inv() \
#center.inv() \
#(left + bottom).inv()
```
