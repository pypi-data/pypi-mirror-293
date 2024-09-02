# Copyright 2016-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
### Functions of a pure math integer nature

"""
from __future__ import annotations

from typing import Iterator
from grscheller.circular_array.ca import CA

__all__ = ['gcd', 'lcm', 'coprime', 'iSqrt', 'isSqr', 'primes', 'comb', 'fibonacci']

# Number Theory mathematical Functions.

def gcd(m: int, n: int) -> int:
    """
    #### Uses Euclidean algorithm to compute the gcd of two integers.

    * takes two integers, returns gcd > 0
    * note that mathematically the gcd of 0 and 0 does not exist
    * taking `gcd(0, 0) = 1` is a better choice than `math.gcd(0, 0) = 0`
      * eliminates lcm & coprime having to edge case test
      * also `gcd(0, 0)` returning 1 instead of 0 more mathematically justified
    """
    if 0 == m == n:
        return 1
    m, n = abs(m), abs(n)
    m, n = (m, n) if m > n else (n, m)
    while n > 0:
        m, n = n, m % n
    return m

def lcm(m: int, n: int) -> int:
    """
    #### Finds the least common multiple (lcm) of two integers.

    * takes two integers `m` and `n`
    * returns `lcm(m, n) > 0`
    """
    m //= gcd(m, n)
    return abs(m*n)

def coprime(m: int, n: int) -> tuple[int, int]:
    """
    #### Makes 2 integers coprime by dividing out their common factors.

    * returns `(0, 0)` when `n = m = 0`
    * returned coprimed values retain their original signs
    """
    coPrime = lambda mm, nn, common: (mm//common, nn//common)
    common = gcd(m, n)
    return m//common, n//common

def iSqrt(n: int) -> int:
    """
    #### Integer square root of a non-negative integer.

    * return the unique `m` such that `m*m <= n < (m+1)*(m+1)`
    * raises: ValueError if `n < 0`
    """
    if n < 0:
        msg = 'iSqrt(n): n must be non-negative'
        raise ValueError(msg)
    high = n
    low = 1
    while high > low:
        high = (high + low) // 2
        low = n // high
    return high

def isSqr(n: int) -> bool:
    """
    #### Returns true if integer argument is a perfect square
    """
    return False if n < 0 else n == iSqrt(n)**2

def primes(start: int=2, end_before: int=100) -> Iterator[int]:
    """
    #### Return a prime number iterator using the Sieve of Eratosthenes algorithm
    """
    if start >= end_before or end_before < 3:
        return (x for x in (0,) if x > 0)
    if start < 2:
        start = 2

    sieve = [x for x in range(3, end_before, 2) if x % 3 != 0]
    stop = int(end_before**(0.5)) + 1
    front = -1
    for prime in sieve:
        front += 1
        if prime > stop:
            break
        for pot_prime in sieve[-1:front:-1]:
            if pot_prime % prime == 0:
                sieve.remove(pot_prime)

    if start <= 3 < end_before:  # We missed [2, 3] but
        sieve.insert(0, 3)       # saved about 60% for
    if start <= 2 < end_before:  # the initial storage
        sieve.insert(0, 2)       # space.

    # return sieve after trimming unwanted values
    return (x for x in sieve if x >= start)

# Combinatorics

def comb(n: int, m: int, targetTop: int=700, targetBot: int=5) -> int:
    """
    #### Implements C(n,m), the number of n items taken m at a time.

    * geared to works efficiently for Python's arbitrary length integers
    * default parameters geared to large values of n and m
    * the defaults work reasonably well for smaller (human size) values
    * for inner loops with smaller values, use targetTop = targetBot = 1
    * or just use math.comb(n, m) instead
    * raises ValueError if n < 0 or m < 0

    """
    # edge cases, justifying below type: ignore statements
    if n < 0 or m < 0:
        raise ValueError('for C(n, m) n and m must be a non-negative ints')
    if n == m or m == 0:
        return 1
    elif m > n:
        return 0

    # using C(n, m) = C(n, n-m) to reduce number of factors in calculation
    if m > (n // 2):
        m = n - m

    # Prepare data structures
    tops: CA[int] = CA(*range(n - m + 1, n + 1))
    bots: CA[int] = CA(*range(1, m+1))

    # Compacting data structures makes algorithm work better for larger values
    size = len(tops)
    while size > targetTop:
        size -= 1
        top, bot = coprime(tops.popL() * tops.popL(), bots.popL() * bots.popL())  # type: ignore
        tops.pushR(top)
        bots.pushR(bot)

    while size > targetBot:
        size -= 1
        bots.pushR(bots.popL() * bots.popL())  # type: ignore

    # Cancel all factors in denominator before multiplying the remaining factors
    # in the numerator.
    for bot in bots:
        for ii in range(len(tops)):
            top, bot = coprime(tops.popL(), bot)  # type: ignore
            if top > 1:
                tops.pushR(top)
            if bot == 1:
                break

    ans = tops.foldL(lambda x, y: x * y)   # need to tweak CA
    assert ans is not None
    return ans

# Fibonacci Iterator

def fibonacci(fib0: int, fib1: int) -> Iterator[int]:
    """
    #### Returns an iterator to a Fibonacci sequence

    * beginning fib0, fib1, ...
    """
    while True:
        yield fib0
        fib0, fib1 = fib1, fib0+fib1
