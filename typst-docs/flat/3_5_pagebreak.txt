= pagebreak

A manual page break.

Must not be used inside any containers.

== Example

```typst
The next page contains
more details on compound theory.
#pagebreak()

== Compound Theory
In 1984, the first ...
```

== Parameters

```
pagebreak(
  weak: bool,
  to: none | str
) -> content
```

=== `weak`: bool (Settable)

If `true`, the page break is skipped if the current page is already empty.

Default: `false`

=== `to`: none | str (Settable)

If given, ensures that the next page will be an even/odd page, with an empty page in between if necessary.

Default: `none`

*Example:*
```typst
#set page(height: 30pt)

First.
#pagebreak(to: "odd")
Third.
```
