= int

A whole number.

The number can be negative, zero, or positive. As Typst uses 64 bits to store integers, integers cannot be smaller than `-9223372036854775808` or larger than `9223372036854775807`. Integer literals are always positive, so a negative integer such as `-1` is semantically the negation `-` of the positive literal `1`. A positive integer greater than the maximum value and a negative integer less than or equal to the minimum value cannot be represented as an integer literal, and are instead parsed as a `float`. The minimum integer value can still be obtained through integer arithmetic.

The number can also be specified as hexadecimal, octal, or binary by starting it with a zero followed by either `x`, `o`, or `b`.

You can convert a value to an integer with this type's constructor.

== Example

```typst
#(1 + 2) \
#(2 - 5) \
#(3 + 4 < 8)

#0xff \
#0o10 \
#0b1001
```

== Constructor

Converts a value to an integer. Raises an error if there is an attempt to produce an integer larger than the maximum 64-bit signed integer or smaller than the minimum 64-bit signed integer.

- Booleans are converted to `0` or `1`.
- Floats and decimals are truncated to the next 64-bit integer.
- Strings are parsed in base 10.

```
int(
  bool: bool | int | float | str | decimal
) -> int
```

```typst
#int(false) \
#int(true) \
#int(2.7) \
#int(decimal("3.8")) \
#(int("27") + int("4"))
```

==== `value`: bool | int | float | str | decimal (Required, Positional)

The value that should be converted to an integer.

== Definitions

=== `signum`

Calculates the sign of an integer.

- If the number is positive, returns `1`.
- If the number is negative, returns `-1`.
- If the number is zero, returns `0`.

```
signum(
  
) -> int
```

```typst
#(5).signum() \
#(-5).signum() \
#(0).signum()
```

=== `bit-not`

Calculates the bitwise NOT of an integer.

For the purposes of this function, the operand is treated as a signed integer of 64 bits.

```
bit-not(
  
) -> int
```

```typst
#4.bit-not() \
#(-1).bit-not()
```

=== `bit-and`

Calculates the bitwise AND between two integers.

For the purposes of this function, the operands are treated as signed integers of 64 bits.

```
bit-and(
  int: int
) -> int
```

```typst
#128.bit-and(192)
```

==== `rhs`: int (Required, Positional)

The right-hand operand of the bitwise AND.

=== `bit-or`

Calculates the bitwise OR between two integers.

For the purposes of this function, the operands are treated as signed integers of 64 bits.

```
bit-or(
  int: int
) -> int
```

```typst
#64.bit-or(32)
```

==== `rhs`: int (Required, Positional)

The right-hand operand of the bitwise OR.

=== `bit-xor`

Calculates the bitwise XOR between two integers.

For the purposes of this function, the operands are treated as signed integers of 64 bits.

```
bit-xor(
  int: int
) -> int
```

```typst
#64.bit-xor(96)
```

==== `rhs`: int (Required, Positional)

The right-hand operand of the bitwise XOR.

=== `bit-lshift`

Shifts the operand's bits to the left by the specified amount.

For the purposes of this function, the operand is treated as a signed integer of 64 bits. An error will occur if the result is too large to fit in a 64-bit integer.

```
bit-lshift(
  int: int
) -> int
```

```typst
#33.bit-lshift(2) \
#(-1).bit-lshift(3)
```

==== `shift`: int (Required, Positional)

The amount of bits to shift. Must not be negative.

=== `bit-rshift`

Shifts the operand's bits to the right by the specified amount. Performs an arithmetic shift by default (extends the sign bit to the left, such that negative numbers stay negative), but that can be changed by the `logical` parameter.

For the purposes of this function, the operand is treated as a signed integer of 64 bits.

```
bit-rshift(
  int: int,
  logical: bool
) -> int
```

```typst
#64.bit-rshift(2) \
#(-8).bit-rshift(2) \
#(-8).bit-rshift(2, logical: true)
```

==== `shift`: int (Required, Positional)

The amount of bits to shift. Must not be negative.

Shifts larger than 63 are allowed and will cause the return value to saturate. For non-negative numbers, the return value saturates at `0`, while, for negative numbers, it saturates at `-1` if `logical` is set to `false`, or `0` if it is `true`. This behavior is consistent with just applying this operation multiple times. Therefore, the shift will always succeed.

==== `logical`: bool

Toggles whether a logical (unsigned) right shift should be performed instead of arithmetic right shift. If this is `true`, negative operands will not preserve their sign bit, and bits which appear to the left after the shift will be `0`. This parameter has no effect on non-negative operands.

Default: `false`

=== `from-bytes`

Converts bytes to an integer.

```
from-bytes(
  bytes: bytes,
  endian: str,
  signed: bool
) -> int
```

```typst
#int.from-bytes(bytes((0, 0, 0, 0, 0, 0, 0, 1))) \
#int.from-bytes(bytes((1, 0, 0, 0, 0, 0, 0, 0)), endian: "big")
```

==== `bytes`: bytes (Required, Positional)

The bytes that should be converted to an integer.

Must be of length at most 8 so that the result fits into a 64-bit signed integer.

==== `endian`: str

The endianness of the conversion.

Default: `"little"`

==== `signed`: bool

Whether the bytes should be treated as a signed integer. If this is `true` and the most significant bit is set, the resulting number will negative.

Default: `true`

=== `to-bytes`

Converts an integer to bytes.

```
to-bytes(
  endian: str,
  size: int
) -> bytes
```

```typst
#array(10000.to-bytes(endian: "big")) \
#array(10000.to-bytes(size: 4))
```

==== `endian`: str

The endianness of the conversion.

Default: `"little"`

==== `size`: int

The size in bytes of the resulting bytes (must be at least zero). If the integer is too large to fit in the specified size, the conversion will truncate the remaining bytes based on the endianness. To keep the same resulting value, if the endianness is big-endian, the truncation will happen at the rightmost bytes. Otherwise, if the endianness is little-endian, the truncation will happen at the leftmost bytes.

Be aware that if the integer is negative and the size is not enough to make the number fit, when passing the resulting bytes to `int.from-bytes`, the resulting number might be positive, as the most significant bit might not be set to 1.

Default: `8`
