"""
Prime number classification utilities.
Provides functions to classify primes into various categories.
"""

import math
from typing import Set
from prime_visualizer.core.prime_generator import is_prime


def is_twin_prime(n: int, primes_set: Set[int]) -> bool:
    """
    Check if a number is part of a twin prime pair (p, p+2).

    Args:
        n (int): The number to check
        primes_set (Set[int]): Set of prime numbers to check against

    Returns:
        bool: True if the number is part of a twin prime pair, False otherwise
    """
    return n in primes_set and ((n - 2) in primes_set or (n + 2) in primes_set)


def is_mersenne_prime(n: int) -> bool:
    """
    Check if a number is a Mersenne prime (a prime number of the form 2^p - 1).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a Mersenne prime, False otherwise
    """
    # First check if n is prime
    if not is_prime(n):
        return False

    # Check if n is of the form 2^p - 1
    n_plus_1 = n + 1
    if n_plus_1 & (n_plus_1 - 1) != 0:  # Check if n+1 is a power of 2
        return False

    # Check if the exponent p is also prime
    p = math.log2(n + 1)
    return is_prime(int(p))


def is_safe_prime(n: int) -> bool:
    """
    Check if a number is a safe prime (a prime p where (p-1)/2 is also prime).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a safe prime, False otherwise
    """
    return n > 2 and is_prime(n) and is_prime((n - 1) // 2)


def is_sophie_germain_prime(n: int) -> bool:
    """
    Check if a number is a Sophie Germain prime (a prime p where 2p+1 is also prime).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a Sophie Germain prime, False otherwise
    """
    return is_prime(n) and is_prime(2*n + 1)


def is_palindromic_prime(n: int) -> bool:
    """
    Check if a number is a palindromic prime (a prime that reads the same forwards and backwards).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a palindromic prime, False otherwise
    """
    return is_prime(n) and str(n) == str(n)[::-1]


def is_circular_prime(n: int) -> bool:
    """
    Check if a number is a circular prime (all rotations of its digits are prime).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a circular prime, False otherwise
    """
    if not is_prime(n):
        return False

    str_n = str(n)
    # Single digit primes are automatically circular
    if len(str_n) == 1:
        return True

    # Check all rotations
    for i in range(1, len(str_n)):
        rotated = int(str_n[i:] + str_n[:i])
        if not is_prime(rotated):
            return False

    return True


def is_factorial_prime(n: int) -> bool:
    """
    Check if a number is a factorial prime (a prime of the form n! ± 1).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a factorial prime, False otherwise
    """
    if not is_prime(n):
        return False

    # Check if n is of the form i! + 1 or i! - 1 for some i
    factorial = 1
    i = 1

    # Check up to a reasonable limit to avoid excessive computation
    while factorial < n + 1 and i < 20:  # 20! is huge, should be enough
        factorial *= i
        if n == factorial - 1 or n == factorial + 1:
            return True
        i += 1

    return False


def is_fibonacci_prime(n: int) -> bool:
    """
    Check if a number is a Fibonacci prime (a prime that is also a Fibonacci number).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a Fibonacci prime, False otherwise
    """
    if not is_prime(n):
        return False

    # A number is Fibonacci if and only if 5n² + 4 or 5n² - 4 is a perfect square
    def is_perfect_square(x):
        sqrt_x = int(math.sqrt(x))
        return sqrt_x * sqrt_x == x

    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)


def is_sexy_prime(n: int, primes_set: Set[int]) -> bool:
    """
    Check if a number is part of a sexy prime pair (primes p, p+6).

    Args:
        n (int): The number to check
        primes_set (Set[int]): Set of prime numbers to check against

    Returns:
        bool: True if the number is part of a sexy prime pair, False otherwise
    """
    return is_prime(n) and ((n + 6) in primes_set or (n - 6) in primes_set)


