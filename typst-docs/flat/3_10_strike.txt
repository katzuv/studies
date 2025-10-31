= strike

Strikes through text.

== Example

```typst
This is #strike[not] relevant.
```

== Parameters

```
strike(
  stroke: auto | length | color | gradient | stroke | tiling | dictionary,
  offset: auto | length,
  extent: length,
  background: bool,
  content: content
) -> content
```

=== `stroke`: auto | length | color | gradient | stroke | tiling | dictionary (Settable)

How to #link("/docs/reference/visualize/stroke/")[stroke] the line.

If set to `auto`, takes on the text's color and a thickness defined in the current font.

_Note:_ Please don't use this for real redaction as you can still copy paste the text.

Default: `auto`

*Example:*
```typst
This is #strike(stroke: 1.5pt + red)[very stricken through]. \
This is #strike(stroke: 10pt)[redacted].
```

=== `offset`: auto | length (Settable)

The position of the line relative to the baseline. Read from the font tables if `auto`.

This is useful if you are unhappy with the offset your font provides.

Default: `auto`

*Example:*
```typst
#set text(font: "Inria Serif")
This is #strike(offset: auto)[low-ish]. \
This is #strike(offset: -3.5pt)[on-top].
```

=== `extent`: length (Settable)

The amount by which to extend the line beyond (or within if negative) the content.

Default: `0pt`

*Example:*
```typst
This #strike(extent: -2pt)[skips] parts of the word.
This #strike(extent: 2pt)[extends] beyond the word.
```

=== `background`: bool (Settable)

Whether the line is placed behind the content.

Default: `false`

*Example:*
```typst
#set strike(stroke: red)
#strike(background: true)[This is behind.] \
#strike(background: false)[This is in front.]
```

=== `body`: content (Required, Positional)

The content to strike through.
