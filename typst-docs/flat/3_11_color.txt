= color

A color in a specific color space.

Typst supports:

- sRGB through the #link("/docs/reference/visualize/color/#definitions-rgb")[rgb function]
- Device CMYK through #link("/docs/reference/visualize/color/#definitions-cmyk")[cmyk function]
- D65 Gray through the #link("/docs/reference/visualize/color/#definitions-luma")[luma function]
- Oklab through the #link("/docs/reference/visualize/color/#definitions-oklab")[oklab function]
- Oklch through the #link("/docs/reference/visualize/color/#definitions-oklch")[oklch function]
- Linear RGB through the #link("/docs/reference/visualize/color/#definitions-linear-rgb")[color.linear-rgb function]
- HSL through the #link("/docs/reference/visualize/color/#definitions-hsl")[color.hsl function]
- HSV through the #link("/docs/reference/visualize/color/#definitions-hsv")[color.hsv function]

== Example

```typst
#rect(fill: aqua)
```

== Predefined colors

Typst defines the following built-in colors:

The predefined colors and the most important color constructors are available globally and also in the color type's scope, so you can write either `color.red` or just `red`.

== Predefined color maps

Typst also includes a number of preset color maps that can be used for #link("/docs/reference/visualize/gradient/#definitions-linear")[gradients]. These are simply arrays of colors defined in the module `color.map`.

```typst
#circle(fill: gradient.linear(..color.map.crest))
```

Some popular presets are not included because they are not available under a free licence. Others, like #link("https://jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap/")[Jet], are not included because they are not color blind friendly. Feel free to use or create a package with other presets that are useful to you!

== Definitions

=== `luma`

Create a grayscale color.

A grayscale color is represented internally by a single `lightness` component.

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
luma(
  int: int | ratio,
  ratio: ratio,
  color: color
) -> color
```

```typst
#for x in range(250, step: 50) {
  box(square(fill: luma(x)))
}
```

==== `lightness`: int | ratio (Required, Positional)

The lightness component.

==== `alpha`: ratio (Required, Positional)

The alpha component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to grayscale.

If this is given, the `lightness` should not be given.

=== `oklab`

Create an #link("https://bottosson.github.io/posts/oklab/")[Oklab] color.

This color space is well suited for the following use cases:

- Color manipulation such as saturating while keeping perceived hue
- Creating grayscale images with uniform perceived lightness
- Creating smooth and uniform color transition and gradients

A linear Oklab color is represented internally by an array of four components:

- lightness (#link("/docs/reference/layout/ratio/")[ratio])
- a (#link("/docs/reference/foundations/float/")[float] or #link("/docs/reference/layout/ratio/")[ratio]. Ratios are relative to `0.4`; meaning `50%` is equal to `0.2`)
- b (#link("/docs/reference/foundations/float/")[float] or #link("/docs/reference/layout/ratio/")[ratio]. Ratios are relative to `0.4`; meaning `50%` is equal to `0.2`)
- alpha (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
oklab(
  ratio: ratio,
  float: float | ratio,
  float: float | ratio,
  ratio: ratio,
  color: color
) -> color
```

```typst
#square(
  fill: oklab(27%, 20%, -3%, 50%)
)
```

==== `lightness`: ratio (Required, Positional)

The lightness component.

==== `a`: float | ratio (Required, Positional)

The a ("green/red") component.

==== `b`: float | ratio (Required, Positional)

The b ("blue/yellow") component.

==== `alpha`: ratio (Required, Positional)

The alpha component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to Oklab.

If this is given, the individual components should not be given.

=== `oklch`

Create an #link("https://bottosson.github.io/posts/oklab/")[Oklch] color.

This color space is well suited for the following use cases:

- Color manipulation involving lightness, chroma, and hue
- Creating grayscale images with uniform perceived lightness
- Creating smooth and uniform color transition and gradients

A linear Oklch color is represented internally by an array of four components:

