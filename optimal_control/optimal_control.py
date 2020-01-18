# Description:
#     Simulate Nonlinear optimal control with constraints only dx/dt = f(x, u).
#     Optimization algorithm is Gradient method, implemented by using Pytorch auto differentiation.
#
# Reference:
#     非線形最適制御入門, p.141 勾配法.

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import truncnorm
import math
import torch
import torch.nn as nn
eps = np.finfo(float).eps

N = 100
dt = 0.1
I1 = np.arange(0, N)                 # 0, 1, ..., N-1
I2 = np.arange(0, N-1)               # 0, 1, ..., N-2(漸化式についてのみ使用可)
reverseI2 = (np.arange(1, N))[::-1]  # N-1, N-2, ..., 1(漸化式についてのみ使用可)

m, g = 1/9.8, 9.8
q1, q2 = 0.1, 0.01

xs = np.full(N, np.nan, dtype=float)
ys = np.full(N, np.nan, dtype=float)
us = np.full(N, np.nan, dtype=float)

lmd1s = np.full(N, np.nan, dtype=float)
lmd2s = np.full(N, np.nan, dtype=float)


def f(x, y, u):
    CL = (2*np.pi*u)/(1+2*u)
    dxdt = 1/2*(1.28*np.sin(u) + 1/(0.7*np.pi)*CL**2) * (np.log(y))**2
    dydt = 1/2*CL * (np.log(y))**2
    return (dxdt, dydt)    # dx/dt, dy/dt


def B(u):
    lb = -0.4
    ub = np.pi
    return 0.01/((u-lb)**2 * (u-ub)**2)


def H(x, y, lmd1, lmd2, u):
    CL = (2*np.pi*u)/(1+2*u)

    H = q1*x**2 - q2*y**2 + B(u)
    H += lmd1 * 1/2*(1.28*torch.sin(u) + 1/(0.7*np.pi)
                     * CL**2) * torch.log(y)**2
    H += lmd2 * 1/2*(CL - 1) * torch.log(y)**2
    return H

# def dHdX(x, y, lmd1, lmd2, u):
#     CL = (2*np.pi*u)/(1+2*u)
#
#     dHdx = 2*q1*x
#     dHdy = -2*q2*y
#     dHdy += lmd1 * (1.28*np.sin(u) + 1/(0.7*np.pi) * CL**2) * np.log(y)/y
#     dHdy += lmd2 * (CL-m*g)*np.log(y)/y
#     return (dHdx, dHdy)


def dHdX_auto(x, y, lmd1, lmd2, u):
    x_ = torch.tensor(x, requires_grad=True)
    y_ = torch.tensor(y, requires_grad=True)
    lmd1_ = torch.tensor(lmd1, requires_grad=True)
    lmd2_ = torch.tensor(lmd2, requires_grad=True)
    u_ = torch.tensor(u, requires_grad=True)

    H_ = H(x_, y_, lmd1_, lmd2_, u_)
    H_.backward()
    return (x_.grad.item(), y_.grad.item())   # dH/dx, dH/dy


# def dHdu(x, y, lmd1, lmd2, u):
#     CL = (2*np.pi*u)/(1+2*u)
#     lb, ub = -0.4, np.pi
#
#     dHdu = 0.02*(ub+lb-2*u)/(u-lb)**3/(u-ub)**3
#     dHdu += lmd1*1/2*(1.28*np.cos(u) + 2/(0.7*np.pi) * CL * 2*np.pi/(1+2*u)**2) * np.log(y)**2
#     dHdu += lmd2*1/2* 2*np.pi/(1+2*u)**2 *np.log(y)**2
#     return dHdu


def dHdu_auto(x, y, lmd1, lmd2, u):
    x_ = torch.tensor(x, requires_grad=True)
    y_ = torch.tensor(y, requires_grad=True)
    lmd1_ = torch.tensor(lmd1, requires_grad=True)
    lmd2_ = torch.tensor(lmd2, requires_grad=True)
    u_ = torch.tensor(u, requires_grad=True)

    H_ = H(x_, y_, lmd1_, lmd2_, u_)
    H_.backward()
    return u_.grad.item()  # dH/du


def L(x, y, u):
    """ Stage cost.
    """
    L = q1*x**2 - q2*y**2 + B(u)
    return L


def constructPhi(xs, ys, us, ss):
    """ Construct phi(a) := J(x, u+a*s), which to be miniized for a.
    """
    def phi(a):
        J = 0
        for k in I1:
            J += L(xs[k], ys[k], us[k] + a*ss[k])*dt
        return J
    return phi


def save(xs, ys, lmd1s, lmd2s, us):
    """  Save to csv.
    """
    return 1


# initial state
xs[0], ys[0] = 0, 1.5


# step 1
us = np.full(N, np.pi/6, dtype=float)

itr = 0
while True:
    # step 2
    for k in I2:
        dxdt, dydt = f(xs[k], ys[k], us[k])
        xs[k+1], ys[k+1] = xs[k] + dxdt * dt, ys[k] + dydt * dt

    # step 3
    lmd1s[-1], lmd2s[-1] = 0, 0
    for k in reverseI2:
        dHdx, dHdy = dHdX_auto(xs[k], ys[k], lmd1s[k], lmd2s[k], us[k])
        lmd1s[k-1], lmd2s[k-1] = lmd1s[k] + dHdx*dt, lmd2s[k] + dHdy*dt

    # step 4
    norm = 0
    for k in I1:
        norm += dHdu_auto(xs[k], ys[k], lmd1s[k], lmd2s[k], us[k])**2 * dt
    norm = np.sqrt(norm)

    if norm < 0.01:
        print("iteration: %d, norm %f" % (itr, norm))
        break

    # step 5
    ss = np.full(N, np.nan, dtype=float)
    for k in I1:
        ss[k] = (-1)*dHdu_auto(xs[k], ys[k], lmd1s[k], lmd2s[k], us[k])

    # phi = constructPhi(xs, ys, us, ss)
    # a = minimize_scalar(phi, bounds=(eps, 1), method='bounded').x
    a = 0.01

    # step 6
    for k in I1:
        us[k] += a*ss[k]

    save(xs, ys, lmd1s, lmd2s, us)

    if itr % 100 == 0:
        print("iteration: %d, norm %f" % (itr, norm))
    itr = itr + 1


def myformat(xs, ys, lmd1s, lmd2s, us):
    """ Header: 
    k, N, dt, q1, q2, x, y, lmd1, lmd2, u
    """
    for i in range(len(xs)):
        print("%d, %d, %f, %f, %f, %f, %f, %f, %f, %f" %
              (i, N, dt, q1, q2, xs[i], ys[i], lmd1s[i], lmd2s[i], us[i]), end="\n")
