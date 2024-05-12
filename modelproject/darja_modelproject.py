from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
import sympy as sm
class stackelbergduopolClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

    ## inverse demand function
    def P(self, x_1, x_2, a = 5, b = 1/4): ## local scope 
        c = a * 1/b
        if 0 <= (x_1 + x_2) <= c: 
            result =  a - b*(x_1 + x_2)
        else: ## can't have a negative price
            result = 0
        return result
    
    

## defining cost functions for firm 1
    def C_1(self, x_1, p = 2): 
        cost_1 = p*x_1
        return cost_1
    

## defining cost function for firm 2
    def C_2(self, x_2, p = 1): ## local scope 
        cost_2 = p*x_2
        return cost_2
    


## solving analytically 
## profit function for firm 1 written only by x_1
    def objective_1(self, x_1, a = 5, b = 1/4, p =1):
        x_2_best = (a-p)/(2*b) - x_1/2
        profit_1 = self.P(x_1, x_2_best) * x_1 - self.C_1(x_1)
        return profit_1
    
    ## negative objective function 
    def neg_objective_1(self, x_1, a = 5, b = 1/4, p =1): 
       negative = -self.objective_1(x_1, a, b, p)
       return negative


    def objective_2(self, x_1, x_2):
        profit_2 = self.P(x_1, x_2) * x_2 - self.C_2(x_2)
        return profit_2


    ## first order conditions
    ## these are calculated by our own, we could use sympy here 
    def derivative_1(self, x_1, a = 5, b = 1/4, p = 2):
        x_2_best = (a-p)/(2*b) - x_1/2
        foc_1 = self.P(x_1, x_2_best) + x_1 * (- b) - p
        return foc_1
    
    def second_derivative_1(self, x_1, a = 5, b = 1/4, p = 2):
         x_2_best = (a-p)/(2*b) - x_1/2
         soc_1 = -b - b - b/2 
         return soc_1

    def derivative_2(self, x_1, x_2, a = 5, b = 1/4, p = 1):
        foc_2 = self.P(x_1, x_2) + x_2 * (-b) - p
        return foc_2


    ## best function of person 2: 
    def best_func2(self, x_1, a = 5, b = 1/4, p =1): 
        x_2 = (a-p)/(2*b) - x_1/2
        return x_2


    def minimize_solver(self, x0, alphas=[0.01,0.05,0.1,0.25,0.5,1], max_iter=500,tol=1e-8):
        # step 1: initialize
        x = x0
        fx = self.neg_objective_1(x0)
        nit = 1
        nfev = 1
        njev = 0
        
            # step 2-6: iteration
        while nit < max_iter:
            
            x_prev = x
            fx_prev = fx
        
        
        # step 3: find good step size (line search)
            fx_ast = np.inf
            x_ast = np.nan
            alpha_ast = np.nan
            for alpha in alphas:
                ## using taylor approximation here 
                # it should be possible to use sympy here to avoid own calculation of derivatives 
                x = x_prev - self.derivative_1(x_prev)/self.second_derivative_1(x_prev)
                fx = self.neg_objective_1(x)
                nfev += 1
                if fx < fx_ast and x >0 :
                    alpha_ast = alpha
                    x_ast = x                
                    fx_ast = fx
        
        # step 4: update guess
            x = x_ast # = x_prev - alpha_ast*jacx

                            
        # step 5: check convergence
            fx = fx_ast # = f(x)
            if abs(fx-fx_prev) < tol:
                break
            
        # step 6. update counter
            nit += 1
        
        return x,nit,nfev,njev
    

    def interactive_figure_profit(self, p1, p2, a_1, b_1):
        ## solution using sympy 
        x_1 = sm.symbols("x_1")
        x_2 = sm.symbols("x_2")
        a = sm.symbols("a")
        b = sm.symbols("b")
        p_1 = sm.symbols("p_1")
        p_2 = sm.symbols("p_2")
        inverse_demand =  a-b*(x_1 + x_2)
        objective_1 = inverse_demand * x_1 - p_1*x_1
        objective_2 = inverse_demand * x_2 - p_2*x_2
        foc = sm.diff(objective_2, x_2)
        sol = sm.solve(sm.Eq(foc,0), x_2)
        sub_objective_1= objective_1.subs(x_2, sol[0])
        foc_1 = sm.diff(sub_objective_1, x_1)
        sol_1 = sm.solve(sm.Eq(foc_1,0), x_1)
        ## optimal solution
        optimal_x1 = sol_1[0].subs(a, a_1).subs(b, b_1).subs(p_1, p1).subs(p_2,p2)
        optimal_x2 = sol[0].subs(x_1, optimal_x1).subs(a, a_1).subs(b, b_1).subs(p_1,p1).subs(p_2,p2)
        objective_1_optimal = objective_1.subs(x_1, optimal_x1).subs(x_2, optimal_x2).subs(a, a_1).subs(b, b_1).subs(p_1,p1)
        objective_2_optimal = objective_2.subs(x_1, optimal_x1).subs(x_2, optimal_x2).subs(a, a_1).subs(b, b_1).subs(p_2,p2)
    # Create a figure
        fig = plt.figure(frameon=True, dpi=500)
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(optimal_x1 , objective_1_optimal, color = "darkgreen",  marker = 'o', label = "$x_L$")
        ax.scatter(optimal_x2,objective_2_optimal, color = "darkred", marker = 'o', label = "$x_F$")
        ax.set_xlim([0,20]) # fixed x1 range
        ax.set_ylim([0,20]) # fixed x2 range
        ax.set_xlabel("$x_L$/$x_F$")
        ax.set_ylabel("Profit of $x_L$/$x_F$")
        ax.set_title("Optimal amount and profit depending on different parameters")
        ax.legend()
        # Show the plot
        plt.show()




    def interactive_figure_profit_extend_i(self, p1, p2, p3, a_1, b_1):
        ## solution using sympy 
        x_1 = sm.symbols("x_1")
        x_2 = sm.symbols("x_2")
        x_3 = sm.symbols("x_3")
        a = sm.symbols("a")
        b = sm.symbols("b")
        p_1 = sm.symbols("p_1")
        p_2 = sm.symbols("p_2")
        p_3 = sm.symbols("p_3")
        inverse_demand_extend =  a-b*(x_1 + x_2 + x_3)
        objective_1_extend = inverse_demand_extend * x_1 - p_1*x_1
        objective_2_extend = inverse_demand_extend * x_2 - p_2*x_2
        objective_3_extend = inverse_demand_extend * x_3 - p_3*x_3
        foc2_extend = sm.diff(objective_2_extend, x_2)
        sol2_extend = sm.solve(sm.Eq(foc2_extend,0), x_2)
        foc3_extend = sm.diff(objective_3_extend, x_3)
        foc3_twovariables = foc3_extend.subs(x_2, sol2_extend[0])
        solution_foc_3 = sm.solve(sm.Eq(foc3_twovariables,0), x_3)
        solution_foc_2 = sol2_extend[0].subs(x_3, solution_foc_3[0])
        objective_1_only_onevariable = objective_1_extend.subs(x_2, solution_foc_2).subs(x_3, solution_foc_3[0])
        foc1_extend = sm.diff(objective_1_only_onevariable, x_1)
        sol1_extend = sm.solve(sm.Eq(foc1_extend,0), x_1)
        optimal_second = solution_foc_2.subs(x_1, sol1_extend[0])
        optimal_third = solution_foc_3[0].subs(x_1, sol1_extend[0])
        ## optimal solution
        optimal_x1 = sol1_extend[0].subs(a, a_1).subs(b, b_1).subs(p_1, p1).subs(p_2,p2).subs(p_3,p3)
        optimal_x2 = optimal_second.subs(a, a_1).subs(b, b_1).subs(p_1, p1).subs(p_2,p2).subs(p_3,p3)
        optimal_x3 = optimal_third.subs(a, a_1).subs(b, b_1).subs(p_1, p1).subs(p_2, p2).subs(p_3,p3)
        objective_1_optimal = objective_1_extend.subs(x_1, optimal_x1).subs(x_2, optimal_x2).subs(x_3, optimal_x3).subs(a, a_1).subs(b, b_1).subs(p_1,p1)
        objective_2_optimal = objective_2_extend.subs(x_1, optimal_x1).subs(x_2, optimal_x2).subs(x_3, optimal_x3).subs(a, a_1).subs(b, b_1).subs(p_2,p2)
        objective_3_optimal = objective_3_extend.subs(x_1, optimal_x1).subs(x_2, optimal_x2).subs(x_3, optimal_x3).subs(a, a_1).subs(b, b_1).subs(p_3,p3)
    # Create a figure
        fig = plt.figure(frameon=True, dpi=500)
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(optimal_x1 , objective_1_optimal, color = "darkgreen",  marker = 'o', label = "$x_L$")
        ax.scatter(optimal_x2,objective_2_optimal, color = "darkred", marker = 'o', label = "$x_{F1}$")
        ax.scatter(optimal_x3,objective_3_optimal, color = "midnightblue", marker = 'o', label = "$x_{F2}$")
        ax.set_xlim([0,20]) # fixed x1 range
        ax.set_ylim([0,20]) # fixed x2 range
        ax.set_xlabel("$x_L$/$x_{F1}$/$x_{F2}$")
        ax.set_ylabel("Profit of $x_L$/$x_{F1}$/$x_{F2}$")
        ax.legend()
        # Show the plot
        plt.show()


    # Function to compute quantities
    def compute_quantities(self,a_val, b_val, p1_val, p2_val):
    # Define inverse demand and cost functions
        # Define symbols
        x_1, x_2, a, b, p_1, p_2 = sm.symbols('x_1 x_2 a b p_1 p_2')
        inverse_demand = a - b * (x_1 + x_2)
        objective_1 = inverse_demand * x_1 - p1_val * x_1
        objective_2 = inverse_demand * x_2 - p2_val * x_2
    
    # Solve for follower's best response
        foc_2 = sm.diff(objective_2, x_2)
        sol_x2 = sm.solve(foc_2, x_2)[0]
    
    # Substitute follower's best response into leader's objective
        sub_objective_1 = objective_1.subs(x_2, sol_x2)
        foc_1 = sm.diff(sub_objective_1, x_1)
        sol_x1 = sm.solve(foc_1, x_1)[0]
    
        # Calculate follower's quantity based on leader's output
        sol_x2_final = sol_x2.subs(x_1, sol_x1)
    
        # Ensure all expressions are fully substituted
        sol_x1_numeric = sol_x1.subs([(a, a_val), (b, b_val), (p_1, p1_val)])
        sol_x2_numeric = sol_x2_final.subs([(a, a_val), (b, b_val), (p_1, p1_val), (p_2, p2_val)])
    
        return float(sol_x1_numeric), float(sol_x2_numeric)

    # Visualization function
    def plot_stackelberg(self,a, b, p1, p2):
        q_leader, q_follower = self.compute_quantities(a, b, p1, p2)
        plt.figure(figsize=(10, 5), frameon=True, dpi=500)
        plt.bar(['Leader', 'Follower'], [q_leader, q_follower], color=['darkgreen', 'darkred'])
        plt.xlabel('Firms')
        plt.ylabel('Quantities')
        plt.title(f'Stackelberg Quantities: a={a}, b={b}, p1={p1}, p2={p2}')
        plt.ylim(0, max(q_leader, q_follower) + 1)
        plt.show()



    def interactive_figure_profit_extend_ii(self, p1, p2, p3, a_1, b_1):
        ## solution using sympy 
        # defining the variables and parameters
        a, b, p_1, p_2, p_3, x_1, x_2, x_3 = sm.symbols('a b p_1 p_2 p_3 x_1 x_2 x_3')
        inverse_demand_extend =  a-b*(x_1 + x_2 + x_3)
        objective_1_extend = inverse_demand_extend * x_1 - p_1*x_1
        objective_2_extend = inverse_demand_extend * x_2 - p_2*x_2
        objective_3_extend = inverse_demand_extend * x_3 - p_3*x_3
        # Third firm's best response
        x_3_expr = (a - b * x_1 - b * x_2 - p_3) / (2 * b)

        #   Second firm's best response
        x_2_expr = sm.solve(sm.diff((a - b * (x_1 + x_2 + x_3_expr)) * x_2 - p_2 * x_2, x_2), x_2)

        # Leader's best response
        x_1_expr = sm.solve(sm.diff((a - b * (x_1 + x_2_expr[0] + x_3_expr.subs(x_2, x_2_expr[0]))) * x_1 - p_1 * x_1, x_1), x_1)

        # inserting parameter values
        param_values = {a: 5, b: 1/4, p_1: 2, p_2: 1, p_3: 1}

        # Substituting values to find specific quantities
        x_1_optimal = x_1_expr[0].subs(param_values)
        x_2_optimal = x_2_expr[0].subs(param_values).subs(x_1, x_1_optimal)
        x_3_optimal = x_3_expr.subs(param_values).subs({x_1: x_1_optimal, x_2: x_2_optimal})

        objective_1_optimal = objective_1_extend.subs(x_1, x_1_optimal).subs(x_2, x_2_optimal).subs(x_3, x_3_optimal).subs(a, a_1).subs(b, b_1).subs(p_1,p1)
        objective_2_optimal = objective_2_extend.subs(x_1, x_1_optimal).subs(x_2, x_2_optimal).subs(x_3, x_3_optimal).subs(a, a_1).subs(b, b_1).subs(p_2,p2)
        objective_3_optimal = objective_3_extend.subs(x_1, x_1_optimal).subs(x_2, x_2_optimal).subs(x_3, x_3_optimal).subs(a, a_1).subs(b, b_1).subs(p_3,p3)
    # Create a figure
        fig = plt.figure(frameon=True, dpi=500)
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(x_1_optimal , objective_1_optimal, color = "darkgreen",  marker = 'o', label = "$x_L$")
        ax.scatter(x_2_optimal,objective_2_optimal, color = "darkred", marker = 'o', label = "$x_{F1}$")
        ax.scatter(x_3_optimal,objective_3_optimal, color = "midnightblue", marker = 'o', label = "$x_{F2}$")
        ax.set_xlim([0,20]) # fixed x1 range
        ax.set_ylim([0,20]) # fixed x2 range
        ax.set_xlabel("$x_L$/$x_{F1}$/$x_{F2}$")
        ax.set_ylabel("Profit of $x_L$/$x_{F1}$/$x_{F2}$")
        ax.legend()
        # Show the plot
        plt.show()