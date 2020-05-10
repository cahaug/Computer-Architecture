"""CPU functionality."""

import sys

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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        return 0b00000001 #true

    def load(self):
        """Load a program into memory."""

        address = 0

        # if there is a system variable
        if len(sys.argv) > 1:
            # load the file at the address
            program_file = sys.argv[1]
            # read file 
            program = open(program_file, "r")

            # for each instruction
            for line in program:
                # remove extra stuff
                line = line.split('#',1)[0].strip()
                # add the line to ram
                self.ram[address] = int(f'0b{line}', 2)
                # increment address variable to run next loop
                address += 1

        # otherwise, demo the default program
        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

            for instruction in program:
                self.ram[address] = instruction
                address += 1



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
        isRunning = True

        # instruction codes
        ldi = 0b10000010
        prn = 0b01000111
        hlt = 0b00000001
        mul = 0b10100010

        while isRunning:
            # load next instruction into instructions register
            ir = self.ram_read(self.pc)
            # cache next two instructions
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # if LDI Instruction: save the value into the register
            if ir == ldi:
                self.reg[operand_a] = operand_b
                self.pc += 3
            # if PRN Instruction: print the value from register
            elif ir == prn:
                print(self.reg[operand_a])
                self.pc += 2
            # if MUL Instruction: get the product of the two register values specified, save in the first
            elif ir == mul:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            # if HLT Instruction: halt the program
            elif ir == hlt:
                running = False
                self.pc += 1
            # if unrecognized command
            else:
                print(f'Unknown instruction register: {ir}')
                # system crash
                sys.exit(1)
