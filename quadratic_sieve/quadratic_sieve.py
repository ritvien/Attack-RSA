import math
import numpy as np
from sympy import isprime, sieve, gcd

class QuadraticSieve:
    """
    Implementation of the Quadratic Sieve factorization algorithm
    """
    
    def __init__(self):
        """Initialize the Quadratic Sieve algorithm"""
        self.factor_base = []
        self.smooth_numbers = []
        self.x_values = []
        
    def is_quadratic_residue(self, a, p):
        """
        Check if a is a quadratic residue modulo p
        """
        if p == 2:
            return True
        
        # Euler's criterion: a^((p-1)/2) ≡ 1 (mod p) if a is a quadratic residue
        return pow(a, (p - 1) // 2, p) == 1
    
    def legendre_symbol(self, a, p):
        """
        Calculate the Legendre symbol (a/p)
        """
        if a % p == 0:
            return 0
        elif self.is_quadratic_residue(a, p):
            return 1
        else:
            return -1
    
    def build_factor_base(self, n, limit):
        """
        Build a factor base of primes p such that n is a quadratic residue modulo p
        """
        self.factor_base = [2]  # Always include 2
        
        # Find primes up to limit where n is a quadratic residue
        for p in sieve.primerange(3, limit+1):
            if self.legendre_symbol(n, p) == 1:
                self.factor_base.append(p)
                
        return self.factor_base
    
    def is_smooth(self, x, factor_base):
        """
        Check if x is B-smooth (all prime factors are in factor_base)
        and return the factorization vector if it is
        """
        if x == 0:
            return None
        
        # Handle negative numbers
        sign = 1
        if x < 0:
            sign = -1
            x = abs(x)
            
        factorization = [0] * len(factor_base)
        
        # Factor using the factor base
        for i, p in enumerate(factor_base):
            while x % p == 0:
                factorization[i] += 1
                x //= p
                
        # If x is not fully factorized, it's not B-smooth
        if x > 1:
            return None
            
        # Convert to binary vector (mod 2)
        for i in range(len(factorization)):
            factorization[i] %= 2
            
        # Handle sign for negative numbers
        if sign == -1 and 2 in factor_base:
            # If -1 is represented in the factor base as 2^k
            idx = factor_base.index(2)
            factorization[idx] = (factorization[idx] + 1) % 2
            
        return factorization
    
    def find_smooth_numbers(self, n, bound):
        """
        Find B-smooth numbers around sqrt(n)
        """
        self.smooth_numbers = []
        self.x_values = []
        
        sqrt_n = math.isqrt(n)
        factor_base = self.factor_base
        
        # Q(x) = x^2 - n
        for x in range(sqrt_n, sqrt_n + bound):
            q_x = x**2 - n
            factorization = self.is_smooth(q_x, factor_base)
            
            if factorization is not None:
                self.smooth_numbers.append((q_x, factorization))
                self.x_values.append(x)
                
                # If we have enough smooth numbers
                if len(self.smooth_numbers) > len(factor_base) + 5:
                    break
                    
        return self.smooth_numbers, self.x_values
    
    def solve_linear_system(self, matrix, mod=2):
        """
        Solve the linear system Ax = 0 (mod 2) using Gaussian elimination
        """
        m = np.array(matrix, dtype=int)
        rows, cols = m.shape
        
        # Gaussian elimination to convert to row echelon form
        for i in range(min(rows, cols)):
            # Find pivot
            pivot_row = None
            for j in range(i, rows):
                if m[j, i] == 1:
                    pivot_row = j
                    break
                    
            if pivot_row is None:
                continue
                
            # Swap rows
            if pivot_row != i:
                m[[i, pivot_row]] = m[[pivot_row, i]]
                
            # Eliminate below
            for j in range(i + 1, rows):
                if m[j, i] == 1:
                    m[j] = (m[j] + m[i]) % mod
                    
        # Back substitution to find dependencies
        dependencies = []
        for i in range(rows):
            # If row is all zeros, its index is part of a dependency
            if np.all(m[i] == 0):
                dependency = [0] * rows
                dependency[i] = 1
                dependencies.append(dependency)
        
        # Find non-trivial combinations
        result = []
        for dep in dependencies:
            combination = [0] * rows
            for i in range(rows):
                if dep[i] == 1:
                    combination[i] = 1
            result.append(combination)
            
        return result
    
    def calculate_squares(self, n, combinations):
        """
        Calculate x^2 ≡ y^2 (mod n) from the combinations
        """
        factors = []
        
        for combo in combinations:
            # Calculate X = product of x_i where combo[i] = 1
            x = 1
            for i, use in enumerate(combo):
                if use == 1:
                    x = (x * self.x_values[i]) % n
            
            # Calculate Y^2 = product of Q(x_i) where combo[i] = 1
            y_squared = 1
            for i, use in enumerate(combo):
                if use == 1:
                    q_x, _ = self.smooth_numbers[i]
                    y_squared = (y_squared * abs(q_x)) % n
            
            # Take square root if possible
            y = math.isqrt(y_squared)
            if y * y != y_squared:
                # This should not happen with a proper combination
                continue
            
            # Calculate GCD to potentially find a factor
            if x != y and x != n - y:
                factor1 = gcd(x - y, n)
                factor2 = gcd(x + y, n)
                
                if 1 < factor1 < n:
                    factors.append(factor1)
                if 1 < factor2 < n:
                    factors.append(factor2)
        
        return factors
    
    def factorize(self, n, bound=None, factor_base_size=None):
        """
        Factor n using the Quadratic Sieve algorithm
        """
        if n <= 1:
            return []
            
        if isprime(n):
            return [n]
            
        # Try trivial division first
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
            if n % p == 0:
                return [p] + self.factorize(n // p)
                
        # Set default parameters if not provided
        if bound is None:
            bound = int(math.log(n)**2)
            
        if factor_base_size is None:
            factor_base_size = int(math.sqrt(math.log(n)) * 4)
        
        # Build factor base
        self.build_factor_base(n, factor_base_size)
        
        # Find smooth numbers
        self.find_smooth_numbers(n, bound)
        
        if len(self.smooth_numbers) < len(self.factor_base):
            # Not enough smooth numbers found, increase bounds
            return self.factorize(n, bound * 2, factor_base_size * 2)
        
        # Create matrix of exponent vectors
        matrix = [factorization for _, factorization in self.smooth_numbers]
        
        # Solve linear system
        combinations = self.solve_linear_system(matrix)
        
        # Calculate squares and find factors
        factors = self.calculate_squares(n, combinations)
        
        if not factors:
            # No factors found, increase bounds
            return self.factorize(n, bound * 2, factor_base_size * 2)
        
        # Complete factorization
        result = []
        for factor in factors:
            result.extend(self.factorize(factor))
            result.extend(self.factorize(n // factor))
            break
        
        return sorted(result)

def factorize(n, bound=None, factor_base_size=None):
    """
    Wrapper function to factorize n using Quadratic Sieve
    """
    qs = QuadraticSieve()
    return qs.factorize(n, bound, factor_base_size)

def rsa_decrypt_with_factors(n, e, c, p, q):
    """
    Decrypt RSA ciphertext c using the factorization of n = p*q
    """
    # Calculate Euler's totient function
    phi = (p - 1) * (q - 1)
    
    # Calculate private key d
    d = pow(e, -1, phi)  # Modular multiplicative inverse
    
    # Decrypt the message
    m = pow(c, d, n)
    
    return m, d