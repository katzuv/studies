= lower

Converts a string or content to lowercase.

== Example

```typst
#lower("ABC") \
#lower[*My Text*] \
#lower[already low]
```

== Parameters

```
lower(
  str: str | content
) -> content
```

=== `text`: str | content (Required, Positional)

The text to convert to lowercase.
