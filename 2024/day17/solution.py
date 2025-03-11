from template.Solution import Solution
import math

A = 'A'
B = 'B'
C = 'C'

class Day17Solution(Solution):
  def __init__(self):
    super().__init__(17)
    self.part1 = True
    self.part2 = False

    self.reg = {}
    self.reg[A] = 0
    self.reg[B] = 0
    self.reg[C] = 0
    self.output = ""

  def combo2val(self, combo):
    '''
    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.
    '''
    if combo >=0 and combo <= 3:
      return combo
    if combo == 4:
      return self.reg[A]
    if combo == 5:
      return self.reg[B]
    if combo == 6:
      return self.reg[C]
    raise ValueError(f"Combo operand should never be greater than 6: {combo}")

  def adv(self, combo):
    '''
    The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand.
    The result of the division operation is truncated to an integer and then written to the A register.

    E.g. an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.
    '''
    numerator = self.reg[A]
    denominator = 2**self.combo2val(combo)
    self.reg[A] = math.trunc(numerator / denominator)
    return 2
  
  def bxl(self, literal):
    '''
    The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
    '''
    self.reg[B] = self.reg[B] ^ literal
    return 2
  
  def bst(self, combo):
    '''
    The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
    '''
    self.reg[B] = self.combo2val(combo) % 8
    return 2

  def jnz(self, literal, ptr):  
    '''
    The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
    if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
    '''
    if self.reg[A] == 0:
      return 2
    else:
      if ptr > literal:
        return literal - ptr
      return ptr - literal
    
  def bxc(self):
    '''
    The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
    '''
    self.reg[B] = self.reg[B] ^ self.reg[C]
    return 2
  
  def out(self, combo):
    '''
    The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
    '''
    val = str(self.combo2val(combo) % 8)
    if len(self.output) > 0:
      self.output += "," + val
    else:
      self.output = val
    return 2
  
  def bdv(self, combo):
    '''
    The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
    '''
    numerator = self.reg[A]
    denominator = 2**self.combo2val(combo)
    self.reg[B] = math.trunc(numerator / denominator)
    return 2
  
  def cdv(self, combo):
    '''
    The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
    '''
    numerator = self.reg[A]
    denominator = 2**self.combo2val(combo)
    self.reg[C] = math.trunc(numerator / denominator)
    return 2

  def Part1(self):
    input = self.readInput()

    self.reg[A] = int(input[0].split(" ")[-1])
    self.reg[B] = int(input[1].split(" ")[-1])
    self.reg[C] = int(input[2].split(" ")[-1])
    self.output = ""

    commands = input[4].split(" ")[-1].split(",")
    ptr = 0

    # Start processing!
    while ptr < len(commands):
      cmd = commands[ptr]
      op = int(commands[ptr+1])

      if cmd == "0":
        ptr += self.adv(op)
      elif cmd == "1":
        ptr += self.bxl(op)
      elif cmd == "2":
        ptr += self.bst(op)
      elif cmd == "3":
        ptr += self.jnz(op, ptr)
      elif cmd == "4":
        ptr += self.bxc()
      elif cmd == "5":
        ptr += self.out( op)
      elif cmd == "6":
        ptr += self.bdv(op)
      elif cmd == "7":
        ptr += self.cdv(op)
      else:
        raise ValueError(f"Combo operand should never be greater than 6: {cmd}")

    return self.output
  
urlpatterns = Day17Solution().urls()