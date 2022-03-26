### TENTTS 
import random
import hashlib
import zlib
import sys
import time
## Usage : python3 bday <hashSelector> <hashBits> 
## Possible characters.
uppercaseLets = 'QWERTYUIOPASDFGHJKLZXCVBNM'
lowercaseLets = 'qwertyuiopasdfghjklzxcvbnm'
numsString = '1234567890'
symb = '/*,.-+'
characs= lowercaseLets+uppercaseLets+numsString+symb
letters= lowercaseLets+uppercaseLets

uppercaseLetsSet = set(uppercaseLets)
lowercaseLetsSet = set(lowercaseLets)
lettersSet= set(letters)
numsStringSet = set(numsString)
symbSet = set(symb)
characsSet = set(characs)

## Flags for hash algorithm setup
hash_selector = 1
hashAlgorithms = ['crc32','md4', 'md5', 'sha1']
hash_bits = 32
## Amount of mesasges in original M dictionary
number_of_Ms = 2**(hash_bits/2)
#number_of_Ms = pow(2,18)

# Flags and variables for evil collision algorithm.
collision = False
## Max iterations to find collision
Max_iterations_for_collision = 50000000


# Msize =  8192
# Original Message. (Password)
#M = "".join(random.SystemRandom().choice(characs) for _ in range(Msize))
M = f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut maximus lorem, nec bibendum nibh. Fusce et sapien id massa posuere dignissim porta ac magna. Etiam ullamcorper imperdiet varius. Aenean tincidunt odio in urna dapibus, in egestas elit venenatis. Pellentesque rhoncus ornare mauris eu consectetur. In tristique nisi nibh, finibus semper ex scelerisque eget. Suspendisse sit amet lacinia velit. Curabitur sit amet massa vitae risus varius mollis. Integer blandit risus in lacus lacinia tempus et non magna. Fusce nec arcu in ex venenatis sodales non vitae nulla.Proin sed tellus euismod tortor ultrices venenatis sit amet vel magna. Nullam consectetur, orci et dapibus dictum, turpis purus posuere ipsum, ac tincidunt orci elit nec lacus. Donec at malesuada lectus. Aenean tempor enim sit amet tincidunt volutpat. Suspendisse posuere risus ac nunc euismod semper. Praesent sit amet faucibus tortor. Phasellus vitae odio lectus. Nam elementum sollicitudin felis eget vehicula. Aenean a nisi mi. Donec felis lacus, venenatis elementum hendrerit rhoncus, sodales vitae elit. Fusce eget purus rutrum, eleifend justo in, porta nibh. Quisque pretium felis in enim porttitor, sit amet mollis dolor porttitor. Maecenas aliquet faucibus est, eget egestas arcu rutrum in.In ultrices sed urna quis auctor. Sed at dolor vitae mauris tempus imperdiet in quis metus. Integer pulvinar lacinia diam a pellentesque. Cras at erat scelerisque, vulputate arcu sagittis, sodales libero. Aenean viverra tempor enim non commodo. Quisque molestie enim in tristique ultrices. Suspendisse sit amet venenatis turpis.Donec nec neque vel lectus mollis rutrum. Donec laoreet ex at erat semper scelerisque. Ut fringilla, velit in pharetra faucibus, turpis odio malesuada tortor, vitae fermentum arcu lacus at mauris. Donec accumsan est dapibus lorem lobortis sodales. Donec vestibulum velit non tellus dapibus, a vulputate massa fermentum. Etiam sit amet purus id tellus euismod placerat sed nec erat. Duis nulla dolor, commodo in leo vel, pharetra dapibus augue. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aenean non odio nec ex vulputate sollicitudin. In facilisis sed lacus a rutrum. Morbi molestie, libero et dignissim pretium, enim orci luctus dui, at malesuada libero dui et risus. Vivamus eget commodo magna. Aliquam congue maximus orci quis tristique. Duis mattis ipsum sit amet felis euismod, ac euismod elit commodo.Integer malesuada laoreet lacus sed consequat. Sed eleifend nisi sit amet tempus accumsan. Maecenas arcu felis, aliquet vel tortor eget, dictum luctus magna. Phasellus placerat lorem eu sapien tempus finibus. Curabitur bibendum interdum purus a varius. Donec pretium cursus tortor sed blandit. Nullam sit amet egestas magna, quis molestie sapien. Quisque pulvinar, leo sit amet cursus viverra, mauris dui vulputate augue, nec dictum enim felis eu velit. Quisque lacinia dolor metus, at imperdiet tellus vestibulum vel. Donec non ante vel lectus eleifend aliquet. Interdum et malesuada fames ac ante ipsum primis in faucibus.Cras vestibulum eu sapien vel hendrerit. Nam quis purus eget velit placerat dictum. Donec velit nisi, consectetur in odio at, pulvinar scelerisque urna. Quisque eget accumsan felis, ac pretium metus. Cras elementum rutrum ante a suscipit. Sed quis efficitur ex, et vestibulum nulla. Sed fringilla nec eros a pellentesque. Etiam mollis tristique massa ac placerat. Sed fringilla suscipit maximus. Donec vel leo a dolor posuere viverra id non massa. Nulla bibendum fringilla nibh, quis venenatis urna tincidunt vel. Curabitur consectetur eros sed massa vehicula, sed porttitor diam auctor.Nulla lacinia, urna et ultrices pretium, felis quam dapibus elit, at ornare lectus dui et turpis. Nullam dignissim augue in erat ullamcorper feugiat. Nunc eget lacinia eros. Donec scelerisque in massa vitae tempus. Sed semper, justo at cursus facilisis, dolor neque posuere ante, id porttitor mauris purus et nisi. Nam quis nibh nec felis dapibus molestie non at dolor. Curabitur elementum, nisl non vehicula efficitur, urna mauris accumsan sapien, tincidunt blandit nulla lacus vel dolor.Donec at ultrices arcu, vel dictum ligula. Aliquam sodales interdum leo, vel maximus leo aliquet at. Morbi quis eleifend leo, vitae elementum quam. Cras sit amet iaculis purus. Ut bibendum elementum mauris, id euismod urna fermentum sit amet. Integer interdum lobortis neque vel cursus. Nulla turpis enim, efficitur non dignissim in, auctor eu nisi.Suspendisse ornare, lorem rhoncus pellentesque viverra, ante magna rutrum ex, ac condimentum sapien tortor sed lectus. Ut finibus semper lobortis. Ut id purus ut leo pretium pharetra. Donec luctus arcu id velit sodales, at consequat massa faucibus. Duis congue, dolor ac maximus ullamcorper, nibh augue pretium elit, quis euismod mi quam molestie enim. Nunc rhoncus id ipsum sed elementum. Nulla ultricies velit ut libero ullamcorper dapibus. Aliquam venenatis tellus libero, a congue ligula pretium quis. Sed et diam sem.Cras vel dignissim mauris. Quisque porta felis eu elit commodo, et placerat velit maximus. Mauris elit ligula, bibendum eu aliquet sed, tincidunt a justo. Sed faucibus eleifend justo at facilisis. Integer at mattis dolor, at viverra urna. Pellentesque vel quam luctus, commodo ipsum sed, sodales mi. Nunc molestie massa varius, mattis lacus condimentum, vestibulum leo. Mauris eget consectetur mi.Quisque efficitur maximus ornare. Mauris ipsum leo, cursus molestie orci id, laoreet egestas augue. Nunc faucibus non leo in varius. Sed tempus ac est quis blandit. Etiam leo lorem, consectetur in turpis sit amet, hendrerit sollicitudin massa. Mauris nec tempus eros, a aliquet ligula. Maecenas tincidunt nisi facilisis auctor dignissim. Donec auctor velit metus, quis malesuada ipsum eleifend sed.Suspendisse potenti. Quisque id magna augue. Nulla venenatis ligula arcu, nec efficitur massa euismod tincidunt. Vestibulum pellentesque lacus sem, quis commodo massa facilisis ac. Suspendisse hendrerit mollis risus et elementum. Sed sed sem purus. Ut at elit ac nunc varius maximus.Curabitur laoreet magna nec lacus viverra, vel volutpat enim auctor. Aliquam non facilisis est. Aliquam erat magna, interdum vel cursus eget, semper sed diam. Nulla tincidunt elit eget lorem cursus scelerisque. Pellentesque sagittis lectus tellus, vitae semper nisi iaculis a. Integer lobortis quam quis odio aliquet, non convallis augue faucibus. Proin eget luctus velit, sed venenatis augue. Fusce augue erat, aliquet vestibulum mollis a, suscipit quis diam. Aenean imperdiet felis sed risus varius pretium. Duis fringilla iaculis metus, vel vestibulum neque tempus sed. Etiam tempor tellus non ultricies mattis. Ut rhoncus mauris sit amet ullamcorper semper.Duis at tellus vel nulla pellentesque dictum eget eu dolor. Mauris dictum ac lacus sit amet congue. Praesent et dolor a turpis malesuada facilisis non eu erat. Pellentesque pharetra mauris felis, sit amet pulvinar ipsum iaculis at. Vivamus ullamcorper nec urna sed dictum. Curabitur aliquet malesuada finibus. Donec congue quam sit amet consequat facilisis. Ut porta in felis a interdum. Vestibulum in dignissim elit. Nam a auctor ligula. Aenean sit amet odio lacinia, aliquet nisl et, luctus odio. Nullam convallis velit orci, sed molestie velit euismod sed. Ut placerat iaculis nulla, feugiat semper odio pellentesque eget.Nunc id vehicula mauris. Donec iaculis porttitor erat, id tristique diam commodo quis. Nulla facilisi. Donec leo metus, dictum eget odio ut, vestibulum tincidunt velit. Fusce risus quam, lobortis ut condimentum id, consequat pulvinar quam. Fusce tincidunt malesuada augue ac semper. Donec laoreet nisl in risus suscipit, eget maximus urna bibendum. Sed efficitur, ex eu aliquam pulvinar, eros sapien aliquam magna, sit amet interdum nunc tortor a neque. Etiam non varius magna, non dapibus sapien. Etiam urna urna, dapibus a mollis vel, finibus ut augue. Nunc est dolor, tincidunt quis aliquet id, tempor a quam. Nullam vel congue est, ut tristique felis.Donec est magna, egestas quis dolor ac, sagittis malesuada nisl. Maecenas feugiat elit hendrerit, condimentum nulla eu, dignissim dolor mauris."
Msize = len(M)
## Original Evil X
#X = "".join(random.SystemRandom().choice(characs) for _ in range(Msize))
X = f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc viverra felis felis, vitae tempor felis iaculis molestie. Phasellus eget mi eget lacus maximus pulvinar. Suspendisse vulputate cursus commodo. Nulla accumsan libero sit amet dui auctor mattis. Morbi quis massa quis eros vehicula tincidunt. Suspendisse tincidunt felis vel elementum convallis. Aliquam euismod purus at nulla aliquet, eu accumsan ex imperdiet. Duis laoreet dui in erat venenatis, ut molestie sapien vulputate. Nam faucibus, augue sagittis dictum tempor, velit diam aliquet mauris, sit amet eleifend dui enim et erat. Suspendisse potenti. Vivamus molestie egestas lectus, sed ornare libero gravida vel. Curabitur in eros id ligula euismod pellentesque. Integer consequat justo nec massa tempor sodales. Aliquam auctor vitae risus in auctor. Nullam a pulvinar odio, at rutrum erat.Nam rutrum vel erat id consectetur. Mauris a lobortis ligula. Ut vitae sem sit amet mauris scelerisque faucibus sit amet vel arcu. Nullam nec laoreet lacus. Sed metus leo, egestas vel neque luctus, efficitur dapibus dolor. Fusce sit amet lorem orci. Ut a lorem non velit lacinia ultrices.In quis est neque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla magna felis, tincidunt eget sapien et, mattis sagittis enim. Fusce sit amet euismod elit. Proin volutpat venenatis quam, ut molestie mauris vehicula eu. Proin nec scelerisque dui. Nulla at pulvinar risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In dui risus, sagittis ut dictum a, mollis vel dui. Nullam eget posuere tortor. Vivamus vel orci dui. Sed et elit sit amet ipsum accumsan interdum. Pellentesque eu quam diam.Proin dignissim posuere faucibus. Pellentesque porttitor neque nisi, id consequat quam eleifend vel. Phasellus egestas eleifend quam, quis iaculis leo faucibus vitae. Cras congue id ex vel sollicitudin. Mauris pharetra elementum sapien vel lobortis. Vestibulum id dolor dolor. Morbi pretium ipsum a enim facilisis, tincidunt condimentum diam lacinia. Suspendisse dictum libero vitae nibh egestas, sed consectetur libero ullamcorper. Aenean fermentum nisl enim, eget suscipit dui feugiat non. Pellentesque sit amet arcu luctus risus mollis molestie. Donec mattis bibendum posuere. Curabitur feugiat eu augue vel vehicula.Suspendisse ac diam iaculis, ornare erat sed, ornare nulla. Integer iaculis ante id interdum gravida. Donec pharetra ante et condimentum lobortis. Integer quis leo non nibh venenatis convallis nec at arcu. Sed suscipit turpis eget pretium pharetra. Praesent blandit tempus nisl, eu varius odio accumsan vel. Curabitur et augue quam.Fusce vestibulum pharetra porttitor. Cras eu nisl consectetur, lacinia eros eu, accumsan sem. Fusce luctus, sem feugiat pharetra porta, urna erat venenatis massa, nec finibus lacus dui non libero. Nulla sit amet lorem in arcu pellentesque eleifend a id enim. In tempus orci in justo tempor, id rutrum libero eleifend. Aenean efficitur at turpis vitae consectetur. Cras ut diam in arcu vehicula egestas. Curabitur facilisis est eu tortor auctor, eu elementum turpis gravida.In leo augue, sollicitudin et finibus sed, vehicula sed leo. Morbi sapien orci, accumsan a consectetur a, lacinia et magna. Praesent id sodales dolor. Aenean vel cursus neque. Nulla consequat, mi id aliquam faucibus, odio ex suscipit eros, vel rhoncus est orci et enim. Donec commodo ipsum ut lectus vehicula sodales. Donec a magna vel lectus rutrum rhoncus.Sed hendrerit maximus placerat. Quisque vel ex quis felis ultrices vehicula. Proin pellentesque et turpis non mattis. Donec diam magna, scelerisque quis euismod eu, pretium id erat. In hac habitasse platea dictumst. Cras elementum ligula sit amet velit convallis, eget pretium quam convallis. Mauris non pharetra diam, eu egestas turpis. Curabitur quis efficitur odio.Ut non interdum neque, vel eleifend nibh. Phasellus pellentesque elementum massa, id porta justo ornare dapibus. Nullam at massa in nisi porttitor efficitur. In vel velit et enim gravida dapibus tristique quis odio. Aliquam tincidunt erat at metus dignissim, a porttitor sem scelerisque. Nunc venenatis dolor sem, eu pretium augue malesuada sed. Sed gravida, magna quis sollicitudin aliquam, lectus arcu posuere tellus, mattis feugiat ipsum enim sed neque.Etiam ut dui ante. Ut ullamcorper nisi sit amet tortor porta vestibulum. Nulla sed ornare libero. Vestibulum lobortis laoreet semper. Ut volutpat consectetur ligula nec accumsan. Nulla sed nulla sit amet tellus maximus ornare at et ante. Mauris nec aliquet massa, et fermentum ligula. Suspendisse potenti. Sed lacinia, ex in tempus suscipit, neque quam mattis sem, at sagittis felis leo vitae est.Sed sagittis ac felis eget malesuada. Mauris posuere, enim nec porttitor congue, ex risus laoreet odio, lacinia laoreet neque neque vitae purus. Morbi pulvinar arcu et diam aliquam ultricies. Praesent iaculis lorem et euismod convallis. Praesent eros quam, maximus id felis quis, consequat dapibus ligula. Suspendisse at sapien dui. Curabitur porttitor at metus sed cursus. Nullam at urna enim. Cras luctus mi a egestas gravida. Cras id arcu consectetur, auctor odio nec, hendrerit leo. Suspendisse quis vulputate urna, ac euismod massa. Quisque mollis ligula nec felis mollis faucibus mattis et sem.Ut eu metus vitae lorem ullamcorper accumsan. Donec lobortis lorem id tincidunt sagittis. Nulla vitae nunc nec dolor ornare aliquam. Quisque sed finibus nunc. Integer libero magna, ullamcorper eget feugiat id, rutrum eu dolor. In blandit nisl vitae augue rutrum, ut blandit tortor rhoncus. Praesent pellentesque hendrerit ullamcorper. Nam eget consectetur elit. Curabitur mattis fringilla fringilla. Etiam eget leo mauris. Aenean sollicitudin, risus vel porta vestibulum, lorem magna rhoncus augue, sed luctus leo mi id dolor. Morbi fringilla magna sed nunc finibus fringilla. Nunc varius nisl eu vestibulum elementum. Donec mollis massa a mollis cursus. Sed justo sem, placerat feugiat neque quis, iaculis volutpat purus. Donec lacinia felis bibendum, dapibus massa nec, aliquam eros.Pellentesque posuere ornare odio nec vulputate. Etiam massa nunc, sagittis nec vulputate pharetra, porttitor in lectus. Donec quis facilisis nunc. Nunc consequat justo odio, ut tempor diam rutrum ut. Sed facilisis porttitor odio eu blandit. Mauris posuere tincidunt felis. Quisque vestibulum vulputate felis, vitae hendrerit augue lacinia vel. Integer molestie leo at nibh porttitor auctor. In volutpat est sed ligula viverra tristique ut vel nisl. Morbi ac interdum dui. Phasellus scelerisque quam et nulla mollis, at auctor dolor posuere. Aenean consequat eleifend velit quis cursus. Morbi a nisi porta nunc feugiat ornare vitae eget lectus. Donec laoreet venenatis nisi.Proin ac lorem sit amet urna bibendum varius eu non urna. Donec sit amet eleifend diam. Suspendisse consectetur risus eget ex tristique, viverra convallis enim condimentum. Donec in sollicitudin elit. Phasellus sed ligula mattis, rhoncus justo at, congue mi. Phasellus quis nulla ante. Nulla non dolor eu libero feugiat tempor. Curabitur varius lacinia porta.Ut in mauris porttitor, dapibus magna et, luctus leo. Integer auctor malesuada ex laoreet ullamcorper. Phasellus quis ullamcorper massa. Maecenas id ullamcorper nisi, non tempor ipsum. Nulla facilisi. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Mauris sit amet blandit risus. Quisque fermentum mattis tortor ut finibus. Suspendisse porttitor consectetur metus, vel tincidunt nulla condimentum a. Suspendisse eu nisl in mauris aliquet aliquam. Vestibulum posuere tempus risus, non ornare urna porttitor in. Nunc mattis id felis eget ornare. Donec et sapien elit. Aliquam gravida fringilla volutpat. Sed cursus odio sed mauris lobortis tristique. Quisque id ex et justo vulputate tempor vitae ac est.Nunc at eros tristique, vestibulum dui et, mattis risus. In non egestas nulla, vitae gravida lacus. Cras pellentesque orci in velit molestie auctor. Mauris dictum velit quis nibh consequat, et volutpat augue tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam viverra, mauris id fermentum fringilla nisi."


    
###################
# HASH FUCTION 

