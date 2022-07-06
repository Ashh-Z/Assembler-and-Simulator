from helper import*
import sys 

def compile_instruction(list,i): ## list is the ith instruction
    s="" 
    ins = list[0]  # instruction type, eg: add,sub etc
    opc = opcodeTable[ins] # opc gets the opcode of the ins 
    type = ins_type[ins] # type gets the category of the instruction, eg: A,B,C etc
    
    if ins == "mov": # if ins is mov then it can be mov reg or mov imm, 
        if '$' in list[2]:
            type = ins_type[ins][1]
            opc = opc[0]
        else :
            type = ins_type[ins][0]
            opc = opc[1]
              
    u_bits = unused_bits[type]

    # if type == 'D':
    #     key = list[2]

    # add,sub,mul,xor,or,and require 3 registers 
    if(type == 'A'):
        if len(list)==4:
            if list[1] in reg and list[2] in reg and list[3] in reg and list[1]!="FLAGS" and list[2]!="FLAGS" and list[3]!="FLAGS":
                s=str( opc + u_bits*'0' + reg[list[1]] + reg[list[2]] + reg[list[3]])
            else:
                if(list[1]=="FLAGS" or list[2]=="FLAGS" or list[3]=="FLAGS" ):
                    print("ERROR--misuse of flag : At line " , i+1 )
                    quit()  ## Ends the program
                else:
                    print("ERROR--typo in register name : At line " , i+1 )
                    quit() ; ## Ends the program
        else:
            print("general syntax ERROR : At line " , i+1 )
            quit()

    elif(type == 'B') :
        if len(list)==3:
            if list[1] in reg  and 0<=float(list[2][1:])<=255 and float(list[2][1:])%1==0 and list[1]!="FLAGS":
                s=str(opc + u_bits*'0' + reg[list[1]] + deci_binary(list[2][1:]) ) ## eg: $Imm = $100 is selected , the we slice the string
            else:
                if(list[1]=="FLAGS"):
                    print("ERROR--misuse of flag : At line " , i+1 )
                    quit()  ## Ends the program

                elif 0>float(list[2][1:]) or float(list[2][1:])>255 or float(list[2][1:])%1!=0:
                    print("ERROR--illegal immediate value : At line " , i+1 )
                    quit()  ## Ends the program

                else:
                    print("ERROR--typo in register name : At line " , i+1 )
                    quit()  ## Ends the program
        else:
            print("general syntax ERROR : At line " , i+1 )
            quit()  ## Ends the program

    elif(type == 'C') :
        if len(list)==3:
            #if list[1] in reg and list[2] in reg and list[1]!="FLAGS" and(list[2]!="FLAGS" or list[0]=="mov"):
            if (list[1] in reg and list[2] in reg and list[2]!= "FLAGS") :
                s=str(opc + u_bits*'0' + reg[list[1]] + reg[list[2]] )

            else:
                #if(list[1]=="FLAGS" or list[2]=="FLAGS"):
                if(list[2]=="FLAGS"):
                    print("ERROR--misuse of flag : At line " , i+1 )
                    quit()  ## Ends the program

                else:
                    print("ERROR--typo in register name : At line " , i+1 )
                    quit()  ## Ends the program

        else:
            print("general syntax ERROR : At line " , i+1 )
            quit()  ## Ends the program

    elif(type == 'D') :
        if len(list)==3:
            if list[1] in reg and list[2] in d_var and list[1]!="FLAGS":
                s=str(opc + u_bits*'0' + reg[list[1]] + deci_binary(d_var[list[2]]) )#also need to add variable
            
            else:
                if(list[1]=="FLAGS"):
                    print("ERROR--misuse of flag : At line " , i+1 )
                    quit()  ## Ends the program

                elif list[2] in d_label:
                    print("ERROR--misuse of labels as variables : At line " , i+1 )
                    quit()  ## Ends the program

                elif list[2] not in d_var:
                    print("ERROR--use of undefined variables : At line " , i+1 )
                    quit()  ## Ends the program

                else:
                    print("ERROR--typo in register name : At line " , i+1 )
                    quit()  ## Ends the program

        else:
            print("general syntax ERROR : At line " , i+1 )
            quit()  ## Ends the program

    elif(type == 'E'):
        if len(list)==2:
            if list[1] in d_label:
                 s=str(opc + u_bits*'0' + deci_binary(d_label[list[1]]) )
            else:
                if list[1] in d_var:
                    print("ERROR--misuse of variables as labels : At line " , i+1 )
                    quit()  ## Ends the program

                elif list[1] not in d_label:
                    print("ERROR--use of undefined label : At line " , i+1 )
                    quit()  ## Ends the program

                else:
                    pass
        else:
            print("general syntax ERROR : At line " , i+1 )
            quit()  ## Ends the program

    elif(type == 'F'):
        if(i==len(l_instruction)-1):
            s=str(opc + u_bits*'0' )
        else:
            print("ERROR--hlt not being used as last instruction : At line " , i+1 )
            quit()  ## Ends the program
    else :
        print("general syntax ERROR : At line " , i+1 )
        quit()  ## Ends the program
    return s

l_instruction = [] ## List containing lines that are to be written in machine code 
d_var=dict()
l_var_keys = []
d_label = dict() 

data=[i for i in sys.stdin.readlines()]
t = 0 

for i in data:
    l1=[ str(g.strip())for g in i.split()]
    if len(l1) != 0 :
        if (l1[0]=="var" and len(l_instruction) == 0):
            t = t + 1
            if len(l1) !=2:
                print("ERROR -- Syntax Error : At line ", t)
                quit()
                
            d_var[l1[1]]=0


        elif(l1[0]=="var" and len(l_instruction) != 0) :
            t = t + 1
            print("ERROR -- variable not declared at the begining : At line " , t)
            quit() ## Ends the program

        elif(l1[0] in opcodeTable) :
            l_instruction.append(l1) 
            t = t + 1
        
        elif(l1[0][-1]==":"): 
            #d_label[l1[0][:len(l1[0]-2):]] = len(l_instruction)
            d_label[l1[0][:-1]] = len(l_instruction)
            l_instruction.append(l1[1::])  
            t = t + 1 

        else : 
            print("ERROR --Typos in instruction name : At line " , t )
            quit() ## Ends the program
            t = t + 1  


hlt_count=l_instruction.count(["hlt"])
if(hlt_count==0):
    print("ERROR -- missing hlt instruction")
    quit() ## Ends the program

else:
    if(hlt_count>1):
        print("ERROR -- too many hlt instruction")
        quit() ## Ends the program
    else:
        l_out=[]
        c = len(l_instruction)
        
        for i in d_var : 
            d_var[i] = c  ##gives memory address to the variable stored in the dictionary
            c = c + 1 
    
        for i in range(len(l_instruction)) :  ## loop that executes for each instruction  
            l_out.append(compile_instruction(l_instruction[i],i))  ##sends the ith instruction for compilation and stores it in l_out
        
        #Error if max input length exceeds 256 
        for i in range(len(l_out)): ##prints the machine code
            if i>255:
                print("Max input exceeded")
                quit()

        for i in range(len(l_out)): ##prints the machine code
            print(l_out[i])



