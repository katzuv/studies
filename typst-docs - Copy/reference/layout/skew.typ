= skew

Skews content.

Skews an element in horizontal and/or vertical direction. The layout will act as if the element was not skewed unless you specify `reflow: true`.

== Example

```typst
#skew(ax: -12deg)[
  This is some fake italic text.
]
```

== Parameters

```
skew(
  ax: angle,
  ay: angle,
  origin: alignment,
  reflow: bool,
  content: content
) -> content
```

=== `ax`: angle (Settable)

The horizontal skewing angle.

Default: `0deg`

*Example:*
```typst
#skew(ax: 30deg)[Skewed]
```

=== `ay`: angle (Settable)

The vertical skewing angle.

Default: `0deg`

*Example:*
```typst
#skew(ay: 30deg)[Skewed]
```

=== `origin`: alignment (Settable)

The origin of the skew transformation.

The origin will stay fixed during the operation.

Default: `center + horizon`

*Example:*
```typst
X #box(skew(ax: -30deg, origin: center + horizon)[X]) X \
X #box(skew(ax: -30deg, origin: bottom + left)[X]) X \
X #box(skew(ax: -30deg, origin: top + right)[X]) X
```

=== `reflow`: bool (Settable)

Whether the skew transformation impacts the layout.

If set to `false`, the skewed content will retain the bounding box of the original content. If set to `true`, the bounding box will take the transformation of the content into account and adjust the layout accordingly.

Default: `false`

*Example:*
```typst
Hello #skew(ay: 30deg, reflow: true, "World")!
```

=== `body`: content (Required, Positional)

The content to skew.
