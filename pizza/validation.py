# compatibility
from __future__ import division
from __future__ import print_function
import numpy as np
from tqdm import tqdm

def num_mushrooms(slices, pizza):

    return np.sum(pizza[slices[0]:slices[2]+1, slices[1]:slices[3]+1])

def size_slice(slices):

    return (slices[3] - slices[1]+1) * (slices[2] - slices[0]+1)

def is_valid_slice_2(slices, pizza, r, c, l, h):
    nm = num_mushrooms(slices, pizza)

    if nm < l:
        
        # print("Not enough mushrooms (" + str(nm) + ")")
        return False
    
    area = size_slice(slices)
    nt = area - nm

    if nt < l:
        
        # print("Not enough tomatoes")
        return False
    '''
    if area > h:

        # print("This slice is too big")
        return False
    '''
    return True

def is_valid_slice(slices, pizza, r, c, l, h):
    '''
    if slices[2] < slices[0] or slices[3] < slices[1]:
        # print("Non valid slices")
        return False
    '''
    if slices[0] < 0 or slices[2] > r or slices[1] < 0 or slices[3] > c:
        # print("Pizza slices out of dimensions")
        return False
    
    nm = num_mushrooms(slices, pizza)

    if nm < l:
        
        # print("Not enough mushrooms (" + str(nm) + ")")
        return False
    
    area = size_slice(slices)
    nt = area - nm

    if nt < l:
        
        # print("Not enough tomatoes")
        return False
    '''
    if area > h:

        # print("This slice is too big")
        return False
    '''
    return True

def check_overlapping(slices, r, c):

    pizza = np.zeros([r, c])

    for i in tqdm(range(len(slices)), desc="checking overlapping"):

        if  np.sum(pizza[slices[i][0]:slices[i][2]+1, slices[i][1]:slices[i][3]+1]) > 0:

            # print("Overlapping slices")
            return False

        pizza[slices[i][0]:slices[i][2]+1, slices[i][1]:slices[i][3]+1] = 1

    return True

def check_solution(slices, loaded_input):
    pizza = loaded_input.pizza
    R = loaded_input.R
    C = loaded_input.C
    L = loaded_input.L
    H = loaded_input.H
    # print("Checking slices validity")
    for i in tqdm(range(len(slices)), desc="checking slice validity"):
        
        if not is_valid_slice(slices[i], pizza, R, C, L, H):

            # print("Non valid slice " + str(i))
            return False

    # print("Checking overlapping")
    if not check_overlapping(slices, R, C):

        return False

    return True

def check_solution_2(slices, loaded_input):
    pizza = loaded_input.pizza
    R = loaded_input.R
    C = loaded_input.C
    L = loaded_input.L
    H = loaded_input.H
    # print("Checking slices validity")
    for i in tqdm(range(len(slices)), desc="checking slice validity"):
        
        if not is_valid_slice_2(slices[i], pizza, R, C, L, H):

            # print("Non valid slice " + str(i))
            return False

    # print("Checking overlapping")
    if not check_overlapping(slices, R, C):

        return False

    return True