from solution import *

class Pizza:
    def __init__(self, R, C, L, H, pizza):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = np.copy(pizza)
    def gen_slices(self, seed):
        R = self.R
        C = self.C
        L = self.L
        H = self.H
        pizza = self.pizza
        return generate_solution_slices(R, C, L, H, pizza, seed)

class Pizza_seed:
    def __init__(self, pizza, seed):
        self.pizza = pizza
        self.seed = seed

