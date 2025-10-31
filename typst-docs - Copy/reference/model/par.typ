= par

A logical subdivison of textual content.

Typst automatically collects _inline-level_ elements into paragraphs. Inline-level elements include #link("/docs/reference/text/text/")[text], #link("/docs/reference/layout/h/")[horizontal spacing], #link("/docs/reference/layout/box/")[boxes], and #link("/docs/reference/math/equation/")[inline equations].

To separate paragraphs, use a blank line (or an explicit #link("/docs/reference/model/parbreak/")[parbreak]). Paragraphs are also automatically interrupted by any block-level element (like #link("/docs/reference/layout/block/")[block], #link("/docs/reference/layout/place/")[place], or anything that shows itself as one of these).

The `par` element is primarily used in set rules to affect paragraph properties, but it can also be used to explicitly display its argument as a paragraph of its own. Then, the paragraph's body may not contain any block-level content.

== Boxes and blocks

As explained above, usually paragraphs only contain inline-level content. However, you can integrate any kind of block-level content into a paragraph by wrapping it in a #link("/docs/reference/layout/box/")[box].

Conversely, you can separate inline-level content from a paragraph by wrapping it in a #link("/docs/reference/layout/block/")[block]. In this case, it will not become part of any paragraph at all. Read the following section for an explanation of why that matters and how it differs from just adding paragraph breaks around the content.

== What becomes a paragraph?

When you add inline-level content to your document, Typst will automatically wrap it in paragraphs. However, a typical document also contains some text that is not semantically part of a paragraph, for example in a heading or caption.

The rules for when Typst wraps inline-level content in a paragraph are as follows:

- All text at the root of a document is wrapped in paragraphs.
- Text in a container (like a block) is only wrapped in a paragraph if the container holds any block-level content. If all of the contents are inline-level, no paragraph is created.

In the laid-out document, it's not immediately visible whether text became part of a paragraph. However, it is still important for various reasons:

- Certain paragraph styling like first-line-indent will only apply to proper paragraphs, not any text. Similarly, par show rules of course only trigger on paragraphs.
- A proper distinction between paragraphs and other text helps people who rely on assistive technologies (such as screen readers) navigate and understand the document properly. Currently, this only applies to HTML export since Typst does not yet output accessible PDFs, but support for this is planned for the near future.
- HTML export will generate a <p> tag only for paragraphs.

When creating custom reusable components, you can and should take charge over whether Typst creates paragraphs. By wrapping text in a #link("/docs/reference/layout/block/")[block] instead of just adding paragraph breaks around it, you can force the absence of a paragraph. Conversely, by adding a #link("/docs/reference/model/parbreak/")[parbreak] after some content in a container, you can force it to become a paragraph even if it's just one word. This is, for example, what #link("/docs/reference/model/list/#parameters-tight")[non-tight] lists do to force their items to become paragraphs.

== Example

```typst
#set par(
  first-line-indent: 1em,
  spacing: 0.65em,
  justify: true,
)

We proceed by contradiction.
Suppose that there exists a set
of positive integers $a$, $b$, and
$c$ that satisfies the equation
$a^n + b^n = c^n$ for some
integer value of $n > 2$.

Without loss of generality,
let $a$ be the smallest of the
three integers. Then, we ...
```

== Parameters

```
par(
  leading: length,
  spacing: length,
  justify: bool,
  linebreaks: auto | str,
  first-line-indent: length | dictionary,
  hanging-indent: length,
  content: content
) -> content
```

=== `leading`: length (Settable)

The spacing between lines.

Leading defines the spacing between the #link("/docs/reference/text/text/#parameters-bottom-edge")[bottom edge] of one line and the #link("/docs/reference/text/text/#parameters-top-edge")[top edge] of the following line. By default, these two properties are up to the font, but they can also be configured manually with a text set rule.

By setting top edge, bottom edge, and leading, you can also configure a consistent baseline-to-baseline distance. You could, for instance, set the leading to `1em`, the top-edge to `0.8em`, and the bottom-edge to `-0.2em` to get a baseline gap of exactly `2em`. The exact distribution of the top- and bottom-edge values affects the bounds of the first and last line.

Default: `0.65em`

=== `spacing`: length (Settable)

The spacing between paragraphs.

Just like leading, this defines the spacing between the bottom edge of a paragraph's last line and the top edge of the next paragraph's first line.

When a paragraph is adjacent to a #link("/docs/reference/layout/block/")[block] that is not a paragraph, that block's #link("/docs/reference/layout/block/#parameters-above")[above] or #link("/docs/reference/layout/block/#parameters-below")[below] property takes precedence over the paragraph spacing. Headings, for instance, reduce the spacing below them by default for a better look.

Default: `1.2em`

=== `justify`: bool (Settable)

Whether to justify text in its line.

Hyphenation will be enabled for justified paragraphs if the #link("/docs/reference/text/text/#parameters-hyphenate")[text function's hyphenate property] is set to `auto` and the current language is known.

Note that the current #link("/docs/reference/layout/align/#parameters-alignment")[alignment] still has an effect on the placement of the last line except if it ends with a #link("/docs/reference/text/linebreak/#parameters-justify")[justified line break].

Default: `false`

=== `linebreaks`: auto | str (Settable)

How to determine line breaks.

When this property is set to `auto`, its default value, optimized line breaks will be used for justified paragraphs. Enabling optimized line breaks for ragged paragraphs may also be worthwhile to improve the appearance of the text.

Default: `auto`

*Example:*
```typst
#set page(width: 207pt)
#set par(linebreaks: "simple")
Some texts feature many longer
words. Those are often exceedingly
challenging to break in a visually
pleasing way.

#set par(linebreaks: "optimized")
Some texts feature many longer
words. Those are often exceedingly
challenging to break in a visually
pleasing way.
```

=== `first-line-indent`: length | dictionary (Settable)

The indent the first line of a paragraph should have.

By default, only the first line of a consecutive paragraph will be indented (not the first one in the document or container, and not paragraphs immediately following other block-level elements).

If you want to indent all paragraphs instead, you can pass a dictionary containing the `amount` of indent as a length and the pair `all: true`. When `all` is omitted from the dictionary, it defaults to `false`.

By typographic convention, paragraph breaks are indicated either by some space between paragraphs or by indented first lines. Consider

- reducing the #link("/docs/reference/model/par/#parameters-spacing")[paragraph spacing] to the #link("/docs/reference/model/par/#parameters-leading")[leading] using `set par(spacing: 0.65em)`
- increasing the #link("/docs/reference/layout/block/#parameters-spacing")[block spacing] (which inherits the paragraph spacing by default) to the original paragraph spacing using `set block(spacing: 1.2em)`

Default: `(amount: 0pt, all: false)`

*Example:*
```typst
#set block(spacing: 1.2em)
#set par(
  first-line-indent: 1.5em,
  spacing: 0.65em,
)

The first paragraph is not affected
by the indent.

But the second paragraph is.

#line(length: 100%)

#set par(first-line-indent: (
  amount: 1.5em,
  all: true,
))

Now all paragraphs are affected
by the first line indent.

Even the first one.
```

=== `hanging-indent`: length (Settable)

The indent that all but the first line of a paragraph should have.

Default: `0pt`

*Example:*
```typst
#set par(hanging-indent: 1em)

#lorem(15)
```

=== `body`: content (Required, Positional)

The contents of the paragraph.

== Definitions

=== `line`

A paragraph line.

This element is exclusively used for line number configuration through set rules and cannot be placed.

The #link("/docs/reference/model/par/#definitions-line-numbering")[numbering] option is used to enable line numbers by specifying a numbering format.

```
line(
  numbering: none | str | function,
  number-align: auto | alignment,
  number-margin: alignment,
  number-clearance: auto | length,
  numbering-scope: str
) -> content
```

```typst
#set par.line(numbering: "1")

Roses are red. \
Violets are blue. \
Typst is there for you.
```

The `numbering` option takes either a predefined #link("/docs/reference/model/numbering/")[numbering pattern] or a function returning styled content. You can disable line numbers for text inside certain elements by setting the numbering to `none` using show-set rules.

```typst
// Styled red line numbers.
#set par.line(
  numbering: n => text(red)[#n]
)

// Disable numbers inside figures.
#show figure: set par.line(
  numbering: none
)

Roses are red. \
Violets are blue.

#figure(
  caption: [Without line numbers.]
)[
  Lorem ipsum \
  dolor sit amet
]

The text above is a sample \
originating from distant times.
```

This element exposes further options which may be used to control other aspects of line numbering, such as its #link("/docs/reference/model/par/#definitions-line-number-align")[alignment] or #link("/docs/reference/model/par/#definitions-line-number-margin")[margin]. In addition, you can control whether the numbering is reset on each page through the #link("/docs/reference/model/par/#definitions-line-numbering-scope")[numbering-scope] option.

==== `numbering`: none | str | function (Settable)

How to number each line. Accepts a #link("/docs/reference/model/numbering/")[numbering pattern or function].

Default: `none`

*Example:*
```typst
#set par.line(numbering: "I")

Roses are red. \
Violets are blue. \
Typst is there for you.
```

==== `number-align`: auto | alignment (Settable)

The alignment of line numbers associated with each line.

The default of `auto` indicates a smart default where numbers grow horizontally away from the text, considering the margin they're in and the current text direction.

Default: `auto`

*Example:*
```typst
#set par.line(
  numbering: "I",
  number-align: left,
)

Hello world! \
Today is a beautiful day \
For exploring the world.
```

==== `number-margin`: alignment (Settable)

The margin at which line numbers appear.

_Note:_ In a multi-column document, the line numbers for paragraphs inside the last column will always appear on the `end` margin (right margin for left-to-right text and left margin for right-to-left), regardless of this configuration. That behavior cannot be changed at this moment.

Default: `start`

*Example:*
```typst
#set par.line(
  numbering: "1",
  number-margin: right,
)

= Report
- Brightness: Dark, yet darker
- Readings: Negative
```

==== `number-clearance`: auto | length (Settable)

The distance between line numbers and text.

The default value of `auto` results in a clearance that is adaptive to the page width and yields reasonable results in most cases.

Default: `auto`

*Example:*
```typst
#set par.line(
  numbering: "1",
  number-clearance: 4pt,
)

Typesetting \
Styling \
Layout
```

==== `numbering-scope`: str (Settable)

Controls when to reset line numbering.

_Note:_ The line numbering scope must be uniform across each page run (a page run is a sequence of pages without an explicit pagebreak in between). For this reason, set rules for it should be defined before any page content, typically at the very start of the document.

Default: `"document"`

*Example:*
```typst
#set par.line(
  numbering: "1",
  numbering-scope: "page",
)

First line \
Second line
#pagebreak()
First line again \
Second line again
```
