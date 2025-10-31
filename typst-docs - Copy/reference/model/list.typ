= list

A bullet list.

Displays a sequence of items vertically, with each item introduced by a marker.

== Example

```typst
Normal list.
- Text
- Math
- Layout
- ...

Multiple lines.
- This list item spans multiple
  lines because it is indented.

Function call.
#list(
  [Foundations],
  [Calculate],
  [Construct],
  [Data Loading],
)
```

== Syntax

This functions also has dedicated syntax: Start a line with a hyphen, followed by a space to create a list item. A list item can contain multiple paragraphs and other block-level content. All content that is indented more than an item's marker becomes part of that item.

== Parameters

```
list(
  tight: bool,
  marker: content | array | function,
  indent: length,
  body-indent: length,
  spacing: auto | length,
  ..: content
) -> content
```

=== `tight`: bool (Settable)

Defines the default #link("/docs/reference/model/list/#parameters-spacing")[spacing] of the list. If it is `false`, the items are spaced apart with #link("/docs/reference/model/par/#parameters-spacing")[paragraph spacing]. If it is `true`, they use #link("/docs/reference/model/par/#parameters-leading")[paragraph leading] instead. This makes the list more compact, which can look better if the items are short.

In markup mode, the value of this parameter is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`. The markup-defined tightness cannot be overridden with set rules.

Default: `true`

*Example:*
```typst
- If a list has a lot of text, and
  maybe other inline content, it
  should not be tight anymore.

- To make a list wide, simply insert
  a blank line between the items.
```

=== `marker`: content | array | function (Settable)

The marker which introduces each item.

Instead of plain content, you can also pass an array with multiple markers that should be used for nested lists. If the list nesting depth exceeds the number of markers, the markers are cycled. For total control, you may pass a function that maps the list's nesting depth (starting from `0`) to a desired marker.

Default: `([•], [‣], [–])`

*Example:*
```typst
#set list(marker: [--])
- A more classic list
- With en-dashes

#set list(marker: ([•], [--]))
- Top-level
  - Nested
  - Items
- Items
```

=== `indent`: length (Settable)

The indent of each item.

Default: `0pt`

=== `body-indent`: length (Settable)

The spacing between the marker and the body of each item.

Default: `0.5em`

=== `spacing`: auto | length (Settable)

The spacing between the items of the list.

If set to `auto`, uses paragraph #link("/docs/reference/model/par/#parameters-leading")[leading] for tight lists and paragraph #link("/docs/reference/model/par/#parameters-spacing")[spacing] for wide (non-tight) lists.

Default: `auto`

=== `children`: content (Required, Positional, Variadic)

The bullet list's children.

When using the list syntax, adjacent items are automatically collected into lists, even through constructs like for loops.

*Example:*
```typst
#for letter in "ABC" [
  - Letter #letter
]
```

== Definitions

=== `item`

A bullet list item.

```
item(
  content: content
) -> content
```

==== `body`: content (Required, Positional)

The item's body.
