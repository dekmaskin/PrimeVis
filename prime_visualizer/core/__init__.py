"""
Core functionality for prime number generation, classification, and visualization.
"""

from prime_visualizer.core.prime_generator import generate_primes, is_prime
from prime_visualizer.core.prime_classifier import classify_prime
from prime_visualizer.core.image_generator import (
    calculate_dimensions,
    generate_visualization
)

__all__ = [
    'generate_primes',
    'is_prime',
    'classify_prime',
    'calculate_dimensions',
    'generate_visualization'
]