def is_cuban_prime(n: int) -> bool:
    """
    Check if a number is a Cuban prime (a prime of the form (3m² + 3m + 1) for some m).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a Cuban prime, False otherwise
    """
    if not is_prime(n):
        return False

    # Check if n = 3m² + 3m + 1 for some m
    # Solving for m: 3m² + 3m + 1 - n = 0
    # Using quadratic formula: m = (-3 + sqrt(9 + 12*(n-1))) / 6
    discriminant = 9 + 12 * (n - 1)
    sqrt_discriminant = math.sqrt(discriminant)

    # Check if sqrt_discriminant is an integer
    if not sqrt_discriminant.is_integer():
        return False

    m = (-3 + int(sqrt_discriminant)) / 6
    return m.is_integer() and m >= 0


def is_happy_number(n: int) -> bool:
    """
    Check if a number is a happy number.

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is happy, False otherwise
    """
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    return n == 1


def is_happy_prime(n: int) -> bool:
    """
    Check if a number is a happy prime (a prime that is also a happy number).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a happy prime, False otherwise
    """
    return is_prime(n) and is_happy_number(n)


def is_chen_prime(n: int) -> bool:
    """
    Check if a number is a Chen prime (a prime p where p+2 is either prime or semiprime).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a Chen prime, False otherwise
    """
    if not is_prime(n):
        return False

    n_plus_2 = n + 2

    # Check if n+2 is prime
    if is_prime(n_plus_2):
        return True

    # Check if n+2 is a semiprime (product of two primes)
    if n_plus_2 < 4:
        return False

    for i in range(2, int(math.sqrt(n_plus_2)) + 1):
        if n_plus_2 % i == 0:
            # i is a factor, check if both i and n_plus_2/i are prime
            return is_prime(i) and is_prime(n_plus_2 // i)

    return False


def is_wieferich_prime(n: int) -> bool:
    """
    Check if a number is a Wieferich prime (a prime p where 2^(p-1) ≡ 1 (mod p²)).

    Args:
        n (int): The number to check

    Returns:
        bool: True if the number is a Wieferich prime, False otherwise
    """
    # Only check small primes due to computational constraints
    # Known Wieferich primes are 1093 and 3511
    if not is_prime(n):
        return False

    return n in {1093, 3511}


def is_isolated_prime(n: int, primes_set: Set[int]) -> bool:
    """
    Check if a number is an isolated prime (neither n-2 nor n+2 is prime).

    Args:
        n (int): The number to check
        primes_set (Set[int]): Set of prime numbers to check against

    Returns:
        bool: True if the number is an isolated prime, False otherwise
    """
    return is_prime(n) and (n-2) not in primes_set and (n+2) not in primes_set


def classify_prime(n: int, primes_set: Set[int]) -> str:
    """
    Classify a prime number by its type.

    Args:
        n (int): The prime number to classify
        primes_set (Set[int]): Set of prime numbers to check against

    Returns:
        str: The type of prime ("regular_prime", "twin_prime", etc.)
    """
    # Check for special prime types in order of computational complexity
    # and relative rarity to make interesting visualizations
    if is_mersenne_prime(n):
        return "mersenne_prime"
    elif is_factorial_prime(n):
        return "factorial_prime"
    elif is_wieferich_prime(n):
        return "wieferich_prime"
    elif is_fibonacci_prime(n):
        return "fibonacci_prime"
    elif is_twin_prime(n, primes_set):
        return "twin_prime"
    elif is_sexy_prime(n, primes_set):
        return "sexy_prime"
    elif is_isolated_prime(n, primes_set):
        return "isolated_prime"
    elif is_safe_prime(n):
        return "safe_prime"
    elif is_sophie_germain_prime(n):
        return "sophie_germain_prime"
    elif is_chen_prime(n):
        return "chen_prime"
    elif is_palindromic_prime(n):
        return "palindromic_prime"
    elif is_circular_prime(n):
        return "circular_prime"
    elif is_cuban_prime(n):
        return "cuban_prime"
    elif is_happy_prime(n):
        return "happy_prime"
    else:
        return "regular_prime"
