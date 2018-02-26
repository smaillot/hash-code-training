from solution import generate_solution, generate_all_slices
from numpy import copy

class Loaded_input:
    def __init__(self, R, C, L, H, pizza):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = copy(pizza)
        self.possible_slices = generate_all_slices(R, C, L, H)
    def generate_solution(self, seed):
        return generate_solution(self, self.possible_slices, seed)

