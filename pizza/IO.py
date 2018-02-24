from verbose import *

def write_list(f, list):

    f.write(" ".join([str(n) for n in list]) + "\n")

def write_array(f, array):

    for line in array:        
        
        write_list(f, line)

def read_input(reader):
    
    ## init params
    input1, input2, input3 = [int(i) for i in reader.readline().split(" ")]
    
    ## n blbl
    input4 = [int(i) for i in reader.readline().split(" ")]
    
    ## blbl
    tab = []
    for _ in range(input4[0]):
        
        tab.append([int(i) for i in reader.readline().split(" ")])
    
    
    return input1, input2, input3, tab

def write_output(f, list_output, array_output):

    write_list(f, list_output)
    write_array(f, array_output)