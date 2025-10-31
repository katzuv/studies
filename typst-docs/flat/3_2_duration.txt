= duration

Represents a positive or negative span of time.

== Constructor

Creates a new duration.

You can specify the #link("/docs/reference/foundations/duration/")[duration] using weeks, days, hours, minutes and seconds. You can also get a duration by subtracting two #link("/docs/reference/foundations/datetime/")[datetimes].

```
duration(
  seconds: int,
  minutes: int,
  hours: int,
  days: int,
  weeks: int
) -> duration
```

```typst
#duration(
  days: 3,
  hours: 12,
).hours()
```

==== `seconds`: int

The number of seconds.

Default: `0`

==== `minutes`: int

The number of minutes.

Default: `0`

==== `hours`: int

The number of hours.

Default: `0`

==== `days`: int

The number of days.

Default: `0`

==== `weeks`: int

The number of weeks.

Default: `0`

== Definitions

=== `seconds`

The duration expressed in seconds.

This function returns the total duration represented in seconds as a floating-point number rather than the second component of the duration.

```
seconds(
  
) -> float
```

=== `minutes`

The duration expressed in minutes.

This function returns the total duration represented in minutes as a floating-point number rather than the second component of the duration.

```
minutes(
  
) -> float
```

=== `hours`

The duration expressed in hours.

This function returns the total duration represented in hours as a floating-point number rather than the second component of the duration.

```
hours(
  
) -> float
```

=== `days`

The duration expressed in days.

This function returns the total duration represented in days as a floating-point number rather than the second component of the duration.

```
days(
  
) -> float
```

=== `weeks`

The duration expressed in weeks.

This function returns the total duration represented in weeks as a floating-point number rather than the second component of the duration.

```
weeks(
  
) -> float
```
