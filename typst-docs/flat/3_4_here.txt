= here

Provides the current location in the document.

You can think of `here` as a low-level building block that directly extracts the current location from the active #link("/docs/reference/context/")[context]. Some other functions use it internally: For instance, `counter.get()` is equivalent to `counter.at(here())`.

Within show rules on #link("/docs/reference/introspection/location/#locatable")[locatable] elements, `here()` will match the location of the shown element.

If you want to display the current page number, refer to the documentation of the #link("/docs/reference/introspection/counter/")[counter] type. While `here` can be used to determine the physical page number, typically you want the logical page number that may, for instance, have been reset after a preface.

== Examples

Determining the current position in the document in combination with the #link("/docs/reference/introspection/location/#definitions-position")[position] method:

```typst
#context [
  I am located at
  #here().position()
]
```

Running a #link("/docs/reference/introspection/query/")[query] for elements before the current position:

```typst
= Introduction
= Background

There are
#context query(
  selector(heading).before(here())
).len()
headings before me.

= Conclusion
```

Refer to the #link("/docs/reference/foundations/selector/")[selector] type for more details on before/after selectors.

== Parameters

```
here(
  
) -> location
```
