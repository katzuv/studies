= figure

A figure with an optional caption.

Automatically detects its kind to select the correct counting track. For example, figures containing images will be numbered separately from figures containing tables.

== Examples

The example below shows a basic figure with an image:

```typst
@glacier shows a glacier. Glaciers
are complex systems.

#figure(
  image("glacier.jpg", width: 80%),
  caption: [A curious figure.],
) <glacier>
```

You can also insert #link("/docs/reference/model/table/")[tables] into figures to give them a caption. The figure will detect this and automatically use a separate counter.

```typst
#figure(
  table(
    columns: 4,
    [t], [1], [2], [3],
    [y], [0.3s], [0.4s], [0.8s],
  ),
  caption: [Timing results],
)
```

This behaviour can be overridden by explicitly specifying the figure's `kind`. All figures of the same kind share a common counter.

== Figure behaviour

By default, figures are placed within the flow of content. To make them float to the top or bottom of the page, you can use the #link("/docs/reference/model/figure/#parameters-placement")[placement] argument.

If your figure is too large and its contents are breakable across pages (e.g. if it contains a large table), then you can make the figure itself breakable across pages as well with this show rule:

See the #link("/docs/reference/layout/block/#parameters-breakable")[block] documentation for more information about breakable and non-breakable blocks.

== Caption customization

You can modify the appearance of the figure's caption with its associated #link("/docs/reference/model/figure/#definitions-caption")[caption] function. In the example below, we emphasize all captions:

```typst
#show figure.caption: emph

#figure(
  rect[Hello],
  caption: [I am emphasized!],
)
```

By using a #link("/docs/reference/foundations/function/#definitions-where")[where] selector, we can scope such rules to specific kinds of figures. For example, to position the caption above tables, but keep it below for all other kinds of figures, we could write the following show-set rule:

```typst
#show figure.where(
  kind: table
): set figure.caption(position: top)

#figure(
  table(columns: 2)[A][B][C][D],
  caption: [I'm up here],
)
```

== Parameters

```
figure(
  content: content,
  placement: none | auto | alignment,
  scope: str,
  caption: none | content,
  kind: auto | str | function,
  supplement: none | auto | content | function,
  numbering: none | str | function,
  gap: length,
  outlined: bool
) -> content
```

=== `body`: content (Required, Positional)

The content of the figure. Often, an #link("/docs/reference/visualize/image/")[image].

=== `placement`: none | auto | alignment (Settable)

The figure's placement on the page.

- `none`: The figure stays in-flow exactly where it was specified like other content.
- `auto`: The figure picks `top` or `bottom` depending on which is closer.
- `top`: The figure floats to the top of the page.
- `bottom`: The figure floats to the bottom of the page.

The gap between the main flow content and the floating figure is controlled by the #link("/docs/reference/layout/place/#parameters-clearance")[clearance] argument on the `place` function.

Default: `none`

*Example:*
```typst
#set page(height: 200pt)

= Introduction
#figure(
  placement: bottom,
  caption: [A glacier],
  image("glacier.jpg", width: 60%),
)
#lorem(60)
```

=== `scope`: str (Settable)

Relative to which containing scope the figure is placed.

Set this to `"parent"` to create a full-width figure in a two-column document.

Has no effect if `placement` is `none`.

Default: `"column"`

*Example:*
```typst
#set page(height: 250pt, columns: 2)

= Introduction
#figure(
  placement: bottom,
  scope: "parent",
  caption: [A glacier],
  image("glacier.jpg", width: 60%),
)
#lorem(60)
```

=== `caption`: none | content (Settable)

The figure's caption.

Default: `none`

=== `kind`: auto | str | function (Settable)

The kind of figure this is.

All figures of the same kind share a common counter.

If set to `auto`, the figure will try to automatically determine its kind based on the type of its body. Automatically detected kinds are #link("/docs/reference/model/table/")[tables] and #link("/docs/reference/text/raw/")[code]. In other cases, the inferred kind is that of an #link("/docs/reference/visualize/image/")[image].

Setting this to something other than `auto` will override the automatic detection. This can be useful if

- you wish to create a custom figure type that is not an #link("/docs/reference/visualize/image/")[image], a #link("/docs/reference/model/table/")[table] or #link("/docs/reference/text/raw/")[code],
- you want to force the figure to use a specific counter regardless of its content.

You can set the kind to be an element function or a string. If you set it to an element function other than #link("/docs/reference/model/table/")[table], #link("/docs/reference/text/raw/")[raw] or #link("/docs/reference/visualize/image/")[image], you will need to manually specify the figure's supplement.

Default: `auto`

*Example:*
```typst
#figure(
  circle(radius: 10pt),
  caption: [A curious atom.],
  kind: "atom",
  supplement: [Atom],
)
```

=== `supplement`: none | auto | content | function (Settable)

The figure's supplement.

If set to `auto`, the figure will try to automatically determine the correct supplement based on the `kind` and the active #link("/docs/reference/text/text/#parameters-lang")[text language]. If you are using a custom figure type, you will need to manually specify the supplement.

If a function is specified, it is passed the first descendant of the specified `kind` (typically, the figure's body) and should return content.

Default: `auto`

*Example:*
```typst
#figure(
  [The contents of my figure!],
  caption: [My custom figure],
  supplement: [Bar],
  kind: "foo",
)
```

=== `numbering`: none | str | function (Settable)

How to number the figure. Accepts a #link("/docs/reference/model/numbering/")[numbering pattern or function].

Default: `"1"`

=== `gap`: length (Settable)

The vertical gap between the body and caption.

Default: `0.65em`

=== `outlined`: bool (Settable)

Whether the figure should appear in an #link("/docs/reference/model/outline/")[outline] of figures.

Default: `true`

== Definitions

=== `caption`

The caption of a figure. This element can be used in set and show rules to customize the appearance of captions for all figures or figures of a specific kind.

In addition to its `pos` and `body`, the `caption` also provides the figure's `kind`, `supplement`, `counter`, and `numbering` as fields. These parts can be used in #link("/docs/reference/foundations/function/#definitions-where")[where] selectors and show rules to build a completely custom caption.

```
caption(
  position: alignment,
  separator: auto | content,
  content: content
) -> content
```

```typst
#show figure.caption: emph

#figure(
  rect[Hello],
  caption: [A rectangle],
)
```

==== `position`: alignment (Settable)

The caption's position in the figure. Either `top` or `bottom`.

Default: `bottom`

*Example:*
```typst
#show figure.where(
  kind: table
): set figure.caption(position: top)

#figure(
  table(columns: 2)[A][B],
  caption: [I'm up here],
)

#figure(
  rect[Hi],
  caption: [I'm down here],
)

#figure(
  table(columns: 2)[A][B],
  caption: figure.caption(
    position: bottom,
    [I'm down here too!]
  )
)
```

==== `separator`: auto | content (Settable)

The separator which will appear between the number and body.

If set to `auto`, the separator will be adapted to the current #link("/docs/reference/text/text/#parameters-lang")[language] and #link("/docs/reference/text/text/#parameters-region")[region].

Default: `auto`

*Example:*
```typst
#set figure.caption(separator: [ --- ])

#figure(
  rect[Hello],
  caption: [A rectangle],
)
```

==== `body`: content (Required, Positional)

The caption's body.

Can be used alongside `kind`, `supplement`, `counter`, `numbering`, and `location` to completely customize the caption.

*Example:*
```typst
#show figure.caption: it => [
  #underline(it.body) |
  #it.supplement
  #context it.counter.display(it.numbering)
]

#figure(
  rect[Hello],
  caption: [A rectangle],
)
```
