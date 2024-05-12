from types import SimpleNamespace
import numpy as np

class StackelbergDuopolyClass:
    def __init__(self):
        """Initialize the Stackelberg duopoly class with default parameters."""
        self.par = SimpleNamespace(a=5, b=1/4, p1=2, p2=1)

    def inverse_demand(self, x_1, x_2):
        """Calculate the price from inverse demand function.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        - x_2 (float): Quantity produced by the follower.
        
        Returns:
        - float: Calculated price.
        """
        c = self.par.a * (1 / self.par.b)
        return self.par.a - self.par.b * (x_1 + x_2) if 0 <= (x_1 + x_2) <= c else 0

    def cost_1(self, x_1):
        """Compute cost for firm 1.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        
        Returns:
        - float: Cost for firm 1.
        """
        return self.par.p1 * x_1

    def cost_2(self, x_2):
        """Compute cost for firm 2.
        
        Parameters:
        - x_2 (float): Quantity produced by the follower.
        
        Returns:
        - float: Cost for firm 2.
        """
        return self.par.p2 * x_2

    def profit_1(self, x_1):
        """Compute profit for firm 1 considering firm 2's best response.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        
        Returns:
        - float: Profit for firm 1.
        """
        x_2_best = (self.par.a - self.par.p2) / (2 * self.par.b) - x_1 / 2
        return self.inverse_demand(x_1, x_2_best) * x_1 - self.cost_1(x_1)

    def neg_profit_1(self, x_1):
        """Negative profit for optimization purposes.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        
        Returns:
        - float: Negative profit for firm 1.
        """
        return -self.profit_1(x_1)

    def profit_2(self, x_1, x_2):
        """Compute profit for firm 2.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        - x_2 (float): Quantity produced by the follower.
        
        Returns:
        - float: Profit for firm 2.
        """
        return self.inverse_demand(x_1, x_2) * x_2 - self.cost_2(x_2)

    def derivative_1(self, x_1):
        """First derivative of the profit function for firm 1 with respect to x_1.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        
        Returns:
        - float: Derivative value.
        """
        x_2_best = (self.par.a - self.par.p2) / (2 * self.par.b) - x_1 / 2
        return self.inverse_demand(x_1, x_2_best) - self.par.p1

    def second_derivative_1(self):
        """Second derivative of the profit function for firm 1 is constant.
        
        Returns:
        - float: Second derivative value (constant).
        """
        return -self.par.b

    def derivative_2(self, x_1, x_2):
        """First derivative of the profit function for firm 2 with respect to x_2.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        - x_2 (float): Quantity produced by the follower.
        
        Returns:
        - float: Derivative value.
        """
        return self.inverse_demand(x_1, x_2) - self.par.p2

    def best_response_2(self, x_1):
        """Best response function of firm 2 given x_1.
        
        Parameters:
        - x_1 (float): Quantity produced by the leader.
        """
        
