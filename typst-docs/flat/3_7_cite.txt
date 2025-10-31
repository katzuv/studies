= cite

Cite a work from the bibliography.

Before you starting citing, you need to add a #link("/docs/reference/model/bibliography/")[bibliography] somewhere in your document.

== Example

```typst
This was already noted by
pirates long ago. @arrgh

Multiple sources say ...
@arrgh @netwok.

You can also call `cite`
explicitly. #cite(<arrgh>)

#bibliography("works.bib")
```

If your source name contains certain characters such as slashes, which are not recognized by the `<>` syntax, you can explicitly call `label` instead.

== Syntax

This function indirectly has dedicated syntax. #link("/docs/reference/model/ref/")[References] can be used to cite works from the bibliography. The label then corresponds to the citation key.

== Parameters

```
cite(
  label: label,
  supplement: none | content,
  form: none | str,
  style: auto | str | bytes
) -> content
```

=== `key`: label (Required, Positional)

The citation key that identifies the entry in the bibliography that shall be cited, as a label.

*Example:*
```typst
// All the same
@netwok \
#cite(<netwok>) \
#cite(label("netwok"))
```

=== `supplement`: none | content (Settable)

A supplement for the citation such as page or chapter number.

In reference syntax, the supplement can be added in square brackets:

Default: `none`

*Example:*
```typst
This has been proven. @distress[p.~7]

#bibliography("works.bib")
```

=== `form`: none | str (Settable)

The kind of citation to produce. Different forms are useful in different scenarios: A normal citation is useful as a source at the end of a sentence, while a "prose" citation is more suitable for inclusion in the flow of text.

If set to `none`, the cited work is included in the bibliography, but nothing will be displayed.

Default: `"normal"`

*Example:*
```typst
#cite(<netwok>, form: "prose")
show the outsized effects of
pirate life on the human psyche.
```

=== `style`: auto | str | bytes (Settable)

The citation style.

This can be:

- `auto` to automatically use the #link("/docs/reference/model/bibliography/#parameters-style")[bibliography's style] for citations.
- A string with the name of one of the built-in styles (see below). Some of the styles listed below appear twice, once with their full name and once with a short alias.
- A path string to a #link("https://citationstyles.org/")[CSL file]. For more details about paths, see the #link("/docs/reference/syntax/#paths")[Paths section].
- Raw bytes from which a CSL style should be decoded.

Default: `auto`
