# Function to convert decimal to binary
def deci_binary(x1):
    x1 = int(x1)
    b = 0
    l = ""
    while x1 != 0:
        b = int(x1)%2 
        l += str(b)
        x1 = x1 // 2 
    l = l[::-1]  # l.reverse()
    bin = (8 - len(l)) * '0' + l  #makes sure the returned binary no. has 8 bits
    return  bin 


# Dictionary containg instructions and their opcode 
opcodeTable = { 
                "add": "10000",
                "sub": "10001",
                "mov": ["10010", "10011"],      #immediate and register cases respectively
                "ld" : "10100",
                "st" : "10101",
                "mul": "10110",
                "div": "10111",
                "rs" : "11000",
                "ls" : "11001",
                "xor": "11010",
                "or" : "11011",
                "and": "11100",
                "not": "11101",
                "cmp": "11110",
                "jmp": "11111",
                "jlt": "01100",
                "jgt": "01101",
                "je" : "01111",
                "hlt": "01010"
            }

# Dictionary contiaing register name and their binary  representation
reg = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110" , "FLAGS":"111"}


# Dictionary that contains the category of each instruction
ins_type = {
            "add": "A",
            "sub": "A",
            "xor": "A",
            "or" : "A",
            "mul": "A",
            "and": "A",

            "mov": ["C","B"], #immediate and register cases respectively
            "rs" : "B",
            "ls" : "B",

            "div": "C",
            "not": "C",
            "cmp": "C",

            "ld" : "D",
            "st" : "D",
            

            "jmp": "E",
            "jlt": "E",
            "jgt": "E",
            "je" : "E",

            "hlt": "F"

            }

#dictionary that contains the category of the instruction and respective unused bits
unused_bits = {
    "A" : 2 , 
    "B" : 0 , 
    "C" : 5 , 
    "D" : 0 , 
    "E" : 3 , 
    "F" : 11 
}

