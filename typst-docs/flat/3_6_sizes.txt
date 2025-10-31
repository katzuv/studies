= Sizes

Forced size styles for expressions within formulas.

These functions allow manual configuration of the size of equation elements to make them look as in a display/inline equation or as if used in a root or sub/superscripts.

== Functions

=== `display`

Forced display style in math.

This is the normal size for block equations.

```
display(
  content: content,
  cramped: bool
) -> content
```

```typst
$sum_i x_i/2 = display(sum_i x_i/2)$
```

==== `body`: content (Required, Positional)

The content to size.

==== `cramped`: bool

Whether to impose a height restriction for exponents, like regular sub- and superscripts do.

Default: `false`

=== `inline`

Forced inline (text) style in math.

This is the normal size for inline equations.

```
inline(
  content: content,
  cramped: bool
) -> content
```

```typst
$ sum_i x_i/2
    = inline(sum_i x_i/2) $
```

==== `body`: content (Required, Positional)

The content to size.

==== `cramped`: bool

Whether to impose a height restriction for exponents, like regular sub- and superscripts do.

Default: `false`

=== `script`

Forced script style in math.

This is the smaller size used in powers or sub- or superscripts.

```
script(
  content: content,
  cramped: bool
) -> content
```

```typst
$sum_i x_i/2 = script(sum_i x_i/2)$
```

==== `body`: content (Required, Positional)

The content to size.

==== `cramped`: bool

Whether to impose a height restriction for exponents, like regular sub- and superscripts do.

Default: `true`

=== `sscript`

Forced second script style in math.

This is the smallest size, used in second-level sub- and superscripts (script of the script).

```
sscript(
  content: content,
  cramped: bool
) -> content
```

```typst
$sum_i x_i/2 = sscript(sum_i x_i/2)$
```

==== `body`: content (Required, Positional)

The content to size.

==== `cramped`: bool

Whether to impose a height restriction for exponents, like regular sub- and superscripts do.

Default: `true`
