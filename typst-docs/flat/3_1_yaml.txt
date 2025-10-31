= yaml

Reads structured data from a YAML file.

The file must contain a valid YAML object or array. YAML mappings will be converted into Typst dictionaries, and YAML sequences will be converted into Typst arrays. Strings and booleans will be converted into the Typst equivalents, null-values (`null`, `~` or empty ``) will be converted into `none`, and numbers will be converted to floats or integers depending on whether they are whole numbers. Custom YAML tags are ignored, though the loaded value will still be present.

Be aware that integers larger than 263-1 will be converted to floating point numbers, which may give an approximative value.

The YAML files in the example contain objects with authors as keys, each with a sequence of their own submapping with the keys "title" and "published"

== Example

```typst
#let bookshelf(contents) = {
  for (author, works) in contents {
    author
    for work in works [
      - #work.title (#work.published)
    ]
  }
}

#bookshelf(
  yaml("scifi-authors.yaml")
)
```

== Parameters

```
yaml(
  str: str | bytes
) -> bytes
```

=== `source`: str | bytes (Required, Positional)

A #link("/docs/reference/syntax/#paths")[path] to a YAML file or raw YAML bytes.

== Definitions

=== `decode`

Reads structured data from a YAML string/bytes.

```
decode(
  str: str | bytes
) -> bytes
```

==== `data`: str | bytes (Required, Positional)

YAML data.

=== `encode`

Encode structured data into a YAML string.

```
encode(
  any
) -> str
```

==== `value`: any (Required, Positional)

Value to be encoded.
