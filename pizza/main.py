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
    

# = read_input(args.input)

start = time()

###########################
## DO (GOOD) STUFF HERE
###########################




      
###########################
## END OF STUFF
###########################

end = time()

#write_output(args.output)

## compute score
score = compute_score()

print("\n\n\n")
info("Score {0:.0f} in {1:.6f}s".format(score, (end - start)))
print("\n\n")