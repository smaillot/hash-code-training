# compatibility
from __future__ import division
from __future__ import print_function

# standard
from time import time
import numpy as np
import multiprocessing as mp 
import random
from tqdm import tqdm
# custom
from IO import read_input, write_output, display_slices, parsing, print_score, disp_input
from pizza import Loaded_input
from solution import solve
from score import compute_score
from validation import check_solution
from matplotlib.pylab import plt
from post_process import improve_solution


if __name__ == '__main__':

    # Parsing arguments
    args = parsing()
    number_tries = args.n
    number_cpu = args.p

    ''' This is where the fun begins'''
    
    # Loading input
    loaded_input = Loaded_input(*read_input(args.input))
    # Initiliasing seeds
    random.seed(time())
    seeds = [random.randint(0, number_tries**10) for _ in range(number_tries)]
    
    ###########################
    ## Find best solution
    ###########################
    start = time()
    solution = solve(loaded_input, seeds, number_cpu)
    end = time()
    
    ###########################
    ## Post-treatment
    ###########################
    
    # Improves the solution
    #solution = improve_solution(solution, loaded_input)
 
    ###########################
    ## Checks solution and writes it out
    ###########################

    

    # Check if solution is valid
    valid = check_solution(solution, loaded_input)
    # display_slices(solution, R, C, pizza)

    # Writing to output
    write_output(args.output, solution)
    # Compute score and display
    score = compute_score(solution) * valid

    print_score(score, loaded_input, end - start)
    

    # plt.show()