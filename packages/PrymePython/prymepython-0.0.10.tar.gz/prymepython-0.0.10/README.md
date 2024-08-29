# Pryme: A Python Module for Working with Prime Numbers (Not published yet)

The `Pryme` package provides various utilities for working with prime numbers. This document outlines the functions available in the package, along with their descriptions and usage.

## Dependencies

The package requires the following libraries:
- `math`
- `functools` (for `lru_cache`)
- `random`
- `sympy`
- `itertools` (for `permutations`)

## Functions

### `list_primes(n)`

Generates a list of all prime numbers up to a given number `n` using the Sieve of Eratosthenes algorithm.

**Parameters:**
- `n` (int): The upper limit up to which prime numbers are generated.

**Returns:**
- List of integers representing prime numbers up to `n`.

### `get_primes()`

Returns a cached list of all prime numbers up to 2,000,000. If the list has not been created yet, it will be generated.

**Returns:**
- List of integers representing prime numbers up to 2,000,000.

### `is_prime(n)`

Determines if a given number `n` is prime by checking its divisibility.

**Parameters:**
- `n` (int): The number to check.

**Returns:**
- Boolean: `True` if `n` is prime, otherwise `False`.

### `sum_primes(n)`

Calculates the sum of all prime numbers up to a given number `n`.

**Parameters:**
- `n` (int): The upper limit up to which primes are summed.

**Returns:**
- Integer: Sum of all prime numbers up to `n`.

### `prime_factors(n)`

Returns a list of the prime factors of a given number `n`.

**Parameters:**
- `n` (int): The number for which to find prime factors.

**Returns:**
- List of integers representing the prime factors of `n`.

### `next_prime(n)`

Finds the next prime number greater than `n` using caching to speed up repeated calls.

**Parameters:**
- `n` (int): The number to find the next prime after.

**Returns:**
- Integer: The next prime number greater than `n`.

### `previous_prime(n)`

Finds the largest prime number smaller than `n` using caching to speed up repeated calls.

**Parameters:**
- `n` (int): The number to find the previous prime before.

**Returns:**
- Integer: The largest prime number smaller than `n`.

### `count_primes(n)`

Returns the count of all prime numbers up to a given number `n`.

**Parameters:**
- `n` (int): The upper limit up to which primes are counted.

**Returns:**
- Integer: Count of all prime numbers up to `n`.

### `prime_product(n)`

Calculates the product of all prime numbers up to a given number `n`.

**Parameters:**
- `n` (int): The upper limit up to which primes are multiplied.

**Returns:**
- Integer: Product of all prime numbers up to `n`.

### `prime_sum_pairs(n)`

Finds pairs of prime numbers whose sum is also a prime.

**Parameters:**
- `n` (int): The upper limit for prime numbers to consider.

**Returns:**
- List of tuples: Each tuple contains a pair of primes whose sum is also a prime.

### `mirror(n)`

Generates a list of the first `n` primes that remain prime when their digits are reversed.

**Parameters:**
- `n` (int): The number of mirror primes to generate.

**Returns:**
- List of integers: Mirror primes.

### `twins(n)`

Returns a list of the first `n` twin prime pairs (pairs of primes that differ by 2).

**Parameters:**
- `n` (int): The number of twin prime pairs to find.

**Returns:**
- List of tuples: Each tuple contains a pair of twin primes.

### `sophie(n)`

Finds the first `n` Sophie Germain primes, which are primes `p` such that `2p + 1` is also prime.

**Parameters:**
- `n` (int): The number of Sophie Germain primes to find.

**Returns:**
- List of integers: Sophie Germain primes.

### `sexy(n)`

Generates the first `n` sexy prime pairs, where two primes differ by 6.

**Parameters:**
- `n` (int): The number of sexy prime pairs to generate.

**Returns:**
- List of tuples: Each tuple contains a pair of sexy primes.

### `randprime()`

Returns a random prime number from the cached list of primes.

**Returns:**
- Integer: A random prime number.

### `cuban_first(n)`

Finds the first `n` Cuban primes of the first kind.

**Parameters:**
- `n` (int): The number of Cuban primes of the first kind to find.

**Returns:**
- List of integers: Cuban primes of the first kind.

### `cuban_second(n)`

Finds the first `n` Cuban primes of the second kind.

**Parameters:**
- `n` (int): The number of Cuban primes of the second kind to find.

**Returns:**
- List of integers: Cuban primes of the second kind.

### `lucas_test(n, k)`

Performs the Lucas primality test `k` times on a number `n` to determine if it's prime, composite, or possibly composite.

**Parameters:**
- `n` (int): The number to test.
- `k` (int): The number of times to perform the test.

**Returns:**
- String: `"prime"`, `"composite"`, or `"possibly composite"`.

### `prime_digit_sum(n)`

Checks if the sum of the digits of a prime number is also prime.

**Parameters:**
- `n` (int): The prime number to check.

**Returns:**
- Boolean: `True` if the sum of the digits of `n` is also prime, otherwise `False`.

### `prime_count_estimate(n)`

Provides an estimate of the number of prime numbers less than or equal to a given number `n` using the Prime Number Theorem (PNT).

**Parameters:**
- `n` (int): The upper limit for estimating the count of primes.

**Returns:**
- Integer: Estimated count of prime numbers less than or equal to `n`.

### `mersenne(n)`

Returns the first `n` Mersenne primes (primes of the form `2^p - 1` where `p` is also prime).

**Parameters:**
- `n` (int): The number of Mersenne primes to find.

**Returns:**
- List of integers: Mersenne primes.

**Note**: Mersenne Primes are extremeley expensive to compute. The function works fine to return up to 10 mersenne primes but grows slower as it returns more Mersenne primes. It took me roughly 1 minute to generate 20 Mersenne primes. Proceed with caution!

