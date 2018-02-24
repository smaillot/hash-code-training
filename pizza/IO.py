from verbose import *

def write_list(f, list):

    f.write(" ".join([str(n) for n in list]) + "\n")

def write_array(f, array):

    for line in array:        
        
        write_list(f, line)

def read_input(reader):
    
    ## init params
    # number of rows, number of columns, minimum number of each ingredient cells in a slice, maximum number of cells of a slice
    R, C, L, H = [int(i) for i in reader.readline().split(" ")]
    
    
    pizza = []
    for _ in range(R):
        
        pizza.append(list(reader.readline().rstrip()))
    
    
    return R, C, L, H, pizza

def write_output(f, list_output, array_output):

    write_list(f, list_output)
    write_array(f, array_output)