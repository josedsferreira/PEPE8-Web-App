

def strHexToBin(strHex, num_bits=8):
    return bin(int(strHex, 16))[2:].zfill(num_bits)

def strDecToBin(strDec, num_bits=8):
    return bin(int(strDec))[2:].zfill(num_bits)

def decToBin_2complement(decimal_number, num_bits=8):
    if decimal_number >= 0:
        binary_string = bin(decimal_number)[2:].zfill(num_bits)
    else:
        binary_string = bin(2**num_bits + decimal_number)[2:]

    return binary_string

class assembler: 
    def __init__(self, assembly_program="assembly_program.txt"):
        print("Assembler starting...")

        self.instructionMap = {
            "LD": ["00000000", "00000001"],
            "ST": ["00001111", "00000010"],
            "ADD": ["00000011", "00000100"],
            "SUB": ["00000101", "00000110"],
            "AND": ["00000111", "00001000"],
            "OR": ["00001001", "00001010"],
            "JMP": ["00001011", "00001111"],
            "JZ": ["00001100", "00001111"],
            "JN": ["00001101", "00001111"],
            "NOP": ["00001110", "00001110"]
        } #instruction followed by opcode for direct addressing and opcode for indirect addressing
        self.symbolTable = {}
        self.lineAddressMap = {}
        self.startFound = False

        with open(assembly_program, 'r') as in_file, open("processed_program.txt", 'w') as out_file:

            """
            Preliminary Pass
            Tasks:
            Remove comments and empty lines
            """
            print("Preliminary Pass")

            for line in in_file:
                line = line.strip()
                if not line:
                    continue
                uncommentedLine = line.split(';')[0].strip()
                out_file.write(uncommentedLine.upper() + "\n")

        with open("processed_program.txt", 'r') as in_file, open("temp.txt", 'w') as out_file:
                
            """
            First Pass
            Tasks:
            Find all labels and exchange them for their values in the symbol table, 
            Build symbol table
            Remove comments
            """
            print("First Pass")

            lineCount = 0
            for line in in_file:
                line = line.strip()
                if not line:
                    continue

                if ":" in line:
                        label, instruction, operand = map(str.strip, line.split(None, 2))

                elif "EQU" in line:
                    label, instruction, operand = map(str.strip, line.split(None, 2))
                    self.symbolTable[label] = operand

                else: 
                    label = ""
                    instruction, operand = map(str.strip, line.split(None, 1))

                if label == "START:" or label == "INICIO:" or self.startFound:
                            
                    if label == "START:" or label == "INICIO:":
                        self.startFound = True
                    
                    lineCount += 1

                    if operand.startswith('[') and operand.endswith(']') and operand[1:-1] in self.symbolTable:
                        operand = self.symbolTable[operand[1:-1]]
                        operand = "[" + operand + "]"

                    elif operand in self.symbolTable:
                        operand = self.symbolTable[operand]

                    if len(instruction) == 0 or len(operand) == 0:
                        continue

                    if ":" in line:
                        self.lineAddressMap[label[:-1]] = str(lineCount)

                    newLine = instruction + " " + operand + "\n"
                    out_file.write(newLine)

        with open("temp.txt", 'r') as in_file, open("processed_program.txt", 'w') as out_file:

            """
                Second Pass
                Tasks:
                Substitute line adresses in JMP operands for the actual addresses
            """

            print("Second Pass")

            for line in in_file:
                line = line.strip()
                if not line:
                    continue
                instruction, operand = map(str.strip, line.split(None, 1))
                if operand in self.lineAddressMap:
                    operand = self.lineAddressMap[operand]
                newLine = instruction + " " + operand + "\n"
                out_file.write(newLine)

            print("Pre processing complete")

        with open("processed_program.txt", 'r') as in_file, open("machine_code.txt", 'w') as out_file:
                
                """
                    Third Pass - Final assembling
                    Tasks:
                    Convert assembly instructions to machine code
                """
    
                print("Assembling...")
    
                for line in in_file:
                    line = line.strip()

                    if not line:
                        continue

                    instruction, operand = map(str.strip, line.split(None, 1))

                    if operand.startswith('[') and operand.endswith(']'):
                        operand = operand[1:-1]
                        instruction = self.instructionMap[instruction][1]
                    else:
                        instruction = self.instructionMap[instruction][0]

                    if operand.endswith('H'):
                        operand = operand[:-1]
                        operand = strHexToBin(operand)
                    else:
                        operand = strDecToBin(operand)

                    newLine = instruction + operand + "\n"
                    out_file.write(newLine)
    
                print("Processing complete")
                