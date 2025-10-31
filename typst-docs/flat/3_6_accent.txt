= accent

Attaches an accent to a base.

== Example

```typst
$grave(a) = accent(a, `)$ \
$arrow(a) = accent(a, arrow)$ \
$tilde(a) = accent(a, \u{0303})$
```

== Parameters

```
accent(
  content: content,
  str: str | content,
  size: relative
) -> content
```

=== `base`: content (Required, Positional)

The base to which the accent is applied. May consist of multiple letters.

*Example:*
```typst
$arrow(A B C)$
```

=== `accent`: str | content (Required, Positional)

The accent to apply to the base.

Supported accents include:

=== `size`: relative (Settable)

The size of the accent, relative to the width of the base.

Default: `100% + 0pt`
