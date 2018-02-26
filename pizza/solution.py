# -*-coding:Latin-1 -*
# compatibility
from __future__ import division
from __future__ import print_function

# custom
from validation import is_valid_slice
import numpy as np
from random import shuffle, randint, seed
from score import compute_score
from tqdm import tqdm
from scipy import optimize
import sys
import numexpr as ne
import multiprocessing as mp


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
    
    possible_slices_local = np.copy(possible_slices)
    shuffle(possible_slices_local)
    covered_cases = np.zeros([R, C], dtype = bool)
    # We screen though each case
    for i in range(R):
        for j in range(C):
            # Check if this case isn't covered yet
            if not(covered_cases[i, j]):
                suitable_slice = False
                k_th_slice = 0
                # We test all possible slices until all slices tested or one valid found
                while not(suitable_slice) and k_th_slice < len(possible_slices_local):
                    
                    pizza_slice = gen_slice([i, j], possible_slices_local[k_th_slice])
                    
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
    
    for k in progress_bar:
        done_queue.get()
        if k % (len(progress_bar) // 100) == 0:
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