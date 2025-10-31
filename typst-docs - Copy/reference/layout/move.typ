= move

Moves content without affecting layout.

The `move` function allows you to move content while the layout still 'sees' it at the original positions. Containers will still be sized as if the content was not moved.

== Example

```typst
#rect(inset: 0pt, move(
  dx: 6pt, dy: 6pt,
  rect(
    inset: 8pt,
    fill: white,
    stroke: black,
    [Abra cadabra]
  )
))
```

== Parameters

```
move(
  dx: relative,
  dy: relative,
  content: content
) -> content
```

=== `dx`: relative (Settable)

The horizontal displacement of the content.

Default: `0% + 0pt`

=== `dy`: relative (Settable)

The vertical displacement of the content.

Default: `0% + 0pt`

=== `body`: content (Required, Positional)

The content to move.
