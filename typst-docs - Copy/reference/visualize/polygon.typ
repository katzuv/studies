= polygon

A closed polygon.

The polygon is defined by its corner points and is closed automatically.

== Example

```typst
#polygon(
  fill: blue.lighten(80%),
  stroke: blue,
  (20%, 0pt),
  (60%, 0pt),
  (80%, 2cm),
  (0%,  2cm),
)
```

== Parameters

```
polygon(
  fill: none | color | gradient | tiling,
  fill-rule: str,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  ..: array
) -> content
```

=== `fill`: none | color | gradient | tiling (Settable)

How to fill the polygon.

When setting a fill, the default stroke disappears. To create a rectangle with both fill and stroke, you have to configure both.

Default: `none`

=== `fill-rule`: str (Settable)

The drawing rule used to fill the polygon.

See the #link("/docs/reference/visualize/curve/#parameters-fill-rule")[curve documentation] for an example.

Default: `"non-zero"`

=== `stroke`: none | auto | length | color | gradient | stroke | tiling | dictionary (Settable)

How to #link("/docs/reference/visualize/stroke/")[stroke] the polygon. This can be:

Can be set to `none` to disable the stroke or to `auto` for a stroke of `1pt` black if and if only if no fill is given.

Default: `auto`

=== `vertices`: array (Required, Positional, Variadic)

The vertices of the polygon. Each point is specified as an array of two #link("/docs/reference/layout/relative/")[relative lengths].

== Definitions

=== `regular`

A regular polygon, defined by its size and number of vertices.

```
regular(
  fill: none | color | gradient | tiling,
  stroke: none | auto | length | color | gradient | stroke | tiling | dictionary,
  size: length,
  vertices: int
) -> content
```

```typst
#polygon.regular(
  fill: blue.lighten(80%),
  stroke: blue,
  size: 30pt,
  vertices: 3,
)
```

==== `fill`: none | color | gradient | tiling

How to fill the polygon. See the general #link("/docs/reference/visualize/polygon/#parameters-fill")[polygon's documentation] for more details.

==== `stroke`: none | auto | length | color | gradient | stroke | tiling | dictionary

How to stroke the polygon. See the general #link("/docs/reference/visualize/polygon/#parameters-stroke")[polygon's documentation] for more details.

==== `size`: length

The diameter of the #link("https://en.wikipedia.org/wiki/Circumcircle")[circumcircle] of the regular polygon.

Default: `1em`

==== `vertices`: int

The number of vertices in the polygon.

Default: `3`
