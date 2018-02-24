# compatibility
from __future__ import division
from __future__ import print_function
import numpy as np

# custom
from verbose import *

def count_cells(slice):

    return slice[2] - slice[0] + slice [3] - slice[1]

def compute_score(cuttings):

    return np.sum([count_cells(slice) for slice in cuttings])

