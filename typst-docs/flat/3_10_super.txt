= super

Renders text in superscript.

The text is rendered smaller and its baseline is raised.

== Example

```typst
1#super[st] try!
```

== Parameters

```
super(
  typographic: bool,
  baseline: length,
  size: length,
  content: content
) -> content
```

=== `typographic`: bool (Settable)

Whether to prefer the dedicated superscript characters of the font.

If this is enabled, Typst first tries to transform the text to superscript codepoints. If that fails, it falls back to rendering raised and shrunk normal letters.

Default: `true`

*Example:*
```typst
N#super(typographic: true)[1]
N#super(typographic: false)[1]
```

=== `baseline`: length (Settable)

The baseline shift for synthetic superscripts. Does not apply if `typographic` is true and the font has superscript codepoints for the given `body`.

Default: `-0.5em`

=== `size`: length (Settable)

The font size for synthetic superscripts. Does not apply if `typographic` is true and the font has superscript codepoints for the given `body`.

Default: `0.6em`

=== `body`: content (Required, Positional)

The text to display in superscript.