def getHash(istr):

    if(not hash_selector):
        
        to_hash = bytes(istr,'utf-8')
        res = hex(zlib.crc32(to_hash) & 0xffffffff)
        
    else:
            
        hashObject = hashlib.new(hashAlgorithms[hash_selector], istr.encode('utf-8'))
        res = '0x'+hashObject.hexdigest()
        
    res = bin(int(res, 16))[2:]
    res = res.zfill(hash_bits)
    if(hash_bits > len(res)):
        return res[ 0: len(res): 1]
    return res[ 0: hash_bits: 1]

# Message mutator fuction
def mutateString(originalStr):
    istr = list(originalStr)
    
    rChars = random.randint(1,40)
    variationsArray=list()
    while (rChars > 0 ):
        rChars -= 1
        rNum = random.randint(0,len(istr)-1)
        
    
        if(istr[rNum]  in lettersSet):
            istr[rNum] = letters[random.randrange(len(letters))]  ##To random from lowercase and uppercase characters
        else:
            if(istr[rNum] in symb):
                istr[rNum] = symb[random.randrange(len(symb))]
            else:
                if(istr[rNum] in numsString):
                    istr[rNum] = numsString[random.randrange(len(numsString))]
        variationsArray.append((rNum, istr[rNum]))
    
    istr = "".join(istr)
    #istr = ""
    return (istr,variationsArray)


