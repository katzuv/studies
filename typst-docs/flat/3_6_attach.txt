= Attach

Subscript, superscripts, and limits.

Attachments can be displayed either as sub/superscripts, or limits. Typst automatically decides which is more suitable depending on the base, but you can also control this manually with the `scripts` and `limits` functions.

If you want the base to stretch to fit long top and bottom attachments (for example, an arrow with text above it), use the #link("/docs/reference/math/stretch/")[stretch] function.

== Example

```typst
$ sum_(i=0)^n a_i = 2^(1+i) $
```

== Syntax

This function also has dedicated syntax for attachments after the base: Use the underscore (`_`) to indicate a subscript i.e. bottom attachment and the hat (`^`) to indicate a superscript i.e. top attachment.

== Functions

=== `attach`

A base with optional attachments.

```
attach(
  content: content,
  t: none | content,
  b: none | content,
  tl: none | content,
  bl: none | content,
  tr: none | content,
  br: none | content
) -> content
```

```typst
$ attach(
  Pi, t: alpha, b: beta,
  tl: 1, tr: 2+3, bl: 4+5, br: 6,
) $
```

==== `base`: content (Required, Positional)

The base to which things are attached.

==== `t`: none | content (Settable)

The top attachment, smartly positioned at top-right or above the base.

You can wrap the base in `limits()` or `scripts()` to override the smart positioning.

Default: `none`

==== `b`: none | content (Settable)

The bottom attachment, smartly positioned at the bottom-right or below the base.

You can wrap the base in `limits()` or `scripts()` to override the smart positioning.

Default: `none`

==== `tl`: none | content (Settable)

The top-left attachment (before the base).

Default: `none`

==== `bl`: none | content (Settable)

The bottom-left attachment (before base).

Default: `none`

==== `tr`: none | content (Settable)

The top-right attachment (after the base).

Default: `none`

==== `br`: none | content (Settable)

The bottom-right attachment (after the base).

Default: `none`

=== `scripts`

Forces a base to display attachments as scripts.

```
scripts(
  content: content
) -> content
```

```typst
$ scripts(sum)_1^2 != sum_1^2 $
```

==== `body`: content (Required, Positional)

The base to attach the scripts to.

=== `limits`

Forces a base to display attachments as limits.

```
limits(
  content: content,
  inline: bool
) -> content
```

```typst
$ limits(A)_1^2 != A_1^2 $
```

==== `body`: content (Required, Positional)

The base to attach the limits to.

==== `inline`: bool (Settable)

Whether to also force limits in inline equations.

When applying limits globally (e.g., through a show rule), it is typically a good idea to disable this.

Default: `true`
