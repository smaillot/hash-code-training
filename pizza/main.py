# compatibility
from __future__ import division
from __future__ import print_function

# standard
from time import time
import numpy as np
import multiprocessing as mp 
# custom
from IO import read_input, write_output, display_slices, parsing, print_score, disp_input
from pizza import Pizza
from solution import worker
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
    # Reading inputs
    R, C, L, H, pizza = read_input(args.input)
    # Loading pizza
    loaded_input = Pizza(R, C, L, H, pizza)

    # Initializing best score and best solution
    # These are shared values between processes
    best_score = mp.Value('i', 0)
    solution = mp.Manager().list([[]])

    # Threads preparation 
    queue = mp.Queue()
    lock = mp.Lock() # Prevents race conditions

    start = time()
    ###########################
    ## Parallel computing
    ###########################
    """ Do not touch anything
    Change solution.worker to change the solution's generator behavior """
    # We screen through each CPU and dedicate one thread for each
    for number_proc in range(number_cpu):
        
        # Creates a process that will be waiting for an argument
        p = mp.Process(target=worker, args=(best_score, solution, number_tries // number_cpu, lock, number_proc, queue))
        # Start de process
        p.start()
        # Send the pizza to a process
        queue.put(loaded_input)

    # Waiting for all threads to finish
    queue.close()
    queue.join_thread()
    p.join()

    solution = solution[0]
    ''' You can change things again '''
    ###########################
    ## Post-treatment
    ###########################
    
    # Improves the solution
    solution = improve_solution(solution, loaded_input)
 
    ###########################
    ## Checks solution and writes it out
    ###########################

    end = time()

    # Check if solution is valid
    valid = check_solution(solution, loaded_input)
    # display_slices(solution, R, C, pizza)

    # Writing to output
    write_output(args.output, solution)
    # Compute score and display
    score = compute_score(solution) * valid

    print_score(score, loaded_input, end - start)
    

    # plt.show()