# Evil X mutator fuction
def mutateX(originalStr):
    istr = list(originalStr)
    
    rChars = random.randint(1,40)
    variationsArray=list()
    while (rChars > 0 ):
        rChars -= 1
        rNum = random.randint(0,len(istr)-1)
        
    
        if(istr[rNum]  in lettersSet):
            istr[rNum] = letters[random.randrange(len(letters))]  ##To random from lowercase and uppercase characters
        else:
            if(istr[rNum] in symb):
                istr[rNum] = symb[random.randrange(len(symb))]
            else:
                if(istr[rNum] in numsString):
                    istr[rNum] = numsString[random.randrange(len(numsString))]
        variationsArray.append((rNum, istr[rNum]))
    
    istr = "".join(istr)
    #istr = ""
    return (istr,variationsArray)

# Function that creates M dictionary
def createMs(originalString):
    dictionary = dict([])
    originalHash = getHash(originalString)
    dictionary[originalHash] = originalString
    it_total = 1
    it_created = 1
    while (it_created < number_of_Ms):
        it_total+=1
        istr,variations = mutateString(originalString)
        hss = getHash(istr)
        #print(hss)
        if(hss not in dictionary):
            dictionary[hss] = variations
            it_created +=1
            
    return dictionary


if(len(sys.argv) > 1 and int(sys.argv[1])>=0 and int(sys.argv[1]) < len(hashAlgorithms)):
    hash_selector = int(sys.argv[1])
    if(len(sys.argv) > 2 and int(sys.argv[2]) > 0 ):
        hash_bits= int(sys.argv[2])
        number_of_Ms = 2**(hash_bits/2)
    else:
        print(f"INVALID HASH BITS SETTINGS FROM CLI ARGUMENTS.")
        exit(0)
