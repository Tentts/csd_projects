### TENTTS 
import random
import gmpy2
import sys
import time 
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
    print(f"USAGE:\n\t python3 pollardrho.py <prime_number>\n")
    exit(0)

def args_handler():
    if(len(sys.argv) < 1):
        print("ERROR. NOT ENOUGH CLI ARGUMENTS.")
        exit(0)
    else:
        pollardNumber = int(sys.argv[1])
        
        print(f"Number is <{pollardNumber}>.")
    
    return pollardNumber


def polardp1(pollardNumber):
    alpha = random.randint(2, pollardNumber-1)
    mcd = gmpy2.gcd(alpha, pollardNumber)
    if 1 < mcd and mcd < pollardNumber:
        return gmpy2.gcd(alpha,pollardNumber)
    
    k = 2
    
    while True:
        alpha = gmpy2.powmod(alpha,k, pollardNumber)
        d = gmpy2.gcd(alpha-1, pollardNumber)
        if(1<d and d<pollardNumber):
            return d
        if(d == pollardNumber):
            return False
        k+=1            


def main():
    pollardNumber = args_handler()
    global PollardDone
    alpha,beta = False, False
    
    t = threading.Thread(target=animate, daemon=True)
    t.start()
    time_start = time.time()
    alpha = polardp1(pollardNumber)
    if(alpha != False):
        beta = gmpy2.t_div(pollardNumber,alpha)
    PollardDone = True
    time_end = time.time() - time_start    
    if alpha != False:
        print(f"\nFound a & b for number <{pollardNumber}>.")
        print(f"a: <{alpha}>\nb: <{beta}>")
        print(f"{alpha}*{beta} = {alpha*beta} = {pollardNumber}")
        
    else:
        print(f"No match found.")
    print(f"Elapsed time:\t{round(time_end, 5)} seconds." )


if __name__ == "__main__":
    main()
