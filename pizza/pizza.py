from solution import generate_solution, generate_all_slices, generate_all_possible_slices
from numpy import copy
import matplotlib.pylab as plt
from IO import display_slices

class Loaded_input:
    def __init__(self, R, C, L, H, pizza):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = copy(pizza)
        self.possible_slices = generate_all_slices(R, C, L, H)
        self.all_possible_slices = generate_all_possible_slices(self)
        print(len(self.all_possible_slices))
        display_slices(self.all_possible_slices, self.R, self.C, self.pizza)
        
    def generate_solution(self, seed):
        R = self.R
        C = self.C
        L = self.L
        H = self.H
        pizza = self.pizza
        return generate_solution(R, C, L, H, pizza, self.possible_slices, seed)

