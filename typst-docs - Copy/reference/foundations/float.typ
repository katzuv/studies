= float

A floating-point number.

A limited-precision representation of a real number. Typst uses 64 bits to store floats. Wherever a float is expected, you can also pass an #link("/docs/reference/foundations/int/")[integer].

You can convert a value to a float with this type's constructor.

NaN and positive infinity are available as `float.nan` and `float.inf` respectively.

== Example

```typst
#3.14 \
#1e4 \
#(10 / 4)
```

== Constructor

Converts a value to a float.

- Booleans are converted to `0.0` or `1.0`.
- Integers are converted to the closest 64-bit float. For integers with absolute value less than `calc.pow(2, 53)`, this conversion is exact.
- Ratios are divided by 100%.
- Strings are parsed in base 10 to the closest 64-bit float. Exponential notation is supported.

```
float(
  bool: bool | int | float | ratio | str | decimal
) -> float
```

```typst
#float(false) \
#float(true) \
#float(4) \
#float(40%) \
#float("2.7") \
#float("1e5")
```

==== `value`: bool | int | float | ratio | str | decimal (Required, Positional)

The value that should be converted to a float.

== Definitions

=== `is-nan`

Checks if a float is not a number.

In IEEE 754, more than one bit pattern represents a NaN. This function returns `true` if the float is any of those bit patterns.

```
is-nan(
  
) -> bool
```

```typst
#float.is-nan(0) \
#float.is-nan(1) \
#float.is-nan(float.nan)
```

=== `is-infinite`

Checks if a float is infinite.

Floats can represent positive infinity and negative infinity. This function returns `true` if the float is an infinity.

```
is-infinite(
  
) -> bool
```

```typst
#float.is-infinite(0) \
#float.is-infinite(1) \
#float.is-infinite(float.inf)
```

=== `signum`

Calculates the sign of a floating point number.

- If the number is positive (including `+0.0`), returns `1.0`.
- If the number is negative (including `-0.0`), returns `-1.0`.
- If the number is NaN, returns `float.nan`.

```
signum(
  
) -> float
```

```typst
#(5.0).signum() \
#(-5.0).signum() \
#(0.0).signum() \
#float.nan.signum()
```

=== `from-bytes`

Interprets bytes as a float.

```
from-bytes(
  bytes: bytes,
  endian: str
) -> float
```

```typst
#float.from-bytes(bytes((0, 0, 0, 0, 0, 0, 240, 63))) \
#float.from-bytes(bytes((63, 240, 0, 0, 0, 0, 0, 0)), endian: "big")
```

==== `bytes`: bytes (Required, Positional)

The bytes that should be converted to a float.

Must have a length of either 4 or 8. The bytes are then interpreted in #link("https://en.wikipedia.org/wiki/IEEE_754")[IEEE 754]'s binary32 (single-precision) or binary64 (double-precision) format depending on the length of the bytes.

==== `endian`: str

The endianness of the conversion.

Default: `"little"`

=== `to-bytes`

Converts a float to bytes.

```
to-bytes(
  endian: str,
  size: int
) -> bytes
```

```typst
#array(1.0.to-bytes(endian: "big")) \
#array(1.0.to-bytes())
```

==== `endian`: str

The endianness of the conversion.

Default: `"little"`

==== `size`: int

The size of the resulting bytes.

This must be either 4 or 8. The call will return the representation of this float in either #link("https://en.wikipedia.org/wiki/IEEE_754")[IEEE 754]'s binary32 (single-precision) or binary64 (double-precision) format depending on the provided size.

Default: `8`