- lightness (#link("/docs/reference/layout/ratio/")[ratio])
- chroma (#link("/docs/reference/foundations/float/")[float] or #link("/docs/reference/layout/ratio/")[ratio]. Ratios are relative to `0.4`; meaning `50%` is equal to `0.2`)
- hue (#link("/docs/reference/layout/angle/")[angle])
- alpha (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
oklch(
  ratio: ratio,
  float: float | ratio,
  angle: angle,
  ratio: ratio,
  color: color
) -> color
```

```typst
#square(
  fill: oklch(40%, 0.2, 160deg, 50%)
)
```

==== `lightness`: ratio (Required, Positional)

The lightness component.

==== `chroma`: float | ratio (Required, Positional)

The chroma component.

==== `hue`: angle (Required, Positional)

The hue component.

==== `alpha`: ratio (Required, Positional)

The alpha component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to Oklch.

If this is given, the individual components should not be given.

=== `linear-rgb`

Create an RGB(A) color with linear luma.

This color space is similar to sRGB, but with the distinction that the color component are not gamma corrected. This makes it easier to perform color operations such as blending and interpolation. Although, you should prefer to use the #link("/docs/reference/visualize/color/#definitions-oklab")[oklab function] for these.

A linear RGB(A) color is represented internally by an array of four components:

- red (#link("/docs/reference/layout/ratio/")[ratio])
- green (#link("/docs/reference/layout/ratio/")[ratio])
- blue (#link("/docs/reference/layout/ratio/")[ratio])
- alpha (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
linear-rgb(
  int: int | ratio,
  int: int | ratio,
  int: int | ratio,
  int: int | ratio,
  color: color
) -> color
```

```typst
#square(fill: color.linear-rgb(
  30%, 50%, 10%,
))
```

==== `red`: int | ratio (Required, Positional)

The red component.

==== `green`: int | ratio (Required, Positional)

The green component.

==== `blue`: int | ratio (Required, Positional)

The blue component.

==== `alpha`: int | ratio (Required, Positional)

The alpha component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to linear RGB(A).

If this is given, the individual components should not be given.

=== `rgb`

Create an RGB(A) color.

The color is specified in the sRGB color space.

An RGB(A) color is represented internally by an array of four components:

- red (#link("/docs/reference/layout/ratio/")[ratio])
- green (#link("/docs/reference/layout/ratio/")[ratio])
- blue (#link("/docs/reference/layout/ratio/")[ratio])
- alpha (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
rgb(
  int: int | ratio,
  int: int | ratio,
  int: int | ratio,
  int: int | ratio,
  str: str,
  color: color
) -> color
```

```typst
#square(fill: rgb("#b1f2eb"))
#square(fill: rgb(87, 127, 230))
#square(fill: rgb(25%, 13%, 65%))
```

==== `red`: int | ratio (Required, Positional)

The red component.

==== `green`: int | ratio (Required, Positional)

The green component.

==== `blue`: int | ratio (Required, Positional)

The blue component.

==== `alpha`: int | ratio (Required, Positional)

The alpha component.

==== `hex`: str (Required, Positional)

Alternatively: The color in hexadecimal notation.

Accepts three, four, six or eight hexadecimal digits and optionally a leading hash.

If this is given, the individual components should not be given.

*Example:*
```typst
#text(16pt, rgb("#239dad"))[
  *Typst*
]
```

==== `color`: color (Required, Positional)

Alternatively: The color to convert to RGB(a).

If this is given, the individual components should not be given.

=== `cmyk`

Create a CMYK color.

This is useful if you want to target a specific printer. The conversion to RGB for display preview might differ from how your printer reproduces the color.

A CMYK color is represented internally by an array of four components:

- cyan (#link("/docs/reference/layout/ratio/")[ratio])
- magenta (#link("/docs/reference/layout/ratio/")[ratio])
- yellow (#link("/docs/reference/layout/ratio/")[ratio])
- key (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

Note that CMYK colors are not currently supported when PDF/A output is enabled.

```
cmyk(
  ratio: ratio,
  ratio: ratio,
  ratio: ratio,
  ratio: ratio,
  color: color
) -> color
```

```typst
#square(
  fill: cmyk(27%, 0%, 3%, 5%)
)
```

==== `cyan`: ratio (Required, Positional)

The cyan component.

==== `magenta`: ratio (Required, Positional)

The magenta component.

==== `yellow`: ratio (Required, Positional)

The yellow component.

==== `key`: ratio (Required, Positional)

The key component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to CMYK.

If this is given, the individual components should not be given.

=== `hsl`

Create an HSL color.

This color space is useful for specifying colors by hue, saturation and lightness. It is also useful for color manipulation, such as saturating while keeping perceived hue.

An HSL color is represented internally by an array of four components:

- hue (#link("/docs/reference/layout/angle/")[angle])
- saturation (#link("/docs/reference/layout/ratio/")[ratio])
- lightness (#link("/docs/reference/layout/ratio/")[ratio])
- alpha (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
hsl(
  angle: angle,
  int: int | ratio,
  int: int | ratio,
  int: int | ratio,
  color: color
) -> color
```

```typst
#square(
  fill: color.hsl(30deg, 50%, 60%)
)
```

==== `hue`: angle (Required, Positional)

The hue angle.

==== `saturation`: int | ratio (Required, Positional)

The saturation component.

==== `lightness`: int | ratio (Required, Positional)

The lightness component.

==== `alpha`: int | ratio (Required, Positional)

The alpha component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to HSL.

If this is given, the individual components should not be given.

=== `hsv`

Create an HSV color.

This color space is useful for specifying colors by hue, saturation and value. It is also useful for color manipulation, such as saturating while keeping perceived hue.

An HSV color is represented internally by an array of four components:

- hue (#link("/docs/reference/layout/angle/")[angle])
- saturation (#link("/docs/reference/layout/ratio/")[ratio])
- value (#link("/docs/reference/layout/ratio/")[ratio])
- alpha (#link("/docs/reference/layout/ratio/")[ratio])

These components are also available using the #link("/docs/reference/visualize/color/#definitions-components")[components] method.

```
hsv(
  angle: angle,
  int: int | ratio,
  int: int | ratio,
  int: int | ratio,
  color: color
) -> color
```

```typst
#square(
  fill: color.hsv(30deg, 50%, 60%)
)
```

==== `hue`: angle (Required, Positional)

The hue angle.

==== `saturation`: int | ratio (Required, Positional)

The saturation component.

==== `value`: int | ratio (Required, Positional)

The value component.

==== `alpha`: int | ratio (Required, Positional)

The alpha component.

==== `color`: color (Required, Positional)

Alternatively: The color to convert to HSL.

If this is given, the individual components should not be given.

=== `components`

Extracts the components of this color.

The size and values of this array depends on the color space. You can obtain the color space using #link("/docs/reference/visualize/color/#definitions-space")[space]. Below is a table of the color spaces and their components:

For the meaning and type of each individual value, see the documentation of the corresponding color space. The alpha component is optional and only included if the `alpha` argument is `true`. The length of the returned array depends on the number of components and whether the alpha component is included.

```
components(
  alpha: bool
) -> array
```

```typst
// note that the alpha component is included by default
#rgb(40%, 60%, 80%).components()
```

==== `alpha`: bool

Whether to include the alpha component.

Default: `true`

=== `space`

Returns the constructor function for this color's space:

- #link("/docs/reference/visualize/color/#definitions-luma")[luma]
- #link("/docs/reference/visualize/color/#definitions-oklab")[oklab]
- #link("/docs/reference/visualize/color/#definitions-oklch")[oklch]
- #link("/docs/reference/visualize/color/#definitions-linear-rgb")[linear-rgb]
- #link("/docs/reference/visualize/color/#definitions-rgb")[rgb]
- #link("/docs/reference/visualize/color/#definitions-cmyk")[cmyk]
- #link("/docs/reference/visualize/color/#definitions-hsl")[hsl]
- #link("/docs/reference/visualize/color/#definitions-hsv")[hsv]

```
space(
  
) -> 
```

```typst
#let color = cmyk(1%, 2%, 3%, 4%)
#(color.space() == cmyk)
```

=== `to-hex`

Returns the color's RGB(A) hex representation (such as `#ffaa32` or `#020304fe`). The alpha component (last two digits in `#020304fe`) is omitted if it is equal to `ff` (255 / 100%).

```
to-hex(
  
) -> str
```

=== `lighten`

Lightens a color by a given factor.

```
lighten(
  ratio: ratio
) -> color
```

==== `factor`: ratio (Required, Positional)

The factor to lighten the color by.

=== `darken`

Darkens a color by a given factor.

```
darken(
  ratio: ratio
) -> color
```

==== `factor`: ratio (Required, Positional)

The factor to darken the color by.

=== `saturate`

Increases the saturation of a color by a given factor.

```
saturate(
  ratio: ratio
) -> color
```

==== `factor`: ratio (Required, Positional)

The factor to saturate the color by.

=== `desaturate`

Decreases the saturation of a color by a given factor.

```
desaturate(
  ratio: ratio
) -> color
```

==== `factor`: ratio (Required, Positional)

The factor to desaturate the color by.

=== `negate`

Produces the complementary color using a provided color space. You can think of it as the opposite side on a color wheel.

```
negate(
  space: any
) -> color
```

```typst
#square(fill: yellow)
#square(fill: yellow.negate())
#square(fill: yellow.negate(space: rgb))
```

==== `space`: any

The color space used for the transformation. By default, a perceptual color space is used.

Default: `oklab`

=== `rotate`

Rotates the hue of the color by a given angle.

```
rotate(
  angle: angle,
  space: any
) -> color
```

==== `angle`: angle (Required, Positional)

The angle to rotate the hue by.

==== `space`: any

The color space used to rotate. By default, this happens in a perceptual color space (#link("/docs/reference/visualize/color/#definitions-oklch")[oklch]).

Default: `oklch`

=== `mix`

Create a color by mixing two or more colors.

In color spaces with a hue component (hsl, hsv, oklch), only two colors can be mixed at once. Mixing more than two colors in such a space will result in an error!

```
mix(
  ..: color | array,
  space: any
) -> color
```

```typst
#set block(height: 20pt, width: 100%)
#block(fill: red.mix(blue))
#block(fill: red.mix(blue, space: rgb))
#block(fill: color.mix(red, blue, white))
#block(fill: color.mix((red, 70%), (blue, 30%)))
```

==== `colors`: color | array (Required, Positional, Variadic)

The colors, optionally with weights, specified as a pair (array of length two) of color and weight (float or ratio).

The weights do not need to add to `100%`, they are relative to the sum of all weights.

==== `space`: any

The color space to mix in. By default, this happens in a perceptual color space (#link("/docs/reference/visualize/color/#definitions-oklab")[oklab]).

Default: `oklab`

=== `transparentize`

Makes a color more transparent by a given factor.

This method is relative to the existing alpha value. If the scale is positive, calculates `alpha - alpha * scale`. Negative scales behave like `color.opacify(-scale)`.

```
transparentize(
  ratio: ratio
) -> color
```

```typst
#block(fill: red)[opaque]
#block(fill: red.transparentize(50%))[half red]
#block(fill: red.transparentize(75%))[quarter red]
```

==== `scale`: ratio (Required, Positional)

The factor to change the alpha value by.

=== `opacify`

Makes a color more opaque by a given scale.

This method is relative to the existing alpha value. If the scale is positive, calculates `alpha + scale - alpha * scale`. Negative scales behave like `color.transparentize(-scale)`.

```
opacify(
  ratio: ratio
) -> color
```

```typst
#let half-red = red.transparentize(50%)
#block(fill: half-red.opacify(100%))[opaque]
#block(fill: half-red.opacify(50%))[three quarters red]
#block(fill: half-red.opacify(-50%))[one quarter red]
```

==== `scale`: ratio (Required, Positional)

The scale to change the alpha value by.
