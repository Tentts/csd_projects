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


def polardRho(pollardNumber):
    alpha = beta = random.randint(2, pollardNumber-1)
    while True:
        alpha = gmpy2.t_mod((alpha**2)+1, pollardNumber)
        beta = gmpy2.t_mod((beta**2)+1, pollardNumber)
        beta = gmpy2.t_mod((beta**2)+1, pollardNumber)
        p = gmpy2.gcd(alpha-beta,pollardNumber)

        if(1<p and p<pollardNumber):
            return p
        if(p == pollardNumber):
            return pollardNumber
            


def main():
    pollardNumber = args_handler()
    global PollardDone
    alpha,beta = False, False
    
    t = threading.Thread(target=animate, daemon=True)
    t.start()
    time_start = time.time()
    alpha = polardRho(pollardNumber)
    beta = gmpy2.t_div(pollardNumber,alpha)
    PollardDone = True

    time_end = time.time() - time_start
    if alpha != 0:
        
        print(f"\nFound a & b for number <{pollardNumber}>.")
        print(f"a: <{alpha}>\nb: <{beta}>")
        print(f"{alpha}*{beta} = {alpha*beta} = {pollardNumber}")
        
    else:
        print(f"No match found.")
    print(f"Elapsed time:\t{round(time_end, 5)} seconds." )


if __name__ == "__main__":
    main()
