"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xf4
        self.sp = self.reg[7]
        self.instructions = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret,
            0b10100000: self.add
        }

    def call(self, op1, op2):
        self.sp -= 1
        self.ram[self.sp] = self.pc + 2
        self.pc = self.reg[op1]
        return (0, True)

    def ret(self, op1, op2):
        self.pc = self.ram[self.sp]
        return (0, True)
        
    def push(self, op1, op2):
        self.sp -= 1
        self.ram[self.sp] = self.reg[op1]
        return (2, True)

    def pop(self, op1, op2):
        self.reg[op1] = self.ram[self.sp]
        self.sp += 1
        return (2, True)
        
    def ldi(self, op1, op2):
        self.reg[op1] = op2
        return (3, True) # will keep running
    
    def hlt(self, op1, op2):
        return (0, False)
    
    def prn(self, op1, op2):
        print(self.reg[op1])
        return (2, True)
    
    def mul(self, op1, op2):
        self.alu('MUL', op1, op2)
        return (3, True)

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value

    def add(self, op1, op2):
        self.alu('ADD', op1, op2)
        return (3, True)

    def load(self, program):
        """Load a program into memory."""

        address = 0


        with open(program) as f:
            for line in f:

                line_string = line.split('#')[0].strip()
               
                try:
                    self.ram_write(address, int(line_string, 2))
                    address += 1
                except ValueError:
                    pass
        f.close()

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

   

        
        while running:
            instruction = self.ram[self.pc]
            op1 = self.ram_read(self.pc+1)
            op2 = self.ram_read(self.pc+2)


            try:
                action = self.instructions[instruction](op1, op2)
                self.pc += action[0]
                running = action[1]
            except KeyError:
                print(f'Error: {instruction} not recognized')
                running = False