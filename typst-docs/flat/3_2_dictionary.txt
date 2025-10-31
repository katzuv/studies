= dictionary

A map from string keys to values.

You can construct a dictionary by enclosing comma-separated `key: value` pairs in parentheses. The values do not have to be of the same type. Since empty parentheses already yield an empty array, you have to use the special `(:)` syntax to create an empty dictionary.

A dictionary is conceptually similar to an array, but it is indexed by strings instead of integers. You can access and create dictionary entries with the `.at()` method. If you know the key statically, you can alternatively use #link("/docs/reference/scripting/#fields")[field access notation] (`.key`) to access the value. Dictionaries can be added with the `+` operator and #link("/docs/reference/scripting/#blocks")[joined together]. To check whether a key is present in the dictionary, use the `in` keyword.

You can iterate over the pairs in a dictionary using a #link("/docs/reference/scripting/#loops")[for loop]. This will iterate in the order the pairs were inserted / declared.

== Example

```typst
#let dict = (
  name: "Typst",
  born: 2019,
)

#dict.name \
#(dict.launch = 20)
#dict.len() \
#dict.keys() \
#dict.values() \
#dict.at("born") \
#dict.insert("city", "Berlin ")
#("name" in dict)
```

== Constructor

Converts a value into a dictionary.

Note that this function is only intended for conversion of a dictionary-like value to a dictionary, not for creation of a dictionary from individual pairs. Use the dictionary syntax `(key: value)` instead.

```
dictionary(
  module: module
) -> dictionary
```

```typst
#dictionary(sys).at("version")
```

==== `value`: module (Required, Positional)

The value that should be converted to a dictionary.

== Definitions

=== `len`

The number of pairs in the dictionary.

```
len(
  
) -> int
```

=== `at`

Returns the value associated with the specified key in the dictionary. May be used on the left-hand side of an assignment if the key is already present in the dictionary. Returns the default value if the key is not part of the dictionary or fails with an error if no default value was specified.

```
at(
  str: str,
  default: any
) -> str
```

==== `key`: str (Required, Positional)

The key at which to retrieve the item.

==== `default`: any

A default value to return if the key is not part of the dictionary.

=== `insert`

Inserts a new pair into the dictionary. If the dictionary already contains this key, the value is updated.

```
insert(
  str: str,
  any
) -> str
```

==== `key`: str (Required, Positional)

The key of the pair that should be inserted.

==== `value`: any (Required, Positional)

The value of the pair that should be inserted.

=== `remove`

Removes a pair from the dictionary by key and return the value.

```
remove(
  str: str,
  default: any
) -> str
```

==== `key`: str (Required, Positional)

The key of the pair to remove.

==== `default`: any

A default value to return if the key does not exist.

=== `keys`

Returns the keys of the dictionary as an array in insertion order.

```
keys(
  
) -> array
```

=== `values`

Returns the values of the dictionary as an array in insertion order.

```
values(
  
) -> array
```

=== `pairs`

Returns the keys and values of the dictionary as an array of pairs. Each pair is represented as an array of length two.

```
pairs(
  
) -> array
```
