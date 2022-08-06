import sys

def hello_bhai(l):
    s=""
    for i in l:
        s+=str(i)
    return s

rf=[ [0 for i in range(16)] for j in range(8)]
pc=0
stop=0
reg = {"000":0, "001":1, "010":2, "011":3, "100":4, "101":5, "110":6, "111":7}
l_instruction=[str(i.strip()) for i in sys.stdin]
while(256-len(l_instruction)):
    l_instruction.append("0000000000000000")
def xory(a,b):
    if (a==1 and b==0 ) or (a==0 and b==1 ):
        return 1
    elif (a==1 and b==1 ) or (a==0 and b==0 ):
        return 0
    else:
        print(f"error at xory")
        quit()
def deci_binary(x1): # Function to convert decimal to binary
    x1 = int(x1)
    b = 0
    l = ""
    while x1 != 0:
        b = int(x1)%2 
        l += str(b)
        x1 = x1 // 2 
    l = l[::-1]  # l.reverse()
    if len(l)<=8:
        bin = (8 - len(l)) * '0' + l  #makes sure the returned binary no. has 8 bits
    else:
        bin=l
    return  bin
# def deci_binary_1(x1): # Function to convert decimal to binary
#     x1 = int(x1)
#     b = 0
#     l = ""
#     while x1 != 0:
#         b = int(x1)%2 
#         l += str(b)
#         x1 = x1 // 2 
#     l = l[::-1]  # l.reverse()
#     if len(l)<=16:
#         bin = (16 - len(l)) * '0' + l  #makes sure the returned binary no. has 8 bits
#     return  bin
def bin_deci(x): # Function to convert binary to decimal
    pow = 0
    t = 0
    x2 = int(x)
    while x2!= 0:
        d = x2%10 
        t = t+ d*(2**pow)
        x2 = x2 // 10
        pow = pow + 1
    return(t)
