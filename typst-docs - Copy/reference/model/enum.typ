= enum

A numbered list.

Displays a sequence of items vertically and numbers them consecutively.

== Example

```typst
Automatically numbered:
+ Preparations
+ Analysis
+ Conclusions

Manually numbered:
2. What is the first step?
5. I am confused.
+  Moving on ...

Multiple lines:
+ This enum item has multiple
  lines because the next line
  is indented.

Function call.
#enum[First][Second]
```

You can easily switch all your enumerations to a different numbering style with a set rule.

```typst
#set enum(numbering: "a)")

+ Starting off ...
+ Don't forget step two
```

You can also use #link("/docs/reference/model/enum/#definitions-item")[enum.item] to programmatically customize the number of each item in the enumeration:

```typst
#enum(
  enum.item(1)[First step],
  enum.item(5)[Fifth step],
  enum.item(10)[Tenth step]
)
```

== Syntax

This functions also has dedicated syntax:

- Starting a line with a plus sign creates an automatically numbered enumeration item.
- Starting a line with a number followed by a dot creates an explicitly numbered enumeration item.

Enumeration items can contain multiple paragraphs and other block-level content. All content that is indented more than an item's marker becomes part of that item.

== Parameters

```
enum(
  tight: bool,
  numbering: str | function,
  start: auto | int,
  full: bool,
  reversed: bool,
  indent: length,
  body-indent: length,
  spacing: auto | length,
  number-align: alignment,
  ..: content | array
) -> content
```

=== `tight`: bool (Settable)

Defines the default #link("/docs/reference/model/enum/#parameters-spacing")[spacing] of the enumeration. If it is `false`, the items are spaced apart with #link("/docs/reference/model/par/#parameters-spacing")[paragraph spacing]. If it is `true`, they use #link("/docs/reference/model/par/#parameters-leading")[paragraph leading] instead. This makes the list more compact, which can look better if the items are short.

In markup mode, the value of this parameter is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`. The markup-defined tightness cannot be overridden with set rules.

Default: `true`

*Example:*
```typst
+ If an enum has a lot of text, and
  maybe other inline content, it
  should not be tight anymore.

+ To make an enum wide, simply
  insert a blank line between the
  items.
```

=== `numbering`: str | function (Settable)

How to number the enumeration. Accepts a #link("/docs/reference/model/numbering/")[numbering pattern or function].

If the numbering pattern contains multiple counting symbols, they apply to nested enums. If given a function, the function receives one argument if `full` is `false` and multiple arguments if `full` is `true`.

Default: `"1."`

*Example:*
```typst
#set enum(numbering: "1.a)")
+ Different
+ Numbering
  + Nested
  + Items
+ Style

#set enum(numbering: n => super[#n])
+ Superscript
+ Numbering!
```

=== `start`: auto | int (Settable)

Which number to start the enumeration with.

Default: `auto`

*Example:*
```typst
#enum(
  start: 3,
  [Skipping],
  [Ahead],
)
```

=== `full`: bool (Settable)

Whether to display the full numbering, including the numbers of all parent enumerations.

Default: `false`

*Example:*
```typst
#set enum(numbering: "1.a)", full: true)
+ Cook
  + Heat water
  + Add ingredients
+ Eat
```

=== `reversed`: bool (Settable)

Whether to reverse the numbering for this enumeration.

Default: `false`

*Example:*
```typst
#set enum(reversed: true)
+ Coffee
+ Tea
+ Milk
```

=== `indent`: length (Settable)

The indentation of each item.

Default: `0pt`

=== `body-indent`: length (Settable)

The space between the numbering and the body of each item.

Default: `0.5em`

=== `spacing`: auto | length (Settable)

The spacing between the items of the enumeration.

If set to `auto`, uses paragraph #link("/docs/reference/model/par/#parameters-leading")[leading] for tight enumerations and paragraph #link("/docs/reference/model/par/#parameters-spacing")[spacing] for wide (non-tight) enumerations.

Default: `auto`

=== `number-align`: alignment (Settable)

The alignment that enum numbers should have.

By default, this is set to `end + top`, which aligns enum numbers towards end of the current text direction (in left-to-right script, for example, this is the same as `right`) and at the top of the line. The choice of `end` for horizontal alignment of enum numbers is usually preferred over `start`, as numbers then grow away from the text instead of towards it, avoiding certain visual issues. This option lets you override this behaviour, however. (Also to note is that the #link("/docs/reference/model/list/")[unordered list] uses a different method for this, by giving the `marker` content an alignment directly.).

Default: `end + top`

*Example:*
```typst
#set enum(number-align: start + bottom)

Here are some powers of two:
1. One
2. Two
4. Four
8. Eight
16. Sixteen
32. Thirty two
```

=== `children`: content | array (Required, Positional, Variadic)

The numbered list's items.

When using the enum syntax, adjacent items are automatically collected into enumerations, even through constructs like for loops.

*Example:*
```typst
#for phase in (
   "Launch",
   "Orbit",
   "Descent",
) [+ #phase]
```

== Definitions

=== `item`

An enumeration item.

```
item(
  none | int,
  content: content
) -> content
```

==== `number`: none | int (Positional, Settable)

The item's number.

Default: `none`

==== `body`: content (Required, Positional)

The item's body.
