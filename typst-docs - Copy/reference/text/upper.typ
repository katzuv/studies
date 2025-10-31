= upper

Converts a string or content to uppercase.

== Example

```typst
#upper("abc") \
#upper[*my text*] \
#upper[ALREADY HIGH]
```

== Parameters

```
upper(
  str: str | content
) -> content
```

=== `text`: str | content (Required, Positional)

The text to convert to uppercase.
