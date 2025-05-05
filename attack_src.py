# attack_src.py
# RSA Attack Simulation Logic

import math
import time
from src import modular_exponentiation, extended_gcd, mod_inv # Reuse functions

# --- Factorization Attack ---
# ... (code factorization_attack và trial_division giữ nguyên) ...
def trial_division(n, limit=1000000):
    """
    Attempts to factor n using trial division up to a limit.

    Args:
        n (int): The number to factor (RSA modulus).
        limit (int): The maximum divisor to check.

    Returns:
        tuple: (p, q) if factorization is successful within the limit, else (None, None).
    """
    if n % 2 == 0:
        # Handle small n=4 case etc.
        p_test, q_test = 2, n // 2
        if p_test * q_test == n:
            return p_test, q_test
        else: # n might be just 2
             return None, None


    # Check odd divisors up to the limit or sqrt(n)
    d = 3
    # Optimization: only check up to sqrt(n)
    check_limit = min(limit, math.isqrt(n))
    while d <= check_limit: # Use check_limit
        if n % d == 0:
            return d, n // d
        d += 2 # Check next odd number

    # # Check if limit itself is a factor (less likely, removed for simplicity/speed)
    # if limit > 1 and n % limit == 0 and limit*limit > n:
    #      return limit, n // limit

    return None, None # Factorization failed within limit or n prime

def factorize_attack(e, n, c):
    """
    Performs factorization attack on RSA parameters.

    Args:
        e (int): Public exponent.
        n (int): Modulus.
        c (int): Ciphertext.

    Returns:
        dict: Results including success status, factors, private key, message, time.
    """
    start_time = time.time()
    result = {
        "attack_type": "Factorization (Trial Division)",
        "success": False,
        "message": "Factorization using trial division failed (limit reached or n is prime/too large).",
        "p": None,
        "q": None,
        "phi": None,
        "d": None,
        "decrypted_message": None,
        "time_taken": 0.0
    }

    # Use a reasonable limit for trial division, maybe smaller than default
    # or dynamically based on n? For simulation, 1M is okay.
    p, q = trial_division(n, limit=1000000) # Keep default limit or adjust if needed

    if p and q:
        # Double check factors are correct
        if p * q != n:
             result["message"] = f"Internal error: Found factors {p}, {q} but p*q != n ({n})."
             # Fall through to failure state below
        else:
            try:
                phi = (p - 1) * (q - 1)
                # Check if e and phi are coprime BEFORE calculating inverse
                if extended_gcd(e, phi)[0] != 1:
                    raise ValueError(f"e ({e}) and phi(n) ({phi}) are not coprime (gcd != 1). Cannot compute d.")

                d = mod_inv(e, phi)
                if d is None:
                     # This case should ideally be caught by the gcd check above
                     raise ValueError(f"Could not compute modular inverse for e={e}, phi={phi}. gcd(e, phi) != 1?")

                decrypted_m = modular_exponentiation(c, d, n)

                result.update({
                    "success": True,
                    "message": "Factorization successful! Private key recovered.",
                    "p": p,
                    "q": q,
                    "phi": phi,
                    "d": d,
                    "decrypted_message": decrypted_m,
                })
            except Exception as err:
                result["message"] = f"Factorization found factors ({p}, {q}), but failed to calculate key/decrypt: {err}"
    else:
         # Keep the default failure message
         pass


    end_time = time.time()
    result["time_taken"] = end_time - start_time
    return result


# --- Wiener's Attack (Small Private Exponent) ---
# ... (code wiener_attack, _continued_fraction_coeffs, _convergents_from_coeffs giữ nguyên) ...
def _continued_fraction_coeffs(numerator, denominator):
    """Calculates coefficients of the continued fraction for num/den."""
    coeffs = []
    while denominator:
        quotient = numerator // denominator
        coeffs.append(quotient)
        numerator, denominator = denominator, numerator % denominator
    return coeffs

