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
    

input1, input2, input3, input4 = read_input(args.input)

start = time()

###########################
## DO (GOOD) STUFF HERE
###########################



print("blbl")
debug("je viens de print blbl")
print("blbl")
info("i'm so proud of myself")
print("blbl")
warn("legere fusion du reacteur, don't panic")
print("blbl")
fatal("boom !")
print("blbl")
info("this was a test")
print("\n\n")

for i in progress(range(10**7), desc="computing"):
    pass

output = np.array(input4) * 2


      
###########################
## END OF STUFF
###########################

end = time()

write_output(args.output, [1, 2, 3], output)

## compute score
score = compute_score(output)

print("\n\n\n")
info("Score {0:.0f} in {1:.6f}s".format(score, (end - start)))
print("\n\n")