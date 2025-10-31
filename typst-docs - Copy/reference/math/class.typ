= class

Forced use of a certain math class.

This is useful to treat certain symbols as if they were of a different class, e.g. to make a symbol behave like a relation. The class of a symbol defines the way it is laid out, including spacing around it, and how its scripts are attached by default. Note that the latter can always be overridden using #link("/docs/reference/math/attach/#functions-limits")[limits] and #link("/docs/reference/math/attach/#functions-scripts")[scripts].

== Example

```typst
#let loves = math.class(
  "relation",
  sym.suit.heart,
)

$x loves y and y loves 5$
```

== Parameters

```
class(
  str: str,
  content: content
) -> content
```

=== `class`: str (Required, Positional)

The class to apply to the content.

=== `body`: content (Required, Positional)

The content to which the class is applied.
