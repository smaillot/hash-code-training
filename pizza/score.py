# compatibility
from __future__ import division
from __future__ import print_function
import numpy as np

def count_cells(slice):
    """
    Specific to this problem
    """
    return (slice[2] - slice[0] + 1) * (slice [3] - slice[1] + 1)

def compute_score(cuttings):
    """
    This function can be generalised
    """
    return np.sum([count_cells(pizza_slice) for pizza_slice in cuttings])

