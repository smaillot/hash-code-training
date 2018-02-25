import numpy as np
from random import shuffle
import matplotlib.pylab as plt
from math import floor
import argparse

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
    
    
    return (R, C, L, H, pizza,)


def write_output(f, array_output):
    '''
    Takes a number of slices and a list of slices
    '''
    number_of_slices = len(array_output)
    write_list(f, [number_of_slices])
    write_array(f, array_output)

def save_slices(number_of_slices, slices):

    with open("/outputs/temp.out", 'w') as f:

        write_output(f, slices)

def display_slices(solution, R, C, pizza):

    mask = np.zeros([R, C])
    slices = np.copy(solution)
    shuffle(slices)

    for i in range(len(slices)):

        row1, col1, row2, col2 = slices[i]
        mask[row1:row2+1, col1:col2+1] = i+floor(1.2*len(slices))

    _, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    axes[0].imshow(mask, 'jet')
    axes[0].set_title('Slices')
    axes[1].imshow((mask > 0).astype(np.int))
    axes[1].set_title('Pizza used')

def parsing():
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
    parser.add_argument("-n", type=int, default=2, help="number of tests")
    parser.add_argument("-p", type=int, default=2, help="number of threads")
    
    # Initialising arguments
    return parser.parse_args()

def print_score(score, loaded_input, delay):
    R = loaded_input.R
    C = loaded_input.C
    print("Score {:.0f} ({:0.2f}%) in {:.6f}s".format(score, 100 * score / (R * C), delay))

def disp_input(pizza):
    '''
    Violet is a tomato
    Yellow is a mushroom
    '''
    
    plt.imshow(pizza)
    plt.show()