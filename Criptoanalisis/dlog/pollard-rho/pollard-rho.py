### TENTTS 
import sys
import time 

import gmpy2
## Animation libs 
import itertools
import threading


## Global defs
PollardDone = False


## Loading animation ::


def animate():
    
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if PollardDone:
            break
        else:
            sys.stdout.write(f"\rBe patient...{c}")
            sys.stdout.flush()
            time.sleep(0.1)
    
###################
def PrintError(message="ERROR"):
    print(f"{message}\nEXECUTION ABORTED...")
    print(f"USAGE:\n\t python3 pollard-rho.py <nbits> <nmodulo> <alpha> <beta> <order>\n")
    exit(0)

def args_handler():
    ### MAIN
    if(len(sys.argv) < 6):
        PrintError(f"ERROR. NOT ENOUGH CLI ARGUMENTS.")
    else:
        nbits = int(sys.argv[1])
        modulo = int(sys.argv[2])
        alpha = int(sys.argv[3])
        beta = int(sys.argv[4])
        order = int(sys.argv[5])
        print(f"Problem is {nbits} b on complexity.")
        print(f"Modulo is {modulo}.")
        print(f"Using {alpha} as ALPHA")
        print(f"Using {beta} as BETA")
        print(f"Using {order} as order")
    
    return nbits, modulo, alpha, beta, order

def fxab(x, a, b, p, alpha, beta):
    
    
    if(x%3 == 1):
        
        x = gmpy2.t_mod(gmpy2.mul(beta,x), p)
        b = gmpy2.t_mod((b+1), (p-1))
        return x,a,b
    if(x%3 == 0):
        
        x = gmpy2.powmod(x,2,p)
        a = gmpy2.t_mod((2*a), (p-1))
        b = gmpy2.t_mod((2*b), (p-1))
        return x,a,b
    if(x%3 == 2):
        
        x = gmpy2.t_mod(gmpy2.mul(alpha,x), p)
        a = gmpy2.t_mod((a+1), (p-1))
        return x,a,b

def pollard_rho(alpha, beta, modulo, order):
    a = aa = b = bb = 0 
    i = x = xx = 1
    while i < modulo:

        x,a,b = fxab(x,a,b,modulo,alpha,beta)
        xx,aa,bb = fxab(xx,aa,bb,modulo,alpha,beta)
        xx,aa,bb = fxab(xx,aa,bb,modulo,alpha,beta)
        
        if x == xx:
            if gmpy2.gcd((b-bb),order) != 1:
                return False
            
            return ((aa-a) * gmpy2.powmod(b-bb,-1, order))%order  
        
        i+=1
    return False

def main():
    nbits,modulo, alpha, beta, order = args_handler()
    global PollardDone
    ## Working animation
    t = threading.Thread(target=animate, daemon=True)
    t.start()
    
    time_start = time.time()
    match = pollard_rho(alpha, beta, modulo, order)
    PollardDone = True
    time_end = time.time() - time_start

    if match != False:
        print(f"Found match on {match}.")
        print(f"{alpha}^{match} mod {modulo} = {pow(alpha, match, modulo)}")
    else:
        print(f"No match found.")
    print(f"Elapsed time:\t{round(time_end, 7)} seconds." )


if __name__ == "__main__":
    main()
