= repr

Returns the string representation of a value.

When inserted into content, most values are displayed as this representation in monospace with syntax-highlighting. The exceptions are `none`, integers, floats, strings, content, and functions.

*Note:* This function is for debugging purposes. Its output should not be considered stable and may change at any time!

== Example

```typst
#none vs #repr(none) \
#"hello" vs #repr("hello") \
#(1, 2) vs #repr((1, 2)) \
#[*Hi*] vs #repr([*Hi*])
```

== Parameters

```
repr(
  any
) -> str
```

=== `value`: any (Required, Positional)

The value whose string representation to produce.
