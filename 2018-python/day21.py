import sys

ip_index = None
instructions = []
for row in sys.stdin.readlines():
  if ip_index == None:
    ip_index = int(row.strip().split(' ')[1])
  else:
    data = row.strip().split(' ')
    instruction = {'opcode': data[0], 'A': int(data[1]), 'B': int(data[2]), 'C': int(data[3])}
    instructions.append(instruction)

# Define all the ops
def addr(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] + reg[B]
  return output

def addi(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] + B
  return output

def mulr(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] * reg[B]
  return output

def muli(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] * B
  return output

def banr(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] & reg[B]
  return output

def bani(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] & B
  return output

def borr(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] | reg[B]
  return output

def bori(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A] | B
  return output

def setr(reg, A, B, C):
  output = reg.copy()
  output[C] = reg[A]
  return output

def seti(reg, A, B, C):
  output = reg.copy()
  output[C] = A
  return output

def gtir(reg, A, B, C):
  output = reg.copy()
  output[C] = int(A > reg[B])
  return output

def gtri(reg, A, B, C):
  output = reg.copy()
  output[C] = int(reg[A] > B)
  return output

def gtrr(reg, A, B, C):
  output = reg.copy()
  output[C] = int(reg[A] > reg[B])
  return output

def eqir(reg, A, B, C):
  output = reg.copy()
  output[C] = int(A == reg[B])
  return output

def eqri(reg, A, B, C):
  output = reg.copy()
  output[C] = int(reg[A] == B)
  return output

def eqrr(reg, A, B, C):
  output = reg.copy()
  output[C] = int(reg[A] == reg[B])
  return output

ops = {
  'addr': addr,
  'addi': addi,

  'mulr': mulr,
  'muli': muli,

  'banr': banr,
  'bani': bani,

  'borr': borr,
  'bori': bori,

  'setr': setr,
  'seti': seti,

  'gtir': gtir,
  'gtri': gtri,
  'gtrr': gtrr,

  'eqir': eqir,
  'eqri': eqri,
  'eqrr': eqrr
}

# I started by reading through the elf code to figure out where it had the ability to halt.
# This occurs on instruction #28, where the program will exit if register 0 and register 2 have the same value.
# I thence modified the `run_program()` method from Day 19 to pay attention to instruction #28:

# Part 1: The first time we reach #28, we print the value of register 2.
# If we had set this value for register 0 in the beginning, then the program would halt at the earliest possible moment.
# This is our answer.

# Part 2: We keep track of the values of register 2 that appear at #28 in a set. 
# Once we see a repeated value, we know we've encountered all possible values of register 0 that might make the program halt.
# The previous such value recorded will be the halting value that causes the longest runtime, so that is our answer.

def run_program(ip, register, verbose = False):
  previous_exit_value = None
  exit_values = set(())
  while ip < len(instructions):
    register[ip_index] = ip

    instruction = instructions[ip]
    next_register = ops[instruction['opcode']](
      register,
      instruction['A'],
      instruction['B'],
      instruction['C']
    )
    if ip == 28:
      exit_value = register[2]
      if previous_exit_value == None:
        print("Part 1:", exit_value)
      if exit_value in exit_values:
        print("Part 2:", previous_exit_value)
        break
      exit_values.add(exit_value)
      previous_exit_value = exit_value
    register = next_register
    ip = register[ip_index] + 1

ip = 0
register = [0, 0, 0, 0, 0, 0]
run_program(ip, register)

# Below is an (unsuccessful) attempt to transcribe the elf code into Python. Keeping it here in case it comes in handy later.

# 2208870 was too low

# L = 65536
# M = 16777215
# N = 2238642
# P = 65899

# #0,1, 2, 3, 5
# a, b, c, d, e = [0, 0, 0, 0, 0]

# c = 123
# c = c & 456
# if c == 72:
#   c = 0
# else:
#   print("BAD BANI")

# while True:
#   # cmd 6
#   e = c | L
#   c = N

#   while True:
#     # cmd 8
#     d = e & 255
#     c = c + d
#     c = c & M
#     c = c * P
#     c = c & M

#     if 256 > e: # for some reason this loop is never entered
#       # cmd 17
#       d = 0
#       while True:
#         # cmd 18
#         b = d + 1
#         b = b * 256

#         if b > e:
#           e = d
#           break # goto 8
#         else:
#           d += 1 
#           # goto 18
#     else:
#       # print(c)
#       if c == a:
#         break
      