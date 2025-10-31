= scale

Scales content without affecting layout.

Lets you mirror content by specifying a negative scale on a single axis.

== Example

```typst
#set align(center)
#scale(x: -100%)[This is mirrored.]
#scale(x: -100%, reflow: true)[This is mirrored.]
```

== Parameters

```
scale(
  factor: auto | length | ratio,
  x: auto | length | ratio,
  y: auto | length | ratio,
  origin: alignment,
  reflow: bool,
  content: content
) -> content
```

=== `factor`: auto | length | ratio (Positional, Settable)

The scaling factor for both axes, as a positional argument. This is just an optional shorthand notation for setting `x` and `y` to the same value.

Default: `100%`

=== `x`: auto | length | ratio (Settable)

The horizontal scaling factor.

The body will be mirrored horizontally if the parameter is negative.

Default: `100%`

=== `y`: auto | length | ratio (Settable)

The vertical scaling factor.

The body will be mirrored vertically if the parameter is negative.

Default: `100%`

=== `origin`: alignment (Settable)

The origin of the transformation.

Default: `center + horizon`

*Example:*
```typst
A#box(scale(75%)[A])A \
B#box(scale(75%, origin: bottom + left)[B])B
```

=== `reflow`: bool (Settable)

Whether the scaling impacts the layout.

If set to `false`, the scaled content will be allowed to overlap other content. If set to `true`, it will compute the new size of the scaled content and adjust the layout accordingly.

Default: `false`

*Example:*
```typst
Hello #scale(x: 20%, y: 40%, reflow: true)[World]!
```

=== `body`: content (Required, Positional)

The content to scale.
