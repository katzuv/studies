= bibliography

A bibliography / reference listing.

You can create a new bibliography by calling this function with a path to a bibliography file in either one of two formats:

- A Hayagriva `.yml` file. Hayagriva is a new bibliography file format designed for use with Typst. Visit its #link("https://github.com/typst/hayagriva/blob/main/docs/file-format.md")[documentation] for more details.
- A BibLaTeX `.bib` file.

As soon as you add a bibliography somewhere in your document, you can start citing things with reference syntax (`@key`) or explicit calls to the #link("/docs/reference/model/cite/")[citation] function (`#cite(<key>)`). The bibliography will only show entries for works that were referenced in the document.

== Styles

Typst offers a wide selection of built-in #link("/docs/reference/model/bibliography/#parameters-style")[citation and bibliography styles]. Beyond those, you can add and use custom #link("https://citationstyles.org/")[CSL] (Citation Style Language) files. Wondering which style to use? Here are some good defaults based on what discipline you're working in:

== Example

```typst
This was already noted by
pirates long ago. @arrgh

Multiple sources say ...
@arrgh @netwok.

#bibliography("works.bib")
```

== Parameters

```
bibliography(
  str: str | bytes | array,
  title: none | auto | content,
  full: bool,
  style: str | bytes
) -> content
```

=== `sources`: str | bytes | array (Required, Positional)

One or multiple paths to or raw bytes for Hayagriva `.yml` and/or BibLaTeX `.bib` files.

This can be a:

- A path string to load a bibliography file from the given path. For more details about paths, see the #link("/docs/reference/syntax/#paths")[Paths section].
- Raw bytes from which the bibliography should be decoded.
- An array where each item is one the above.

=== `title`: none | auto | content (Settable)

The title of the bibliography.

- When set to `auto`, an appropriate title for the #link("/docs/reference/text/text/#parameters-lang")[text language] will be used. This is the default.
- When set to `none`, the bibliography will not have a title.
- A custom title can be set by passing content.

The bibliography's heading will not be numbered by default, but you can force it to be with a show-set rule: `show bibliography: set heading(numbering: "1.")`

Default: `auto`

=== `full`: bool (Settable)

Whether to include all works from the given bibliography files, even those that weren't cited in the document.

To selectively add individual cited works without showing them, you can also use the `cite` function with #link("/docs/reference/model/cite/#parameters-form")[form] set to `none`.

Default: `false`

=== `style`: str | bytes (Settable)

The bibliography style.

This can be:

- A string with the name of one of the built-in styles (see below). Some of the styles listed below appear twice, once with their full name and once with a short alias.
- A path string to a #link("https://citationstyles.org/")[CSL file]. For more details about paths, see the #link("/docs/reference/syntax/#paths")[Paths section].
- Raw bytes from which a CSL style should be decoded.

Default: `"ieee"`
