= selector

A filter for selecting elements within the document.

You can construct a selector in the following ways:

- you can use an element #link("/docs/reference/foundations/function/")[function]
- you can filter for an element function with #link("/docs/reference/foundations/function/#definitions-where")[specific fields]
- you can use a #link("/docs/reference/foundations/str/")[string] or #link("/docs/reference/foundations/regex/")[regular expression]
- you can use a #link("/docs/reference/foundations/label/")[<label>]
- you can use a #link("/docs/reference/introspection/location/")[location]
- call the #link("/docs/reference/foundations/selector/")[selector] constructor to convert any of the above types into a selector value and use the methods below to refine it

Selectors are used to #link("/docs/reference/styling/#show-rules")[apply styling rules] to elements. You can also use selectors to #link("/docs/reference/introspection/query/")[query] the document for certain types of elements.

Furthermore, you can pass a selector to several of Typst's built-in functions to configure their behaviour. One such example is the #link("/docs/reference/model/outline/")[outline] where it can be used to change which elements are listed within the outline.

Multiple selectors can be combined using the methods shown below. However, not all kinds of selectors are supported in all places, at the moment.

== Example

```typst
#context query(
  heading.where(level: 1)
    .or(heading.where(level: 2))
)

= This will be found
== So will this
=== But this will not.
```

== Constructor

Turns a value into a selector. The following values are accepted:

- An element function like a `heading` or `figure`.
- A `<label>`.
- A more complex selector like `heading.where(level: 1)`.

```
selector(
  str: str | regex | label | selector | location | function
) -> selector
```

==== `target`: str | regex | label | selector | location | function (Required, Positional)

Can be an element function like a `heading` or `figure`, a `<label>` or a more complex selector like `heading.where(level: 1)`.

== Definitions

=== `or`

Selects all elements that match this or any of the other selectors.

```
or(
  ..: str | regex | label | selector | location | function
) -> selector
```

==== `others`: str | regex | label | selector | location | function (Required, Positional, Variadic)

The other selectors to match on.

=== `and`

Selects all elements that match this and all of the other selectors.

```
and(
  ..: str | regex | label | selector | location | function
) -> selector
```

==== `others`: str | regex | label | selector | location | function (Required, Positional, Variadic)

The other selectors to match on.

=== `before`

Returns a modified selector that will only match elements that occur before the first match of `end`.

```
before(
  label: label | selector | location | function,
  inclusive: bool
) -> selector
```

==== `end`: label | selector | location | function (Required, Positional)

The original selection will end at the first match of `end`.

==== `inclusive`: bool

Whether `end` itself should match or not. This is only relevant if both selectors match the same type of element. Defaults to `true`.

Default: `true`

=== `after`

Returns a modified selector that will only match elements that occur after the first match of `start`.

```
after(
  label: label | selector | location | function,
  inclusive: bool
) -> selector
```

==== `start`: label | selector | location | function (Required, Positional)

The original selection will start at the first match of `start`.

==== `inclusive`: bool

Whether `start` itself should match or not. This is only relevant if both selectors match the same type of element. Defaults to `true`.

Default: `true`
