from solution import remove_node_graph, generate_solution, generate_all_slices, generate_all_possible_slices, slices_to_graph
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
        self.graph = slices_to_graph(self.all_possible_slices)
        start = time()
        print(len(self.graph))
        for i in range(len(self.graph)):
            
            remove_node_graph(i, self.graph)
        print("{:.6f}s".format(time() - start))



        

    def generate_solution(self, seed):
        R = self.R
        C = self.C
        L = self.L
        H = self.H
        pizza = self.pizza
        return generate_solution(R, C, L, H, pizza, self.possible_slices, seed)

