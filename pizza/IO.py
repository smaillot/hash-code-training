from verbose import *
import numpy as np
import matplotlib.pyplot as plt

def write_list(f, list):

    f.write(" ".join([str(n) for n in list]) + "\n")

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

def disp_pizza(pizza):
    '''
    Violet is a tomato
    Yellow is a mushroom
    '''

    plt.imshow(pizza)
    plt.show()


def write_output(f, list_output, array_output):

    write_list(f, list_output)
    write_array(f, array_output)