def _convergents_from_coeffs(coeffs):
    """Generates convergents (k/d) from continued fraction coefficients."""
    # Corrected Initialization based on standard algorithm:
    # h_n = a_n * h_{n-1} + h_{n-2}
    # k_n = a_n * k_{n-1} + k_{n-2}
    # Initialize h_{-2}=0, k_{-2}=1, h_{-1}=1, k_{-1}=0
    h_prev2, k_prev2 = 0, 1
    h_prev1, k_prev1 = 1, 0

    for i, a_i in enumerate(coeffs):
        h_curr = a_i * h_prev1 + h_prev2
        k_curr = a_i * k_prev1 + k_prev2

        # Yield k/d (numerator/denominator of convergent)
        # k_curr is the denominator here, representing potential 'd'
        if k_curr != 0: # Avoid division by zero
             # Convergent is h_curr / k_curr
             # We test k_curr as potential 'd' and h_curr as potential 'k'
             # from the Wiener's condition ed - k*phi = 1 -> e/phi approx k/d
             # No, Wiener uses e/n approx k/d. So yield (h_curr, k_curr) -> (potential k, potential d)
             yield (h_curr, k_curr)

        # Update previous values
        h_prev2, k_prev2 = h_prev1, k_prev1
        h_prev1, k_prev1 = h_curr, k_curr

def wiener_attack(e, n, c):
    """
    Performs Wiener's attack based on continued fractions for small d.
    Condition for success: d < (1/3) * n^(1/4)

    Args:
        e (int): Public exponent.
        n (int): Modulus.
        c (int): Ciphertext.

    Returns:
        dict: Results including success status, found d, message, time.
    """
    start_time = time.time()
    result = {
        "attack_type": "Wiener's Attack (Small d)",
        "success": False,
        "message": "Wiener's attack failed. Private exponent 'd' might not be small enough (d < (1/3)n^(1/4)?) or conditions not met.",
        "d": None,
        "k": None, # Convergent numerator
        "phi_candidate": None,
        "p": None, # Factors if found
        "q": None,
        "decrypted_message": None,
        "time_taken": 0.0
    }

    try:
        cf_coeffs = _continued_fraction_coeffs(e, n)
        # The convergents approximate e/n. Let the convergent be k'/d' (using different notation to avoid clash)
        # Wiener's theorem relates e/n to k/d where ed - k*phi = 1.
        # The convergents k'/d' of e/n are candidates for k/d.
        for k_candidate, d_candidate in _convergents_from_coeffs(cf_coeffs):
            # Basic checks on candidates
            if k_candidate == 0 or d_candidate == 0:
                continue
            # d must be odd (usually, unless phi is weird, but safe check)
            # Let's not filter by d_candidate oddness here, check later if needed.

            # From e*d - k*phi = 1 (or some small integer, usually 1)
            # If k_candidate and d_candidate are the correct k and d...
            # Check if d_candidate is a valid private exponent candidate
            # Test if M = C^d (mod n) works. This is the direct check.

            # Check 1: Try decrypting directly with d_candidate
            try:
                 test_m = modular_exponentiation(c, d_candidate, n)
                 # Verify if this m^e = c mod n
                 test_c = modular_exponentiation(test_m, e, n)
                 if test_c == c:
                     # Potential success! Now try to derive p, q if possible (for full verification)
                     # We need phi = (e*d - 1) / k
                     # Check if (e * d_candidate - 1) is divisible by k_candidate
                     if (e * d_candidate - 1) % k_candidate == 0:
                         phi_candidate = (e * d_candidate - 1) // k_candidate

                         # Now solve x^2 - (n - phi + 1)x + n = 0 for p, q
                         s = n - phi_candidate + 1
                         discriminant = s*s - 4*n

                         if discriminant >= 0:
                             sqrt_discriminant = math.isqrt(discriminant)
                             if sqrt_discriminant * sqrt_discriminant == discriminant:
                                 if (s + sqrt_discriminant) % 2 == 0:
                                     p_candidate = (s + sqrt_discriminant) // 2
                                     q_candidate = n // p_candidate # Use division for robustness

                                     if p_candidate * q_candidate == n and p_candidate != 1 and q_candidate != 1:
                                         # All checks pass!
                                         result.update({
                                             "success": True,
                                             "message": "Wiener's attack successful! Small private exponent 'd' found.",
                                             "d": d_candidate,
                                             "k": k_candidate,
                                             "phi_candidate": phi_candidate,
                                             "p": p_candidate,
                                             "q": q_candidate,
                                             "decrypted_message": test_m, # Use the already computed one
                                         })
                                         break # Exit loop once found
                     # If we reach here after finding a working d, but couldn't derive p,q,
                     # it's still a success in finding d and M, but maybe flag it?
                     # For now, let's assume finding p, q is required for full confirmation.
                     # If the direct decryption check (test_c == c) passed but factor check failed,
                     # we might still report success but without p, q. Let's stick to requiring p,q check.

            except OverflowError:
                 # d_candidate might be too large for modular_exponentiation if n is huge
                 # but d is small. Should not happen with typical RSA params.
                 continue
            except Exception:
                 # Ignore other potential errors during the candidate check phase
                 continue

    except Exception as err:
         result["message"] = f"An error occurred during Wiener's attack processing: {err}"


    end_time = time.time()
    result["time_taken"] = end_time - start_time
    return result


