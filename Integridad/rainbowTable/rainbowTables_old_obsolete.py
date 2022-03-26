### TENTTS 
import random
import hashlib
import zlib
import csv
import os
import sys
import time
import math

## Usage : python3 rainbowTalbe <dictionaryFile> <hashSelector> <hashBits> 
## Possible characters.
uppercaseLets = 'QWERTYUIOPASDFGHJKLZXCVBNM'
lowercaseLets = 'qwertyuiopasdfghjklzxcvbnm'
numbersString = '0123456789'
symb = '/*,.-+#$@'
letters = lowercaseLets+uppercaseLets
alphanumeric = letters+numbersString
characs = alphanumeric+symb

lettersSet          = set(letters)
alphanumericSet     = set(alphanumeric)
characsSet          = set(characs)

passwdSpace = numbersString+'ABCDEF'
passwdSpaceSize = len(passwdSpace)
minPasswordSize = 6
maxPasswordSize = 8

CharacterRecodedSize = int(round(math.log(passwdSpaceSize,2),0))

## Flags for hash algorithm setup
hash_selector = 0
hashAlgorithms = ['crc32','md4', 'md5', 'sha1']
hash_bits = 32


## Loading animation ::
RainbowTableComplete = False
import itertools
import threading

def animate():
    
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if RainbowTableComplete:
            
            break
        else:
            sys.stdout.write(f"\rBe patient...{c}")
            sys.stdout.flush()
            time.sleep(0.1)
def PrintError(message="ERROR"):
    print(f"{message}\nEXECUTION ABORTED...")
    print("USAGE:\n\t python3 rainbowTables.py <dictionary_path> <hash_to_use> <n_hash_bits> <n_rt_chains> <n_rt_rows>\nhash_to_use:\n\t· 0 - crc32\t- max 32 bits\n\t· 1 - md4\t- max 128 bits\n\t· 2 - md5\t- max 128 bits\n\t· 3 - sha1\t- max 160 bits\n")
    exit(0)

#########################
# SAVE & LOAD FUNCTIONS #
#########################

def saveRT(fpath = "./rainbowtablepath.csv", rainbowTable = dict()):

    with open(fpath,"w") as fichero:
            csvW = csv.writer(fichero)
            for key_ , value_ in rainbowTable.items():
                csvW.writerow([key_, value_])

    return True

def getRT(fpath = "./rainbowtablepath.csv"):
    with open(fpath, "r") as infile:
            reader = csv.reader(infile)
            rainbowTable = {rows[0]:rows[1] for rows in reader}

    # rainbowTable = dict([])
    # for row in tmpDict:
    #     rainbowTable[row] = int(str(tmpDict[row]), 10)
    return rainbowTable

################
# HASH FUCTION #
################
def getHash(istr):

    if(not hash_selector):
        
        to_hash = bytes(istr,'utf-8')
        res = hex(zlib.crc32(to_hash) & 0xffffffff)
        
    else:
        hashObject = hashlib.md5(istr.encode('utf-8'))
        res = f"0x{hashObject.hexdigest()}"
        
    res = bin(int(res, 16))[2:]
    if(hash_bits > len(res)):
        res = res[ 0: len(res): 1]
    else:
        res = res[ 0: hash_bits: 1]
    res = res.zfill(hash_bits)
    return int(res,2)

#####################
# RECODING FUNCTION #
#####################
# https://crypto.stackexchange.com/questions/37832/how-to-create-reduction-functions-in-rainbow-tables
# def R(i, x): # i'th reduction function
#   return (x + i) mod (espacio de caracteres**tamaño de contraseña)
# 
# 
# 


def recoder(iFunction = 0, hashValue = 0):
    recodedString = []
    
    recodedValue = ((hashValue) + iFunction)%(passwdSpaceSize**maxPasswordSize)
    
    recodedString = []
    binaryInteger = (bin(recodedValue)[2:]).zfill(maxPasswordSize*CharacterRecodedSize)
    #print(binaryInteger)
    for ditget in range(0, len(binaryInteger), CharacterRecodedSize):
        recodedString.append(passwdSpace[int(binaryInteger[ditget:ditget + CharacterRecodedSize])%passwdSpaceSize])

    return "".join(recodedString)


############################
# RAINBOW TABLE GENERATION #
############################

TableColumns    = 5000     # t
TableNRows      = 10000     # n


def rainbowTableGenerator():
    Rtable = dict()
    LRT = len(Rtable)
    while LRT < TableNRows:
        P0 = "".join( [passwdSpace[int(os.urandom(2).hex(),16) % passwdSpaceSize] for _ in range(maxPasswordSize)] )
        
        P1 = P0
        ColumnsIterator = 0 
        while ColumnsIterator < TableColumns:
            
            P1 = recoder(TableColumns-1, getHash(P1))
            ColumnsIterator += 1

        if(LRT%1000 == 0):print(f"Generated {LRT} entries, {TableNRows - LRT} left.")
        Rtable[P0] = getHash(P1)
        LRT = len(Rtable)
    return Rtable

