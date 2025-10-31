= arguments

Captured arguments to a function.

== Argument Sinks

Like built-in functions, custom functions can also take a variable number of arguments. You can specify an _argument sink_ which collects all excess arguments as `..sink`. The resulting `sink` value is of the `arguments` type. It exposes methods to access the positional and named arguments.

```typst
#let format(title, ..authors) = {
  let by = authors
    .pos()
    .join(", ", last: " and ")

  [*#title* \ _Written by #by;_]
}

#format("ArtosFlow", "Jane", "Joe")
```

== Spreading

Inversely to an argument sink, you can _spread_ arguments, arrays and dictionaries into a function call with the `..spread` operator:

```typst
#let array = (2, 3, 5)
#calc.min(..array)
#let dict = (fill: blue)
#text(..dict)[Hello]
```

== Constructor

Construct spreadable arguments in place.

This function behaves like `let args(..sink) = sink`.

```
arguments(
  ..: any
) -> arguments
```

```typst
#let args = arguments(stroke: red, inset: 1em, [Body])
#box(..args)
```

==== `arguments`: any (Required, Positional, Variadic)

The arguments to construct.

== Definitions

=== `at`

Returns the positional argument at the specified index, or the named argument with the specified name.

If the key is an #link("/docs/reference/foundations/int/")[integer], this is equivalent to first calling #link("/docs/reference/foundations/arguments/#definitions-pos")[pos] and then #link("/docs/reference/foundations/array/#definitions-at")[array.at]. If it is a #link("/docs/reference/foundations/str/")[string], this is equivalent to first calling #link("/docs/reference/foundations/arguments/#definitions-named")[named] and then #link("/docs/reference/foundations/dictionary/#definitions-at")[dictionary.at].

```
at(
  int: int | str,
  default: any
) -> str
```

==== `key`: int | str (Required, Positional)

The index or name of the argument to get.

==== `default`: any

A default value to return if the key is invalid.

=== `pos`

Returns the captured positional arguments as an array.

```
pos(
  
) -> array
```

=== `named`

Returns the captured named arguments as a dictionary.

```
named(
  
) -> dictionary
```
