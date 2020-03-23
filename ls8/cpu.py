"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = self.registers[0]
        self.ir = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
            0b10100010: self.mul,

        }
        
    def ldi(self, op1, op2):
        self.registers[op1] = op2
        return (3, True) # will keep running
    
    def hlt(self, op1, op2):
        return (0, False)
    
    def prn(self, op1, op2):
        print(self.registers[op1])
        return (2, True)
    
    def mul(self, op1, op2):
        self.alu('MUL', op1, op2)
        return (3, True)

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # TODO read from print.ls8

        with open(program) as f:

            for line in f:
                # takes the binary number before the comment and removes whitespace
                cmd = line.split('#')[0].strip() 

                try:
                    self.ram_write(int(cmd, 2), address) # 2 is BASE 2
                    address += 1
                except ValueError:
                    pass
                
            for instruction in program:
                self.ram[address] = instruction
                address += 1
        
        f.close()

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram[self.pc]
            
            op1 = self.ram_read(self.pc + 1)
            op2 = self.ram_read(self.pc + 2)

            try:
                out = self.ir[instruction](op1, op2)
                self.pc += out[0]
                running = out[1]

            except:
                print('Error: unknown input')
                sys.exit()