############################
# PASSWORD FINDER FUNCTION #
############################
def passwordFinder(PZero = "", rainbowTable= dict([])):
    
    
    iteratorQuantity = 0
    ValuesList = rainbowTable.values()
    
    while iteratorQuantity < TableColumns:
        ## hash-recoding n times
        iteratorR = TableColumns-iteratorQuantity   ## Number n of starting Rfunction
        Pe = PZero
        while(iteratorR < TableColumns-1):          ## Series of H(R(n,hash))
            #print(f"R {iteratorR}/{iteratorQuantity} : {Pe}")
            Pe = getHash(recoder(iteratorR, Pe))
            iteratorR+=1
        if(Pe in ValuesList):
            print(f"Found value {Pe} in rainbow table after {iteratorQuantity} steps.")
            break
        iteratorQuantity += 1
        
    if(iteratorQuantity == TableColumns):
        print("Error on password finder function. No collision found.")
        return -1
    ## Taking first key with value Pe
    Pwd = [key for key, value in rainbowTable.items() if value == Pe][0]

    print(f"Initial password for recoded value \'{Pe}\': {Pwd}")

    PwdHash = getHash(Pwd)
    Previous = Pwd
    indexCounter = 0
    while(PwdHash != PZero): #and indexCounter < TableColumns):
        #print(f"{indexCounter}\t| PwdHash {PwdHash}/{Pwd}\t!=\t{PZero}/{recoder(PZero)}")
        Previous = Pwd
        Pwd = recoder(indexCounter,PwdHash)
        PwdHash = getHash(Pwd)
        
        # if(Pe == Pwd): 
        #     print(f"Oops! We're again at {Pe}. Previous was {Previous}.")
        #     break
        indexCounter+=1
    
    if(indexCounter >= TableColumns):
        return -1
    return Pwd
    

#################
# MAIN FUNCTION #
#################
def mainFunction():
    if(len(sys.argv) > 1):
        fpath = sys.argv[1]
        if(len(sys.argv) > 2 and int(sys.argv[2])>=0 and int(sys.argv[2]) < len(hashAlgorithms)):
            hash_selector = int(sys.argv[2])
            if(len(sys.argv) > 3 and int(sys.argv[3]) > 0 ):
                hash_bits= int(sys.argv[3])
                number_of_Ms = pow(2,hash_bits/2)
                if(len(sys.argv) > 4 and int(sys.argv[4]) > 0 ):
                    TableColumns = int(sys.argv[4])
                    if(len(sys.argv) > 5 and int(sys.argv[5]) > 0 ):
                        TableNRows = int(sys.argv[5])
                    else:
                        PrintError(f"WRONG RAINBOW TABLE ROWS ARGUMENT.")
                else:
                    PrintError(f"WRONG RAINBOW TABLE CHAINS ARGUMENT.")
            else:
                PrintError(f"WRONG HASH BITS ARGUMENT.")
        else:
            PrintError(f"ERROR. WRONG HASH ALGORITHM ARGUMENT.")
    else:
        PrintError(f"ERROR. INSUFFICIENT CLI ARGUMENTS.")

    print(f"Hash algorithm selected: {hashAlgorithms[int(hash_selector)]}\nUsing {str(hash_bits)} first bits from hash values.")
    print(f"\nRainbow table parameters:\n\tRainbow chains:\t\t{TableColumns}\n\tRainbow table rows:\t{TableNRows}")

    if(hash_selector): hashObject = hashlib.new(hashAlgorithms[hash_selector])


    if(os.path.exists(fpath)):
        print(f"File {fpath} detected.\nMake sure that the chosen file has been built using the same hash algorithm.\nLoading rainbow tables...")
        
        rainbowTable = getRT(fpath)
        if(len(rainbowTable) == 0):
            print(f"ERROR. YOUR CHOSEN RAINBOW TABLE IS EMPTY OR PATH IS WRONG.")
            exit(0)
        print(f"Rainbow table loaded. {str(len(rainbowTable))} entries found.")

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
            
        RTGenStartTime = time.time()
        print(f"Generating {fpath}...")
        # t = threading.Thread(target=animate,daemon=True, name="thread_animation")
        # t.start()

        rainbowTable = rainbowTableGenerator()
        print(f"Rainbow Table generated.")
        print(f"Saving Rainbow Table...")
        saveRT(fpath, rainbowTable)

        RainbowTableComplete = True

        RTGenEndTime = time.time()
        print(f"{fpath} generation done.")
    #print(rainbowTable)

    print(f"Starting rainbow table password retrieval test...")
    
    crackedPassword = -1
    while crackedPassword == -1: 
    
        EvilPassword    = ''.join(random.SystemRandom().choice(passwdSpace) for _ in range(maxPasswordSize))
        EvilHash        = getHash(EvilPassword)


        print(f"Looking for password collision:\nPassword:\t \' {EvilPassword} \'\nHash:\t \' {EvilHash} \'")
        RainbowTableComplete = False
        # t = threading.Thread(target=animate,daemon=True, name="thread_animation")
        # t.start()
        startTime = time.time()
        crackedPassword = passwordFinder(EvilHash, rainbowTable)
        RainbowTableComplete = True
        elapsedTime =  time.time() - startTime
        print("====================== END ======================\n")
        ## Posting results
        if(crackedPassword != -1):
            print(f"Password collision found for hash {EvilHash}!")
            print(f"[Password / Hash]: [{crackedPassword}/{getHash(crackedPassword)}]")
            print(f"Took {str(elapsedTime)} seconds.")
        else:
            print(f"No password detected after {str(elapsedTime)} seconds.")
        print("================================================\n")


if __name__ == "__main__":

    mainFunction()