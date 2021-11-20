"""
Description:
    Solving Linear Equation Ax = b by Constraint Propagation

Parameters:
    A: coefficient matrices
    b: right-hand side column vector

Comment:
"""
import numpy as np
import numpy.linalg as LA

A = np.array([
    [2, 1], \
    [1, -1]
    ])
b = np.array([5, 1])

# A = np.array([
#     [2, 4, 6], \
#     [4, 5, 6], \
#     [3, 1, -2]
#     ])
# b = np.array([18, 24, 4])

# A = np.array([
#     [9, 8, 9, 2], \
#     [5, 2, 7, 3], \
#     [6, 4, 3, 6], \
#     [8, 2, 5, 6]
#     ])
# b = np.array([42, 45, 53, 63])

M, N = A.shape
x = LA.solve(A, b)
x_lb = np.full(N, 0)
x_ub = np.full(N, 10.0)


def interval_overlap(lb1, ub1, lb2, ub2):
    if ub1 < lb2 or ub2 < lb1:  # non-overlap
        return lb1, ub1
    else:  # overlap
        return max(lb1, lb2), min(ub1, ub2)


for _ in range(2):
    for n in range(N):
        for m in range(M):
            if (A[m][n] != 0):
                lb = b[m] - sum([
                    max(A[m][i] * x_lb[i], A[m][i] * x_ub[i])
                    for i in range(N)
                    if i != n
                ])

                ub = b[m] - sum([
                    min(A[m][i] * x_lb[i], A[m][i] * x_ub[i])
                    for i in range(N)
                    if i != n
                ])

                lb, ub = \
                min(lb / A[m][n], ub / A[m][n]), max(lb / A[m][n], ub / A[m][n])

                # update
                x_lb[n], x_ub[n] = interval_overlap(x_lb[n], x_ub[n], lb, ub)

                print(f'x[{n}] in [{lb}, {ub}]')
                print(f'x[{n}] in [{x_lb[n]}, {x_ub[n]}]')
                print("\n")

for n in range(N):
    print(f'{x[n]} in [{x_lb[n]}, {x_ub[n]}]')
