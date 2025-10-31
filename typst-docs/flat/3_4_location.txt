= location

Identifies an element in the document.

A location uniquely identifies an element in the document and lets you access its absolute position on the pages. You can retrieve the current location with the #link("/docs/reference/introspection/here/")[here] function and the location of a queried or shown element with the #link("/docs/reference/foundations/content/#definitions-location")[location()] method on content.

== Locatable elements

Currently, only a subset of element functions is locatable. Aside from headings and figures, this includes equations, references, quotes and all elements with an explicit label. As a result, you _can_ query for e.g. #link("/docs/reference/model/strong/")[strong] elements, but you will find only those that have an explicit label attached to them. This limitation will be resolved in the future.

== Definitions

=== `page`

Returns the page number for this location.

Note that this does not return the value of the #link("/docs/reference/introspection/counter/")[page counter] at this location, but the true page number (starting from one).

If you want to know the value of the page counter, use `counter(page).at(loc)` instead.

Can be used with #link("/docs/reference/introspection/here/")[here] to retrieve the physical page position of the current context:

```
page(
  
) -> int
```

```typst
#context [
  I am located on
  page #here().page()
]
```

=== `position`

Returns a dictionary with the page number and the x, y position for this location. The page number starts at one and the coordinates are measured from the top-left of the page.

If you only need the page number, use `page()` instead as it allows Typst to skip unnecessary work.

```
position(
  
) -> dictionary
```

=== `page-numbering`

Returns the page numbering pattern of the page at this location. This can be used when displaying the page counter in order to obtain the local numbering. This is useful if you are building custom indices or outlines.

If the page numbering is set to `none` at that location, this function returns `none`.

```
page-numbering(
  
) -> function
```
