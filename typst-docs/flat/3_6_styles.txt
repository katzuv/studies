= Styles

Alternate letterforms within formulas.

These functions are distinct from the #link("/docs/reference/text/text/")[text] function because math fonts contain multiple variants of each letter.

== Functions

=== `upright`

Upright (non-italic) font style in math.

```
upright(
  content: content
) -> content
```

```typst
$ upright(A) != A $
```

==== `body`: content (Required, Positional)

The content to style.

=== `italic`

Italic font style in math.

For roman letters and greek lowercase letters, this is already the default.

```
italic(
  content: content
) -> content
```

==== `body`: content (Required, Positional)

The content to style.

=== `bold`

Bold font style in math.

```
bold(
  content: content
) -> content
```

```typst
$ bold(A) := B^+ $
```

==== `body`: content (Required, Positional)

The content to style.
