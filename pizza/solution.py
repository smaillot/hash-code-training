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

def generate_solution(R, C, L, H, pizza, seed_number = []):
    """Specific
    Tests each case if it isn't covered by a slice, test all possible slices that can be fitted onto this slice, check the next case
    """
    if seed_number !=[]:
        seed(seed_number) # seed initialisation

    slices = []
    
    possible_slices = generate_all_slices(R, C, L, H)
    shuffle(possible_slices)
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
                    
                    pizza_slice = gen_slice([i, j], possible_slices[k_th_slice])
                    
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


        
def worker(best_score, best_slices, number_tries, l, number_proc, q):
    """General
    q.get() must be a pizza with the method generate_solution(int seed)
    """
    # Progress bar that is updated by process 0
    progress_bar = range(number_tries)
    if number_proc == 0:
        progress_bar = tqdm(range(number_tries), desc = "Advancement on process 0")

    # Pizza object get
    pizza = q.get()
    
    for _ in progress_bar:
        
        # We calculate a solution from a seed and evaluate its score
        seed = randint(0, 2**31)        
        slices = pizza.generate_solution(seed)
        score = compute_score(slices)
        
        # Lock state to prevent race condition
        l.acquire()

        # If our solution is better we save it in the shared variable
        if score > best_score.value:
            best_score.value = score
            
            best_slices[0] = slices
        # End of atomic operation
        l.release()

    

     
    
