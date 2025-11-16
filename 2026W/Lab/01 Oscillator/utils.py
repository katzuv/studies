from pathlib import Path
from typing import Callable

import autograd.numpy as np
from autograd import grad


def propagate_error(
    func: Callable,
    values: tuple[float, ...] | list[float],
    errors: tuple[float, ...] | list[float]
) -> float:
    """
    Generic function for error propagation using autograd.
    
    :param func: A function that takes multiple arguments and returns a scalar value.
                 Must use autograd.numpy operations for automatic differentiation.
    :param values: The values of the input parameters.
    :param errors: The uncertainties/errors of the input parameters.
    :return: The propagated error (uncertainty) in the output.
        
    Examples:
        >>> # For f(x, y) = x * y
        >>> def multiply(x, y):
        ...     return x * y
        >>> propagate_error(multiply, (3.0, 4.0), (0.1, 0.2))
    """
    # Convert to numpy arrays for easier handling
    values = np.array(values, dtype=float)
    errors = np.array(errors, dtype=float)
    
    # Compute gradients with respect to each parameter
    gradients = []
    for i in range(len(values)):
        # Create a gradient function for the i-th parameter
        grad_func = grad(lambda *args: func(*args), i)
        # Evaluate the gradient at the given values
        gradient_value = grad_func(*values)
        gradients.append(gradient_value)
    
    gradients = np.array(gradients)
    
    # Apply error propagation formula: σ_f² = Σ(∂f/∂x_i)² * σ_i²
    error_squared = np.sum((gradients ** 2) * (errors ** 2))
    
    return np.sqrt(error_squared)


def get_edited_data_path(path: Path, start_index: int) -> Path:
    data = path.read_text()
    for replacement in (
        ("\t\t", ","),
        ("\t", ","),
        ("	count B	count C	count D", ""),
        ("count A", "ticks"),
        ("#", "line"),
        ("time(s)", "time"),
    ):
        data = data.replace(replacement[0], replacement[1])

    header = data.splitlines()[0]
    data = f"{header}\n" + "\n".join(
        line.removesuffix(",") for line in data.splitlines()[start_index:]
    )  # Trim data before sine.

    new_path = path.with_suffix(".csv")
    new_path.write_text(data)

    return new_path
