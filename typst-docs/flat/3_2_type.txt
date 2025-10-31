= type

Describes a kind of value.

To style your document, you need to work with values of different kinds: Lengths specifying the size of your elements, colors for your text and shapes, and more. Typst categorizes these into clearly defined _types_ and tells you where it expects which type of value.

Apart from basic types for numeric values and #link("/docs/reference/foundations/int/")[typical] #link("/docs/reference/foundations/float/")[types] #link("/docs/reference/foundations/str/")[known] #link("/docs/reference/foundations/array/")[from] #link("/docs/reference/foundations/dictionary/")[programming] languages, Typst provides a special type for #link("/docs/reference/foundations/content/")[content.] A value of this type can hold anything that you can enter into your document: Text, elements like headings and shapes, and style information.

== Example

```typst
#let x = 10
#if type(x) == int [
  #x is an integer!
] else [
  #x is another value...
]

An image is of type
#type(image("glacier.jpg")).
```

The type of `10` is `int`. Now, what is the type of `int` or even `type`?

```typst
#type(int) \
#type(type)
```

== Compatibility

In Typst 0.7 and lower, the `type` function returned a string instead of a type. Compatibility with the old way will remain until Typst 0.14 to give package authors time to upgrade.

- Checks like `int == "integer"` evaluate to `true`
- Adding/joining a type and string will yield a string
- The `in` operator on a type and a dictionary will evaluate to `true` if the dictionary has a string key matching the type's name

== Constructor

Determines a value's type.

```
type(
  any
) -> type
```

```typst
#type(12) \
#type(14.7) \
#type("hello") \
#type(<glacier>) \
#type([Hi]) \
#type(x => x + 1) \
#type(type)
```

==== `value`: any (Required, Positional)

The value whose type's to determine.
