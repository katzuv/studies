= document

The root element of a document and its metadata.

All documents are automatically wrapped in a `document` element. You cannot create a document element yourself. This function is only used with #link("/docs/reference/styling/#set-rules")[set rules] to specify document metadata. Such a set rule must not occur inside of any layout container.

```typst
#set document(title: [Hello])

This has no visible output, but
embeds metadata into the PDF!
```

Note that metadata set with this function is not rendered within the document. Instead, it is embedded in the compiled PDF file.

== Parameters

```
document(
  title: none | content,
  author: str | array,
  description: none | content,
  keywords: str | array,
  date: none | auto | datetime
) -> content
```

=== `title`: none | content (Settable)

The document's title. This is often rendered as the title of the PDF viewer window.

While this can be arbitrary content, PDF viewers only support plain text titles, so the conversion might be lossy.

Default: `none`

=== `author`: str | array (Settable)

The document's authors.

Default: `()`

=== `description`: none | content (Settable)

The document's description.

Default: `none`

=== `keywords`: str | array (Settable)

The document's keywords.

Default: `()`

=== `date`: none | auto | datetime (Settable)

The document's creation date.

If this is `auto` (default), Typst uses the current date and time. Setting it to `none` prevents Typst from embedding any creation date into the PDF metadata.

The year component must be at least zero in order to be embedded into a PDF.

If you want to create byte-by-byte reproducible PDFs, set this to something other than `auto`.

Default: `auto`
