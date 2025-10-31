= rotate

Rotates content without affecting layout.

Rotates an element by a given angle. The layout will act as if the element was not rotated unless you specify `reflow: true`.

== Example

```typst
#stack(
  dir: ltr,
  spacing: 1fr,
  ..range(16)
    .map(i => rotate(24deg * i)[X]),
)
```

== Parameters

```
rotate(
  angle: angle,
  origin: alignment,
  reflow: bool,
  content: content
) -> content
```

=== `angle`: angle (Positional, Settable)

The amount of rotation.

Default: `0deg`

*Example:*
```typst
#rotate(-1.571rad)[Space!]
```

=== `origin`: alignment (Settable)

The origin of the rotation.

If, for instance, you wanted the bottom left corner of the rotated element to stay aligned with the baseline, you would set it to `bottom + left` instead.

Default: `center + horizon`

*Example:*
```typst
#set text(spacing: 8pt)
#let square = square.with(width: 8pt)

#box(square())
#box(rotate(30deg, origin: center, square()))
#box(rotate(30deg, origin: top + left, square()))
#box(rotate(30deg, origin: bottom + right, square()))
```

=== `reflow`: bool (Settable)

Whether the rotation impacts the layout.

If set to `false`, the rotated content will retain the bounding box of the original content. If set to `true`, the bounding box will take the rotation of the content into account and adjust the layout accordingly.

Default: `false`

*Example:*
```typst
Hello #rotate(90deg, reflow: true)[World]!
```

=== `body`: content (Required, Positional)

The content to rotate.
