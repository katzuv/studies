= hide

Hides content without affecting layout.

The `hide` function allows you to hide content while the layout still 'sees' it. This is useful to create whitespace that is exactly as large as some content. It may also be useful to redact content because its arguments are not included in the output.

== Example

```typst
Hello Jane \
#hide[Hello] Joe
```

== Parameters

```
hide(
  content: content
) -> content
```

=== `body`: content (Required, Positional)

The content to hide.
