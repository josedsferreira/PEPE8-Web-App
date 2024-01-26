import array

class pepe8: 
    def __init__(self):
        self.PC = 0 #Program Counter
        self.A = 0b00000000 #Accumulator
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000000
        self.ESCR_A = False
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False

        self.haltFlag = False

        self.instructions = [] #Instruction memory with 16 bits for each instruction and operand
        self.data = [0b00000000] * 255 #Data memory with 255 positions (FF in hex)
        self.program = [] #Program in assembly strings for interface


    def clock(self):
        if self.PC < self.instructions.length:
            line = self.instructions[self.PC]
        else:
            print("Out of program")
            self.haltFlag = True
            return

        self.PC += 1
        instruction = int(line[:8])
        operand = int(line[8:])

        match instruction:
            case 0:
                self.LD(operand)
            case 1:
                self.LD_m(operand)
            case 2:
                self.ST(operand)
            case 3:
                self.ADD(operand)
            case 4:
                self.ADD_m(operand)
            case 5:
                self.SUB(operand)
            case 6:
                self.SUB_m(operand)
            case 7:
                self.AND(operand)
            case 8:
                self.AND_m(operand)
            case 9:
                self.OR(operand)
            case 10:
                self.OR_m(operand)
            case 11 if operand == self.PC:
                print("HALT - Program execution completed!")
                self.haltFlag = True
            case 11:
                self.JMP(operand)
            case 12:
                self.JZ(operand)
            case 13:
                self.JN(operand)
            case 14:
                # NOP no operation
                pass


    def loadProgram(self, assembly_program = "assembly_program.txt", machine_code = "machine_code.txt"):
        
        with open(assembly_program, 'r') as in_file:
            for line in in_file:
                line = line.strip()
                if not line:
                    continue
                self.program.append(line)

    def reset(self):
        self.PC = 0b00000000
        self.A = 0b00000000
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000000
        self.ESCR_A = False
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False
        self.haltFlag = False

    #Instruction set
    def LD(self, operand):
        self.A = operand
        self.SEL_PC = 0b00000000
        #self.SEL_ALU = 0b00000000 #No ALU operation
        self.ESCR_A = True
        self.SEL_A = True
        self.SEL_B = False
        self.WR = False

    def LD_m(self, operand):
        self.A = self.data[operand]
        self.SEL_PC = 0b00000000
        #self.SEL_ALU = 0b00000000 #No ALU operation
        self.ESCR_A = True
        self.SEL_A = True
        self.SEL_B = True
        self.WR = False

    def ST(self, operand):
        self.data[operand] = self.A
        self.SEL_PC = 0b00000000
        #self.SEL_ALU = 0b00000000 #No ALU operation
        self.ESCR_A = False
        #self.SEL_A = True #no effect
        #self.SEL_B = True
        self.WR = True

    def ADD(self, operand):
        self.A += operand
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000000 #add
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False
    
    def ADD_m(self, operand):
        self.A += self.data[operand]
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000000 #add
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = True
        self.WR = False

    def SUB(self, operand):
        self.A -= operand
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000001 #sub
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False

    def SUB_m(self, operand):
        self.A -= self.data[operand]
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000001 #add
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = True
        self.WR = False

    def AND(self, operand):
        self.A &= operand
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000010 #and
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False

    def AND_m(self, operand):
        self.A &= self.data[operand]
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000010 #and
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = True
        self.WR = False

    def OR(self, operand):
        self.A |= operand
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000011 #or
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False

    def OR_m(self, operand):
        self.A |= operand
        self.SEL_PC = 0b00000000
        self.SEL_ALU = 0b00000011 #or
        self.ESCR_A = True
        self.SEL_A = False
        self.SEL_B = False
        self.WR = False

    def JMP(self, operand):
        self.PC = operand - 1 #minus one because the clock will increment it back
        self.SEL_PC = 0b00000001
        #self.SEL_ALU = 0b00000000 #No ALU operation
        self.ESCR_A = False
        #self.SEL_A = False
        #self.SEL_B = False
        self.WR = False

    def JZ(self, operand):
        if self.A == 0:
            self.PC = operand - 1 #minus one because the clock will increment it back
        self.SEL_PC = 0b00000010
        #self.SEL_ALU = 0b00000000 #No ALU operation
        self.ESCR_A = False
        #self.SEL_A = False
        #self.SEL_B = False
        self.WR = False

    def JN(self, operand):
        if self.A < 0:
            self.PC = operand - 1 #minus one because the clock will increment it back
        self.SEL_PC = 0b00000011
        #self.SEL_ALU = 0b00000000 #No ALU operation
        self.ESCR_A = False
        #self.SEL_A = False
        #self.SEL_B = False
        self.WR = False

