# -*-coding:Latin-1 -*
# compatibility
from __future__ import division
from __future__ import print_function

# custom
from validation import is_valid_slice
import numpy as np
from random import shuffle, randint, seed, choice
from score import compute_score
from tqdm import tqdm
from scipy import optimize
import multiprocessing as mp
import sys
from collections import defaultdict
from networkx import Graph

def generate_all_slices(R, C, L, H):
    '''Specific
    L : minimum number of each ingredient in a slice
    H : max size for a slice
    We generate all the possible slices that we can make out of the pizza. We know that their size (or area) is between 2 * L and H
    The generated slices start at 0, 0
    '''
    list_of_slices = []
    for A in range(2 * L, H + 1):
        
        for row_size in range(1, A + 1):
            
            if A % row_size == 0:
                column_size = A // row_size
                if column_size < (C + 1):
                    list_of_slices.append([0, 0, row_size - 1, column_size - 1])
                
    return list_of_slices

def gen_slice(starting_point, origin_slice):
    '''Specific
    Takes a slice starting from the origin (like all generated from generate_all_slices) and translates it to the starting point
    Sends an error if slice is outside 
    '''
    if origin_slice[0] != 0 or origin_slice[1] != 0:
        # print("Non origin slice")
        raise "Cet endroit est problématique"
        #TODO : wouhou une if qui renvoie rien mais on veut foutre la merde
    else:
        x, y = starting_point
        _, _, row, col = origin_slice
        return [x, y, row + x, col + y]

def generate_solution(R, C, L, H, pizza, possible_slices, seed_number = []):
    """Specific
    Tests each case if it isn't covered by a slice, test all possible slices that can be fitted onto this slice, check the next case
    """
    if seed_number !=[]:
        seed(seed_number) # seed initialisation

    slices = []

    
    
    covered_cases = np.zeros([R, C], dtype = bool)
    # We screen though each case
    for i in range(R):
        for j in range(C):
            
            # Check if this case isn't covered yet
            if not(covered_cases[i, j]):
                suitable_slice = False
                
                k_th_slice = 0
                # We test all possible slices until all slices tested or one valid found
                while not(suitable_slice) and k_th_slice < len(possible_slices):
                    
                    pizza_slice = gen_slice([i, j], choice(possible_slices))
                    
                    suitable_slice = is_valid_slice(pizza_slice, pizza, R, C, L, H)
                    if suitable_slice:
                    
                        # So far we only know the slice's within the pizza's borders and has the minimum amount of mushrooms and tomatoes.
                        # Thus we have to test if it doesn't cover another slice.
                        # We test each case in the chosen slice
                        try:
                            for k in range(pizza_slice[0], pizza_slice[2] + 1):
                                for l in range(pizza_slice[1], pizza_slice[3] + 1):
                                    if covered_cases[k, l]:
                                        # We accountered an already covered case
                                        # The slice isn't suitable anymore
                                        suitable_slice = False
                                        raise Exception()
                        except Exception:
                            # The slice isn't suitable so we pass the exception
                            pass
                        else:
                            # The slice is good and is added to the list of slices
                            slices.append(pizza_slice)
                            # We have to update our array of tested cases
                            for k in range(pizza_slice[0], pizza_slice[2] + 1):
                                for l in range(pizza_slice[1], pizza_slice[3] + 1):
                                    covered_cases[k, l] = True
                    k_th_slice += 1
           
    return slices


        


