= vec

A column vector.

Content in the vector's elements can be aligned with the #link("/docs/reference/math/vec/#parameters-align")[align] parameter, or the `&` symbol.

== Example

```typst
$ vec(a, b, c) dot vec(1, 2, 3)
    = a + 2b + 3c $
```

== Parameters

```
vec(
  delim: none | str | array | symbol,
  align: alignment,
  gap: relative,
  ..: content
) -> content
```

=== `delim`: none | str | array | symbol (Settable)

The delimiter to use.

Can be a single character specifying the left delimiter, in which case the right delimiter is inferred. Otherwise, can be an array containing a left and a right delimiter.

Default: `("(", ")")`

*Example:*
```typst
#set math.vec(delim: "[")
$ vec(1, 2) $
```

=== `align`: alignment (Settable)

The horizontal alignment that each element should have.

Default: `center`

*Example:*
```typst
#set math.vec(align: right)
$ vec(-1, 1, -1) $
```

=== `gap`: relative (Settable)

The gap between elements.

Default: `0% + 0.2em`

*Example:*
```typst
#set math.vec(gap: 1em)
$ vec(1, 2) $
```

=== `children`: content (Required, Positional, Variadic)

The elements of the vector.
