# compatibility
from __future__ import division
from __future__ import print_function
import numpy as np

# custom
from verbose import *

def num_mushrooms(slices, pizza):

    return np.sum(pizza[slices[0]:slices[2]+1, slices[1]:slices[3]+1])

def size_slice(slices):

    return (slices[3] - slices[1]+1) * (slices[2] - slices[0]+1)

def is_valid_slice(slices, pizza, r, c, l, h):

    if slices[2] < slices[0] or slices[3] < slices[1]:
        fatal("Non valid slices")
        return False

    if slices[0] < 0 or slices[2] > r or slices[1] < 0 or slices[3] > c:
        fatal("Pizza slices out of dimensions")
        return False

    nm = num_mushrooms(slices, pizza)

    if nm < l:
        
        fatal("Not enough mushrooms (" + str(nm) + ")")
        return False
    
    area = size_slice(slices)
    nt = area - nm

    if nt < l:
        
        fatal("Not enough tomatoes")
        return False

    if area > h:

        fatal("This slice is too big")
        return False

    return True

def check_overlapping(slices, r, c):

    pizza = np.zeros([r, c])

    for i in progress(range(len(slices)), desc="checking overlapping"):

        if  np.sum(pizza[slices[i][0]:slices[i][2]+1, slices[i][1]:slices[i][3]+1]) > 0:

            fatal("Overlapping slices")
            return False

        pizza[slices[i][0]:slices[i][2]+1, slices[i][1]:slices[i][3]+1] = 1

    return True

def check_slices(slices, pizza, r, c, l, h):

    info("Checking slices validity")
    for i in progress(range(len(slices)), desc="checking slice validity"):
        
        if not is_valid_slice(slices[i], pizza, r, c, l, h):

            fatal("Non valid slice " + str(i))
            return False

    info("Checking overlapping")
    if not check_overlapping(slices, r, c):

        return False

    return True