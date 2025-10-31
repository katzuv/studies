= line

A line from one point to another.

== Example

```typst
#set page(height: 100pt)

#line(length: 100%)
#line(end: (50%, 50%))
#line(
  length: 4cm,
  stroke: 2pt + maroon,
)
```

== Parameters

```
line(
  start: array,
  end: none | array,
  length: relative,
  angle: angle,
  stroke: length | color | gradient | stroke | tiling | dictionary
) -> content
```

=== `start`: array (Settable)

The start point of the line.

Must be an array of exactly two relative lengths.

Default: `(0% + 0pt, 0% + 0pt)`

=== `end`: none | array (Settable)

The point where the line ends.

Default: `none`

=== `length`: relative (Settable)

The line's length. This is only respected if `end` is `none`.

Default: `0% + 30pt`

=== `angle`: angle (Settable)

The angle at which the line points away from the origin. This is only respected if `end` is `none`.

Default: `0deg`

=== `stroke`: length | color | gradient | stroke | tiling | dictionary (Settable)

How to #link("/docs/reference/visualize/stroke/")[stroke] the line.

Default: `1pt + black`

*Example:*
```typst
#set line(length: 100%)
#stack(
  spacing: 1em,
  line(stroke: 2pt + red),
  line(stroke: (paint: blue, thickness: 4pt, cap: "round")),
  line(stroke: (paint: blue, thickness: 1pt, dash: "dashed")),
  line(stroke: (paint: blue, thickness: 1pt, dash: ("dot", 2pt, 4pt, 2pt))),
)
```
