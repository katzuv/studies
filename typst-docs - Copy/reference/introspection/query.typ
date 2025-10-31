= query

Finds elements in the document.

The `query` functions lets you search your document for elements of a particular type or with a particular label. To use it, you first need to ensure that #link("/docs/reference/context/")[context] is available.

== Finding elements

In the example below, we manually create a table of contents instead of using the #link("/docs/reference/model/outline/")[outline] function.

To do this, we first query for all headings in the document at level 1 and where `outlined` is true. Querying only for headings at level 1 ensures that, for the purpose of this example, sub-headings are not included in the table of contents. The `outlined` field is used to exclude the "Table of Contents" heading itself.

Note that we open a `context` to be able to use the `query` function.

```typst
#set page(numbering: "1")

#heading(outlined: false)[
  Table of Contents
]
#context {
  let chapters = query(
    heading.where(
      level: 1,
      outlined: true,
    )
  )
  for chapter in chapters {
    let loc = chapter.location()
    let nr = numbering(
      loc.page-numbering(),
      ..counter(page).at(loc),
    )
    [#chapter.body #h(1fr) #nr \ ]
  }
}

= Introduction
#lorem(10)
#pagebreak()

== Sub-Heading
#lorem(8)

= Discussion
#lorem(18)
```

To get the page numbers, we first get the location of the elements returned by `query` with #link("/docs/reference/foundations/content/#definitions-location")[location]. We then also retrieve the #link("/docs/reference/introspection/location/#definitions-page-numbering")[page numbering] and #link("/docs/reference/introspection/counter/#page-counter")[page counter] at that location and apply the numbering to the counter.

== A word of caution

To resolve all your queries, Typst evaluates and layouts parts of the document multiple times. However, there is no guarantee that your queries can actually be completely resolved. If you aren't careful a query can affect itself—leading to a result that never stabilizes.

In the example below, we query for all headings in the document. We then generate as many headings. In the beginning, there's just one heading, titled `Real`. Thus, `count` is `1` and one `Fake` heading is generated. Typst sees that the query's result has changed and processes it again. This time, `count` is `2` and two `Fake` headings are generated. This goes on and on. As we can see, the output has a finite amount of headings. This is because Typst simply gives up after a few attempts.

In general, you should try not to write queries that affect themselves. The same words of caution also apply to other introspection features like #link("/docs/reference/introspection/counter/")[counters] and #link("/docs/reference/introspection/state/")[state].

```typst
= Real
#context {
  let elems = query(heading)
  let count = elems.len()
  count * [= Fake]
}
```

== Command line queries

You can also perform queries from the command line with the `typst query` command. This command executes an arbitrary query on the document and returns the resulting elements in serialized form. Consider the following `example.typ` file which contains some invisible #link("/docs/reference/introspection/metadata/")[metadata]:

You can execute a query on it as follows using Typst's CLI:

Frequently, you're interested in only one specific field of the resulting elements. In the case of the `metadata` element, the `value` field is the interesting one. You can extract just this field with the `--field` argument.

If you are interested in just a single element, you can use the `--one` flag to extract just it.

== Parameters

```
query(
  label: label | selector | location | function
) -> array
```

=== `target`: label | selector | location | function (Required, Positional)

Can be

- an element function like a `heading` or `figure`,
- a `<label>`,
- a more complex selector like `heading.where(level: 1)`,
- or `selector(heading).before(here())`.

Only #link("/docs/reference/introspection/location/#locatable")[locatable] element functions are supported.
