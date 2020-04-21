"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.instructions = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
            0b10100010: self.mul,
        }

    def prn(self, op1, op2):
        print(self.reg[op1])
        return (2, True)
    
    def hlt(self, op1, op2):
        return (0, False)
    
    def ldi(self, op1, op2):
        self.reg[op1] = op2
        return (3, True)

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value

    def mul(self, reg_a, reg_b):
        self.alu('MUL', reg_a, reg_b)
        return (3, True)

    def load(self):
        """Load a program into memory."""

        address = 0

        file_name = sys.argv[1]

        with open(file_name) as f:
            for line in f:
                line_string = line.split('#')[0].strip()
                if line_string == '':
                    continue
                inst = int(line_string, 2)
                
                self.ram[address] = inst
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
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
        # Load instruction
        running = True

        pc = 0
        
        while running:
            instruction = self.ram[pc]
            op1 = self.ram_read(pc+1)
            op2 = self.ram_read(pc+2)

            try:
                action = self.instructions[instruction](op1, op2)
                pc += action[0]
                running = action[1]
            except KeyError:
                print(f'Error: {instruction} not recognized')
                running = False