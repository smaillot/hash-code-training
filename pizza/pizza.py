from solution import generate_solution, generate_all_slices, generate_all_possible_slices
from numpy import copy
import matplotlib.pylab as plt
from IO import display_slices
from time import time


class Loaded_input:
    def __init__(self, R, C, L, H, pizza):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = copy(pizza)
        self.possible_slices = generate_all_slices(R, C, L, H)
        self.all_possible_slices = generate_all_possible_slices(self)

        

    def generate_solution(self, seed):
        
        return generate_solution(self, seed)

