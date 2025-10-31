= locate

Determines the location of an element in the document.

Takes a selector that must match exactly one element and returns that element's #link("/docs/reference/introspection/location/")[location]. This location can, in particular, be used to retrieve the physical #link("/docs/reference/introspection/location/#definitions-page")[page] number and #link("/docs/reference/introspection/location/#definitions-position")[position] (page, x, y) for that element.

== Examples

Locating a specific element:

```typst
#context [
  Introduction is at: \
  #locate(<intro>).position()
]

= Introduction <intro>
```

== Parameters

```
locate(
  label: label | selector | location | function
) -> location
```

=== `selector`: label | selector | location | function (Required, Positional)

A selector that should match exactly one element. This element will be located.

Especially useful in combination with

- #link("/docs/reference/introspection/here/")[here] to locate the current context,
- a #link("/docs/reference/introspection/location/")[location] retrieved from some queried element via the #link("/docs/reference/foundations/content/#definitions-location")[location()] method on content.
