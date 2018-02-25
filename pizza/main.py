# compatibility
from __future__ import division
from __future__ import print_function

# standard
from time import time
import numpy as np
import multiprocessing as mp 
# custom
from IO import read_input, write_output, display_slices, parsing
from pizza import Pizza
from solution import worker
from score import compute_score
from disp_debug import disp_pizza
from validation import check_slices
from matplotlib.pylab import plt
from extend_slices import extend_slices


if __name__ == '__main__':

    # Parsing arguments
    args = parsing()
    number_tries = args.n
    number_cpu = args.p

    ''' This is where the fun begins'''
    # Reading inputs
    R, C, L, H, pizza = read_input(args.input)
    # Loading pizza
    pizza_test = Pizza(R, C, L, H, pizza)

    # Initializing best score and best solution
    # These are shared values between processes
    best_score = mp.Value('i', 0)
    slices = mp.Manager().list([[]])

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
        p = mp.Process(target=worker, args=(best_score, slices, number_tries // number_cpu, lock, number_proc, queue))
        # Start de process
        p.start()
        # Send the pizza to a process
        queue.put(pizza_test)

    # Waiting for all threads to finish
    queue.close()
    queue.join_thread()
    p.join()

    slices = slices[0]
    ''' You can change things again '''
    ###########################
    ## Post-treatment
    ###########################
    
    # Improves the solution
    slices = extend_slices(slices, pizza, R, C, L, H)
 
    ###########################
    ## Checks solution and writes it out
    ###########################

    end = time()

    # Check if solution is valid
    valid = check_slices(slices, pizza, R, C, L, H)
    # display_slices(slices, R, C, pizza)

    # Writing to output
    write_output(args.output, slices)
    # Compute score and display
    score = compute_score(slices) * valid

    print("\n\n\n")
    print("Score {:.0f} ({:0.2f}%) in {:.6f}s".format(score, 100 * score / (R * C), end - start))
    print("\n\n")

    # plt.show()