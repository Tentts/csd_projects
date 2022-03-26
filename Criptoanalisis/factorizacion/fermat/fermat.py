### TENTTS 
import gmpy2
import sys
import time 
## Animation libs
import itertools
import threading


## Global defs
fermatDone = False

## Loading animation ::
def animate():
    
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if fermatDone:
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
        fermatNumber = int(sys.argv[1])
        
        print(f"Number is <{fermatNumber}>.")
    
    return fermatNumber

def fermat(fermatNumber):
    
    alpha = gmpy2.isqrt(fermatNumber)+1
    beta = gmpy2.sub(alpha**2, fermatNumber)

    while not gmpy2.is_square(beta):
        alpha+=1
        beta = gmpy2.sub(alpha**2, fermatNumber)
        
    return gmpy2.sub(alpha, gmpy2.isqrt(beta)),gmpy2.add(alpha, gmpy2.isqrt(beta))


def main():
    fermatNumber = args_handler()
    global fermatDone
    alpha,beta = False, False
    
    t = threading.Thread(target=animate, daemon=True)
    t.start()
    time_start = time.time()
    alpha,beta = fermat(fermatNumber)
    fermatDone = True

    time_end = time.time() - time_start
    
    
    if alpha != 0:
        
        print(f"\nFound a & b for number <{fermatNumber}>.")
        print(f"a: <{alpha}>\nb: <{beta}>")
        print(f"{alpha}*{beta} = {alpha*beta} = {fermatNumber}")
        
    else:
        print(f"No match found.")
    print(f"Elapsed time:\t{round(time_end, 5)} seconds." )


if __name__ == "__main__":
    main()
