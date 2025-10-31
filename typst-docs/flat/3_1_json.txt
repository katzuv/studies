= json

Reads structured data from a JSON file.

The file must contain a valid JSON value, such as object or array. JSON objects will be converted into Typst dictionaries, and JSON arrays will be converted into Typst arrays. Strings and booleans will be converted into the Typst equivalents, `null` will be converted into `none`, and numbers will be converted to floats or integers depending on whether they are whole numbers.

Be aware that integers larger than 263-1 will be converted to floating point numbers, which may result in an approximative value.

The function returns a dictionary, an array or, depending on the JSON file, another JSON data type.

The JSON files in the example contain objects with the keys `temperature`, `unit`, and `weather`.

== Example

```typst
#let forecast(day) = block[
  #box(square(
    width: 2cm,
    inset: 8pt,
    fill: if day.weather == "sunny" {
      yellow
    } else {
      aqua
    },
    align(
      bottom + right,
      strong(day.weather),
    ),
  ))
  #h(6pt)
  #set text(22pt, baseline: -8pt)
  #day.temperature °#day.unit
]

#forecast(json("monday.json"))
#forecast(json("tuesday.json"))
```

== Parameters

```
json(
  str: str | bytes
) -> bytes
```

=== `source`: str | bytes (Required, Positional)

A #link("/docs/reference/syntax/#paths")[path] to a JSON file or raw JSON bytes.

== Definitions

=== `decode`

Reads structured data from a JSON string/bytes.

```
decode(
  str: str | bytes
) -> bytes
```

==== `data`: str | bytes (Required, Positional)

JSON data.

=== `encode`

Encodes structured data into a JSON string.

```
encode(
  any,
  pretty: bool
) -> str
```

==== `value`: any (Required, Positional)

Value to be encoded.

==== `pretty`: bool

Whether to pretty print the JSON with newlines and indentation.

Default: `true`
