import numpy as np
from random import shuffle

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


def write_output(f, array_output):
    '''
    Takes a number of slices and a list of slices
    '''
    number_of_slices = len(array_output)
    write_list(f, [number_of_slices])
    write_array(f, array_output)

def save_slices(slices):

    with open("/outputs/temp.out", 'w') as f:

        write_output(f, slices)

def display_slices(solution, R, C, pizza):

    mask = np.zeros([R, C])
    slices = solution
    shuffle(slices)

    for i in range(len(slices)):

        row1, col1, row2, col2 = slices[i]
        mask[row1:row2+1, col1:col2+1] = i+1

    fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    axes[0].imshow(mask)
    axes[1].imshow((mask > 0).astype(np.int))