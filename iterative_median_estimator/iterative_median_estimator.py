import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

"""
function:
    parameter:
        float datam x[i] (on-line)
    reutrn:
        estimated median value

how it works:
    A mean is characterized as a minimizer of a loss $L(a) = \sum_{i \in [N]} (x_i - a)**2 $,
    so the derivative wrt a is $ -2*\sum_{i \in [N]} (x_i -a) $.
    Similarly,
    a median is characterized as a minimizer of a loss $L(a) = \sum_{i \in [N]} |x_i - a| $,
    so the derivative wrt a is $ \sum_{i \in [N]} sign(x_i - a) $.

    We estimate median iteratively by a gradient method, especially using Adam.

"""

N = 500
alpha = 1.0 * 10**(0)

# -------------------------------------------
# Adam
# https://arxiv.org/abs/1412.6980
# -------------------------------------------
def adam_closure(theta0, alpha: int):
    beta1, beta2, eps = 0.9, 0.999, 10**(-8)
    theta, m, v = theta0, 0, 0
    t = 0

    def adam(grad: float):
        nonlocal t, theta, m, v

        t += 1
        m = beta1 * m + (1-beta1)*grad
        v = beta2 * v + (1-beta2)*grad**2
        m_hat = m / (1-beta1**t)
        v_hat = v / (1-beta2**t)
        theta = theta - alpha*m_hat/(np.sqrt(v_hat)+ eps)

        return theta

    return adam

adam1 = adam_closure(theta0 = 0, alpha = alpha)
adam2 = adam_closure(theta0 = 0, alpha = alpha)


# -------------------------------------------
# x ~ bimodal distribution
# -------------------------------------------
def data_closure():
    mu1, sd1 = 0, 10
    mu2, sd2 = 100, 10
    weight = 0.1
    t = 0
    def generate_datam():
        if np.random.uniform(0, 1) < weight:
            return np.random.normal(mu1, sd1)
        else:
            return np.random.normal(mu2, sd2)

    return generate_datam

generate_datam = data_closure()


# -------------------------------------------
# main
# -------------------------------------------
X, mean_estm, median_estm = np.zeros(N), np.zeros(N), np.zeros(N)

for i in range(1, N):
    x = generate_datam()
    X[i] = x
    mean_estm[i] = adam1(grad = -2*(x - mean_estm[i-1]))
    median_estm[i] = adam2(grad = -np.sign(x - median_estm[i-1]))


print(f"mean:\n\testimate = {mean_estm[-1]}, true = {np.mean(X)}")
print(f"median:\n\testimate = {median_estm[-1]}, true = {np.median(X)}")


df = pd.DataFrame(data={
    'x': X,
    'true mean (updated iteratively)': [np.mean(X[:i]) for i in range(N)],
    'mean estimate': mean_estm,
    'true median (updated iteratively)': [np.median(X[:i]) for i in range(N)],
    "median estimate": median_estm})

sns.lineplot(data=df['x'], linewidth=1, alpha = 0.5)
sns.lineplot(data=df.drop(['x'], axis=1), palette="tab10", linewidth=1, alpha = 1)
plt.show()