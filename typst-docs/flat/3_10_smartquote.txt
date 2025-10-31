= smartquote

A language-aware quote that reacts to its context.

Automatically turns into an appropriate opening or closing quote based on the active #link("/docs/reference/text/text/#parameters-lang")[text language].

== Example

```typst
"This is in quotes."

#set text(lang: "de")
"Das ist in Anführungszeichen."

#set text(lang: "fr")
"C'est entre guillemets."
```

== Syntax

This function also has dedicated syntax: The normal quote characters (`'` and `"`). Typst automatically makes your quotes smart.

== Parameters

```
smartquote(
  double: bool,
  enabled: bool,
  alternative: bool,
  quotes: auto | str | array | dictionary
) -> content
```

=== `double`: bool (Settable)

Whether this should be a double quote.

Default: `true`

=== `enabled`: bool (Settable)

Whether smart quotes are enabled.

To disable smartness for a single quote, you can also escape it with a backslash.

Default: `true`

*Example:*
```typst
#set smartquote(enabled: false)

These are "dumb" quotes.
```

=== `alternative`: bool (Settable)

Whether to use alternative quotes.

Does nothing for languages that don't have alternative quotes, or if explicit quotes were set.

Default: `false`

*Example:*
```typst
#set text(lang: "de")
#set smartquote(alternative: true)

"Das ist in anderen Anführungszeichen."
```

=== `quotes`: auto | str | array | dictionary (Settable)

The quotes to use.

- When set to `auto`, the appropriate single quotes for the #link("/docs/reference/text/text/#parameters-lang")[text language] will be used. This is the default.
- Custom quotes can be passed as a string, array, or dictionary of either string: a string consisting of two characters containing the opening and closing double quotes (characters here refer to Unicode grapheme clusters) array: an array containing the opening and closing double quotes dictionary: an array containing the double and single quotes, each specified as either auto, string, or array

Default: `auto`

*Example:*
```typst
#set text(lang: "de")
'Das sind normale Anführungszeichen.'

#set smartquote(quotes: "()")
"Das sind eigene Anführungszeichen."

#set smartquote(quotes: (single: ("[[", "]]"),  double: auto))
'Das sind eigene Anführungszeichen.'
```
