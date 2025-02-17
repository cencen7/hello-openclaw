import numpy as np

"""
we need to compute the Jocobian matrix, which represnets the derivative of f(x) respect to x
then compute the backpropagation of the function f(x) with respect to x

s = sorted(x)
m = mediam(x)
f(x) = s / m

apply the chain rule to compute df/dx
df/dx 
= df/ds * ds/dx + df/dm * dm/dx
= 1/m * I * P - s / m^2 * g(T)
= 1/m * P(T) * v - g dot (s(T) * v / m^2)
P(T) v maps the gradient from sorted indices back to original indices.
s(T) v is the dot product, capturing how much the median term affects the overall gradient.



compute df/ds: 1/m * I where I is the identity matrix
compute df/dm: -s / m^2
comptute ds/dx: x = Px where P is the permutation matrix ==> ds/dx = P
compute dm/dx: 1/n * I where n is the number of elements in x
if x has odd number of elements, m = x[n//2]
if x has even number of elements, m = (x[n//2] + x[n//2 - 1]) / 2
The median 𝑚.m depends on the middle element(s) of 𝑥; 
Its derivative is a sparse vector g

"""
def f(x): 
    return np.sort(x) / np.medium(x)

def compute_backpropagation(x, v):
    """
    compute the backpropagation of the function f(x) with respect to x
    f(x) = np.sort(x) / np.medium(x)
    given output gradient v.
    """
    n = len(x)
    s = np.sort(x)
    m = np.median(x)

    # compute permutation matrix P
    P = np.zeros((n, n))
    sorted_indices = np.argsort(x)
    for i, idx in enumerate(sorted_indices):
        P[i, idx] = 1
    
    # compute derivative of median w.r.t x
    g = np.zeros(n)
    if n % 2 == 1:
        meian_idx = sorted_indices[n//2]
        g[meian_idx] = 1
    else:
        median_idx1 = sorted_indices[n//2]
        median_idx2 = sorted_indices[n//2 - 1]
        g[median_idx1] = 0.5
        g[median_idx2] = 0.5

    # compute gradient
    P_T_v = np.dot(P.T, v)
    s_T_v = np.dot(s, v)
    gradient = (1/m) * P_T_v - g * (s_T_v / m**2)

    return gradient

# Example
x = np.array([3.0, 1.0, 4.0, 1.5, 2.5])
v = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
grad = compute_backpropagation(x, v)
print("Gradient:", grad)


    