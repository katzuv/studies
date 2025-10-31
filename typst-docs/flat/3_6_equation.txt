= equation

A mathematical equation.

Can be displayed inline with text or as a separate block. An equation becomes block-level through the presence of at least one space after the opening dollar sign and one space before the closing dollar sign.

== Example

```typst
#set text(font: "New Computer Modern")

Let $a$, $b$, and $c$ be the side
lengths of right-angled triangle.
Then, we know that:
$ a^2 + b^2 = c^2 $

Prove by induction:
$ sum_(k=1)^n k = (n(n+1)) / 2 $
```

By default, block-level equations will not break across pages. This can be changed through `show math.equation: set block(breakable: true)`.

== Syntax

This function also has dedicated syntax: Write mathematical markup within dollar signs to create an equation. Starting and ending the equation with at least one space lifts it into a separate block that is centered horizontally. For more details about math syntax, see the #link("/docs/reference/math/")[main math page].

== Parameters

```
equation(
  block: bool,
  numbering: none | str | function,
  number-align: alignment,
  supplement: none | auto | content | function,
  content: content
) -> content
```

=== `block`: bool (Settable)

Whether the equation is displayed as a separate block.

Default: `false`

=== `numbering`: none | str | function (Settable)

How to #link("/docs/reference/model/numbering/")[number] block-level equations.

Default: `none`

*Example:*
```typst
#set math.equation(numbering: "(1)")

We define:
$ phi.alt := (1 + sqrt(5)) / 2 $ <ratio>

With @ratio, we get:
$ F_n = floor(1 / sqrt(5) phi.alt^n) $
```

=== `number-align`: alignment (Settable)

The alignment of the equation numbering.

By default, the alignment is `end + horizon`. For the horizontal component, you can use `right`, `left`, or `start` and `end` of the text direction; for the vertical component, you can use `top`, `horizon`, or `bottom`.

Default: `end + horizon`

*Example:*
```typst
#set math.equation(numbering: "(1)", number-align: bottom)

We can calculate:
$ E &= sqrt(m_0^2 + p^2) \
    &approx 125 "GeV" $
```

=== `supplement`: none | auto | content | function (Settable)

A supplement for the equation.

For references to equations, this is added before the referenced number.

If a function is specified, it is passed the referenced equation and should return content.

Default: `auto`

*Example:*
```typst
#set math.equation(numbering: "(1)", supplement: [Eq.])

We define:
$ phi.alt := (1 + sqrt(5)) / 2 $ <ratio>

With @ratio, we get:
$ F_n = floor(1 / sqrt(5) phi.alt^n) $
```

=== `body`: content (Required, Positional)

The contents of the equation.
