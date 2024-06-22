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
expected_utility_1 = np.zeros(par.J)
realized_utility_1 = np.zeros(par.J)

# set seed 
np.random.seed(2024)
# the noise for each career track, assuming normal distribution according to problem set 
epsilon = np.random.normal(0, par.sigma, (par.J, par.K))

# Calculate expected utility and realized utility for each career choice
for j in range(par.J):
    v_j = par.v[j] 
    u_ij_k = v_j + epsilon[j, :]
    expected_utility_1[j] = v_j + 1/par.K * np.sum(epsilon[j,:])
    realized_utility_1[j] = np.mean(u_ij_k)

## QUESTION 2

# Initialize storage for results
share_careers = np.zeros((par.N, par.J))
avg_subjective_utility = np.zeros(par.N)
avg_realized_utility = np.zeros(par.N)

# set seed 
np.random.seed(2024)

## for 
epsilon_friends = np.random.normal(0, par.sigma, (par.J, par.N))


# Simulation
for i in range(1, par.N + 1):  # For each graduate
    career_choices = np.zeros(par.J)
    subjective_utilities = []
    realized_utilities = []

    for k in range(par.K):  # For each simulation
        # Generate noise for friends
        epsilon_friends = np.random.normal(0, par.sigma, (par.J, i))
        
        # Calculate prior expected utility
        prior_expected_utility = par.v + np.mean(epsilon_friends, axis=1)
        
        # Generate noise for the graduate
        epsilon_graduate = np.random.normal(0, par.sigma, par.J)
        
        # Choose career with highest expected utility
        chosen_career = np.argmax(prior_expected_utility)
        career_choices[chosen_career] += 1
        
        # Calculate subjective expected utility and realized utility
        subjective_utility = prior_expected_utility[chosen_career]
        realized_utility = par.v[chosen_career] + epsilon_graduate[chosen_career]
        
        subjective_utilities.append(subjective_utility)
        realized_utilities.append(realized_utility)
    
    # Store results
    share_careers[i-1, :] = career_choices / par.K
    avg_subjective_utility[i-1] = np.mean(subjective_utilities)
    avg_realized_utility[i-1] = np.mean(realized_utilities)




## QUESTION 3
# Initialize storage for results
share_careers_3 = np.zeros((par.N, par.J))
avg_subjective_utility_3 = np.zeros(par.N)
avg_realized_utility_3 = np.zeros(par.N)
share_switching_3 = np.zeros(par.N)




# Initialize storage for conditional switching shares
conditional_switching_3 = np.zeros((par.N, par.J))

# Simulation
for i in range(1, par.N + 1):  # For each graduate
    career_choices = np.zeros(par.J)
    subjective_utilities = []
    realized_utilities = []
    switch_count = 0
    initial_choice_counts = np.zeros(par.J)
    initial_to_switch_counts = np.zeros(par.J)
    
    for k in range(par.K):  # For each simulation
        # Generate noise for friends
        epsilon_friends = np.random.normal(0, par.sigma, (par.J, i))
        
        # Calculate prior expected utility
        prior_expected_utility = par.v + np.mean(epsilon_friends, axis=1)
        
        # Generate noise for the graduate
        epsilon_graduate = np.random.normal(0, par.sigma, par.J)
        
        # Choose career with highest expected utility
        initial_choice = np.argmax(prior_expected_utility)
        initial_choice_counts[initial_choice] += 1
        
        # Calculate subjective expected utility and realized utility
        initial_subjective_utility = prior_expected_utility[initial_choice]
        initial_realized_utility = par.v[initial_choice] + epsilon_graduate[initial_choice]
        
        # Calculate new priors for switching
        new_priors = np.where(
            np.arange(par.J) == initial_choice,
            initial_realized_utility,
            prior_expected_utility - par.c
        )
        
        # Determine new optimal career
        new_choice = np.argmax(new_priors)
        career_choices[new_choice] += 1
        
        # Store subjective expected utility and realized utility
        subjective_utility = new_priors[new_choice]
        realized_utility = (par.v[new_choice] + epsilon_graduate[new_choice]) if new_choice != initial_choice else initial_realized_utility
        
        subjective_utilities.append(subjective_utility)
        realized_utilities.append(realized_utility)
        
        # Check if switched and update counts
        if new_choice != initial_choice:
            switch_count += 1
            initial_to_switch_counts[initial_choice] += 1
    
    # Store results
    share_careers_3[i-1, :] = career_choices / par.K
    avg_subjective_utility_3[i-1] = np.mean(subjective_utilities)
    avg_realized_utility_3[i-1] = np.mean(realized_utilities)
    share_switching_3[i-1] = switch_count / par.K
    conditional_switching_3[i-1, :] = initial_to_switch_counts / np.maximum(initial_choice_counts, 1)  # avoid division by zero
