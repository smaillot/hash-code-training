from solution import generate_solution
from numpy import copy

class Loaded_input:
    def __init__(self, R, C, L, H, pizza):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = copy(pizza)
    def generate_solution(self, seed):
        R = self.R
        C = self.C
        L = self.L
        H = self.H
        pizza = self.pizza
        return generate_solution(R, C, L, H, pizza, seed)

