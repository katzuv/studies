= symbol

A Unicode symbol.

Typst defines common symbols so that they can easily be written with standard keyboards. The symbols are defined in modules, from which they can be accessed using #link("/docs/reference/scripting/#fields")[field access notation]:

- General symbols are defined in the #link("/docs/reference/symbols/sym/")[sym module]
- Emoji are defined in the #link("/docs/reference/symbols/emoji/")[emoji module]

Moreover, you can define custom symbols with this type's constructor function.

```typst
#sym.arrow.r \
#sym.gt.eq.not \
$gt.eq.not$ \
#emoji.face.halo
```

Many symbols have different variants, which can be selected by appending the modifiers with dot notation. The order of the modifiers is not relevant. Visit the documentation pages of the symbol modules and click on a symbol to see its available variants.

```typst
$arrow.l$ \
$arrow.r$ \
$arrow.t.quad$
```

== Constructor

Create a custom symbol with modifiers.

```
symbol(
  ..: str | array
) -> symbol
```

```typst
#let envelope = symbol(
  "🖂",
  ("stamped", "🖃"),
  ("stamped.pen", "🖆"),
  ("lightning", "🖄"),
  ("fly", "🖅"),
)

#envelope
#envelope.stamped
#envelope.stamped.pen
#envelope.lightning
#envelope.fly
```

==== `variants`: str | array (Required, Positional, Variadic)

The variants of the symbol.

Can be a just a string consisting of a single character for the modifierless variant or an array with two strings specifying the modifiers and the symbol. Individual modifiers should be separated by dots. When displaying a symbol, Typst selects the first from the variants that have all attached modifiers and the minimum number of other modifiers.
