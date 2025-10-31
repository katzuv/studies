= measure

Measures the layouted size of content.

The `measure` function lets you determine the layouted size of content. By default an infinite space is assumed, so the measured dimensions may not necessarily match the final dimensions of the content. If you want to measure in the current layout dimensions, you can combine `measure` and #link("/docs/reference/layout/layout/")[layout].

== Example

The same content can have a different size depending on the #link("/docs/reference/context/")[context] that it is placed into. In the example below, the `#content` is of course bigger when we increase the font size.

```typst
#let content = [Hello!]
#content
#set text(14pt)
#content
```

For this reason, you can only measure when context is available.

```typst
#let thing(body) = context {
  let size = measure(body)
  [Width of "#body" is #size.width]
}

#thing[Hey] \
#thing[Welcome]
```

The measure function returns a dictionary with the entries `width` and `height`, both of type #link("/docs/reference/layout/length/")[length].

== Parameters

```
measure(
  width: auto | length,
  height: auto | length,
  content: content
) -> dictionary
```

=== `width`: auto | length

The width available to layout the content.

Setting this to `auto` indicates infinite available width.

Note that using the `width` and `height` parameters of this function is different from measuring a sized #link("/docs/reference/layout/block/")[block] containing the content. In the following example, the former will get the dimensions of the inner content instead of the dimensions of the block.

Default: `auto`

*Example:*
```typst
#context measure(lorem(100), width: 400pt)

#context measure(block(lorem(100), width: 400pt))
```

=== `height`: auto | length

The height available to layout the content.

Setting this to `auto` indicates infinite available height.

Default: `auto`

=== `content`: content (Required, Positional)

The content whose size to measure.
