= Syntax

Typst is a markup language. This means that you can use simple syntax to accomplish common layout tasks. The lightweight markup syntax is complemented by set and show rules, which let you style your document easily and automatically. All this is backed by a tightly integrated scripting language with built-in and user-defined functions.

== Modes

Typst has three syntactical modes: Markup, math, and code. Markup mode is the default in a Typst document, math mode lets you write mathematical formulas, and code mode lets you use Typst's scripting features.

You can switch to a specific mode at any point by referring to the following table:

Once you have entered code mode with `#`, you don't need to use further hashes unless you switched back to markup or math mode in between.

== Markup

Typst provides built-in markup for the most common document elements. Most of the syntax elements are just shortcuts for a corresponding function. The table below lists all markup that is available and links to the best place to learn more about their syntax and usage.

== Math mode

Math mode is a special markup mode that is used to typeset mathematical formulas. It is entered by wrapping an equation in `$` characters. This works both in markup and code. The equation will be typeset into its own block if it starts and ends with at least one space (e.g. `$ x^2 $`). Inline math can be produced by omitting the whitespace (e.g. `$x^2$`). An overview over the syntax specific to math mode follows:

== Code mode

Within code blocks and expressions, new expressions can start without a leading `#` character. Many syntactic elements are specific to expressions. Below is a table listing all syntax that is available in code mode:

== Comments

Comments are ignored by Typst and will not be included in the output. This is useful to exclude old versions or to add annotations. To comment out a single line, start it with `//`:

```typst
// our data barely supports
// this claim

We show with $p < 0.05$
that the difference is
significant.
```

Comments can also be wrapped between `/*` and `*/`. In this case, the comment can span over multiple lines:

```typst
Our study design is as follows:
/* Somebody write this up:
   - 1000 participants.
   - 2x2 data design. */
```

== Escape sequences

Escape sequences are used to insert special characters that are hard to type or otherwise have special meaning in Typst. To escape a character, precede it with a backslash. To insert any Unicode codepoint, you can write a hexadecimal escape sequence: `\u{1f600}`. The same kind of escape sequences also work in #link("/docs/reference/foundations/str/")[strings].

```typst
I got an ice cream for
\$1.50! \u{1f600}
```

== Paths

Typst has various features that require a file path to reference external resources such as images, Typst files, or data files. Paths are represented as #link("/docs/reference/foundations/str/")[strings]. There are two kinds of paths: Relative and absolute.

- A relative path searches from the location of the Typst file where the feature is invoked. It is the default: #image("images/logo.png")
- An absolute path searches from the root of the project. It starts with a leading /: #image("/assets/logo.png")

By default, the project root is the parent directory of the main Typst file. For security reasons, you cannot read any files outside of the root directory.

If you want to set a specific folder as the root of your project, you can use the CLI's `--root` flag. Make sure that the main file is contained in the folder's subtree!

In the web app, the project itself is the root directory. You can always read all files within it, no matter which one is previewed (via the eye toggle next to each Typst file in the file panel).

A package can only load files from its own directory. Within it, absolute paths point to the package root, rather than the project root. For this reason, it cannot directly load files from the project directory. If a package needs resources from the project (such as a logo image), you must pass the already loaded image, e.g. as a named parameter `logo: image("mylogo.svg")`. Note that you can then still customize the image's appearance with a set rule within the package.

In the future, paths might become a #link("https://github.com/typst/typst/issues/971")[distinct type from strings], so that they can retain knowledge of where they were constructed. This way, resources could be loaded from a different root.
