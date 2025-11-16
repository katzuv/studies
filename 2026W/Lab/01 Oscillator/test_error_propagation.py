"""
Unit tests for error propagation using autograd.

Run with: pytest test_error_propagation.py -v
"""
import autograd.numpy as np
import pytest

from utils import propagate_error


class TestErrorPropagation:
    """Test suite for the propagate_error function."""

    def test_multiplication(self):
        """Test error propagation for f(x, y) = x * y."""
        def multiply(x, y):
            return x * y
        
        x, y = 3.0, 4.0
        dx, dy = 0.1, 0.2
        
        # Using autograd
        error_autograd = propagate_error(multiply, (x, y), (dx, dy))
        
        # Manual calculation: σ_f = sqrt((y*σ_x)² + (x*σ_y)²)
        error_manual = np.sqrt((y * dx)**2 + (x * dy)**2)
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_division(self):
        """Test error propagation for f(x, y) = x / y."""
        def divide(x, y):
            return x / y
        
        x, y = 10.0, 2.0
        dx, dy = 0.1, 0.05
        
        # Using autograd
        error_autograd = propagate_error(divide, (x, y), (dx, dy))
        
        # Manual calculation: σ_f = sqrt((1/y*σ_x)² + (x/y²*σ_y)²)
        error_manual = np.sqrt((dx / y)**2 + (x * dy / y**2)**2)
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_square_root(self):
        """Test error propagation for f(x) = sqrt(x)."""
        def sqrt_func(x):
            return np.sqrt(x)
        
        x = 9.0
        dx = 0.3
        
        # Using autograd
        error_autograd = propagate_error(sqrt_func, (x,), (dx,))
        
        # Manual calculation: σ_f = σ_x / (2*sqrt(x))
        error_manual = dx / (2 * np.sqrt(x))
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_power_function(self):
        """Test error propagation for f(x) = x^n."""
        def power_func(x):
            return x ** 3
        
        x = 2.0
        dx = 0.1
        
        # Using autograd
        error_autograd = propagate_error(power_func, (x,), (dx,))
        
        # Manual calculation: σ_f = n * x^(n-1) * σ_x
        n = 3
        error_manual = n * x**(n-1) * dx
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_spring_constant_calculation(self):
        """Test error propagation for spring constant k = (m * g) / L."""
        def spring_constant_func(mass, g_val, length_val):
            return (mass * g_val) / length_val
        
        mass = 42.42e-3
        g = 9.81
        length = 9.8 / 100
        mass_error = 1e-5
        g_error = 0.1
        length_error = 0.1 / 100
        
        # Using autograd
        error_autograd = propagate_error(
            spring_constant_func,
            (mass, g, length),
            (mass_error, g_error, length_error)
        )
        
        # Manual calculation using partial derivatives
        error_manual = np.sqrt(
            ((mass / length) * g_error) ** 2
            + ((mass * g) * length_error * (1 / length**2)) ** 2
            + ((g / length) * mass_error) ** 2
        )
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_natural_frequency_calculation(self):
        """Test error propagation for natural frequency ω = sqrt(k / m)."""
        def natural_frequency_func(spring_const, mass):
            return np.sqrt(spring_const / mass)
        
        k = 8.55072
        k_error = 0.08722
        m = 217.88e-3
        m_error = 1e-5
        
        # Using autograd
        error_autograd = propagate_error(
            natural_frequency_func,
            (k, m),
            (k_error, m_error)
        )
        
        # Correct manual calculation using proper partial derivatives
        # ∂ω/∂k = 1/(2*sqrt(k*m))
        # ∂ω/∂m = -sqrt(k)/(2*m^(3/2))
        grad_k = 1 / (2 * np.sqrt(k * m))
        grad_m = -np.sqrt(k) / (2 * m**(3/2))
        error_manual = np.sqrt((grad_k * k_error)**2 + (grad_m * m_error)**2)
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_exponential_function(self):
        """Test error propagation for f(x) = exp(x)."""
        def exp_func(x):
            return np.exp(x)
        
        x = 1.0
        dx = 0.1
        
        # Using autograd
        error_autograd = propagate_error(exp_func, (x,), (dx,))
        
        # Manual calculation: σ_f = exp(x) * σ_x
        error_manual = np.exp(x) * dx
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_trigonometric_function(self):
        """Test error propagation for f(x) = sin(x)."""
        def sin_func(x):
            return np.sin(x)
        
        x = np.pi / 4
        dx = 0.01
        
        # Using autograd
        error_autograd = propagate_error(sin_func, (x,), (dx,))
        
        # Manual calculation: σ_f = |cos(x)| * σ_x
        error_manual = np.abs(np.cos(x)) * dx
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_combined_operations(self):
        """Test error propagation for complex function f(x, y, z) = x*y + z^2."""
        def complex_func(x, y, z):
            return x * y + z**2
        
        x, y, z = 2.0, 3.0, 1.0
        dx, dy, dz = 0.1, 0.1, 0.05
        
        # Using autograd
        error_autograd = propagate_error(complex_func, (x, y, z), (dx, dy, dz))
        
        # Manual calculation: ∂f/∂x = y, ∂f/∂y = x, ∂f/∂z = 2z
        grad_x = y
        grad_y = x
        grad_z = 2 * z
        error_manual = np.sqrt((grad_x * dx)**2 + (grad_y * dy)**2 + (grad_z * dz)**2)
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)

    def test_zero_error(self):
        """Test that zero errors result in zero propagated error."""
        def multiply(x, y):
            return x * y
        
        error = propagate_error(multiply, (3.0, 4.0), (0.0, 0.0))
        
        assert error == 0.0

    def test_single_variable(self):
        """Test error propagation with a single variable."""
        def square(x):
            return x**2
        
        x = 5.0
        dx = 0.1
        
        error_autograd = propagate_error(square, (x,), (dx,))
        error_manual = 2 * x * dx  # ∂(x²)/∂x = 2x
        
        assert np.isclose(error_autograd, error_manual, rtol=1e-10)


