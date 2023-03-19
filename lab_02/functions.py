from math import sqrt, ceil, floor, pi

import numpy as np


def min_round(num: float) -> float:
    if num > 0:
        return ceil(num)
    return floor(num)


def to_radians(angle_degrees: float) -> float:
    return pi * angle_degrees / 180


def multiply_matrices(matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray | None:
    if matrix_a.shape != matrix_b.shape or matrix_a.shape[0] != matrix_a.shape[1]:
        raise ValueError

    result_matrix = np.zeros(matrix_a.shape)
    length = matrix_a.shape[0]

    for i in range(length):
        for j in range(length):
            for k in range(length):
                result_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]

    return result_matrix
