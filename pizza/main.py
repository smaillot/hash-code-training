# compatibility
from __future__ import division
from __future__ import print_function

# standard
import argparse
from time import time
import numpy as np

# custom
from IO import read_input, write_output, write_array
from solution import *
from score import compute_score
from disp_debug import disp_pizza
from validation import check_slices
from extend_slices import extend_slices

## parsing arguments
parser = argparse.ArgumentParser(description='Test program.')
parser.add_argument('input', help='path to input file', type=argparse.FileType("rt"))
parser.add_argument('-n', type=int)
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3],
                    default=1,
                    help="increase output verbosity,")
# verbosity:    0 -> quiet
#               1 -> warnings
#               2 -> info
#               3 -> debug

args = parser.parse_args()


R, C, L, H, pizza = read_input(args.input)
logs = []

###########################
## DO (GOOD) STUFF HERE
###########################

for _ in tqdm(range(args.n), desc="looping"):

    start = time()
    slices1 = generate_best_solution(R, C, L, H, pizza, 10)
    step = time()
    slices2 = extend_slices(slices1, pizza, R, C, L, H)
    end = time()
    valid = check_slices(slices2, pizza, R, C, L, H)
    
    if valid:

        logs.append([compute_score(slices1), compute_score(slices2), step-start, end-start])
      
###########################
## END OF STUFF
###########################

with open('logs.out', 'w') as f:

    write_array(f, logs)