import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import ipywidgets as widgets # for interactive plots/buttons
from scipy import optimize # for numerical solutions
import sympy as sm # for analytical solution
from types import SimpleNamespace


## QUESTION 1
par = SimpleNamespace()
par.J = 3
par.N = 10
par.K = 10000 ## number of simulations 

par.F = np.arange(1,par.N+1)
par.sigma = 2 ## sigma of the normal distribution 

par.v = np.array([1,2,3])
par.c = 1

# Initialize arrays to store results
expected_utility = np.zeros(par.J)
realized_utility = np.zeros(par.J)

# set seed 
np.random.seed(2024)
# the noise for each career track, assuming normal distribution according to problem set 
epsilon = np.random.normal(0, par.sigma, (par.J, par.K))

# Calculate expected utility and realized utility for each career choice
for j in range(par.J):
    v_j = par.v[j] 
    u_ij_k = v_j + epsilon[j, :]
    expected_utility[j] = v_j + 1/par.K * np.sum(epsilon[j,:])
    realized_utility[j] = np.mean(u_ij_k)





