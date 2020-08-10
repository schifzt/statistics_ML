"""
Description:
   test script of this papar.
   + Free probability for purely discrete eigenvalues of random matrices
       + Proposition 5.2, Example 5.4
    
Parameters:
    n: size of matrices
    U: samples from Haar measure(uniform distribution on SO(n)). Unitary matrix.

Comment:
    There may be error in Examples 5.4. Index k=1,2,3 should be k=2,3,4.
"""
import numpy as np
import numpy.linalg as LA
from numpy.random import default_rng
import matplotlib.pyplot as plt
import seaborn as sns
rng = default_rng()


# def GUE(n):
#     M = rng.normal(0, 1, size=(n, n)) + rng.normal(0, 1, size=(n, n)) * 1j
#     return (M + np.conjugate(M.T)) / 2


# def GUE2(n, mu):
#     U = Haar(n)
#     D = np.diag(mu)
#     return U @ D @ np.conjugate(U).T


def Haar(n):
    M = rng.normal(0, 1, size=(n, n))
    U, _, _ = LA.svd(M)
    return U


def P(D, U):
    return D + U @ D @ np.conjugate(U).T


n = 500

mu1 = np.array([(-1)**(i % 2) / (i + 1)
                for i in range(n)])  # absolutely convergent series
mu2 = np.array([(-1)**(i % 2) * np.log(i + 1) / (i + 1) ** 3
                for i in range(n)])  # absolutely convergent series
mu3 = np.array([1 / 2 ** (i + 1)
                for i in range(n)])  # absolutely convergent series

mu = mu3
D = np.diag(mu)
U = Haar(n)
# G = GUE2(n, mu2)

EV = LA.eigvals(P(D, U))
EV = np.sort(EV)[::-1]
EV = np.real(EV)
# print(EV)

MU = np.sort(mu)[::-1]
# print(MU)

idx = np.arange(n)


sns.set()
sns.set_style('whitegrid')
sns.set_palette('gray')

len = 20
ax = sns.scatterplot(x=idx[:len], y=EV[:len], color='g')
for i in range(int(len/2)):
    plt.hlines(MU[i], 0, len, linestyle="dotted", color="gray")

ax.set_xlabel("$i$")
ax.set_ylabel("$\lambda_i$")


plt.show()
