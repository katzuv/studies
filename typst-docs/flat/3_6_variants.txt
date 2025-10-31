= Variants

Alternate typefaces within formulas.

These functions are distinct from the #link("/docs/reference/text/text/")[text] function because math fonts contain multiple variants of each letter.

== Functions

=== `serif`

Serif (roman) font style in math.

This is already the default.

```
serif(
  content: content
) -> content
```

==== `body`: content (Required, Positional)

The content to style.

=== `sans`

Sans-serif font style in math.

```
sans(
  content: content
) -> content
```

```typst
$ sans(A B C) $
```

==== `body`: content (Required, Positional)

The content to style.

=== `frak`

Fraktur font style in math.

```
frak(
  content: content
) -> content
```

```typst
$ frak(P) $
```

==== `body`: content (Required, Positional)

The content to style.

=== `mono`

Monospace font style in math.

```
mono(
  content: content
) -> content
```

```typst
$ mono(x + y = z) $
```

==== `body`: content (Required, Positional)

The content to style.

=== `bb`

Blackboard bold (double-struck) font style in math.

For uppercase latin letters, blackboard bold is additionally available through #link("/docs/reference/symbols/sym/")[symbols] of the form `NN` and `RR`.

```
bb(
  content: content
) -> content
```

```typst
$ bb(b) $
$ bb(N) = NN $
$ f: NN -> RR $
```

==== `body`: content (Required, Positional)

The content to style.

=== `cal`

Calligraphic font style in math.

```
cal(
  content: content
) -> content
```

```typst
Let $cal(P)$ be the set of ...
```

This corresponds both to LaTeX's `\mathcal` and `\mathscr` as both of these styles share the same Unicode codepoints. Switching between the styles is thus only possible if supported by the font via #link("/docs/reference/text/text/#parameters-features")[font features].

For the default math font, the roundhand style is available through the `ss01` feature. Therefore, you could define your own version of `\mathscr` like this:

```typst
#let scr(it) = text(
  features: ("ss01",),
  box($cal(it)$),
)

We establish $cal(P) != scr(P)$.
```

(The box is not conceptually necessary, but unfortunately currently needed due to limitations in Typst's text style handling in math.)

==== `body`: content (Required, Positional)

The content to style.
