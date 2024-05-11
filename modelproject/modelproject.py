from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
import sympy as sm
class stackelbergduopolClass1:

    def __init__(self):

        par = self.par = SimpleNamespace()
        par.x_1 = sm.symbols("x_1")
        par.x_2 = sm.symbols("x_2")
        par.a = sm.symbols("a")
        par.b = sm.symbols("b")
        par.p_1 = sm.symbols("p_1")
        par.p_2 = sm.symbols("p_2")
        par.inverse_demand =  par.a-par.b*(par.x_1 + par.x_2)
        par.objective_1 = par.inverse_demand * par.x_1 - par.p_1*par.x_1
        par.objective_2 = par.inverse_demand * par.x_2 - par.p_2*par.x_2
        par.foc = sm.diff(par.objective_2, par.x_2)
        sol = sm.solve(sm.Eq(par.foc,0), par.x_2)
        sub_objective_1= par.objective_1.subs(par.x_2, sol[0])
        foc_1 = sm.diff(sub_objective_1, par.x_1)
        sol_1 = sm.solve(sm.Eq(foc_1,0), par.x_1)
        sol_func = sm.lambdify(args=(par.x_1),expr= par.objective_1)
    


    