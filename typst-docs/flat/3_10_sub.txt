= sub

Renders text in subscript.

The text is rendered smaller and its baseline is lowered.

== Example

```typst
Revenue#sub[yearly]
```

== Parameters

```
sub(
  typographic: bool,
  baseline: length,
  size: length,
  content: content
) -> content
```

=== `typographic`: bool (Settable)

Whether to prefer the dedicated subscript characters of the font.

If this is enabled, Typst first tries to transform the text to subscript codepoints. If that fails, it falls back to rendering lowered and shrunk normal letters.

Default: `true`

*Example:*
```typst
N#sub(typographic: true)[1]
N#sub(typographic: false)[1]
```

=== `baseline`: length (Settable)

The baseline shift for synthetic subscripts. Does not apply if `typographic` is true and the font has subscript codepoints for the given `body`.

Default: `0.2em`

=== `size`: length (Settable)

The font size for synthetic subscripts. Does not apply if `typographic` is true and the font has subscript codepoints for the given `body`.

Default: `0.6em`

=== `body`: content (Required, Positional)

The text to display in subscript.
