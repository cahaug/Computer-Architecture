

"""CPU functionality."""

import sys

# OP CODES
HLT = 0b00000001  # Halt function, if HLT is encountered running = False
LDI = 0b10000010  # SAVE function
PRN = 0b01000111  # PRINT function
MUL = 0b10100010  # MULTIPLY function
PUSH = 0b01000101  # PUSH function -- add the value from the given register to the stack
POP = 0b01000110 # POP function -- pop the value from the top of the stack to the given register
CALL = 0b01010000  # CALL function
RET = 0b00010001  # RET function
ADD = 0b10100000  # ADD function


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # initialize RAM of 256
        self.ram = [0] * 256
        # program counter
        self.pc = 0
        # 8-bit registry
        self.reg = [0] * 8
        # start our stack pointer at register memory end -1
        self.SP = 7
        # store the SP in the registry at the end of memory -1
        self.reg[self.SP] = len(self.ram)-1
        # create our branchtable (beautify, remove if elses by calling directly)
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_halt
        self.branchtable[LDI] = self.handle_save
        self.branchtable[PRN] = self.handle_print
        self.branchtable[ADD] = self.handle_add
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[POP] = self.pop_method
        self.branchtable[PUSH] = self.push_method
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret

    # HLT - Halt
    def handle_halt(self, operand_a, operand_b):
        self.running = False
        self.pc +=1

    # LDI: save the value into the register
    def handle_save(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    # PRN: print the value from register
    def handle_print(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    # ADD: get the sum of the two register values
    def handle_add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    # MUL: get the product of the two register values
    def handle_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    # POP
    def pop_method(self, operand_a, operand_b):
        # POP value of stack at location SP
        value = self.ram_read(self.reg[self.SP])
        # store the value in register given
        self.reg[operand_a] = value
        # increment the Stack Pointer (SP)
        self.reg[self.SP] += 1
        self.pc += 2
    
    # PUSH
    def push_method(self, operand_a, operand_b):
        # decrement the Stack Pointer (SP)
        self.reg[self.SP] -= 1
        # read the next value for register location
        register_value = self.reg[operand_a]
        # take the value in that register and add to stack
        self.ram_write(self.reg[self.SP], register_value)
        self.pc += 2
    
    # CALL
    def handle_call(self):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.pc + 2
        reg = self.ram[self.pc + 1]
        reg_value = self.reg[reg]
        self.pc = reg_value

    # RET
    def handle_ret(self):
        return_value = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc = return_value



    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        return 0b00000001 #true for ram successfully written

    def load(self):
        """Load a program into memory."""
        address = 0
        arguments = sys.argv
        if len(arguments) < 2:
            print('Need proper filename passed')
            sys.exit(1)
        filename = arguments[1]
        with open(filename) as f:
            for line in f:
                comment_split = line.split('#')
                if comment_split[0] == '' or comment_split[0] == '\n':
                    continue
                command = comment_split[0].strip()
                # print(command, int(command, 2))
                self.ram_write(int(command, 2), address)
                address += 1

        # address = 0

        # # if there is a system variable
        # if len(sys.argv) > 1:
        #     # load the file at the address
        #     program_file = sys.argv[1]
        #     # read file 
        #     program = open(program_file, "r")

        #     # for each instruction
        #     for line in program:
        #         # remove extra stuff
        #         line = line.split('#',1)[0].strip()
        #         # add the line to ram
        #         self.ram[address] = int(f'0b{line}', 2)
        #         # increment address variable to run next loop
        #         address += 1

        # # otherwise, demo the default program
        # else:
        #     program = [
        #         # From print8.ls8
        #         0b10000010, # LDI R0,8
        #         0b00000000,
        #         0b00001000,
        #         0b01000111, # PRN R0
        #         0b00000000,
        #         0b00000001, # HLT
        #     ]

        #     for instruction in program:
        #         self.ram[address] = instruction
        #         address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        #implement math functions
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # start the program
        IR = None

        self.running = True

        while self.running:
            self.trace()
            # Add our instruction to the instruction register from ram
            IR = self.ram[self.pc]
            # Extract the command
            COMMAND = IR
            # print(COMMAND)

            # Execution Loop #
            if COMMAND in self.branchtable:
                self.branchtable[COMMAND]()
            else:
                # error message
                print(f'Unknown instruction, {COMMAND}')
                # crash
                sys.exit(1)
