= HTML

HTML files describe a document structurally. The aim of Typst's HTML export is to capture the structure of an input document and produce semantically rich HTML that retains this structure. The resulting HTML should be accessible, human-readable, and editable by hand and downstream tools.

PDF, PNG, and SVG export, in contrast, all produce _visual_ representations of a fully-laid out document. This divergence in the formats' intents means that Typst cannot simply produce perfect HTML for your existing Typst documents. It cannot always know what the best semantic HTML representation of your content is.

Instead, it gives _you_ full control: You can check the current export format through the #link("/docs/reference/foundations/target/")[target] function and when it is set to HTML, generate #link("/docs/reference/html/elem/")[raw HTML elements]. The primary intended use of these elements is in templates and show rules. This way, the document's contents can be fully agnostic to the export target and content can be shared between PDF and HTML export.

Currently, Typst will always output a single HTML file. Support for outputting directories with multiple HTML documents and assets, as well as support for outputting fragments that can be integrated into other HTML documents is planned.

Typst currently does not output CSS style sheets, instead focussing on emitting semantic markup. You can of course write your own CSS styles and still benefit from sharing your _content_ between PDF and HTML. For the future, we plan to give you the option of automatically emitting CSS, taking more of your existing set rules into account.

== Exporting as HTML

Pass `--format html` to the `compile` or `watch` subcommand or provide an output file name that ends with `.html`. Note that you must also pass `--features html` or set `TYPST_FEATURES=html` to enable this experimental export target.

When using `typst watch`, Typst will spin up a live-reloading HTTP server. You can configure it as follows:

- Pass `--port` to change the port. (Defaults to the first free port in the range 3000-3005.)
- Pass `--no-reload` to disable injection of a live reload script. (The HTML that is written to disk isn't affected either way.)
- Pass `--no-serve` to disable the server altogether.

Not currently available.

== HTML-specific functionality

Typst exposes HTML-specific functionality in the global `html` module. See below for the definitions it contains.

== Definitions

- #link("/docs/reference/html/elem/")[elem]An HTML element that can contain Typst content.
- #link("/docs/reference/html/frame/")[frame]An element that lays out its content as an inline SVG.
