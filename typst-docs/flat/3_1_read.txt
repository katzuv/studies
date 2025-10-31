= read

Reads plain text or data from a file.

By default, the file will be read as UTF-8 and returned as a #link("/docs/reference/foundations/str/")[string].

If you specify `encoding: none`, this returns raw #link("/docs/reference/foundations/bytes/")[bytes] instead.

== Example

```typst
An example for a HTML file: \
#let text = read("example.html")
#raw(text, lang: "html")

Raw bytes:
#read("tiger.jpg", encoding: none)
```

== Parameters

```
read(
  str: str,
  encoding: none | str
) -> bytes
```

=== `path`: str (Required, Positional)

Path to a file.

For more details, see the #link("/docs/reference/syntax/#paths")[Paths section].

=== `encoding`: none | str

The encoding to read the file with.

If set to `none`, this function returns raw bytes.

Default: `"utf8"`
