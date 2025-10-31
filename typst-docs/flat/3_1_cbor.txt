= cbor

Reads structured data from a CBOR file.

The file must contain a valid CBOR serialization. Mappings will be converted into Typst dictionaries, and sequences will be converted into Typst arrays. Strings and booleans will be converted into the Typst equivalents, null-values (`null`, `~` or empty ``) will be converted into `none`, and numbers will be converted to floats or integers depending on whether they are whole numbers.

Be aware that integers larger than 263-1 will be converted to floating point numbers, which may result in an approximative value.

== Parameters

```
cbor(
  str: str | bytes
) -> bytes
```

=== `source`: str | bytes (Required, Positional)

A #link("/docs/reference/syntax/#paths")[path] to a CBOR file or raw CBOR bytes.

== Definitions

=== `decode`

Reads structured data from CBOR bytes.

```
decode(
  bytes: bytes
) -> bytes
```

==== `data`: bytes (Required, Positional)

CBOR data.

=== `encode`

Encode structured data into CBOR bytes.

```
encode(
  any
) -> bytes
```

==== `value`: any (Required, Positional)

Value to be encoded.
