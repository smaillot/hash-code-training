# compatibility
from __future__ import division
from __future__ import print_function

# standard
import argparse
from time import time
import numpy as np
import multiprocessing as mp 
# custom
from IO import read_input, write_output, display_slices
from pizza import *
from solution import *
from score import *
from disp_debug import disp_pizza
from validation import check_slices
from matplotlib.pylab import plt
from extend_slices import extend_slices


if __name__ == '__main__':
    queue = mp.Queue()
    tasks = mp.JoinableQueue()

    number_cpu = min(mp.cpu_count() - 1, 1)

    ## parsing arguments
    parser = argparse.ArgumentParser(description='Test program.')
    parser.add_argument('input', help='path to input file', type=argparse.FileType("rt"))
    parser.add_argument('output', help='path to output file', type=argparse.FileType("wt"))
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3],
                        default=1,
                        help="increase output verbosity,")
    # verbosity:    0 -> quiet
    #               1 -> warnings
    #               2 -> info
    #               3 -> debug
    parser.add_argument("-n", type=int, default=2, help="number of tests")
    parser.add_argument("-p", type=int, default=2, help="number of threads")
    

    args = parser.parse_args()
    number_tries = args.n
    number_cpu = args.p
    R, C, L, H, pizza = read_input(args.input)

    start = time()

    ###########################
    ## DO (mostly) GOOD STUFF HERE
    ###########################
    
    pizza_test = Pizza(R, C, L, H, pizza)
    pizza_tests = [Pizza_seed(pizza_test, i) for i in range(number_tries)]
    best_score = mp.Value('i', 0)
    number_solutions = mp.Value('i', 0)
    slices = mp.Manager().list([[]])
    lock = mp.Lock()
    
    
    for i in range(number_cpu):
        pz_t = pizza_tests[i]
        p = mp.Process(target=worker, args=(best_score, slices, number_solutions, number_tries, lock,queue))
        p.start()

    
        queue.put(pizza_test)
        
        

    # Waiting
    queue.close()
    queue.join_thread()
    p.join()

    slices = slices[0]

        
    ###########################
    ## END OF STUFF
    ###########################

    end = time()
    write_output(args.output, slices)
    valid = check_slices(slices, pizza, R, C, L, H)
    #display_slices(slices, R, C, pizza)
    
    ## compute score
    score = compute_score(slices) * valid

    

    print("\n\n\n")
    print("Score {:.0f} ({:0.2f}%) in {:.6f}s".format(score, 100 * score / (R * C), end - start))
    print("\n\n")

    #plt.show()