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
## profit function
    def objective_1(self, x_1, x_2):
        profit_1 = self.P(x_1, x_2) * x_1 - self.C_1(x_1)
        return profit_1


    def objective_2(self, x_1, x_2):
        profit_2 = self.P(x_1, x_2) * x_2 - self.C_2(x_2)
        return profit_2


        
        