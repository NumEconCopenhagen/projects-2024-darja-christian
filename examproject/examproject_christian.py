import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from types import SimpleNamespace

def market_clearing_conditions(p, par):
    """
    Calculate the market clearing conditions for goods 1 and 2.
    
    Parameters:
    - p (list): List containing prices [p1, p2].
    - par (SimpleNamespace): Namespace containing model parameters.
    
    Returns:
    - list: List containing market clearing conditions for good1 and good2.
    """
    w = 1  # numeraire
    p1, p2 = p

    # Prevent division by zero
    if p1 == 0 or p2 == 0:
        return [np.inf, np.inf]

    # Optimal labor
    l1 = (p1 * par.A ** par.gamma / w) ** (1 / (1 - par.gamma))
    l2 = (p2 * par.A ** par.gamma / w) ** (1 / (1 - par.gamma))
    l_total = l1 + l2

    # Optimal production
    y1 = par.A * l1 ** par.gamma
    y2 = par.A * l2 ** par.gamma

    # Optimal consumption
    c1 = par.alpha * (w * l_total + par.T + (p1 * y1 - w * l1) + (p2 * y2 - w * l2)) / p1
    c2 = (1 - par.alpha) * (w * l_total + par.T + (p1 * y1 - w * l1) + (p2 * y2 - w * l2)) / (p2 + par.tau)

    # Market clearing conditions
    good1_market_clearing = y1 - c1
    good2_market_clearing = y2 - c2

    return [good1_market_clearing, good2_market_clearing]

def check_market_clearing_range(p1_vals, p2_vals, par):
    """
    Check if market clearing conditions hold for a range of p1 and p2 values.
    
    Parameters:
    - p1_vals (numpy array): Array of p1 values.
    - p2_vals (numpy array): Array of p2 values.
    - par (SimpleNamespace): Namespace containing model parameters.
    
    Returns:
    - bool: True if market clearing conditions hold for any combination of p1 and p2, False otherwise.
    """
    for p1 in p1_vals:
        for p2 in p2_vals:
            conditions = market_clearing_conditions([p1, p2], par)
            if all(abs(cond) < 1e-6 for cond in conditions):  # Check if conditions are approximately zero
                return True
    return False

def main():
    """
    Main function to set up parameters and check market clearing conditions over a range.
    
    Returns:
    - str: Message about market clearing conditions.
    """
    par = SimpleNamespace()
    # firms
    par.A = 1.0
    par.gamma = 0.5

    # households
    par.alpha = 0.3
    par.nu = 1.0
    par.epsilon = 2.0

    # government
    par.tau = 0.0
    par.T = 0.0

    # Check market clearing conditions over a range of p1 and p2 values
    p1_vals = np.linspace(0.1, 2.0, 10)
    p2_vals = np.linspace(0.1, 2.0, 10)
    if not check_market_clearing_range(p1_vals, p2_vals, par):
        return "The market clearing conditions do not hold for any combination of p1 and p2 in the given ranges."
    else:
        return "Market clearing conditions hold for some combination of p1 and p2 in the given ranges."

if __name__ == "__main__":
    result = main()
    print(result)
