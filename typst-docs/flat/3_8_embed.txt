= embed

A file that will be embedded into the output PDF.

This can be used to distribute additional files that are related to the PDF within it. PDF readers will display the files in a file listing.

Some international standards use this mechanism to embed machine-readable data (e.g., ZUGFeRD/Factur-X for invoices) that mirrors the visual content of the PDF.

== Example

== Notes

- This element is ignored if exporting to a format other than PDF.
- File embeddings are not currently supported for PDF/A-2, even if the embedded file conforms to PDF/A-1 or PDF/A-2.

== Parameters

```
embed(
  str: str,
  bytes: bytes,
  relationship: none | str,
  mime-type: none | str,
  description: none | str
) -> content
```

=== `path`: str (Required, Positional)

The #link("/docs/reference/syntax/#paths")[path] of the file to be embedded.

Must always be specified, but is only read from if no data is provided in the following argument.

=== `data`: bytes (Required, Positional)

Raw file data, optionally.

If omitted, the data is read from the specified path.

=== `relationship`: none | str (Settable)

The relationship of the embedded file to the document.

Ignored if export doesn't target PDF/A-3.

Default: `none`

=== `mime-type`: none | str (Settable)

The MIME type of the embedded file.

Default: `none`

=== `description`: none | str (Settable)

A description for the embedded file.

Default: `none`
