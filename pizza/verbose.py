try:
    from colorama import init
    init()
except:
    pass

class ccolor:
    
    BKG_RED = '\033[41m'
    RED = '\033[31m'
    BKG_YELLOW = '\033[43m'
    YELLOW = '\033[33m'
    BKG_BLUE = '\033[46m'
    BLUE = '\033[36m'
    GRAY = '\033[90m'
    ENDC = '\033[0m'

def set_verbosity(v):

    global verbosity
    verbosity = v

def fatal(msg):
    
    print(ccolor.BKG_RED + "[FATAL]" + ccolor.ENDC + " " + ccolor.RED + msg + ccolor.ENDC)

def warn(msg):
    
    if verbosity > 0:
        
        print(ccolor.BKG_YELLOW + "[WARNING]" + ccolor.ENDC + " " + ccolor.YELLOW + msg + ccolor.ENDC)
        
def info(msg):
    
    if verbosity > 1:
        
        print(ccolor.BKG_BLUE + "[INFO]" + ccolor.ENDC + " " + ccolor.BLUE + msg + ccolor.ENDC)
        
def debug(msg): 
    
    if verbosity > 2:
        
        print(ccolor.GRAY + "[DEBUG] " + ccolor.GRAY + msg + ccolor.ENDC)

def end_color():

    print ccolor.ENDC

try:
    from tqdm import tqdm as progress
except:
    set_verbosity(1)
    warn("tqdm is not installed !")
    info("this library is used to display progress bar")
    def progress(range):
        return range