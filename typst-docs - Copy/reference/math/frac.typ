= frac

A mathematical fraction.

== Example

```typst
$ 1/2 < (x+1)/2 $
$ ((x+1)) / 2 = frac(a, b) $
```

== Syntax

This function also has dedicated syntax: Use a slash to turn neighbouring expressions into a fraction. Multiple atoms can be grouped into a single expression using round grouping parenthesis. Such parentheses are removed from the output, but you can nest multiple to force them.

== Parameters

```
frac(
  content: content,
  content: content
) -> content
```

=== `num`: content (Required, Positional)

The fraction's numerator.

=== `denom`: content (Required, Positional)

The fraction's denominator.