def solve(loaded_input, seeds, number_cpu):
    # Initializing best score and best solution
    # These are shared values between processes
    best_score = mp.Value('i', 0)
    solution = mp.Manager().list([[]])

    # Threads preparation 
    task_queue = mp.Queue()
    done_queue = mp.Queue()
    # Tasks queue
    for seed in seeds:
        task_queue.put(seed)
    lock = mp.Lock() # Prevents race conditions

    
    ###########################
    ## Parallel computing
    ###########################
    """ Do not touch anything
    Change solution.worker to change the solution's generator behavior """
    # We screen through each CPU and dedicate one thread for each
    processes = [mp.Process(target=worker, args=(best_score, solution, lock, loaded_input, task_queue, done_queue)) for _ in range(number_cpu)]
    progress_bar = tqdm(range(len(seeds)), desc = "Generating solutions")
    for p in processes:
        # Create a process that will race through the execution queue
        p.start()

    # Load loading screen

    refresh_rate = max(1, (len(progress_bar) // 100))
    
    for k in progress_bar:
        done_queue.get()
        if k % refresh_rate == 0:
            progress_bar.set_description("Current best score : " + str(best_score.value))
    
    # Stop all processes
    for p in processes:
        task_queue.put('STOP')
    
    return solution[0]

def worker(best_score, best_solution, l, loaded_input, q, output):
    """General
    q.get() must be a loaded_input with the method generate_solution(int seed)
    """
    # We get the seed that will generate our solution
    # STOP stops the worker
    for seed in iter(q.get, 'STOP'):

        # We calculate a solution from a seed and evaluate its score
        solution = loaded_input.generate_solution(seed)
        score = compute_score(solution)

        # Lock state to prevent race condition
        l.acquire()
        #print(score)
        # If our solution is better we save it in the shared variable
        if score > best_score.value:
            
            best_score.value = score
            
            best_solution[0] = solution
        # End of atomic operation
        l.release()
        output.put(True)


def generate_all_possible_slices(loaded_input):
    ''' Generates all the possible pizza slices '''
    R = loaded_input.R
    C = loaded_input.C
    L = loaded_input.L
    H = loaded_input.H
    pizza = loaded_input.pizza
    all_slices = generate_all_slices(R, C, L, H)
    all_possible_slices = []

    # We screen through each pizza cell
    for i in range(R):
        for j in range(C):
            for local_slice in all_slices:
                translated_slice = gen_slice([i, j], local_slice)

                if is_valid_slice(translated_slice, pizza, R, C, L, H):
                    all_possible_slices.append(translated_slice)
            #print(len(all_possible_slices))
    
    return all_possible_slices

def is_inside_another_slice(pizza_slice1, pizza_slice2):
    pizza1_start_x = pizza_slice1[0]
    pizza1_start_y = pizza_slice1[1]
    pizza1_end_x = pizza_slice1[2]
    pizza1_end_y = pizza_slice1[3]
    pizza2_start_x = pizza_slice2[0]
    pizza2_end_x = pizza_slice2[2]
    pizza2_start_y = pizza_slice2[1]
    pizza2_end_y = pizza_slice2[3]

    return ((pizza1_start_x <= pizza2_end_x) and (pizza1_end_x >= pizza2_start_x) and (pizza1_start_y <= pizza2_end_y) and (pizza1_end_y >= pizza2_start_y))

def slices_to_graph(slices):
    ''' Converts a list of slices to a graph 
    We will use a dictionnary for this proof of concept and will then improve the system later on
    graph[node] = adjacence_list'''
    graph = Graph()
    # Matches a node number to a slice
    convert_table = len(slices) * [[]]
    # We have to convert each slice to a node
    node_number = 0
    for pizza_slice in slices:
        graph.add_node(node_number)
        convert_table[node_number] = pizza_slice
        node_number += 1
    
    for node_number in graph.nodes():
        pizza_slice = convert_table[node_number]
        # Is there a recover between pizza_slice and pizza_slice_2 ?
        for node_number_concurrent in graph.nodes():
            if node_number_concurrent != node_number:
                pizza_slice_2 = convert_table[node_number_concurrent]
                # We test all cells of our part until we meet nothing or another part
            
                if is_inside_another_slice(pizza_slice, pizza_slice_2):
                    graph.add_edge(node_number, node_number_concurrent)

    #print(len(graph))
    return graph


def remove_node_graph(node_to_pop, graph):
    graph.remove_node(node_to_pop)

