# compatibility
from __future__ import division
from __future__ import print_function

# standard
import argparse
from time import time
import numpy as np

# custom
from verbose import *
from IO import read_input, write_output
from solution import *
from score import compute_score
from disp_debug import disp_pizza
from validation import check_slices

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

args = parser.parse_args()

## set verbosity level
verbosity = args.verbosity
set_verbosity(verbosity)

try:
    print("\n")
    info('Input file:' + str(args.input))
    info('Output file:' + str(args.output))
    print("\n")
except IOError as error:
    parser.error(error)
    

R, C, L, H, pizza = read_input(args.input)

start = time()

###########################
## DO (GOOD) STUFF HERE
###########################


# forced solution for small.in
slices = np.array([[0, 0, 0, 1], [1, 0, 2, 0]])

      
###########################
## END OF STUFF
###########################

end = time()

valid = check_slices(slices, pizza, R, C, L, H)
write_output(args.output, slices)

## compute score

score = compute_score(slices) * valid

print("\n\n\n")
info("Score {0:.0f} in {1:.6f}s".format(score, (end - start)))
print("\n\n")
end_color()