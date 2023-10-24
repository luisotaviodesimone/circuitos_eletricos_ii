import sympy as sp
import numpy as np

s = sp.Symbol("s")
m = sp.Symbol("m")

# matrixA = sp.Matrix([
#   [8 + 2*s, 2*s, 0, -1, 0],
#   [2*s, 4+2*s, 0, -1, 0],
#   [0, 0, 0, 1, 1],
#   [4, -1, 1, 0, 0],
#   [0, 0, 1, 0, -1]
# ])

# matrixA = sp.Matrix([
#   [1/2, 0, 1],
#   [5/2, 1/6+1/3+2*s, 0],
#   [1, 1, -4*s]
# ])


matrixA = sp.Matrix(
    [
        [1 / 16 + 1 / 9, 0, -1 / 9, 0],
        [-1 / 16, -1 / (3), 0, 0],
        [0, -1 / 5, -1 + s * 2, -1],
        [0, -1, 0, s * 5],
    ]
)

# matrixB = sp.Matrix([
#   [2-3/s],
#   [2],
#   [3/s],
#   [0],
#   [4]
# ])

# matrixB = sp.Matrix([
#   [0],
#   [-2],
#   [-8]
# ])

matrixB = sp.Matrix([[0], [0], [2 * 7], [5 * 11]])


solution = matrixA.solve(matrixB)

print(np.array(solution))

H = solution[2] / solution[0]

print()
print(sp.simplify(H))
