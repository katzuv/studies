= toml

Reads structured data from a TOML file.

The file must contain a valid TOML table. TOML tables will be converted into Typst dictionaries, and TOML arrays will be converted into Typst arrays. Strings, booleans and datetimes will be converted into the Typst equivalents and numbers will be converted to floats or integers depending on whether they are whole numbers.

The TOML file in the example consists of a table with the keys `title`, `version`, and `authors`.

== Example

```typst
#let details = toml("details.toml")

Title: #details.title \
Version: #details.version \
Authors: #(details.authors
  .join(", ", last: " and "))
```

== Parameters

```
toml(
  str: str | bytes
) -> bytes
```

=== `source`: str | bytes (Required, Positional)

A #link("/docs/reference/syntax/#paths")[path] to a TOML file or raw TOML bytes.

== Definitions

=== `decode`

Reads structured data from a TOML string/bytes.

```
decode(
  str: str | bytes
) -> bytes
```

==== `data`: str | bytes (Required, Positional)

TOML data.

=== `encode`

Encodes structured data into a TOML string.

```
encode(
  any,
  pretty: bool
) -> str
```

==== `value`: any (Required, Positional)

Value to be encoded.

==== `pretty`: bool

Whether to pretty-print the resulting TOML.

Default: `true`
