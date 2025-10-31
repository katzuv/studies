= raw

Raw text with optional syntax highlighting.

Displays the text verbatim and in a monospace font. This is typically used to embed computer code into your document.

== Example

```typst
Adding `rbx` to `rcx` gives
the desired result.

What is ```rust fn main()``` in Rust
would be ```c int main()``` in C.

```rust
fn main() {
    println!("Hello World!");
}
```

This has ``` `backticks` ``` in it
(but the spaces are trimmed). And
``` here``` the leading space is
also trimmed.
```

You can also construct a #link("/docs/reference/text/raw/")[raw] element programmatically from a string (and provide the language tag via the optional #link("/docs/reference/text/raw/#parameters-lang")[lang] argument).

```typst
#raw("fn " + "main() {}", lang: "rust")
```

== Syntax

This function also has dedicated syntax. You can enclose text in 1 or 3+ backticks (```) to make it raw. Two backticks produce empty raw text. This works both in markup and code.

When you use three or more backticks, you can additionally specify a language tag for syntax highlighting directly after the opening backticks. Within raw blocks, everything (except for the language tag, if applicable) is rendered as is, in particular, there are no escape sequences.

The language tag is an identifier that directly follows the opening backticks only if there are three or more backticks. If your text starts with something that looks like an identifier, but no syntax highlighting is needed, start the text with a single space (which will be trimmed) or use the single backtick syntax. If your text should start or end with a backtick, put a space before or after it (it will be trimmed).

== Parameters

```
raw(
  str: str,
  block: bool,
  lang: none | str,
  align: alignment,
  syntaxes: str | bytes | array,
  theme: none | auto | str | bytes,
  tab-size: int
) -> content
```

=== `text`: str (Required, Positional)

The raw text.

You can also use raw blocks creatively to create custom syntaxes for your automations.

*Example:*
```typst
// Parse numbers in raw blocks with the
// `mydsl` tag and sum them up.
#show raw.where(lang: "mydsl"): it => {
  let sum = 0
  for part in it.text.split("+") {
    sum += int(part.trim())
  }
  sum
}

```mydsl
1 + 2 + 3 + 4 + 5
```
```

=== `block`: bool (Settable)

Whether the raw text is displayed as a separate block.

In markup mode, using one-backtick notation makes this `false`. Using three-backtick notation makes it `true` if the enclosed content contains at least one line break.

Default: `false`

*Example:*
```typst
// Display inline code in a small box
// that retains the correct baseline.
#show raw.where(block: false): box.with(
  fill: luma(240),
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

// Display block code in a larger block
// with more padding.
#show raw.where(block: true): block.with(
  fill: luma(240),
  inset: 10pt,
  radius: 4pt,
)

With `rg`, you can search through your files quickly.
This example searches the current directory recursively
for the text `Hello World`:

```bash
rg "Hello World"
```
```

=== `lang`: none | str (Settable)

The language to syntax-highlight in.

Apart from typical language tags known from Markdown, this supports the `"typ"`, `"typc"`, and `"typm"` tags for #link("/docs/reference/syntax/#markup")[Typst markup], #link("/docs/reference/syntax/#code")[Typst code], and #link("/docs/reference/syntax/#math")[Typst math], respectively.

Default: `none`

*Example:*
```typst
```typ
This is *Typst!*
```

This is ```typ also *Typst*```, but inline!
```

=== `align`: alignment (Settable)

The horizontal alignment that each line in a raw block should have. This option is ignored if this is not a raw block (if specified `block: false` or single backticks were used in markup mode).

By default, this is set to `start`, meaning that raw text is aligned towards the start of the text direction inside the block by default, regardless of the current context's alignment (allowing you to center the raw block itself without centering the text inside it, for example).

Default: `start`

*Example:*
```typst
#set raw(align: center)

```typc
let f(x) = x
code = "centered"
```
```

=== `syntaxes`: str | bytes | array (Settable)

Additional syntax definitions to load. The syntax definitions should be in the #link("https://www.sublimetext.com/docs/syntax.html")[sublime-syntax file format].

You can pass any of the following values:

- A path string to load a syntax file from the given path. For more details about paths, see the #link("/docs/reference/syntax/#paths")[Paths section].
- Raw bytes from which the syntax should be decoded.
- An array where each item is one the above.

Default: `()`

*Example:*
```typst
#set raw(syntaxes: "SExpressions.sublime-syntax")

```sexp
(defun factorial (x)
  (if (zerop x)
    ; with a comment
    1
    (* x (factorial (- x 1)))))
```
```

=== `theme`: none | auto | str | bytes (Settable)

The theme to use for syntax highlighting. Themes should be in the #link("https://www.sublimetext.com/docs/color_schemes_tmtheme.html")[tmTheme file format].

You can pass any of the following values:

- `none`: Disables syntax highlighting.
- `auto`: Highlights with Typst's default theme.
- A path string to load a theme file from the given path. For more details about paths, see the #link("/docs/reference/syntax/#paths")[Paths section].
- Raw bytes from which the theme should be decoded.

Applying a theme only affects the color of specifically highlighted text. It does not consider the theme's foreground and background properties, so that you retain control over the color of raw text. You can apply the foreground color yourself with the #link("/docs/reference/text/text/")[text] function and the background with a #link("/docs/reference/layout/block/#parameters-fill")[filled block]. You could also use the #link("/docs/reference/data-loading/xml/")[xml] function to extract these properties from the theme.

Default: `auto`

*Example:*
```typst
#set raw(theme: "halcyon.tmTheme")
#show raw: it => block(
  fill: rgb("#1d2433"),
  inset: 8pt,
  radius: 5pt,
  text(fill: rgb("#a2aabc"), it)
)

```typ
= Chapter 1
#let hi = "Hello World"
```
```

=== `tab-size`: int (Settable)

The size for a tab stop in spaces. A tab is replaced with enough spaces to align with the next multiple of the size.

Default: `2`

*Example:*
```typst
#set raw(tab-size: 8)
```tsv
Year	Month	Day
2000	2	3
2001	2	1
2002	3	10
```
```

== Definitions

=== `line`

A highlighted line of raw text.

This is a helper element that is synthesized by #link("/docs/reference/text/raw/")[raw] elements.

It allows you to access various properties of the line, such as the line number, the raw non-highlighted text, the highlighted text, and whether it is the first or last line of the raw block.

```
line(
  int: int,
  int: int,
  str: str,
  content: content
) -> content
```

==== `number`: int (Required, Positional)

The line number of the raw line inside of the raw block, starts at 1.

==== `count`: int (Required, Positional)

The total number of lines in the raw block.

==== `text`: str (Required, Positional)

The line of raw text.

==== `body`: content (Required, Positional)

The highlighted raw text.
