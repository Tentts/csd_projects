### TENTTS 
import sys
import time
import gmpy2
import numpy as np
## Global defs
BSGSDone = False
nbits = 0
nmodulo = 0
nalpha = 0
nbeta = 0

baby_steps = dict([], dtype= np.uint64)
#baby_steps = dict([])



## Loading animation ::

import itertools
import threading

def animate(msg):
    
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if BSGSDone:
            break
        else:
            sys.stdout.write(f"\rWorking on {msg}...{c}")
            sys.stdout.flush()
            time.sleep(0.1)
    
###################
def PrintError(message="ERROR"):
    print(f"{message}\nEXECUTION ABORTED...")
    print(f"USAGE:\n\t python3 bsgs.py <nbits> <nmodulo> <alpha> <beta>\n")
    exit(0)

def args_handler():
    global nbits
    global nmodulo
    global nalpha 
    global nbeta
    ### MAIN
    if(len(sys.argv) < 5):
        print(f"ERROR. NOT ENOUGH CLI ARGUMENTS.")
        exit(0)
    else:
        nbits = int(sys.argv[1])
        nmodulo = int(sys.argv[2])
        nalpha = int(sys.argv[3])
        nbeta = int(sys.argv[4])
        print(f"Problem is {nbits} b on complexity.")
        print(f"Modulo is {nmodulo}.")
        print(f"Using {nalpha} as ALPHA")
        print(f"Using {nbeta} as BETA")



## Babysteps function
def babySteps (nalpha, n_numero, nmodulo):
    r = 1
    while (r < n_numero):
        gamma = np.uint64(gmpy2.powmod(nalpha,r, nmodulo))
        baby_steps[gamma] = r
        r=r+1
    return 1

def giantSteps(nalpha, ngamma, nmodulo, nnumero):
    nq = 0 
    while nq < nnumero:
        if(ngamma in baby_steps):
            nk = nq*nnumero + baby_steps[ngamma]
            return nk
        k = gmpy2.powmod(nalpha, (-nnumero), nmodulo)
        ngamma = gmpy2.powmod(ngamma * k, 1, nmodulo)
        nq = nq+1
    return -1


def main():
    args_handler()
    startTime = time.time()

    n_numero = gmpy2.isqrt(nmodulo)+1


    print(f"Size of new dicitonary: {n_numero} pairs.")
    ## BabySteps
    print(f"BabySteps starting now...")
    t = threading.Thread(target=animate, daemon=True, args=["baby steps",])
    t.start()
    babySteps(nalpha, n_numero, nmodulo)
    BSGSDone = True
    babyStepsTime = time.time() - startTime
    print(f"BabySteps done in {round(babyStepsTime,3 )}s.")
    ngamma = nbeta
    ## GiantSteps()
    print(f"GiantSteps starting now...")
    match = giantSteps(nalpha, ngamma, nmodulo,n_numero)
    endTime = time.time() - startTime
    print(f"Size of babysteps: {sys.getsizeof(baby_steps)} Bytes -> {round(sys.getsizeof(baby_steps)/(1024**2),2)} MB")
    giantStepsTime = endTime - babyStepsTime
    print(f"GiantSteps done in {round(giantStepsTime,7 )}s.")

    print(f"Original number: {nbeta}")
    if match != -1:
        print(f"Found match on {match}.")
        print(f"{nalpha}^{match} mod {nmodulo} = {pow(nalpha, match, nmodulo)}")
    else:
        print(f"No match found.")
    print(f"Took {round(endTime,7 )} seconds:" )
    print(f"\t· {round(babyStepsTime,7 )}s on baby steps.")

    print(f"\t· {round(giantStepsTime,7 )}s on giant steps.")

if __name__ == "__main__":
    main()