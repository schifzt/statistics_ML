import numpy as np


# -------------------------------------------------------------------------
# (rho, alpha)がrho < alphaを満たすならば、L0ノルム最小化により再構成可能
rho = 0.3   # sparsity parameter
alpha = 0.3 # dim_measurement / dim_signal
dim_signal = 100
dim_measurement = int(alpha*dim_signal)

is_integer = False
# -------------------------------------------------------------------------

np.set_printoptions(
    formatter={'all':lambda x: '{:<10d}'.format(int(x)) if x == 0 else "{:.3f}".format(x)},
    threshold=np.inf
    )

# Create a true signal x0. dim = dim_signal
x0 = np.zeros(dim_signal)
K = 0
for n in range(dim_signal):
    if np.random.rand() > rho:
        x0[n] = np.random.normal(0, 1)
        K += 1
        if is_integer:
            x0[n] = int(x0[n])
    else:
        pass

# Create measurement matrix A. dim = dim_measurement x dim_signal
mean = np.zeros(dim_measurement*dim_signal)
cov = np.identity(dim_measurement*dim_signal) * 1/dim_signal
A = np.random.multivariate_normal(mean, cov).reshape((dim_measurement, dim_signal))
if is_integer:
    A = A.astype(int)

# Create measurement vector y := Ag
y = A@x0

print(x0)
# print(K)
# print(A)
print(y)

# Create output string for matrix
def matrix2string(A: np.ndarray):
    M, N = A.shape
    out = "["
    for m in range(M):
        out += "| "
        for n in range(N-1):
            out += "{:.3f}".format(A[m][n]) + ", "
        out += "{:.3f}".format(A[m][N-1])
        out += "\n"
        out += "     "
    out += "|]"

    return out


# Create dzn file
with open("input.dzn", "w") as f:
    s = ""
    s += f"dim_signal = {dim_signal};\n"
    s += f"dim_measurement = {dim_measurement};\n"
    s += f"K = {K};\n"
    s += "\n"
    s += "x0 = " + np.array2string(x0, separator=", ") + ";\n"
    s += "y  = " + np.array2string(y, separator=", ") + ";\n"
    s += "\n"
    s += "A = " + matrix2string(A) + ";\n"
    f.write(s)
