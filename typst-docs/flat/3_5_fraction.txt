= fraction

Defines how the remaining space in a layout is distributed.

Each fractionally sized element gets space based on the ratio of its fraction to the sum of all fractions.

For more details, also see the #link("/docs/reference/layout/h/")[h] and #link("/docs/reference/layout/v/")[v] functions and the #link("/docs/reference/layout/grid/")[grid function].

== Example

```typst
Left #h(1fr) Left-ish #h(2fr) Right
```
