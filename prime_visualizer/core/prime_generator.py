"""
Prime number generation utilities.
Provides efficient methods for generating and testing prime numbers.
"""

import math
from typing import List, Set


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is prime, False otherwise
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check for divisibility by numbers of form 6k ± 1
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def generate_primes(limit: int) -> List[int]:
    """
    Generate a list of prime numbers up to the given limit using the Sieve of Eratosthenes.

    Args:
        limit (int): The upper bound for prime number generation

    Returns:
        List[int]: A list of prime numbers up to the limit
    """
    # Special case for small limits
    if limit < 2:
        return []

    # Initialize the sieve
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    # Mark multiples of each prime as non-prime
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False

    # Collect the primes
    return [i for i in range(limit + 1) if sieve[i]]


def generate_primes_set(limit: int) -> Set[int]:
    """
    Generate a set of prime numbers up to the given limit.

    Args:
        limit (int): The upper bound for prime number generation

    Returns:
        Set[int]: A set of prime numbers up to the limit
    """
    return set(generate_primes(limit))


def nth_prime(n: int) -> int:
    """
    Find the nth prime number.

    Args:
        n (int): The index of the prime number to find (1-based indexing)

    Returns:
        int: The nth prime number

    Raises:
        ValueError: If n < 1
    """
    if n < 1:
        raise ValueError("n must be a positive integer")

    # Approximate upper bound for the nth prime (using prime number theorem)
    if n < 6:
        # Handle small cases directly
        primes = [2, 3, 5, 7, 11]
        return primes[n-1]

    # Use approximation: nth prime is roughly n * log(n)
    limit = int(n * (math.log(n) + math.log(math.log(n))))

    # Generate primes up to the estimated limit
    primes = generate_primes(limit)

    # Return the nth prime if available, otherwise generate more primes
    if len(primes) >= n:
        return primes[n-1]
    else:
        # If our estimate was too low, double the limit and try again
        return nth_prime(n)


def prime_count_estimate(x: int) -> int:
    """
    Estimate the number of primes less than or equal to x using Prime Number Theorem.

    Args:
        x (int): The upper bound

    Returns:
        int: Estimated number of primes less than or equal to x
    """
    if x < 2:
        return 0
    return int(x / math.log(x))
