import numpy as np

# Global variable for the true S (in a real problem, S is unknown)
true_S = None

def noisy_xor(X, noise_prob=0.02):
    """
    Simulate the noisy_xor function.
    Given an input binary vector X (numpy array), this function computes:
      noisy_xor(X) = HammingWeight(true_S XOR X XOR u)
    where u is a noise vector with each bit being 1 with probability noise_prob.
    """
    global true_S
    # Generate noise vector u: each bit is 1 with probability noise_prob
    u = (np.random.rand(len(true_S)) < noise_prob).astype(int)
    # Compute bitwise XOR: true_S ⊕ X ⊕ u
    result = true_S ^ X ^ u
    # Return the number of 1's in the result
    return result.sum()

def recover_S(N, M):
    """
    Recover the unknown N-bit number S using paired queries.
    
    Parameters:
      N: Number of bits in S.
      M: Number of paired queries for each bit (each pair makes 2 calls).
      
    Returns:
      recovered_S: The recovered S as a numpy array of bits (0's and 1's).
    """
    recovered_S = np.zeros(N, dtype=int)
    
    # Process each bit independently
    for i in range(N):
        differences = []
        # Construct e_i: vector with 1 only at position i
        X_ei = np.zeros(N, dtype=int)
        X_ei[i] = 1
        for _ in range(M):
            # Query A: use an all-zero vector
            X0 = np.zeros(N, dtype=int)
            a = noisy_xor(X0)
            # Query B: use e_i (which flips the i-th bit of true_S)
            b = noisy_xor(X_ei)
            # The difference isolates the effect of flipping the i-th bit.
            differences.append(b - a)
        avg_d = np.mean(differences)
        # In an ideal (noiseless) scenario:
        #  - If true_S[i] = 1, f(e_i) - f(0) should be -1.
        #  - If true_S[i] = 0, it should be +1.
        # So, if the average difference is negative, infer bit=1; otherwise, 0.
        recovered_S[i] = 1 if avg_d < 0 else 0
        
    return recovered_S


# Set the number of bits for S.
N = 100

# For simulation, generate a random true S (each bit 0 or 1).
true_S = np.random.randint(0, 2, size=N)
print("True S =", true_S)

# Determine M (number of paired queries per bit) so that total calls (2*M*N) <= 10000.
M = 10000 // (2 * N)
print("Number of paired queries per bit, M =", M)

# Recover S using the paired queries.
recovered_S = recover_S(N, M)
print("Recovered S =", recovered_S)

# Check if recovery was successful.
if np.array_equal(true_S, recovered_S):
    print("Successfully recovered S!")
else:
    print("Failed to recover S.")
