= module

An module of definitions.

A module

- be built-in
- stem from a #link("/docs/reference/scripting/#modules")[file import]
- stem from a #link("/docs/reference/scripting/#packages")[package import] (and thus indirectly its entrypoint file)
- result from a call to the #link("/docs/reference/foundations/plugin/")[plugin] function

You can access definitions from the module using #link("/docs/reference/scripting/#fields")[field access notation] and interact with it using the #link("/docs/reference/scripting/#modules")[import and include syntaxes]. Alternatively, it is possible to convert a module to a dictionary, and therefore access its contents dynamically, using the #link("/docs/reference/foundations/dictionary/#constructor")[dictionary constructor].

== Example

```typst
#import "utils.typ"
#utils.add(2, 5)

#import utils: sub
#sub(1, 4)
```
