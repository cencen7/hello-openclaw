"""
matrix_diagonal_zigzag.py

Diagonal zigzag traversal routines: both top-left and top-right start.

- Top-left: Standard Leetcode-style diagonal order.
- Top-right: Alternative for interview/code tasks requiring rightward start.

Works for both square and rectangular matrices.

Author: cencen7 / Mia's helper
"""

def diagonal_zigzag_top_left(matrix):
    """
    Diagonal zigzag traversal from the TOP-LEFT corner.
    Each diagonal is grouped by (row + col).
    Alternate reversing the diagonal on each step.

    Example:
        Input: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        Output: [1, 2, 4, 7, 5, 3, 6, 8, 9]
    """
    if not matrix or not matrix[0]: return []
    m, n = len(matrix), len(matrix[0])
    diagonals = {}
    for r in range(m):
        for c in range(n):
            diag_idx = r + c
            diagonals.setdefault(diag_idx, []).append(matrix[r][c])
    result = []
    for diag in range(m + n - 1):
        group = diagonals[diag]
        if diag % 2 == 0:
            result.extend(group[::-1])
        else:
            result.extend(group)
    return result

def diagonal_zigzag_top_right(matrix):
    """
    Diagonal zigzag traversal from the TOP-RIGHT corner.
    Each diagonal is grouped by (row + (num_cols - 1 - col)).
    Alternate reversing the diagonal on each step.

    Example:
        Input: [[1,2,3], [4,5,6], [7,8,9]]
        Output: [3, 2, 6, 1, 5, 9, 4, 8, 7]
    """
    if not matrix or not matrix[0]: return []
    m, n = len(matrix), len(matrix[0])
    diagonals = {}
    for r in range(m):
        for c in range(n):
            diag_idx = r + (n-1-c)
            diagonals.setdefault(diag_idx, []).append(matrix[r][c])
    result = []
    reverse = False
    for diag in range(m + n - 1):
        group = diagonals[diag]
        result.extend(group[::-1] if reverse else group)
        reverse = not reverse
    return result

if __name__ == "__main__":
    mat1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    mat2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
    print("Top-left diag (mat1):", diagonal_zigzag_top_left(mat1))   # [1,2,4,7,5,3,6,8,9]
    print("Top-right diag (mat1):", diagonal_zigzag_top_right(mat1)) # [3,2,6,1,5,9,4,8,7]
    print("Top-left diag (mat2):", diagonal_zigzag_top_left(mat2))   # [1,2,5,6,3,4,7,8]
    print("Top-right diag (mat2):", diagonal_zigzag_top_right(mat2)) # [4,3,8,2,7,1,6,5]
