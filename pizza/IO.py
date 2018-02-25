from verbose import *
import numpy as np


def write_list(f, number_of_slices):

    f.write(" ".join([str(n) for n in number_of_slices]) + "\n")

def write_array(f, array):

    for line in array:        
        
        write_list(f, line)

def read_input(reader):
    '''
    init params
    # number of rows, number of columns, minimum number of each ingredient cells in a slice, maximum number of cells of a slice
    True is a mushroom, False is a Tomato
    '''
    R, C, L, H = [int(i) for i in reader.readline().split(" ")]
    
    
    pizza = np.zeros([R, C], dtype = bool)
    for i in range(R):
        
        pizza[i, :] = [c == 'M' for c in list(reader.readline().rstrip())]
    
    
    return R, C, L, H, pizza


def write_output(f, number_of_slices, array_output):
    '''
    Takes a number of slices and a list of slices
    '''
    write_list(f, [number_of_slices])
    write_array(f, array_output)
def save_slices(slices):

    with open("/outputs/temp.out", 'w') qs f:

        write_output(f, slices)