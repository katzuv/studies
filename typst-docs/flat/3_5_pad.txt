= pad

Adds spacing around content.

The spacing can be specified for each side individually, or for all sides at once by specifying a positional argument.

== Example

```typst
#set align(center)

#pad(x: 16pt, image("typing.jpg"))
_Typing speeds can be
 measured in words per minute._
```

== Parameters

```
pad(
  left: relative,
  top: relative,
  right: relative,
  bottom: relative,
  x: relative,
  y: relative,
  rest: relative,
  content: content
) -> content
```

=== `left`: relative (Settable)

The padding at the left side.

Default: `0% + 0pt`

=== `top`: relative (Settable)

The padding at the top side.

Default: `0% + 0pt`

=== `right`: relative (Settable)

The padding at the right side.

Default: `0% + 0pt`

=== `bottom`: relative (Settable)

The padding at the bottom side.

Default: `0% + 0pt`

=== `x`: relative (Settable)

A shorthand to set `left` and `right` to the same value.

Default: `0% + 0pt`

=== `y`: relative (Settable)

A shorthand to set `top` and `bottom` to the same value.

Default: `0% + 0pt`

=== `rest`: relative (Settable)

A shorthand to set all four sides to the same value.

Default: `0% + 0pt`

=== `body`: content (Required, Positional)

The content to pad at the sides.
