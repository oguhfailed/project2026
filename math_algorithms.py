"""
Simple explanations of complex mathematical algorithms in Python.
Each algorithm is kept short and readable, with a plain-English comment block.
"""


# ---------------------------------------------------------------------------
# 1. EUCLIDEAN ALGORITHM — Greatest Common Divisor (GCD)
#
# Idea: the GCD of two numbers doesn't change if you replace the larger
# number with the remainder of dividing the two. Keep going until the
# remainder is 0.
# Example: gcd(48, 18) → gcd(18, 12) → gcd(12, 6) → gcd(6, 0) = 6
# ---------------------------------------------------------------------------
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ---------------------------------------------------------------------------
# 2. SIEVE OF ERATOSTHENES — Find all primes up to n
#
# Idea: start with every number marked "prime". For each prime p found,
# cross out all its multiples. What's left is prime.
# ---------------------------------------------------------------------------
def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):  # cross out multiples
                is_prime[multiple] = False

    return [num for num, prime in enumerate(is_prime) if prime]


# ---------------------------------------------------------------------------
# 3. BINARY SEARCH — Find a target in a sorted list
#
# Idea: look at the middle element. If it's too big, search the left half;
# if too small, search the right half. Repeat. Each step halves the work.
# Time complexity: O(log n) vs O(n) for a linear scan.
# ---------------------------------------------------------------------------
def binary_search(sorted_list, target):
    low, high = 0, len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return mid          # found — return index
        elif sorted_list[mid] < target:
            low = mid + 1       # target is in the right half
        else:
            high = mid - 1      # target is in the left half

    return -1  # not found


# ---------------------------------------------------------------------------
# 4. FIBONACCI WITH MEMOIZATION — Fast nth Fibonacci number
#
# Naive recursion recalculates the same values over and over (exponential
# time). Memoization stores results so each value is computed only once
# (linear time).
# ---------------------------------------------------------------------------
def fibonacci(n, memo={}):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


# ---------------------------------------------------------------------------
# 5. NEWTON'S METHOD — Square root without math.sqrt
#
# Idea: make a guess, then improve it by averaging the guess with
# n / guess. Repeat until the guess is accurate enough.
# This converges very fast (quadratic convergence).
# ---------------------------------------------------------------------------
def square_root(n, tolerance=1e-10):
    guess = n / 2.0
    while True:
        better = (guess + n / guess) / 2.0
        if abs(better - guess) < tolerance:
            return better
        guess = better


# ---------------------------------------------------------------------------
# 6. QUICKSORT — Efficient recursive sorting
#
# Idea: pick a "pivot" element, split the list into items smaller and
# larger than the pivot, then sort each half recursively.
# Average time complexity: O(n log n).
# ---------------------------------------------------------------------------
def quicksort(lst):
    if len(lst) <= 1:
        return lst
    pivot = lst[len(lst) // 2]
    left   = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right  = [x for x in lst if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# ---------------------------------------------------------------------------
# 7. CAESAR CIPHER — Simple substitution encryption
#
# Idea: shift every letter in the message by a fixed number of positions
# in the alphabet. To decrypt, shift in the opposite direction.
# ---------------------------------------------------------------------------
def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)  # keep spaces, punctuation as-is
    return ''.join(result)


# ---------------------------------------------------------------------------
# DEMO — run each algorithm and print results
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 1. GCD (Euclidean Algorithm) ===")
    print(f"gcd(48, 18) = {gcd(48, 18)}")          # 6
    print(f"gcd(100, 75) = {gcd(100, 75)}")         # 25

    print("\n=== 2. Sieve of Eratosthenes ===")
    primes = sieve_of_eratosthenes(50)
    print(f"Primes up to 50: {primes}")

    print("\n=== 3. Binary Search ===")
    data = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"Search 7 in {data} → index {binary_search(data, 7)}")
    print(f"Search 6 in {data} → index {binary_search(data, 6)} (not found)")

    print("\n=== 4. Fibonacci with Memoization ===")
    for i in [0, 1, 5, 10, 20, 30]:
        print(f"  fib({i:2d}) = {fibonacci(i)}")

    print("\n=== 5. Newton's Method (Square Root) ===")
    for n in [2, 9, 144, 1000]:
        print(f"  sqrt({n}) ≈ {square_root(n):.10f}")

    print("\n=== 6. Quicksort ===")
    unsorted = [3, 6, 8, 10, 1, 2, 1]
    print(f"  Before: {unsorted}")
    print(f"  After:  {quicksort(unsorted)}")

    print("\n=== 7. Caesar Cipher ===")
    message   = "Hello, World!"
    encrypted = caesar_cipher(message, shift=3)
    decrypted = caesar_cipher(encrypted, shift=3, decrypt=True)
    print(f"  Original:  {message}")
    print(f"  Encrypted: {encrypted}")
    print(f"  Decrypted: {decrypted}")
