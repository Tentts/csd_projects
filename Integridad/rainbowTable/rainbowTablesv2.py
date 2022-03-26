### TENTTS 
import math
import random
import hashlib
import csv
import os
import sys
import time

## Usage : python3 rainbowTablev2 <hashSelector> <hashBits> <chain_size> <table_Rows> <dictionaryFile>
## Characters sets.
# uppercaseLets = 'QWERTYUIOPASDFGHJKLZXCVBNM'
# lowercaseLets = 'qwertyuiopasdfghjklzxcvbnm'
# numbersString = '0123456789'

SPACE = "0123456789" # CHARACTERS SPACE
SPACE_SIZE = len(SPACE)
PASSWORDSIZE = 8

chain_size = 1500
table_Rows = 10000

## Flags for hash algorithm setup
hash_selector = 1
hash_bits = 32
HASH_ALGORITHMS = ['crc32','md4', 'md5', 'sha1']



def PrintError(message="ERROR"):
    print(f"{message}\nEXECUTION ABORTED...")
    print("USAGE:\n\t python3 rainbowTablesv2.py <hash_algorithm_to_use> <n_hash_bits> <n_rt_chains> <n_rt_rows> <dictionary_path>\nhash_to_use:\n\t· 1 - md4\t- max 128 bits\n\t· 2 - md5\t- max 128 bits\n\t· 3 - sha1\t- max 160 bits\n")
    exit(0)


def argsHandler():
    global chain_size
    global table_Rows
    global hash_selector
    global hash_bits

    if(len(sys.argv) > 6 or len(sys.argv) < 4):
        PrintError(f"ERROR. INSUFFICIENT CLI ARGUMENTS.")

    if(int(sys.argv[1])>0 and int(sys.argv[1]) < len(HASH_ALGORITHMS)):
        hash_selector = int(sys.argv[1])
    else:
        PrintError(f"ERROR. WRONG HASH ALGORITHM SELECTION.")
    if(int(sys.argv[2]) > 0 ):
        hash_bits = int(sys.argv[2])
    else:
        PrintError(f"WRONG HASH BITS ARGUMENT.")
    if(int(sys.argv[3]) > 0 ):
        chain_size = int(sys.argv[3])
    else:
        PrintError(f"WRONG RAINBOW TABLE CHAINS ARGUMENT.")
    if(int(sys.argv[4]) > 0 ):
        table_Rows = int(sys.argv[4])
    else:
        PrintError(f"WRONG RAINBOW TABLE ROWS ARGUMENT.")
    
    if(len(sys.argv) > 5 and sys.argv[5]):
        fpath = sys.argv[5]
    else:
        fpath = f"files/{HASH_ALGORITHMS[hash_selector]}_{hash_bits}b_{chain_size}x{table_Rows}_PS{PASSWORDSIZE}.csv"
    

    print(f"Hash algorithm selected: {HASH_ALGORITHMS[int(hash_selector)]}\nUsing {str(hash_bits)} first bits from hash values.")
    print(f"\nRainbow table parameters:\n\tChain steps:\t\t{chain_size}\n\tRainbow table rows:\t{table_Rows}")
    if(hash_selector): hashObject = hashlib.new(HASH_ALGORITHMS[hash_selector])
    sys.setrecursionlimit(100000)
    return fpath


###########################################
# GET - CREATE - SAVE - LOAD RT FUNCTIONS #
###########################################


def getRT(fpath=""):
    if(os.path.exists(fpath)):
        print(f"File {fpath} detected.\nMake sure that the chosen file has been built using the same algorithm.\nLoading rainbow tables...")
        
        rainbowTable = readRT(fpath)
        if(len(rainbowTable) == 0):
            print(f"ERROR. YOUR CHOSEN RAINBOW TABLE IS EMPTY OR PATH IS WRONG.")
            exit(0)
        print(f"Rainbow table loaded. {len(rainbowTable)} entries found.")

    else:

        print(f"File {fpath} does not exist.")
        ans = 'K'
        while(ans not in 'YyNn'):
            print(f"Do you want to create \'{fpath}\' now?[Y/n]")
            ans = 'Y'
            ans = input()

            if(ans in 'Nn' and ans not in ''):
                print(f"Fatal error. Execution is not able to continue without creating dictionary.")
                exit(0)
        rainbowTable = createRT(fpath)
        
    return rainbowTable

def createRT(fpath=""):

    RTGenStartTime = time.time()
    print(f"Generating {fpath}...") 

    rainbowTable = rainbowTableGenerator()

    print(f"Rainbow Table generated.")
    print(f"Saving Rainbow Table...")
    saveRT(fpath, rainbowTable)

    RTGenEndTime = time.time()
    print(f"{fpath} generation done. Took {RTGenEndTime-RTGenStartTime} seconds.")

    return rainbowTable

def saveRT(fpath = "./rainbowtablepath.csv", rainbowTable = dict()):

    with open(fpath,"w") as fichero:
            csvW = csv.writer(fichero)
            for key_ , value_ in rainbowTable.items():
                csvW.writerow([key_, value_])

    return True

def readRT(fpath = "./rainbowtablepath.csv"):

    with open(fpath, "r") as infile:
            reader = csv.reader(infile)
            rainbowTable = {rows[0]:rows[1] for rows in reader}

    return rainbowTable

