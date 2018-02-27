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
from solution import sub_pizzas
from score import compute_score
from disp_debug import disp_pizza
from validation import check_slices
from extend_slices import extend_slices

## parsing arguments
parser = argparse.ArgumentParser(description='Test program.')
parser.add_argument('input', help='path to input file', type=argparse.FileType("rt"))
parser.add_argument('output', help='path to outputfile', type=argparse.FileType("wt"))
parser.add_argument('-i', help='height of subblocs', type=int)
parser.add_argument('-j', help='width of subblocs', type=int)
parser.add_argument('-s', help='desired score', type=int)
parser.add_argument('-b', help='batch size', type=int)

args = parser.parse_args()


R_tot, C_tot, L, H, pizza = read_input(args.input)
logs = []

R = args.i
C = args.j
pizzas = sub_pizzas(pizza, R, C)

###########################
## DO (GOOD) STUFF HERE
###########################

area = R_tot * C_tot
precision = np.floor(area / 2)

while precision < args.s:
    
    final_slices = []
    n=1
        
    for p, i, j in pizzas:
        
        R = p.shape[0]
        C = p.shape[1]
        lim = R * C * precision / area
        best = 0
    
        while best < lim:
            
            slices = generate_best_solution(R, C, L, H, p, args.b)
            score = compute_score(slices)
            if score > best:
                best = score
                
            try:
                print("slice " + str(n) + " / " + str(len(pizzas)) + "\tbest\t" + str(best) + "( " + str(best / R / C * 100) + "% )\t/ " + str(lim) + "( " + str(lim / R / C * 100) + "% )")
            except:
                pass
            
        slices_transl = [[sl[0]+i, sl[1]+j, sl[2]+i, sl[3]+j] for sl in slices]
        final_slices += slices_transl
        n+=1
    
    precision = np.floor((3 * precision + area) / 4)

    score_before = compute_score(final_slices)
    final_slices = extend_slices(final_slices, pizza, R_tot, C_tot, L, H)
    valid = check_slices(final_slices, pizza, R_tot, C_tot, L, H)
    score = compute_score(final_slices) * valid
    args.output.seek(0) 
    args.output.truncate()       
    write_output(args.output, final_slices)
    try:
        print("Score :\t" + str(score_before) + "\t( " + str(score_before / R_tot / C_tot * 100) + "% )")
        print("Final score :\t" + str(score) + "\t( " + str(score / R_tot / C_tot * 100) + "% )")
    except:
        pass
      
###########################
## END OF STUFF
###########################

