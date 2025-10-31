= direction

The four directions into which content can be laid out.

Possible values are:

- `ltr`: Left to right.
- `rtl`: Right to left.
- `ttb`: Top to bottom.
- `btt`: Bottom to top.

These values are available globally and also in the direction type's scope, so you can write either of the following two:

```typst
#stack(dir: rtl)[A][B][C]
#stack(dir: direction.rtl)[A][B][C]
```

== Definitions

=== `axis`

The axis this direction belongs to, either `"horizontal"` or `"vertical"`.

```
axis(
  
) -> str
```

```typst
#ltr.axis() \
#ttb.axis()
```

=== `start`

The start point of this direction, as an alignment.

```
start(
  
) -> alignment
```

```typst
#ltr.start() \
#rtl.start() \
#ttb.start() \
#btt.start()
```

=== `end`

The end point of this direction, as an alignment.

```
end(
  
) -> alignment
```

```typst
#ltr.end() \
#rtl.end() \
#ttb.end() \
#btt.end()
```

=== `inv`

The inverse direction.

```
inv(
  
) -> direction
```

```typst
#ltr.inv() \
#rtl.inv() \
#ttb.inv() \
#btt.inv()
```