############################
# RAINBOW TABLE GENERATION #
############################

def rainbowTableGenerator():
    RTable = dict([])
    HTable = dict([])
    print(f"Generating {chain_size}x{table_Rows}")
    LRT = len(RTable)
    while LRT < table_Rows: 
        ## Creamos contraseña al azar
        initialPasswd = "".join( [SPACE[int(os.urandom(2).hex(),16) % SPACE_SIZE] for _ in range(PASSWORDSIZE)] )
        ## Obtenemos la cadena correspondiente
        finalHash = getChain(initialPasswd)
        ## Si no existe ese hash en nuestra tabla lo introducimos
        if finalHash not in HTable:
            ## Empleamos un diccionario extra para controlar los hashes introducidos
            HTable[finalHash]=initialPasswd
            RTable[initialPasswd] = finalHash 
        LRT = len(RTable)
    return RTable

def getChain(passwd=""):
    ## Generacion de una cadena (r(h(p)))
    p = passwd
    for chainIndex in range(chain_size):
        PHash   = H(p)
        p       = recoder(PHash, chainIndex)
    
    return p
    
################
# HASH FUCTION #
################
def H(istr):
    ## Funcion hash.
    hashObject = hashlib.new(HASH_ALGORITHMS[hash_selector], istr.encode('utf-8'))
    res = f"0x{hashObject.hexdigest()}"

    res = bin(int(res, 16))[2:]
    if(hash_bits < len(res)):
        res = res[ 0: hash_bits: 1]
    res = f"0b{res.zfill(hash_bits)}"
    return int(res,2)

#####################
# RECODING FUNCTION #
#####################

CharacterRecodedSize = int(round(math.log(SPACE_SIZE,2)))

def recoder(hashValue = "", chainIndex = 0):
    ## Funcion recodificante.
    recodedString = []
    recodedValue = (hashValue + chainIndex)%(SPACE_SIZE**PASSWORDSIZE)
    binaryInteger = (bin(recodedValue)[2:]).zfill(PASSWORDSIZE*CharacterRecodedSize)
    
    for ditget in range(0, CharacterRecodedSize*PASSWORDSIZE, CharacterRecodedSize):
        recodedString.append(SPACE[int(binaryInteger[ditget:ditget + CharacterRecodedSize],2)%SPACE_SIZE])

    return "".join(recodedString)

############################
# PASSWORD FINDER FUNCTION #
############################
def passwordAttack(rainbowTable= dict([]), h = "" ):
    
    ## Recoded hashes vector
    hashes = rainbowTable.values()
    ## From chain_size-1 to 0:
    for rIterator in range(chain_size -1, 0, -1):
        ## Recursive  generation 
        PwdGenerated = PwdRabbithole(h, chain_size-1, rIterator)
        if(PwdGenerated in hashes):
            passwd = [key for key, value in rainbowTable.items() if value == PwdGenerated][0]
            i = 0
            findingHash = H(passwd)
            while(findingHash != h and i <= rIterator):
                passwd = recoder(findingHash, i)
                findingHash = H(passwd)
                if(findingHash == h):
                    return passwd
                i+=1
    return -1

def PwdRabbithole(hashValue, chainIndex , targetIndex = 0):
    ## If recoder iterator == j(target iterator) return recoder
    if(chainIndex == targetIndex):
        return recoder(hashValue, chainIndex)
    ## If i still != j, keep going down the chain rabbithole 
    return recoder(H(PwdRabbithole(hashValue, chainIndex-1, targetIndex)),chainIndex)



#################
# MAIN FUNCTION #
#################
def mainFunction():
    

    ## Flags for algorithm setup
    ## ArgsHandler sets hash_bits, hash_type, rt chain steps, rt size
    fpath = argsHandler()
    rainbowTable = getRT(fpath)
    
    targetIterations = 1000
    print(f"Rainbow table size: {sys.getsizeof(rainbowTable)} bytes ({round(sys.getsizeof(rainbowTable) /(1024**2), 4)} MB)")
    print(f"Starting rainbow table attack test...")
    iterations= 0 
    cracked = 0
    avgtime = 0
    while iterations < targetIterations : 
        
        EvilPassword    = "".join(random.SystemRandom().choice(SPACE) for _ in range(PASSWORDSIZE))
        EvilHash        = H(EvilPassword)
        startTime = time.time()
        crackedPassword = passwordAttack(rainbowTable, EvilHash )
        elapsedTime =  time.time() - startTime
        
        if(crackedPassword != -1 and (H(crackedPassword) == EvilHash)):
            avgtime += elapsedTime
            cracked += 1 
        iterations +=1
    avgtime /= cracked
    print(f"================ TEST REPORT ===============")
    print(f"Attack setup:")
    print(f"\tHash algorithm: {HASH_ALGORITHMS[int(hash_selector)]}\nHash bits:{hash_bits}")
    print(f"\nRainbow table parameters:\n\tChain steps:\t\t{chain_size}\n\tRainbow table rows:\t{table_Rows}")
    print(f"{iterations} search iterations completed.")
    print(f"Succesful iterations: {cracked}/{iterations} ({(cracked/iterations) * 100})")
    print(f"Average time spent on succesful iterations: {avgtime}")
    print(f"=======================================")
    
if __name__ == "__main__":
    
    mainFunction()