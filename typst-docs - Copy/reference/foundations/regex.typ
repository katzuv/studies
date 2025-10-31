= regex

A regular expression.

Can be used as a #link("/docs/reference/styling/#show-rules")[show rule selector] and with #link("/docs/reference/foundations/str/")[string methods] like `find`, `split`, and `replace`.

#link("https://docs.rs/regex/latest/regex/#syntax")[See here] for a specification of the supported syntax.

== Example

```typst
// Works with string methods.
#"a,b;c".split(regex("[,;]"))

// Works with show rules.
#show regex("\d+"): set text(red)

The numbers 1 to 10.
```

== Constructor

Create a regular expression from a string.

```
regex(
  str: str
) -> regex
```

==== `regex`: str (Required, Positional)

The regular expression as a string.

Most regex escape sequences just work because they are not valid Typst escape sequences. To produce regex escape sequences that are also valid in Typst (e.g. `\\`), you need to escape twice. Thus, to match a verbatim backslash, you would need to write `regex("\\\\")`.

If you need many escape sequences, you can also create a raw element and extract its text to use it for your regular expressions:
