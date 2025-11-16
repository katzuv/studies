"""
Test script to verify that autograd error propagation produces correct results.
"""
import autograd.numpy as np
from utils import propagate_error


def test_multiplication():
    """Test error propagation for f(x, y) = x * y"""
    # For f(x, y) = x * y, the error is: σ_f = sqrt((y*σ_x)² + (x*σ_y)²)
    def multiply(x, y):
        return x * y
    
    x, y = 3.0, 4.0
    dx, dy = 0.1, 0.2
    
    # Using autograd
    error_autograd = propagate_error(multiply, (x, y), (dx, dy))
    
    # Manual calculation
    error_manual = np.sqrt((y * dx)**2 + (x * dy)**2)
    
    print(f"Multiplication test:")
    print(f"  Autograd error: {error_autograd:.10f}")
    print(f"  Manual error:   {error_manual:.10f}")
    print(f"  Difference:     {abs(error_autograd - error_manual):.2e}")
    assert np.isclose(error_autograd, error_manual, rtol=1e-10)
    print("  ✓ Passed")


def test_division():
    """Test error propagation for f(x, y) = x / y"""
    # For f(x, y) = x / y, the error is: σ_f = sqrt((1/y*σ_x)² + (x/y²*σ_y)²)
    def divide(x, y):
        return x / y
    
    x, y = 10.0, 2.0
    dx, dy = 0.1, 0.05
    
    # Using autograd
    error_autograd = propagate_error(divide, (x, y), (dx, dy))
    
    # Manual calculation
    error_manual = np.sqrt((dx / y)**2 + (x * dy / y**2)**2)
    
    print(f"\nDivision test:")
    print(f"  Autograd error: {error_autograd:.10f}")
    print(f"  Manual error:   {error_manual:.10f}")
    print(f"  Difference:     {abs(error_autograd - error_manual):.2e}")
    assert np.isclose(error_autograd, error_manual, rtol=1e-10)
    print("  ✓ Passed")


def test_sqrt():
    """Test error propagation for f(x) = sqrt(x)"""
    # For f(x) = sqrt(x), the error is: σ_f = σ_x / (2*sqrt(x))
    def sqrt_func(x):
        return np.sqrt(x)
    
    x = 9.0
    dx = 0.3
    
    # Using autograd
    error_autograd = propagate_error(sqrt_func, (x,), (dx,))
    
    # Manual calculation
    error_manual = dx / (2 * np.sqrt(x))
    
    print(f"\nSquare root test:")
    print(f"  Autograd error: {error_autograd:.10f}")
    print(f"  Manual error:   {error_manual:.10f}")
    print(f"  Difference:     {abs(error_autograd - error_manual):.2e}")
    assert np.isclose(error_autograd, error_manual, rtol=1e-10)
    print("  ✓ Passed")


def test_spring_constant():
    """Test error propagation for spring constant calculation"""
    # k = (m * g) / L
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
    
    # Manual calculation (from original code)
    error_manual = np.sqrt(
        ((mass / length) * g_error) ** 2
        + ((mass * g) * length_error * (1 / length**2)) ** 2
        + ((g / length) * mass_error) ** 2
    )
    
    print(f"\nSpring constant test:")
    print(f"  Autograd error: {error_autograd:.10f}")
    print(f"  Manual error:   {error_manual:.10f}")
    print(f"  Difference:     {abs(error_autograd - error_manual):.2e}")
    assert np.isclose(error_autograd, error_manual, rtol=1e-10)
    print("  ✓ Passed")


def test_natural_frequency():
    """Test error propagation for natural frequency calculation"""
    # ω = sqrt(k / m)
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
    
    # Manual calculation (from original code)
    # This is a bit more complex in the original, but essentially:
    # For ω = sqrt(k/m), partial derivatives are:
    # ∂ω/∂k = 1/(2*sqrt(k*m))
    # ∂ω/∂m = -sqrt(k)/(2*m^(3/2))
    grad_k = 1 / (2 * np.sqrt(k * m))
    grad_m = -np.sqrt(k) / (2 * m**(3/2))
    error_manual = np.sqrt((grad_k * k_error)**2 + (grad_m * m_error)**2)
    
    print(f"\nNatural frequency test:")
    print(f"  Autograd error: {error_autograd:.10f}")
    print(f"  Manual error:   {error_manual:.10f}")
    print(f"  Difference:     {abs(error_autograd - error_manual):.2e}")
    assert np.isclose(error_autograd, error_manual, rtol=1e-10)
    print("  ✓ Passed")


if __name__ == "__main__":
    print("Testing autograd error propagation...")
    print("=" * 50)
    
    test_multiplication()
    test_division()
    test_sqrt()
    test_spring_constant()
    test_natural_frequency()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
