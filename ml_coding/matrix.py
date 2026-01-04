import numpy as np

def reshape_matrix(a: list[list[int|float]], new_shape: tuple[int, int]) -> list[list[int|float]]:
	#Write your code here and return a python list after reshaping by using numpy's tolist() method
    # validation logic here
    if a is None:
        return
    if len(a) == 0:
        return a
    n_rows, n_cols = len(a), len(a[0])
    if n_rows * n_cols != new_shape[0] * new_shape[1]:
        return []
    # method 1: numpy
    #reshaped_matrix = np.array(a).reshape(new_shape).tolist()

    # method 2: native
    # current: i, j; --> position: i * n_cols + j 
    # --> reshaped: pos // new_shape[1], pos % new_shape[1]
    reshaped_matrix = [
        [0.0 for _ in range(new_shape[1])] for _ in range(new_shape[0])
    ]
    for i in range(n_rows):
        for j in range(n_cols):
            pos = i * n_cols + j 
            new_i, new_j = pos // new_shape[1], pos % new_shape[1]
            # print(f'i: {i}; j:{j}')
            reshaped_matrix[new_i][new_j] = a[i][j]
	
    return reshaped_matrix


def calculate_matrix_mean(matrix: list[list[float]], mode: str) -> list[float]:
    """
    if mode == 'column':
	    means = numpy.mean(np.array(matrix), axis=0)
    elif mode == 'row':
        means = numpy.mean(np.array(matrix), axis=1)
    else:
        means = None
    """
    if matrix is None:
        return
    if len(matrix) == 0:
        return matrix
    n_rows, n_cols = len(matrix), len(matrix[0])
    
    if mode == 'row':
        means = []
        for i in range(n_rows):
            row_mean = sum(matrix[i]) / n_cols
            means.append(row_mean)
    elif mode == 'column':
        means = []
        for j in range(n_cols):
            col_mean = sum([matrix[i][j] for i in range(n_rows)]) / n_rows
            means.append(col_mean)
    else:
        raise ValueError(f"input mode can only be row or column!")
    
    return means


import math

def calculate_eigenvalues(matrix: list[list[float|int]]) -> list[float]:
    """

    matrix = [[2, 1], [1, 2]]
    matrix - lambda * I 
    ||
    [[2-lambda, 1]
    [1, 2-lambda]]

    det (matrix - lamba * I)
    (2-lambda)(2-lambda)  - 1 = 0
    4 + lambda^2 - 4*lambda - 1 = 0
    lambda^2 - 4*lambda + 3 = 0
    (lambda - 3)(lambda - 1) = 0

    ===============
    matrix = [[a, b], [c, d]]
    (a-lambda)(d-lambda) - b*d = 0
    lambda**2 - (a+d)*lambda + a*d - c*b = 0
    trace = (a+d)
    det(A) = a*d - c*b

    lambda_ans1 = (trace + sqrt(trace**2 - 4*det)) / 2
    lambda_ans2 = (trace - sqrt(trace**2 - 4*det)) / 2

    """
    if matrix is None:
        return
    if len(matrix) == 0:
        return matrix
    if len(matrix) != 2 or len(matrix[0]) != 2:
        raise ValueError('not valid')
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    
    trace = a + d
    det = a * d - c * b
    lambda_ans1 = (trace + math.sqrt(trace**2 - 4 * det)) / 2
    lambda_ans2 = (trace - math.sqrt(trace**2 - 4 * det)) / 2
    eigenvalues = [lambda_ans1, lambda_ans2]
    return eigenvalues


def inverse_2x2(matrix: list[list[float]]) -> list[list[float]] | None:
    """
    Calculate the inverse of a 2x2 matrix.
    
    Args:
        matrix: A 2x2 matrix represented as [[a, b], [c, d]]
    
    Returns:
        The inverse matrix as a 2x2 list, or None if the matrix is singular
        (i.e., determinant equals zero)

    inversed of 
    [[a, b]
    [c, d]]
    ||
    (1/a*d - b*c) * [[d, -b], [-c, a]]
    """
    # Your code here
    if len(matrix) == 0:
        return matrix
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    det = a * d - b * c
    # invertible does not exist
    if det == 0:
        return
    inversed = [[d*(1/det), -b*(1/det)], [-c*(1/det), a*(1/det)]]
    return inversed


import numpy as np

def transform_matrix(A: list[list[int|float]], T: list[list[int|float]], S: list[list[int|float]]) -> list[list[int|float]]:
    """
	m, n = A.shape
	check conditions:
	1. matrix empty
	2. if T dimension is not m x n, invalid
	3. if S dimension is not n x n, invalid
	4. if T is not invertible, invalid
	5. if S is not invertible, invalid
	"""
	if len(A) == 0:
		return A
	if len(T) == 0 or len(S) == 0:
		return -1
	
	A = np.array(A)
	T = np.array(T)
	S = np.array(S)
	m, n = A.shape

	if T.shape != (m, n):
		return -1
	if S.shape != (n, n):
		return -1
	
	if np.linalg.det(T) == 0:
		return -1
	if np.linalg.det(S) == 0:
		return -1

	transformed_matrix = np.linalg.inv(T) @ A @ S

	return transformed_matrix




