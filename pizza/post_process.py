from __future__ import division
from __future__ import print_function
import numpy as np
from tqdm import tqdm
from validation import is_valid_slice

def compute_emptyness(slices, R, C):
    
    pizza = np.zeros([R, C])
    
    for i in tqdm(range(len(slices)), desc="Computing emptyness"):
    
        pizza[slices[i][0]:slices[i][2]+1, slices[i][1]:slices[i][3]+1] = 1
             
    return pizza

def sum_slice(pizza_slice, pizza_filling):
    
    return np.sum(pizza_filling[pizza_slice[0]:pizza_slice[2]+1, pizza_slice[1]:pizza_slice[3]+1])

def is_overlapping(new_slice, previous_slice, pizza_filling):
    
    return not (sum_slice(new_slice, pizza_filling) == sum_slice(previous_slice, pizza_filling))

def extend_slice(input_pizza_slice, input_pizza_filling, pizza, R, C, L, H):
    
    pizza_slice = np.copy(input_pizza_slice)
    pizza_filling = np.copy(input_pizza_filling)
    ok = True
    while ok:
    
        ok = False
        
        # add row on bottom
        if pizza_slice[2] < R-1:
            pizza_slice[2] += 1
            if is_valid_slice(pizza_slice, pizza, R, C, L, H) and not is_overlapping(pizza_slice, input_pizza_slice, pizza_filling):
                pizza_filling[pizza_slice[0]:pizza_slice[2]+1, pizza_slice[1]:pizza_slice[3]+1] = 1
                ok = True
            else:
                pizza_slice[2] -= 1    
                      
        # add col on right
        if pizza_slice[3] < C-1:
            
            pizza_slice[3] += 1
            if is_valid_slice(pizza_slice, pizza, R, C, L, H) and not is_overlapping(pizza_slice, input_pizza_slice, pizza_filling):
                pizza_filling[pizza_slice[0]:pizza_slice[2]+1, pizza_slice[1]:pizza_slice[3]+1] = 1
                ok = True
            else:
                pizza_slice[3] -= 1
        
        # add row on top
        if pizza_slice[0] > 0:
            pizza_slice[0] -= 1
            if is_valid_slice(pizza_slice, pizza, R, C, L, H) and not is_overlapping(pizza_slice, input_pizza_slice, pizza_filling):
                pizza_filling[pizza_slice[0]:pizza_slice[2]+1, pizza_slice[1]:pizza_slice[3]+1] = 1
                ok = True
            else:
                pizza_slice[0] += 1
        
        # add col on left
        if pizza_slice[1] > 0:
            pizza_slice[1] -= 1
            if is_valid_slice(pizza_slice, pizza, R, C, L, H) and not is_overlapping(pizza_slice, input_pizza_slice, pizza_filling):
                pizza_filling[pizza_slice[0]:pizza_slice[2]+1, pizza_slice[1]:pizza_slice[3]+1] = 1
                ok = True
            else:
                pizza_slice[1] += 1
    
    return pizza_slice, pizza_filling

def improve_solution(input_slices, pizza, R, C, L, H):
    
    slices = np.copy(input_slices)
    pizza_filling = np.copy(compute_emptyness(slices, R, C))
    
    for i in tqdm(range(len(slices)), desc="Extending slices"):
        
        pizza_slice, pizza_filling = extend_slice(slices[i], pizza_filling, pizza, R, C, L, H)
        slices[i] = pizza_slice
        
              
    return slices