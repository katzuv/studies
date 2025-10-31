= eval

Evaluates a string as Typst code.

This function should only be used as a last resort.

== Example

```typst
#eval("1 + 1") \
#eval("(1, 2, 3, 4)").len() \
#eval("*Markup!*", mode: "markup") \
```

== Parameters

```
eval(
  str: str,
  mode: str,
  scope: dictionary
) -> dictionary
```

=== `source`: str (Required, Positional)

A string of Typst code to evaluate.

=== `mode`: str

The #link("/docs/reference/syntax/#modes")[syntactical mode] in which the string is parsed.

Default: `"code"`

*Example:*
```typst
#eval("= Heading", mode: "markup")
#eval("1_2^3", mode: "math")
```

=== `scope`: dictionary

A scope of definitions that are made available.

Default: `(:)`

*Example:*
```typst
#eval("x + 1", scope: (x: 2)) \
#eval(
  "abc/xyz",
  mode: "math",
  scope: (
    abc: $a + b + c$,
    xyz: $x + y + z$,
  ),
)
```
