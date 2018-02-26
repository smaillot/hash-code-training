# compatibility
from __future__ import division
from __future__ import print_function

# standard
import argparse
from time import time
import numpy as np

# custom
from IO import read_input, write_output, write_array, write_list
from solution import *
from score import compute_score
from disp_debug import disp_pizza
from validation import check_slices
from extend_slices import extend_slices

## parsing arguments
parser = argparse.ArgumentParser(description='Test program.')
parser.add_argument('input', help='path to input file', type=argparse.FileType("rt"))
parser.add_argument('output', help='path to outputfile', type=argparse.FileType("wt"))

args = parser.parse_args()


R, C, L, H, pizza = read_input(args.input)
logs = []

###########################
## DO (GOOD) STUFF HERE
###########################

best = 0
i = 0

while best < R*C:
    
    i += 1
    print("it:\t"+str(i)+"\t\tbest:\t"+str(best)+"\t("+str(100 * best / R / C)+"%)")
    start = time()
    slices1 = generate_best_solution(R, C, L, H, pizza, 1)
    step = time()
    slices2 = extend_slices(slices1, pizza, R, C, L, H)
    end = time()
    valid = check_slices(slices2, pizza, R, C, L, H)
    
    if valid:

        score1 = compute_score(slices1)
        score2 = compute_score(slices2)
        logs.append([score1, score2, step-start, end-start])
        print("\tfound:\t"+str(score2)+"\t("+str(100 * score2 / R / C)+"%)")
        
        if score2 > best:
            
            best = score2
            write_output(args.output, slices2)
            print('\t\tnew best !')
            
      
###########################
## END OF STUFF
###########################

with open('logs.out', 'w') as f:

    write_list(f, [len(logs)])
    write_array(f, logs)