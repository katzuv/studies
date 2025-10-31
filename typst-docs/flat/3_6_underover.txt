= Under/Over

Delimiters above or below parts of an equation.

The braces and brackets further allow you to add an optional annotation below or above themselves.

== Functions

=== `underline`

A horizontal line under content.

```
underline(
  content: content
) -> content
```

```typst
$ underline(1 + 2 + ... + 5) $
```

==== `body`: content (Required, Positional)

The content above the line.

=== `overline`

A horizontal line over content.

```
overline(
  content: content
) -> content
```

```typst
$ overline(1 + 2 + ... + 5) $
```

==== `body`: content (Required, Positional)

The content below the line.

=== `underbrace`

A horizontal brace under content, with an optional annotation below.

```
underbrace(
  content: content,
  none | content
) -> content
```

```typst
$ underbrace(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content above the brace.

==== `annotation`: none | content (Positional, Settable)

The optional content below the brace.

Default: `none`

=== `overbrace`

A horizontal brace over content, with an optional annotation above.

```
overbrace(
  content: content,
  none | content
) -> content
```

```typst
$ overbrace(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content below the brace.

==== `annotation`: none | content (Positional, Settable)

The optional content above the brace.

Default: `none`

=== `underbracket`

A horizontal bracket under content, with an optional annotation below.

```
underbracket(
  content: content,
  none | content
) -> content
```

```typst
$ underbracket(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content above the bracket.

==== `annotation`: none | content (Positional, Settable)

The optional content below the bracket.

Default: `none`

=== `overbracket`

A horizontal bracket over content, with an optional annotation above.

```
overbracket(
  content: content,
  none | content
) -> content
```

```typst
$ overbracket(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content below the bracket.

==== `annotation`: none | content (Positional, Settable)

The optional content above the bracket.

Default: `none`

=== `underparen`

A horizontal parenthesis under content, with an optional annotation below.

```
underparen(
  content: content,
  none | content
) -> content
```

```typst
$ underparen(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content above the parenthesis.

==== `annotation`: none | content (Positional, Settable)

The optional content below the parenthesis.

Default: `none`

=== `overparen`

A horizontal parenthesis over content, with an optional annotation above.

```
overparen(
  content: content,
  none | content
) -> content
```

```typst
$ overparen(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content below the parenthesis.

==== `annotation`: none | content (Positional, Settable)

The optional content above the parenthesis.

Default: `none`

=== `undershell`

A horizontal tortoise shell bracket under content, with an optional annotation below.

```
undershell(
  content: content,
  none | content
) -> content
```

```typst
$ undershell(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content above the tortoise shell bracket.

==== `annotation`: none | content (Positional, Settable)

The optional content below the tortoise shell bracket.

Default: `none`

=== `overshell`

A horizontal tortoise shell bracket over content, with an optional annotation above.

```
overshell(
  content: content,
  none | content
) -> content
```

```typst
$ overshell(1 + 2 + ... + 5, "numbers") $
```

==== `body`: content (Required, Positional)

The content below the tortoise shell bracket.

==== `annotation`: none | content (Positional, Settable)

The optional content above the tortoise shell bracket.

Default: `none`
