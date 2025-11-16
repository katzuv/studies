# Error Propagation with Autograd

This document demonstrates how to use the generic `propagate_error()` function for automatic error propagation.

## Overview

The `propagate_error()` function in `utils.py` uses autograd to automatically compute error propagation for any mathematical function. This eliminates the need to manually derive and code partial derivatives.

## Basic Usage

```python
from utils import propagate_error
import autograd.numpy as np

# Example 1: Simple multiplication
def multiply(x, y):
    return x * y

x_val, y_val = 10.0, 5.0
x_err, y_err = 0.1, 0.05

result_error = propagate_error(multiply, (x_val, y_val), (x_err, y_err))
print(f"Result: {multiply(x_val, y_val)} ± {result_error}")
```

## How It Works

The function implements the standard error propagation formula:

```
σ_f² = Σ(∂f/∂x_i)² * σ_i²
```

Where:
- `σ_f` is the uncertainty in the output
- `∂f/∂x_i` are the partial derivatives (computed automatically by autograd)
- `σ_i` are the input uncertainties

## Requirements

Your function must:
1. Use `autograd.numpy` instead of regular `numpy` for operations
2. Return a scalar value (single number, not an array)
3. Accept numeric inputs

## Applied in Oscillator Code

### Before (Manual Calculation)
```python
import numpy as np

k1_error = np.sqrt(
    ((k1_mass / length) * g_error) ** 2
    + ((k1_mass * g) * length_error * (1 / length**2)) ** 2
    + ((g / length) * MASS_ERROR) ** 2
)
```

### After (Autograd)
```python
import autograd.numpy as np
from utils import propagate_error

def spring_constant_func(mass, g_val, length_val):
    return (mass * g_val) / length_val

k1_error = propagate_error(
    spring_constant_func,
    (k1_mass, g, length),
    (MASS_ERROR, g_error, length_error)
)
```

## Benefits

1. **No manual derivatives**: Autograd computes them automatically
2. **Less error-prone**: No risk of mistakes in derivative formulas
3. **More maintainable**: Function definition is simpler and clearer
4. **Reusable**: Same function works for any calculation
5. **Accurate**: Matches manual calculations to machine precision

## More Examples

### Complex Function
```python
import autograd.numpy as np
from utils import propagate_error

def complex_calc(a, b, c):
    return np.sqrt(a**2 + b**2) * np.exp(-c)

result_error = propagate_error(
    complex_calc,
    (1.0, 2.0, 0.5),
    (0.1, 0.1, 0.05)
)
```

### Natural Frequency
```python
def natural_frequency(spring_const, mass):
    return np.sqrt(spring_const / mass)

freq_error = propagate_error(
    natural_frequency,
    (SPRING_CONSTANT, CART_MASS),
    (SPRING_CONSTANT_ERROR, MASS_ERROR)
)
```
