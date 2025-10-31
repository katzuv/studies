= heading

A section heading.

With headings, you can structure your document into sections. Each heading has a _level,_ which starts at one and is unbounded upwards. This level indicates the logical role of the following content (section, subsection, etc.) A top-level heading indicates a top-level section of the document (not the document's title).

Typst can automatically number your headings for you. To enable numbering, specify how you want your headings to be numbered with a #link("/docs/reference/model/numbering/")[numbering pattern or function].

Independently of the numbering, Typst can also automatically generate an #link("/docs/reference/model/outline/")[outline] of all headings for you. To exclude one or more headings from this outline, you can set the `outlined` parameter to `false`.

== Example

```typst
#set heading(numbering: "1.a)")

= Introduction
In recent years, ...

== Preliminaries
To start, ...
```

== Syntax

Headings have dedicated syntax: They can be created by starting a line with one or multiple equals signs, followed by a space. The number of equals signs determines the heading's logical nesting depth. The `offset` field can be set to configure the starting depth.

== Parameters

```
heading(
  level: auto | int,
  depth: int,
  offset: int,
  numbering: none | str | function,
  supplement: none | auto | content | function,
  outlined: bool,
  bookmarked: auto | bool,
  hanging-indent: auto | length,
  content: content
) -> content
```

=== `level`: auto | int (Settable)

The absolute nesting depth of the heading, starting from one. If set to `auto`, it is computed from `offset + depth`.

This is primarily useful for usage in #link("/docs/reference/styling/#show-rules")[show rules] (either with #link("/docs/reference/foundations/function/#definitions-where")[where] selectors or by accessing the level directly on a shown heading).

Default: `auto`

*Example:*
```typst
#show heading.where(level: 2): set text(red)

= Level 1
== Level 2

#set heading(offset: 1)
= Also level 2
== Level 3
```

=== `depth`: int (Settable)

The relative nesting depth of the heading, starting from one. This is combined with `offset` to compute the actual `level`.

This is set by the heading syntax, such that `== Heading` creates a heading with logical depth of 2, but actual level `offset + 2`. If you construct a heading manually, you should typically prefer this over setting the absolute level.

Default: `1`

=== `offset`: int (Settable)

The starting offset of each heading's `level`, used to turn its relative `depth` into its absolute `level`.

Default: `0`

*Example:*
```typst
= Level 1

#set heading(offset: 1, numbering: "1.1")
= Level 2

#heading(offset: 2, depth: 2)[
  I'm level 4
]
```

=== `numbering`: none | str | function (Settable)

How to number the heading. Accepts a #link("/docs/reference/model/numbering/")[numbering pattern or function].

Default: `none`

*Example:*
```typst
#set heading(numbering: "1.a.")

= A section
== A subsection
=== A sub-subsection
```

=== `supplement`: none | auto | content | function (Settable)

A supplement for the heading.

For references to headings, this is added before the referenced number.

If a function is specified, it is passed the referenced heading and should return content.

Default: `auto`

*Example:*
```typst
#set heading(numbering: "1.", supplement: [Chapter])

= Introduction <intro>
In @intro, we see how to turn
Sections into Chapters. And
in @intro[Part], it is done
manually.
```

=== `outlined`: bool (Settable)

Whether the heading should appear in the #link("/docs/reference/model/outline/")[outline].

Note that this property, if set to `true`, ensures the heading is also shown as a bookmark in the exported PDF's outline (when exporting to PDF). To change that behavior, use the `bookmarked` property.

Default: `true`

*Example:*
```typst
#outline()

#heading[Normal]
This is a normal heading.

#heading(outlined: false)[Hidden]
This heading does not appear
in the outline.
```

=== `bookmarked`: auto | bool (Settable)

Whether the heading should appear as a bookmark in the exported PDF's outline. Doesn't affect other export formats, such as PNG.

The default value of `auto` indicates that the heading will only appear in the exported PDF's outline if its `outlined` property is set to `true`, that is, if it would also be listed in Typst's #link("/docs/reference/model/outline/")[outline]. Setting this property to either `true` (bookmark) or `false` (don't bookmark) bypasses that behavior.

Default: `auto`

*Example:*
```typst
#heading[Normal heading]
This heading will be shown in
the PDF's bookmark outline.

#heading(bookmarked: false)[Not bookmarked]
This heading won't be
bookmarked in the resulting
PDF.
```

=== `hanging-indent`: auto | length (Settable)

The indent all but the first line of a heading should have.

The default value of `auto` indicates that the subsequent heading lines will be indented based on the width of the numbering.

Default: `auto`

*Example:*
```typst
#set heading(numbering: "1.")
#heading[A very, very, very, very, very, very long heading]
```

=== `body`: content (Required, Positional)

The heading's title.
