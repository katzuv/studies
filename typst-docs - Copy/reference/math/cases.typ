= cases

A case distinction.

Content across different branches can be aligned with the `&` symbol.

== Example

```typst
$ f(x, y) := cases(
  1 "if" (x dot y)/2 <= 0,
  2 "if" x "is even",
  3 "if" x in NN,
  4 "else",
) $
```

== Parameters

```
cases(
  delim: none | str | array | symbol,
  reverse: bool,
  gap: relative,
  ..: content
) -> content
```

=== `delim`: none | str | array | symbol (Settable)

The delimiter to use.

Can be a single character specifying the left delimiter, in which case the right delimiter is inferred. Otherwise, can be an array containing a left and a right delimiter.

Default: `("{", "}")`

*Example:*
```typst
#set math.cases(delim: "[")
$ x = cases(1, 2) $
```

=== `reverse`: bool (Settable)

Whether the direction of cases should be reversed.

Default: `false`

*Example:*
```typst
#set math.cases(reverse: true)
$ cases(1, 2) = x $
```

=== `gap`: relative (Settable)

The gap between branches.

Default: `0% + 0.2em`

*Example:*
```typst
#set math.cases(gap: 1em)
$ x = cases(1, 2) $
```

=== `children`: content (Required, Positional, Variadic)

The branches of the case distinction.
