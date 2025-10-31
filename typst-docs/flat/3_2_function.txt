= function

A mapping from argument values to a return value.

You can call a function by writing a comma-separated list of function _arguments_ enclosed in parentheses directly after the function name. Additionally, you can pass any number of trailing content blocks arguments to a function _after_ the normal argument list. If the normal argument list would become empty, it can be omitted. Typst supports positional and named arguments. The former are identified by position and type, while the latter are written as `name: value`.

Within math mode, function calls have special behaviour. See the #link("/docs/reference/math/")[math documentation] for more details.

== Example

```typst
// Call a function.
#list([A], [B])

// Named arguments and trailing
// content blocks.
#enum(start: 2)[A][B]

// Version without parentheses.
#list[A][B]
```

Functions are a fundamental building block of Typst. Typst provides functions for a variety of typesetting tasks. Moreover, the markup you write is backed by functions and all styling happens through functions. This reference lists all available functions and how you can use them. Please also refer to the documentation about #link("/docs/reference/styling/#set-rules")[set] and #link("/docs/reference/styling/#show-rules")[show] rules to learn about additional ways you can work with functions in Typst.

== Element functions

Some functions are associated with _elements_ like #link("/docs/reference/model/heading/")[headings] or #link("/docs/reference/model/table/")[tables]. When called, these create an element of their respective kind. In contrast to normal functions, they can further be used in #link("/docs/reference/styling/#set-rules")[set rules], #link("/docs/reference/styling/#show-rules")[show rules], and #link("/docs/reference/foundations/selector/")[selectors].

== Function scopes

Functions can hold related definitions in their own scope, similar to a #link("/docs/reference/scripting/#modules")[module]. Examples of this are #link("/docs/reference/foundations/assert/#definitions-eq")[assert.eq] or #link("/docs/reference/model/list/#definitions-item")[list.item]. However, this feature is currently only available for built-in functions.

== Defining functions

You can define your own function with a #link("/docs/reference/scripting/#bindings")[let binding] that has a parameter list after the binding's name. The parameter list can contain mandatory positional parameters, named parameters with default values and #link("/docs/reference/foundations/arguments/")[argument sinks].

The right-hand side of a function binding is the function body, which can be a block or any other expression. It defines the function's return value and can depend on the parameters. If the function body is a #link("/docs/reference/scripting/#blocks")[code block], the return value is the result of joining the values of each expression in the block.

Within a function body, the `return` keyword can be used to exit early and optionally specify a return value. If no explicit return value is given, the body evaluates to the result of joining all expressions preceding the `return`.

Functions that don't return any meaningful value return #link("/docs/reference/foundations/none/")[none] instead. The return type of such functions is not explicitly specified in the documentation. (An example of this is #link("/docs/reference/foundations/array/#definitions-push")[array.push]).

```typst
#let alert(body, fill: red) = {
  set text(white)
  set align(center)
  rect(
    fill: fill,
    inset: 8pt,
    radius: 4pt,
    [*Warning:\ #body*],
  )
}

#alert[
  Danger is imminent!
]

#alert(fill: blue)[
  KEEP OFF TRACKS
]
```

== Importing functions

Functions can be imported from one file (#link("/docs/reference/scripting/#modules")[module]) into another using `import`. For example, assume that we have defined the `alert` function from the previous example in a file called `foo.typ`. We can import it into another file by writing `import "foo.typ": alert`.

== Unnamed functions

You can also created an unnamed function without creating a binding by specifying a parameter list followed by `=>` and the function body. If your function has just one parameter, the parentheses around the parameter list are optional. Unnamed functions are mainly useful for show rules, but also for settable properties that take functions like the page function's #link("/docs/reference/layout/page/#parameters-footer")[footer] property.

```typst
#show "once?": it => [#it #it]
once?
```

== Note on function purity

In Typst, all functions are _pure._ This means that for the same arguments, they always return the same result. They cannot "remember" things to produce another value when they are called a second time.

The only exception are built-in methods like #link("/docs/reference/foundations/array/#definitions-push")[array.push(value)]. These can modify the values they are called on.

== Definitions

=== `with`

Returns a new function that has the given arguments pre-applied.

```
with(
  ..: any
) -> function
```

==== `arguments`: any (Required, Positional, Variadic)

The arguments to apply to the function.

=== `where`

Returns a selector that filters for elements belonging to this function whose fields have the values of the given arguments.

```
where(
  ..: any
) -> selector
```

```typst
#show heading.where(level: 2): set text(blue)
= Section
== Subsection
=== Sub-subsection
```

==== `fields`: any (Required, Positional, Variadic)

The fields to filter for.
