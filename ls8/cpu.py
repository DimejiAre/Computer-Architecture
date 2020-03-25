"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = []

        if len(sys.argv) != 2:
            print("usage: 03-fileio02.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split('#')[0].strip()

                    if num == '':
                        continue

                    value = int(num, 2)
                    program.append(value)

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):

        # LDI = self.LDI
        # PRN = self.PRN
        # MUL = self.MUL
        # HLT = self.HLT
        # ram_read = self.ram_read
        # alu = self.alu
        # reg = self.reg

        # class Dispatch:

        #     def __init__(self):
        #         # Set up the branch table
        #         self.branchtable = {}
        #         self.branchtable[LDI] = self.handle_ldi
        #         self.branchtable[PRN] = self.handle_prn
        #         self.branchtable[MUL] = self.handle_mul
        #         self.branchtable[HLT] = self.handle_hlt
        #         self.pc = 0

        #     def handle_ldi(self):
        #         operand_a = ram_read(self.pc + 1)
        #         operand_b = ram_read(self.pc + 2)
        #         reg[operand_a] = operand_b
        #         inc_size = (LDI >> 6) + 1
        #         self.pc += inc_size

        #     def handle_prn(self):
        #         operand_a = ram_read(self.pc + 1)
        #         print(reg[operand_a])
        #         inc_size = (PRN >> 6) + 1
        #         self.pc += inc_size

        #     def handle_mul(self):
        #         operand_a = ram_read(self.pc + 1)
        #         operand_b = ram_read(self.pc + 2)
        #         alu('MUL', operand_a, operand_b)
        #         inc_size = (MUL >> 6) + 1
        #         self.pc += inc_size

        #     def handle_hlt(self):
        #         sys.exit(1)

        #     def run(self):
        #         #calls into the branch table
        #         ir = LDI
        #         self.branchtable[ir]()

        #         ir = LDI
        #         self.branchtable[ir]()

        #         ir = MUL
        #         self.branchtable[ir]()

        #         ir = PRN
        #         self.branchtable[ir]()

        #         ir = HLT
        #         self.branchtable[ir]()

        # c = Dispatch()
        # c.run()

        """Run the CPU."""
        running = True
        inc_size = 0
        self.pc = 0
        sp = 7

        while running:
            IR = self.ram[self.pc]

            if IR == self.LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                inc_size = (self.LDI >> 6) + 1
            
            elif IR == self.PRN:
                operand_a = self.ram_read(self.pc + 1)
                print(self.reg[operand_a])
                inc_size = (self.PRN >> 6) + 1

            elif IR == self.MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu('MUL', operand_a, operand_b)
                inc_size = (self.MUL >> 6) + 1

            elif IR == self.PUSH:
                register = self.ram_read(self.pc + 1)
                val = self.reg[register]

                self.reg[sp] -= 1
                self.ram_write(self.reg[sp], val)
                inc_size = (self.PUSH >> 6) + 1

            elif IR == self.POP:
                register = self.ram_read(self.pc + 1)
                val = self.ram_read(self.reg[sp])

                self.reg[register] = val
                self.reg[sp] += 1
                inc_size = (self.POP >> 6) + 1

            
            elif IR == self.HLT:
                running = False

            else:
                print("Invalid Instruction")
                running = False

            self.pc += inc_size