else:
    print(f"ERROR. ARGUMENT [Hash algorithm] NOT VALID")
    exit(0)


print(f"Hash algorithm selected: {hashAlgorithms[int(hash_selector)]}\nUsing {hash_bits} first bits from hash values.")
startTime = time.time()

MDictionary = createMs(M)

GenTotalTime = time.time() - startTime
print(f"Took {GenTotalTime} seconds.")
print(f"Dictionary size: {sys.getsizeof(MDictionary)} bytes ({round(sys.getsizeof(MDictionary) /(1024**2), 4)} MB)")
print(f"Starting hash collision finder...")
print(f"Original evil message (X): \n\t{X[0:80]}...")
EvilIterations = 0
Xi = X
variationsX = list()
## Until collision or it > MAX, check collision and mutate Evil X 
while( ( collision == False ) and EvilIterations < Max_iterations_for_collision):
    
    XHash = getHash(Xi)
    ## If Collision, exit. Else mutate Evil X
    if( XHash in MDictionary ):
        collision = True
    else:
        Xi,variationsX = mutateX(X)
    
    EvilIterations+=1

totalElapsedTime =  time.time() - startTime
searchTime = totalElapsedTime - GenTotalTime
print("==================================================\tEND\t==================================================")
## Posting results
if(collision):
    
    print(f"Collision detected for X variation: \n\t{variationsX}")
    print(f"Took {EvilIterations} iterations. ({searchTime} seconds to search).")
    print(f"Total elapsed time: {totalElapsedTime} seconds.")
    print(f"XHash:\t{XHash}")
    print(f"XHash(Hex):\t{hex(int(XHash,base=2))}")
    print(f"XHash(int):\t{int(XHash,base=2)}")
    
    print(f"Password variation collision from Dictionary:\n\t{MDictionary[XHash]}")
else:
    print(f"No collision detected after {EvilIterations} iterations.")

