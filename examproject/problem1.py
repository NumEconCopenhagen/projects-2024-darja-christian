import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import ipywidgets as widgets # for interactive plots/buttons
from scipy import optimize # for numerical solutions
import sympy as sm # for analytical solution
from types import SimpleNamespace

import numpy as np
from types import SimpleNamespace

# Define parameters
par = SimpleNamespace()
par.A = 1.0
par.gamma = 0.5
par.alpha = 0.3
par.nu = 1.0
par.epsilon = 2.0
par.tau = 0.0
par.T = 0.0

# Define the range for p1 and p2
p1_range = np.linspace(0.1, 2.0, 10)
p2_range = np.linspace(0.1, 2.0, 10)
w = 1.0  # wage

# Functions to calculate optimal values
def optimal_labor(w, p, A, gamma):
    return (p * A**gamma / w)**(1 / (1 - gamma))

def optimal_output(A, l, gamma):
    return A * l**gamma

def optimal_profit(w, p, A, gamma):
    l = optimal_labor(w, p, A, gamma)
    return p * optimal_output(A, l, gamma) - w * l

def consumer_utility(w, T, p1, p2, tau, alpha, nu, epsilon):
    lhs = alpha / p1 + (1 - alpha) / (p2 + tau)
    rhs = (1 + nu * (1 + epsilon) / (1 + epsilon))
    return lhs, rhs

# Check market clearing conditions
results = []
for p1 in p1_range:
    for p2 in p2_range:
        l1 = optimal_labor(w, p1, par.A, par.gamma)
        l2 = optimal_labor(w, p2, par.A, par.gamma)
        y1 = optimal_output(par.A, l1, par.gamma)
        y2 = optimal_output(par.A, l2, par.gamma)
        pi1 = optimal_profit(w, p1, par.A, par.gamma)
        pi2 = optimal_profit(w, p2, par.A, par.gamma)
        
        # Total labor and goods
        total_labor = l1 + l2
        total_goods1 = y1
        total_goods2 = y2
        
        # Optimal consumption
        c1 = par.alpha * (w * total_labor + par.T + pi1 + pi2) / p1
        c2 = (1 - par.alpha) * (w * total_labor + par.T + pi1 + pi2) / (p2 + par.tau)
        
        # Check market clearing conditions
        labor_market_clearing = np.isclose(total_labor, l1 + l2)
        goods_market1_clearing = np.isclose(total_goods1, c1)
        goods_market2_clearing = np.isclose(total_goods2, c2)
        
        results.append({
            'p1': p1,
            'p2': p2,
            'labor_market': labor_market_clearing,
            'goods_market1': goods_market1_clearing,
            'goods_market2': goods_market2_clearing
        })




## QUESTION 2


# Functions to calculate optimal values
def optimal_labor(w, p, A, gamma):
    return (p * A * gamma / w)**(1 / (1 - gamma))

def optimal_output(A, l, gamma):
    return A * l**gamma

def optimal_profit(w, p, A, gamma):
    l = optimal_labor(w, p, A, gamma)
    return p * optimal_output(A, l, gamma) - w * l

def equilibrium_conditions(vars, par):
    p1, p2 = vars

    # Optimal labor and output for each good
    l1 = optimal_labor(w, p1, par.A, par.gamma)
    l2 = optimal_labor(w, p2, par.A, par.gamma)
    y1 = optimal_output(par.A, l1, par.gamma)
    y2 = optimal_output(par.A, l2, par.gamma)
    pi1 = optimal_profit(w, p1, par.A, par.gamma)
    pi2 = optimal_profit(w, p2, par.A, par.gamma)
    
    # Total labor
    total_labor = l1 + l2
    
    # Household income
    income = w * total_labor + par.T + pi1 + pi2
    
    # Optimal consumption
    c1 = par.alpha * income / p1
    c2 = (1 - par.alpha) * income / p2
    
    # Market clearing conditions
    goods_market1 = y1 - c1
    goods_market2 = y2 - c2
    ## we will only concentrate on two out of three markets 
    return goods_market1, goods_market2

def absolute_sum(vars, par):
    result = equilibrium_conditions(vars, par)
    #return np.sum(np.square(residuals))
    return sum(np.abs(result))