# --- Brute-Force Attack (Message) ---

def brute_force_message_attack(e, n, c, limit=1000000):
    """
    Attempts to find the original message M by trying values 0..limit.
    C = M^e mod n

    Args:
        e (int): Public exponent.
        n (int): Modulus.
        c (int): Ciphertext.
        limit (int): The maximum value of M to check.

    Returns:
        dict: Results including success status, message, time.
    """
    start_time = time.time()
    result = {
        "attack_type": "Brute-Force (Message)",
        "success": False,
        "message": f"Brute-force failed. Message M not found within the tested limit (M <= {limit}). This attack is generally infeasible for secure RSA.",
        "limit_tested": limit,
        "decrypted_message": None,
        "time_taken": 0.0
    }

    # Check trivial case M=0 -> C=0, M=1 -> C=1
    if c == 0:
        m_candidate = 0
        c_candidate = modular_exponentiation(m_candidate, e, n)
        if c_candidate == c:
             result.update({
                "success": True,
                "message": f"Brute-force successful (found M=0).",
                "decrypted_message": 0,
             })
             end_time = time.time()
             result["time_taken"] = end_time - start_time
             return result
    if c == 1:
        m_candidate = 1
        c_candidate = modular_exponentiation(m_candidate, e, n)
        if c_candidate == c:
             result.update({
                "success": True,
                "message": f"Brute-force successful (found M=1).",
                "decrypted_message": 1,
             })
             end_time = time.time()
             result["time_taken"] = end_time - start_time
             return result

    # Iterate from 2 up to the limit
    for m_candidate in range(2, limit + 1):
        # Calculate m^e mod n
        try:
            c_candidate = modular_exponentiation(m_candidate, e, n)
        except Exception as calc_err:
            # Handle potential errors during calculation if needed
            result["message"] = f"Error during modular exponentiation for M={m_candidate}: {calc_err}"
            break # Stop the attack if calculation fails

        # Compare with the target ciphertext
        if c_candidate == c:
            result.update({
                "success": True,
                "message": f"Brute-force successful! Found message M by testing values up to {limit}.",
                "decrypted_message": m_candidate,
            })
            break # Exit loop once found

    end_time = time.time()
    result["time_taken"] = end_time - start_time
    # Update message if failed to include the limit tested
    if not result["success"]:
         result["message"] = f"Brute-force failed. Message M not found within the tested limit (M <= {limit}). This attack is generally infeasible for secure RSA."

    return result