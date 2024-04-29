from types import SimpleNamespace
import numpy as np
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
    
    