def EE_execute(s,pc,rf,reg):
    global stop
    if s[:5]=="01010": #type F and hlt 
        stop=1
        return  pc+1
    elif s[:5]=="10011" or s[:5]=="10111" or s[:5]=="11101" or s[:5]=="11110": # type C
        r1,r2=reg[s[10:13]],reg[s[13:16]]
        if s[:5]=="10011": # mov(reg)
            for i in range(16):
                rf[r1][i]=rf[r2][i]
        elif s[:5]=="11101": # invert
            for i in range(16):
                rf[r1][i]=0 if rf[r2][i]==1 else 1
        elif s[:5]=="11110": # cmp
            a=bin_deci(hello_bhai(rf[r1]))
            b=bin_deci(hello_bhai(rf[r2]))
            if a<b:
                rf[7][13]=1
            elif a==b:
                rf[7][15]=1
            else:
                rf[7][14]=1
        else: # div
            a=bin_deci(hello_bhai(rf[r1]))
            b=bin_deci(hello_bhai(rf[r2]))
            if b!=0:
                c=deci_binary(int(a/b))
                co=0
                for i in range(16):
                    if i<8:
                        rf[0][i]=0
                    else:
                        rf[0][i]=c[co]
                        co+=1
                c=deci_binary(a%b)
                co=0
                for i in range(16):
                    if i<8:
                        rf[1][i]=0
                    else:
                        rf[1][i]=c[co]
                        co+=1
            else:
                print("\"Division by 0\" Error at pc ",end="")
                PC_dump(pc)
                quit()
        return pc+1 
    elif s[:5]=="10100" or s[:5]=="10101": # type D
        r1,val=reg[s[5:8]],bin_deci(s[8:16])
        if s[:5]=="10100": # ld
            rf[r1]=[int(i) for i in l_instruction[val]]
        else: #st
            l_instruction[val]=hello_bhai(rf[r1])
        return pc+1
    elif s[:5]=="11111" or s[:5]=="01100" or s[:5]=="01101" or s[:5]=="01111": # type E
        if s[:5]=="01111" and rf[7][15]==1: #je
            rf[7][15]=0
            return bin_deci(s[8:16])
        elif s[:5]=="01101" and rf[7][14]==1: #jgt
            rf[7][14]=0
            return bin_deci(s[8:16])
        elif s[:5]=="01100" and rf[7][13]==1: #jlt
            rf[7][13]=0
            return bin_deci(s[8:16])
        else: #jmp
            return bin_deci(s[8:16])
    elif s[:5]=="10000" or s[:5]=="10001" or s[:5]=="10110" or s[:5]=="11010" or s[:5]=="11011" or s[:5]=="11100": # type A
        r1,r2,r3=reg[s[7:10]],reg[s[10:13]],reg[s[13:16]]
        if s[:5]=="10000": # add
            ci=0
            for i in range(15,-1,-1):
                s=rf[r1][i]+rf[r2][i]+ci
                if s==3:
                    rf[r3][i]=1
                    ci=1
                elif s==2:
                    rf[r3][i]=0
                    ci=1
                elif s==1 or s==0:
                    ci=0
                    rf[r3][i]=s
                else:
                    print(f"error at {pc}")
                    quit()
            if ci==1:
                rf[7][12]=1
        elif s[:5]=="10001": # sub
            a=bin_deci(hello_bhai(rf[r1]))
            b=bin_deci(hello_bhai(rf[r2]))
            if b>a:
                rf[r3]=[0 for i in range(16)]
                rf[7][12]=1
            else:
                ci=0
                for i in range(15,-1,-1):
                    rf[r3][i]=xory(xory(rf[r1][i],rf[r2][i]),ci)
                    ci=(ci and (not xory(rf[r1][i],rf[r2][i]))) or (rf[r2][i] and (not rf[r1][i]))
                if ci==1:
                    rf[7][12]=1
        elif s[:5]=="11010": # xor
            for i in range(16):
                rf[r3][i]=xory(rf[r1][i],rf[r2][i])
        elif s[:5]=="11011": # or
            for i in range(16):
                rf[r3][i]=rf[r1][i] or rf[r2][i]
        elif s[:5]=="11100": # and
            for i in range(16):
                rf[r3][i]=rf[r1][i] and rf[r2][i]
        else: #mul
            a=bin_deci(hello_bhai(rf[r1]))
            b=bin_deci(hello_bhai(rf[r2]))
            c=deci_binary(a*b)
            for i in range(-1,-17,-1):
                rf[r3][i]=c[i]
            if len(c)>16:
                rf[7][12]=1
        return pc+1
    else: #type B
        r1,val=reg[s[5:8]],bin_deci(s[8:16])
        if s[:5]=="10010": # mov(imm)
            c=0
            for i in range(16):
                if i<8:
                    rf[r1][i]=0
                else:
                    rf[r1][i]=int(s[8+c])
                    c+=1
        elif s[:5]=="11000": # rs
            val=val%8
            while(val!=0):
                rf[r1].insert(0,0)
                r1.pop()
                val-=1
        elif s[:5]=="11001": # ls
            val=val%8
            while(val!=0):
                rf[r1].append(0)
                r1.pop(0)
                val-=1
        else:
            print("\"instruction not defined\" Error at pc ",end="")
            PC_dump(pc)
            quit()
        return pc+1
def PC_dump(pc):
    print(deci_binary(pc),end=' ')
def RF_dump(rf):
    print(hello_bhai(rf[0])+" "+hello_bhai(rf[1])+" "+hello_bhai(rf[2])+" "+hello_bhai(rf[3])+" "+hello_bhai(rf[4])+" "+hello_bhai(rf[5])+" "+hello_bhai(rf[6])+" "+hello_bhai(rf[7]))
def MEM_dump(l_instruction):
    for i in l_instruction:
        print(i)
while(stop==0):
    instruction=l_instruction[pc]
    new_pc=EE_execute(instruction,pc,rf,reg)
    PC_dump(pc)
    RF_dump(rf)
    pc=new_pc
    rf[7][12]=0
MEM_dump(l_instruction)