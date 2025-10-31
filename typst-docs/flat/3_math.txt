= Math

Typst has special #link("/docs/reference/syntax/#math")[syntax] and library functions to typeset mathematical formulas. Math formulas can be displayed inline with text or as separate blocks. They will be typeset into their own block if they start and end with at least one space (e.g. `$ x^2 $`).

== Variables

In math, single letters are always displayed as is. Multiple letters, however, are interpreted as variables and functions. To display multiple letters verbatim, you can place them into quotes and to access single letter variables, you can use the #link("/docs/reference/scripting/#expressions")[hash syntax].

```typst
$ A = pi r^2 $
$ "area" = pi dot "radius"^2 $
$ cal(A) :=
    { x in RR | x "is natural" } $
#let x = 5
$ #x < 17 $
```

== Symbols

Math mode makes a wide selection of #link("/docs/reference/symbols/sym/")[symbols] like `pi`, `dot`, or `RR` available. Many mathematical symbols are available in different variants. You can select between different variants by applying #link("/docs/reference/foundations/symbol/")[modifiers] to the symbol. Typst further recognizes a number of shorthand sequences like `=>` that approximate a symbol. When such a shorthand exists, the symbol's documentation lists it.

```typst
$ x < y => x gt.eq.not y $
```

== Line Breaks

Formulas can also contain line breaks. Each line can contain one or multiple _alignment points_ (`&`) which are then aligned.

```typst
$ sum_(k=0)^n k
    &= 1 + ... + n \
    &= (n(n+1)) / 2 $
```

== Function calls

Math mode supports special function calls without the hash prefix. In these "math calls", the argument list works a little differently than in code:

- Within them, Typst is still in "math mode". Thus, you can write math directly into them, but need to use hash syntax to pass code expressions (except for strings, which are available in the math syntax).
- They support positional and named arguments, as well as argument spreading.
- They don't support trailing content blocks.
- They provide additional syntax for 2-dimensional argument lists. The semicolon (`;`) merges preceding arguments separated by commas into an array argument.

```typst
$ frac(a^2, 2) $
$ vec(1, 2, delim: "[") $
$ mat(1, 2; 3, 4) $
$ mat(..#range(1, 5).chunks(2)) $
$ lim_x =
    op("lim", limits: #true)_x $
```

To write a verbatim comma or semicolon in a math call, escape it with a backslash. The colon on the other hand is only recognized in a special way if directly preceded by an identifier, so to display it verbatim in those cases, you can just insert a space before it.

Functions calls preceded by a hash are normal code function calls and not affected by these rules.

== Alignment

When equations include multiple _alignment points_ (`&`), this creates blocks of alternatingly right- and left-aligned columns. In the example below, the expression `(3x + y) / 7` is right-aligned and `= 9` is left-aligned. The word "given" is also left-aligned because `&&` creates two alignment points in a row, alternating the alignment twice. `& &` and `&&` behave exactly the same way. Meanwhile, "multiply by 7" is right-aligned because just one `&` precedes it. Each alignment point simply alternates between right-aligned/left-aligned.

```typst
$ (3x + y) / 7 &= 9 && "given" \
  3x + y &= 63 & "multiply by 7" \
  3x &= 63 - y && "subtract y" \
  x &= 21 - y/3 & "divide by 3" $
```

== Math fonts

You can set the math font by with a #link("/docs/reference/styling/#show-rules")[show-set rule] as demonstrated below. Note that only special OpenType math fonts are suitable for typesetting maths.

```typst
#show math.equation: set text(font: "Fira Math")
$ sum_(i in NN) 1 + i $
```

== Math module

All math functions are part of the `math` #link("/docs/reference/scripting/#modules")[module], which is available by default in equations. Outside of equations, they can be accessed with the `math.` prefix.

== Definitions

- #link("/docs/reference/math/accent/")[accent]Attaches an accent to a base.
- #link("/docs/reference/math/attach")[attach]Subscript, superscripts, and limits.
- #link("/docs/reference/math/binom/")[binom]A binomial expression.
- #link("/docs/reference/math/cancel/")[cancel]Displays a diagonal line over a part of an equation.
- #link("/docs/reference/math/cases/")[cases]A case distinction.
- #link("/docs/reference/math/class/")[class]Forced use of a certain math class.
- #link("/docs/reference/math/equation/")[equation]A mathematical equation.
- #link("/docs/reference/math/frac/")[frac]A mathematical fraction.
- #link("/docs/reference/math/lr")[lr]Delimiter matching.
- #link("/docs/reference/math/mat/")[mat]A matrix.
- #link("/docs/reference/math/op/")[op]A text operator in an equation.
- #link("/docs/reference/math/primes/")[primes]Grouped primes.
- #link("/docs/reference/math/roots")[roots]Square and non-square roots.
- #link("/docs/reference/math/sizes")[sizes]Forced size styles for expressions within formulas.
- #link("/docs/reference/math/stretch/")[stretch]Stretches a glyph.
- #link("/docs/reference/math/styles")[styles]Alternate letterforms within formulas.
- #link("/docs/reference/math/underover")[underover]Delimiters above or below parts of an equation.
- #link("/docs/reference/math/variants")[variants]Alternate typefaces within formulas.
- #link("/docs/reference/math/vec/")[vec]A column vector.
