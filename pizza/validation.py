# compatibility
from __future__ import division
from __future__ import print_function
import numpy as np

# custom
from verbose import *

def num_mushrooms(slice, pizza):

    return np.sum(pizza[slice[0]:slice[2], slice[1]:slice[3]])

def size_slice(slice):

    return slice.shape[0] * slice.shape[1] 

def is_valid_slice(slice, pizza, r, c, l, h):

    if slice[2] < slice[0] or slice[3] < slice[1]:
        fatal("Non valid slice")
        return False

    if slice[0] < 0 or slice[2] > r or slice[1] < 0 or slice[3] > c:
        fatal("Pizza slice out of dimensions")
        return False

    nm = num_mushrooms(slice, pizza)

    if nm < l:
        
        fatal("Not enough mushrooms")
        return false
    
    area = size_slice(slice)
    nt = area - nm

    if nt < l:
        
        fatal("Not enough tomatoes")
        return false

    if area > h:

        fatal("This slice is too big")
        return False

    return True

def check_overlapping(slices, r, c):

    pizza = np.zeros([r, c])

    for i in progress(range(len(slices)), desc="checking overlapping"):

        if  np.sum(pizza[slices[i][0]:slices[i][2], slices[i][1]:slices[i][3]]) > 0:

            fatal("Overlapping slices")
            return False

        pizza[slices[i][0]:slices[i][2], slices[i][1]:slices[i][3]] = 1

    return True

def check_slices(slices, pizza, r, c, l, h):

    info("Checking slices validity")
    for i in progress(range(len(slices)), desc="checking slice validity"):

        if not is_valid_slice(slice, pizza, r, c, l, h):

            Fatal("Non valid slice " + str(i))
            return False

    info("Checking overlapping")
    if not check_overlapping(slices, r, c):

        return False

    return True