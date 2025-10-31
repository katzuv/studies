= terms

A list of terms and their descriptions.

Displays a sequence of terms and their descriptions vertically. When the descriptions span over multiple lines, they use hanging indent to communicate the visual hierarchy.

== Example

```typst
/ Ligature: A merged glyph.
/ Kerning: A spacing adjustment
  between two adjacent letters.
```

== Syntax

This function also has dedicated syntax: Starting a line with a slash, followed by a term, a colon and a description creates a term list item.

== Parameters

```
terms(
  tight: bool,
  separator: content,
  indent: length,
  hanging-indent: length,
  spacing: auto | length,
  ..: content | array
) -> content
```

=== `tight`: bool (Settable)

Defines the default #link("/docs/reference/model/terms/#parameters-spacing")[spacing] of the term list. If it is `false`, the items are spaced apart with #link("/docs/reference/model/par/#parameters-spacing")[paragraph spacing]. If it is `true`, they use #link("/docs/reference/model/par/#parameters-leading")[paragraph leading] instead. This makes the list more compact, which can look better if the items are short.

In markup mode, the value of this parameter is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`. The markup-defined tightness cannot be overridden with set rules.

Default: `true`

*Example:*
```typst
/ Fact: If a term list has a lot
  of text, and maybe other inline
  content, it should not be tight
  anymore.

/ Tip: To make it wide, simply
  insert a blank line between the
  items.
```

=== `separator`: content (Settable)

The separator between the item and the description.

If you want to just separate them with a certain amount of space, use `h(2cm, weak: true)` as the separator and replace `2cm` with your desired amount of space.

Default: `h(amount: 0.6em, weak: true)`

*Example:*
```typst
#set terms(separator: [: ])

/ Colon: A nice separator symbol.
```

=== `indent`: length (Settable)

The indentation of each item.

Default: `0pt`

=== `hanging-indent`: length (Settable)

The hanging indent of the description.

This is in addition to the whole item's `indent`.

Default: `2em`

*Example:*
```typst
#set terms(hanging-indent: 0pt)
/ Term: This term list does not
  make use of hanging indents.
```

=== `spacing`: auto | length (Settable)

The spacing between the items of the term list.

If set to `auto`, uses paragraph #link("/docs/reference/model/par/#parameters-leading")[leading] for tight term lists and paragraph #link("/docs/reference/model/par/#parameters-spacing")[spacing] for wide (non-tight) term lists.

Default: `auto`

=== `children`: content | array (Required, Positional, Variadic)

The term list's children.

When using the term list syntax, adjacent items are automatically collected into term lists, even through constructs like for loops.

*Example:*
```typst
#for (year, product) in (
  "1978": "TeX",
  "1984": "LaTeX",
  "2019": "Typst",
) [/ #product: Born in #year.]
```

== Definitions

=== `item`

A term list item.

```
item(
  content: content,
  content: content
) -> content
```

==== `term`: content (Required, Positional)

The term described by the list item.

==== `description`: content (Required, Positional)

The description of the term.