class TestConstants:
    """Test suite for a error calculations."""

    def test_constants_import(self):
        """Test that constants module imports successfully."""
        import constants
        
        assert hasattr(constants, 'k1_error')
        assert hasattr(constants, 'k2_error')
        assert hasattr(constants, 'SPRING_CONSTANT_ERROR')
        assert hasattr(constants, 'NATURAL_FREQUENCY_ERROR')

    def test_error_values_are_positive(self):
        """Test that all error values are positive."""
        import constants
        
        assert constants.k1_error > 0
        assert constants.k2_error > 0
        assert constants.SPRING_CONSTANT_ERROR > 0
        assert constants.NATURAL_FREQUENCY_ERROR > 0

    def test_k1_error_value(self):
        """Test that k1_error matches expected value."""
        import constants
        
        # Expected value from autograd calculation
        expected = 0.0612546643
        assert np.isclose(constants.k1_error, expected, rtol=1e-8)

    def test_k2_error_value(self):
        """Test that k2_error matches expected value."""
        import constants
        
        # Expected value from autograd calculation
        expected = 0.0620919646
        assert np.isclose(constants.k2_error, expected, rtol=1e-8)

    def test_spring_constant_error_value(self):
        """Test that SPRING_CONSTANT_ERROR matches expected value."""
        import constants
        
        # Expected value from autograd calculation
        expected = 0.0872212472
        assert np.isclose(constants.SPRING_CONSTANT_ERROR, expected, rtol=1e-8)

    def test_natural_frequency_error_value(self):
        """Test that NATURAL_FREQUENCY_ERROR matches expected value."""
        import constants
        
        # Expected value from autograd calculation (corrected from buggy manual calculation)
        expected = 0.0319511696
        assert np.isclose(constants.NATURAL_FREQUENCY_ERROR, expected, rtol=1e-8)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
