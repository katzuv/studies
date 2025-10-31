= image

A raster or vector graphic.

You can wrap the image in a #link("/docs/reference/model/figure/")[figure] to give it a number and caption.

Like most elements, images are _block-level_ by default and thus do not integrate themselves into adjacent paragraphs. To force an image to become inline, put it into a #link("/docs/reference/layout/box/")[box].

== Example

```typst
#figure(
  image("molecular.jpg", width: 80%),
  caption: [
    A step in the molecular testing
    pipeline of our lab.
  ],
)
```

== Parameters

```
image(
  str: str | bytes,
  format: auto | str | dictionary,
  width: auto | relative,
  height: auto | relative | fraction,
  alt: none | str,
  fit: str,
  scaling: auto | str,
  icc: auto | str | bytes
) -> content
```

=== `source`: str | bytes (Required, Positional)

A #link("/docs/reference/syntax/#paths")[path] to an image file or raw bytes making up an image in one of the supported #link("/docs/reference/visualize/image/#parameters-format")[formats].

Bytes can be used to specify raw pixel data in a row-major, left-to-right, top-to-bottom format.

*Example:*
```typst
#let original = read("diagram.svg")
#let changed = original.replace(
  "#2B80FF", // blue
  green.to-hex(),
)

#image(bytes(original))
#image(bytes(changed))
```

=== `format`: auto | str | dictionary (Settable)

The image's format.

By default, the format is detected automatically. Typically, you thus only need to specify this when providing raw bytes as the #link("/docs/reference/visualize/image/#parameters-source")[source] (even then, Typst will try to figure out the format automatically, but that's not always possible).

Supported formats are `"png"`, `"jpg"`, `"gif"`, `"svg"` as well as raw pixel data. Embedding PDFs as images is #link("https://github.com/typst/typst/issues/145")[not currently supported].

When providing raw pixel data as the `source`, you must specify a dictionary with the following keys as the `format`:

- `encoding` (#link("/docs/reference/foundations/str/")[str]): The encoding of the pixel data. One of: "rgb8" (three 8-bit channels: red, green, blue) "rgba8" (four 8-bit channels: red, green, blue, alpha) "luma8" (one 8-bit channel) "lumaa8" (two 8-bit channels: luma and alpha)
- `width` (#link("/docs/reference/foundations/int/")[int]): The pixel width of the image.
- `height` (#link("/docs/reference/foundations/int/")[int]): The pixel height of the image.

The pixel width multiplied by the height multiplied by the channel count for the specified encoding must then match the `source` data.

Default: `auto`

*Example:*
```typst
#image(
  read(
    "tetrahedron.svg",
    encoding: none,
  ),
  format: "svg",
  width: 2cm,
)

#image(
  bytes(range(16).map(x => x * 16)),
  format: (
    encoding: "luma8",
    width: 4,
    height: 4,
  ),
  width: 2cm,
)
```

=== `width`: auto | relative (Settable)

The width of the image.

Default: `auto`

=== `height`: auto | relative | fraction (Settable)

The height of the image.

Default: `auto`

=== `alt`: none | str (Settable)

A text describing the image.

Default: `none`

=== `fit`: str (Settable)

How the image should adjust itself to a given area (the area is defined by the `width` and `height` fields). Note that `fit` doesn't visually change anything if the area's aspect ratio is the same as the image's one.

Default: `"cover"`

*Example:*
```typst
#set page(width: 300pt, height: 50pt, margin: 10pt)
#image("tiger.jpg", width: 100%, fit: "cover")
#image("tiger.jpg", width: 100%, fit: "contain")
#image("tiger.jpg", width: 100%, fit: "stretch")
```

=== `scaling`: auto | str (Settable)

A hint to viewers how they should scale the image.

When set to `auto`, the default is left up to the viewer. For PNG export, Typst will default to smooth scaling, like most PDF and SVG viewers.

_Note:_ The exact look may differ across PDF viewers.

Default: `auto`

=== `icc`: auto | str | bytes (Settable)

An ICC profile for the image.

ICC profiles define how to interpret the colors in an image. When set to `auto`, Typst will try to extract an ICC profile from the image.

Default: `auto`

== Definitions

=== `decode`

Decode a raster or vector graphic from bytes or a string.

```
decode(
  str: str | bytes,
  format: auto | str | dictionary,
  width: auto | relative,
  height: auto | relative | fraction,
  alt: none | str,
  fit: str,
  scaling: auto | str
) -> content
```

==== `data`: str | bytes (Required, Positional)

The data to decode as an image. Can be a string for SVGs.

==== `format`: auto | str | dictionary

The image's format. Detected automatically by default.

==== `width`: auto | relative

The width of the image.

==== `height`: auto | relative | fraction

The height of the image.

==== `alt`: none | str

A text describing the image.

==== `fit`: str

How the image should adjust itself to a given area.

==== `scaling`: auto | str

A hint to viewers how they should scale the image.
