= highlight

Highlights text with a background color.

== Example

```typst
This is #highlight[important].
```

== Parameters

```
highlight(
  fill: none | color | gradient | tiling,
  stroke: none | length | color | gradient | stroke | tiling | dictionary,
  top-edge: length | str,
  bottom-edge: length | str,
  extent: length,
  radius: relative | dictionary,
  content: content
) -> content
```

=== `fill`: none | color | gradient | tiling (Settable)

The color to highlight the text with.

Default: `rgb("#fffd11a1")`

*Example:*
```typst
This is #highlight(
  fill: blue
)[highlighted with blue].
```

=== `stroke`: none | length | color | gradient | stroke | tiling | dictionary (Settable)

The highlight's border color. See the #link("/docs/reference/visualize/rect/#parameters-stroke")[rectangle's documentation] for more details.

Default: `(:)`

*Example:*
```typst
This is a #highlight(
  stroke: fuchsia
)[stroked highlighting].
```

=== `top-edge`: length | str (Settable)

The top end of the background rectangle.

Default: `"ascender"`

*Example:*
```typst
#set highlight(top-edge: "ascender")
#highlight[a] #highlight[aib]

#set highlight(top-edge: "x-height")
#highlight[a] #highlight[aib]
```

=== `bottom-edge`: length | str (Settable)

The bottom end of the background rectangle.

Default: `"descender"`

*Example:*
```typst
#set highlight(bottom-edge: "descender")
#highlight[a] #highlight[ap]

#set highlight(bottom-edge: "baseline")
#highlight[a] #highlight[ap]
```

=== `extent`: length (Settable)

The amount by which to extend the background to the sides beyond (or within if negative) the content.

Default: `0pt`

*Example:*
```typst
A long #highlight(extent: 4pt)[background].
```

=== `radius`: relative | dictionary (Settable)

How much to round the highlight's corners. See the #link("/docs/reference/visualize/rect/#parameters-radius")[rectangle's documentation] for more details.

Default: `(:)`

*Example:*
```typst
Listen #highlight(
  radius: 5pt, extent: 2pt
)[carefully], it will be on the test.
```

=== `body`: content (Required, Positional)

The content that should be highlighted.
