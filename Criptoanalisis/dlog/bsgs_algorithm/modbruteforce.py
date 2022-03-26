### TENTTS 
import sys
import time
import gmpy2
## Loading animation ::
BruteForceDone = False
import itertools
import threading

def animate( FunctionStr = 'the task'):
    
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if BruteForceDone:
            print('\nDone!')
            break
        else:
            sys.stdout.write('\rWorking on '+ FunctionStr +' ....................'+c)
            sys.stdout.flush()
            time.sleep(0.1)
    
###################

max_iterations = -1
def bruteforcer (nalpha, nbeta, nmodulo):

    i = 0
    while i < max_iterations:
        if(gmpy2.powmod(nalpha,i,nmodulo) == nbeta):
            return i
        else:
            i+=1
    return -1

if(len(sys.argv) < 5):
    print("ERROR. NOT ENOUGH CLI ARGUMENTS.")
    exit(0)
else:
    nbits = int(sys.argv[1])
    nmodulo = int(sys.argv[2])
    nalpha = int(sys.argv[3])
    nbeta = int(sys.argv[4])
    max_iterations = pow(2,nbits)
    print(f"Number is {nbits} bits long.")
    print(f"Modulo is {nmodulo}.")
    print(f"Using {nalpha} as ALPHA")
    print(f"Using {nbeta} as BETA")
    print(f"Max iterations:"+str(max_iterations))
startTime = time.time()
t = threading.Thread(target=animate, daemon=True,args=["bruteforce attack", ])
t.start()
match = bruteforcer(nalpha, nbeta, nmodulo)
BruteForceDone = True
endTime = time.time()
if(not (match == -1)):
    print(f"Found match on {match}.")
else:
    print(f"No match found.")
print(f"Took {endTime - startTime}seconds." )