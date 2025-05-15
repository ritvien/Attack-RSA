import random
import math # Needed for gcd if not using math.gcd (Python 3.9+)

def modular_exponentiation(base, exp, mod):
    '''
    Tính modulo của lũy thừa (Modular Exponentiation)

    Parameters:
        base (int): cơ số
        exp (int): lũy thừa/số mũ
        mod (int): modulo

    Return:
            int: kết quả của phép tính modulo lũy thừa (base^exp % mod)

    '''
    result = 1
    base = base % mod # Ensure base is within modulo range initially
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        # Square the base and reduce modulo
        base = (base * base) % mod
        # Integer division for the exponent
        exp //= 2
    return result

def miller_rabin_test(n, k=50):
    '''
    Hàm kiểm tra số nguyên tố bằng thuật toán Miller-Rabin (Primality Test)

    Parameters:
        n (int): Số cần kiểm tra tính nguyên tố
        k (int): Số lần lặp, thử lại (càng to càng chính xác)

    Return:
        bool: True nếu có khả năng là số nguyên tố, False nếu là hợp số

    '''
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False # Optimization for even numbers

    # Write n-1 as 2^r * d where d is odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2) # Pick a random base 'a'
        x = modular_exponentiation(a, d, n) # x = a^d % n

        if x == 1 or x == n - 1:
            continue # Potentially prime, try next witness

        # Check if repeated squaring leads to n-1
        is_witness = True
        for _ in range(r - 1):
            x = modular_exponentiation(x, 2, n) # x = x^2 % n
            if x == n - 1:
                is_witness = False # Found n-1, continue outer loop
                break
        
        if is_witness: # If loop finished without finding n-1
             return False # Definitely composite

    return True # Probably prime after k iterations

def _generate_prime_candidate(length):
    """Generates an odd integer of a specified bit length."""
    p = random.getrandbits(length)
    # Ensure it has the correct bit length (most significant bit is 1)
    # and make it odd
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    """Generates a prime number of a specified bit length using Miller-Rabin."""
    p = 4
    # Keep generating candidates until one passes the primality test
    while not miller_rabin_test(p):
        p = _generate_prime_candidate(length)
    return p

# Use math.gcd if available (Python 3.9+), otherwise implement Euclidean algorithm
try:
    from math import gcd
except ImportError:
    def gcd(a, b):
        """Tính ước chung lớn nhất (Greatest Common Divisor)"""
        while b != 0:
            a, b = b, a % b
        return a

def extended_gcd(a, b):
    """Thuật toán Euclid mở rộng (Extended Euclidean Algorithm)."""
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inv(a, m):
    '''
    Tính nghịch đảo modulo của a modulo m bằng thuật toán Euclid mở rộng.
    (Modular Inverse using Extended Euclidean Algorithm)

    Parameters:
        a (int): Số nguyên cần tìm nghịch đảo modulo
        m (int): Modulo

    Return:
        int or None: Nghịch đảo modulo của a mod m, hoặc None nếu không tồn tại
    '''
    d, x, y = extended_gcd(a, m)
    if d != 1:
        return None # Inverse does not exist if gcd(a, m) != 1
    else:
        return x % m

def generate_rsa_keys(key_size=1024):
    '''
    Tạo cặp khóa RSA và các giá trị trung gian.
    (Generate RSA key pair and intermediate values)

    Parameters:
        key_size (int): Độ dài bit mong muốn cho modulus n.

    Return:
        tuple: ((e, n), (d, n), p, q, phi)
               Khóa công khai (e,n), Khóa bí mật (d,n), số nguyên tố p, số nguyên tố q, phi(n)
               Returns None if key generation fails (e.g., cannot find mod_inv).
    '''
    if key_size < 16: # Need enough bits for distinct p, q and operations
        raise ValueError("Key size must be at least 16 bits.")

    # 1. Generate two distinct large prime numbers p and q
    p = generate_prime_number(key_size // 2)
    q = generate_prime_number(key_size // 2)
    # Ensure p and q are distinct
    while p == q:
        q = generate_prime_number(key_size // 2)

    # 2. Calculate n = p * q
    n = p * q

    # 3. Calculate phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)

    # 4. Choose public exponent e
    # e must be 1 < e < phi and gcd(e, phi) == 1
    # Common choices are 3, 17, 65537 for efficiency, try 65537 first
    e = 65537
    if gcd(e, phi) != 1 or e >= phi: # Fallback if 65537 doesn't work
         e = random.randint(3, phi - 1)
         while gcd(e, phi) != 1:
             # Ensure e is odd as phi is always even
              if e % 2 == 0:
                  e = random.randint(3, phi - 1)
                  continue
              e = random.randint(3, phi - 1)


    # 5. Calculate private exponent d
    # d is the modular multiplicative inverse of e modulo phi
    d = mod_inv(e, phi)

    if d is None:
        # This should theoretically not happen if gcd(e, phi) == 1
        return None # Indicate failure

    # Return public key, private key, and intermediate values
    return (e, n), (d, n), p, q, phi

def encrypt(original_num, public_key):
    """
    Mã hóa một số nguyên bằng khóa công khai RSA.
    (Encrypt an integer using the RSA public key)

    Parameters:
        original_num (int): Số nguyên cần mã hóa (plaintext)
        public_key (tuple): Cặp khóa công khai RSA (e, n)

    Returns:
        int: Số nguyên đã được mã hóa (ciphertext)

    Raises:
        ValueError: If original_num >= n. RSA plaintext must be smaller than modulus.
    """
    e, n = public_key
    if original_num >= n:
         raise ValueError(f"Plaintext {original_num} is too large for modulus {n}.")

    return modular_exponentiation(original_num, e, n)

def decrypt(encoded_num, private_key):
    """
    Giải mã một số nguyên đã mã hóa bằng khóa riêng RSA.
    (Decrypt an encrypted integer using the RSA private key)

    Parameters:
        encoded_num (int): Số nguyên đã được mã hóa (ciphertext)
        private_key (tuple): Cặp khóa riêng RSA (d, n)

    Returns:
        int: Số nguyên đã được giải mã (original plaintext)
    """
    d, n = private_key
    # Ensure ciphertext is smaller than n, although it should be by definition
    if encoded_num >= n:
         raise ValueError(f"Ciphertext {encoded_num} is invalid for modulus {n}.")
    return modular_exponentiation(encoded_num, d, n)