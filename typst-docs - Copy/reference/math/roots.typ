= Roots

Square and non-square roots.

== Example

```typst
$ sqrt(3 - 2 sqrt(2)) = sqrt(2) - 1 $
$ root(3, x) $
```

== Functions

=== `root`

A general root.

```
root(
  none | content,
  content: content
) -> content
```

```typst
$ root(3, x) $
```

==== `index`: none | content (Positional, Settable)

Which root of the radicand to take.

Default: `none`

==== `radicand`: content (Required, Positional)

The expression to take the root of.

=== `sqrt`

A square root.

```
sqrt(
  content: content
) -> content
```

```typst
$ sqrt(3 - 2 sqrt(2)) = sqrt(2) - 1 $
```

==== `radicand`: content (Required, Positional)

The expression to take the square root of.
