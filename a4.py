import math

def func1(s):
    sin = s.split()
    if sin[1][-1] == 'B' :
        p2 = 3
    elif sin[1][-1] == 'b'  :
        p2 = 0 

    if sin[1][-2] == 'k' :
        p1 = 10
    elif sin[1][-2] == 'M' :
        p1 = 20 
    elif sin[1][-2] == 'G' : 
        p1 = 30

    t = int(sin[0])
    n = 0
    while t!=1 :
        t = t/2 
        n = n+1

    arr = [n,p1,p2]
    return arr

def func2(x):
    n = 0 
    t = x 
    while(t!=1):
        t = t/2 
        n = n+1 
    return n  

space = str(input()) # space in memory ; Mb - mega bits ; MB - mega bytes 

spower = func1(space)

memty = str(input("Enter memory address type : "))
memty_arr = memty.split()
'''
1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size (depends on CPU)
'''

li = int(input("Lenght of one instruction in bits - ")) # lenght of instruction 
rl = int(input("Length of register ")) # length of register 

ins = li*(2**(spower[1]+spower[2]))
insf = int(math.log(ins,2))

if(rl>=insf):
    print("Error:Cant support any register")
    exit()

elif(insf-rl>=6):
    opcode=5
    pbit=insf-rl-opcode

elif(insf-rl>=4 and insf-rl<=5):
    opcode=3
    pbit=insf-rl-opcode


# if memty_arr[0] == "Bit" :
#     padd = 1 
# elif memty_arr[0] == "Nibble" :
#     padd = 4 
# elif memty_arr[0] == "Byte" :
#     padd = 8
# elif memty_arr[0] == "Word" :
#     padd = int(input("Enter CPU Size - "))
# # elif memty == "Word Addressable Memory"
# #
# #
# #

print("QUERY 1 ------------")
#TYPE A
print("\nType-A opcode bits: ",opcode)
print("Type-A P-bit address bits: ",pbit)
print("Type-A reg address bits: ",rl)
print("No of instructions Type-A ISA supports: ",2**opcode)
print("No of registers Type-A ISA supports: ",2**rl)

print()

if(2*rl>=insf):
    print("Error:Cant support any register")
    exit()

elif(insf-2*rl>=6):
    opcode_b=5
    r_bit=insf-2*rl-opcode_b

elif(insf-2*rl>=4 and insf-2*rl<=5):
    opcode_b=3
    r_bit=insf-2*rl-opcode_b


#TYPE B
print("\nType-B opcode bits: ",opcode_b)
print("Type-B R-bit filler bits: ",r_bit)
print("Type-B reg address bits: ",2*rl)
print("No of instructions Type-B ISA supports: ",2**opcode_b)
print("No of registers Type-B ISA supports: ",2**rl)


print("QUERY 2 ------------")
tyq2 = int(input("Enter type of query 2 (1 or 2) - "))

if tyq2 == 1 :
    cbits = int(input("CPU bits = "))
    new = str(input("New type = "))

    #cbits_pow = func2(cbits)

    adpin1 = (spower[0] + spower[1] + spower[2]) - func2(padd)

    adpin2 = ((spower[0] + spower[1] + spower[2])) - func2(cbits)

    print("Address pins saved/required = " , adpin2 - adpin1)

elif tyq2 == 2 :
    cbits = int(input("CPU bits = "))
    naddpins = int(input("No. of address pins = "))
    memtype = str(input("Type of memory - "))

    memtype_arr = memtype.split()

    if memtype_arr[0] == "Bit" :
        x = 0 
    elif memtype_arr[0] == "Nibble" :
        x = 2    
    elif memtype_arr[0] == "Byte" :
        x = 3
    elif memty_arr[0] == "Word" : 
        x = cbits 
    
    ans = naddpins + func2(cbits) - 3 

    if ans > 30 : 
        val = 2**(ans - 30) 
        print(str(val) + " " + "GB")
    elif ans >20 :
        val = 2**(ans - 20)
        print(str(val) + " " + "MB")
    else :
        val = 2**(ans - 10)
        print(str(val) + " " + "KB")
