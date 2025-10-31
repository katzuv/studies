= Left/Right

Delimiter matching.

The `lr` function allows you to match two delimiters and scale them with the content they contain. While this also happens automatically for delimiters that match syntactically, `lr` allows you to match two arbitrary delimiters and control their size exactly. Apart from the `lr` function, Typst provides a few more functions that create delimiter pairings for absolute, ceiled, and floored values as well as norms.

== Example

```typst
$ [a, b/2] $
$ lr(]sum_(x=1)^n], size: #50%) x $
$ abs((x + y) / 2) $
```

== Functions

=== `lr`

Scales delimiters.

While matched delimiters scale by default, this can be used to scale unmatched delimiters and to control the delimiter scaling more precisely.

```
lr(
  size: relative,
  content: content
) -> content
```

==== `size`: relative (Settable)

The size of the brackets, relative to the height of the wrapped content.

Default: `100% + 0pt`

==== `body`: content (Required, Positional)

The delimited content, including the delimiters.

=== `mid`

Scales delimiters vertically to the nearest surrounding `lr()` group.

```
mid(
  content: content
) -> content
```

```typst
$ { x mid(|) sum_(i=1)^n w_i|f_i (x)| < 1 } $
```

==== `body`: content (Required, Positional)

The content to be scaled.

=== `abs`

Takes the absolute value of an expression.

```
abs(
  size: relative,
  content: content
) -> content
```

```typst
$ abs(x/2) $
```

==== `size`: relative

The size of the brackets, relative to the height of the wrapped content.

==== `body`: content (Required, Positional)

The expression to take the absolute value of.

=== `norm`

Takes the norm of an expression.

```
norm(
  size: relative,
  content: content
) -> content
```

```typst
$ norm(x/2) $
```

==== `size`: relative

The size of the brackets, relative to the height of the wrapped content.

==== `body`: content (Required, Positional)

The expression to take the norm of.

=== `floor`

Floors an expression.

```
floor(
  size: relative,
  content: content
) -> content
```

```typst
$ floor(x/2) $
```

==== `size`: relative

The size of the brackets, relative to the height of the wrapped content.

==== `body`: content (Required, Positional)

The expression to floor.

=== `ceil`

Ceils an expression.

```
ceil(
  size: relative,
  content: content
) -> content
```

```typst
$ ceil(x/2) $
```

==== `size`: relative

The size of the brackets, relative to the height of the wrapped content.

==== `body`: content (Required, Positional)

The expression to ceil.

=== `round`

Rounds an expression.

```
round(
  size: relative,
  content: content
) -> content
```

```typst
$ round(x/2) $
```

==== `size`: relative

The size of the brackets, relative to the height of the wrapped content.

==== `body`: content (Required, Positional)

The expression to round.
