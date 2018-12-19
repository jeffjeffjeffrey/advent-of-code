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

def run_program(ip, register, verbose = False):
  while ip < len(instructions):
    register[ip_index] = ip
    instruction = instructions[ip]
    next_register = ops[instruction['opcode']](
      register,
      instruction['A'],
      instruction['B'],
      instruction['C']
    )
    if verbose:
      print("ip:", ip, register, instruction['opcode'],[instruction['A'], instruction['B'], instruction['C']], next_register)
    register = next_register
    ip = register[ip_index] + 1
  return register

# Part 1

ip = 0
register = [0, 0, 0, 0, 0, 0]

register = run_program(ip, register)
print("Part 1 program output:", register[0])

# Part 2

# Same as part 1, but begin with register [1, 0, 0, 0, 0, 0]

# The program runs for a long time withouth halting. Something is up.
# After breaking execution and analyzing the registers at several different points,
# we start to get a sense of what this program is doing:

# The program starts by multiplying r0 by a bunch of stuff to get a big number N.
# Then we enter some loops:

# r4 holds onto the big number N
# r1 and r3 each iterate from 1 to N
# if r1 * r3 == N, then add r1 to r0

# r5 is used for logical flow
# r2 is the instruction pointer

# Rewriting this logic in Python looks like this:

# sum = 0
# for i in range(1, N+1):
#   for j in range(1, N+1):
#     if i * j == N:
#       sum += i

# Eureka! This is simply finding the sum of the divisors of N.
# For Part 1, N = 185. We could use brute force.
# For Part 2, N = 10551275. Yikes! Brute force would never work here.

# Luckily, we can bypass this very inefficient loop by computing the divisor sum using math.

# To see the end of the program, begin here:
print("The final few iterations of Part 2:")
N = 10551275
divisor_sum = sum([1, 5, 7, 25, 35, 175, 60293, 301465, 422051, 1507325, 2110255, 10551275])
ip = 9
register = [divisor_sum, N, 9, N, N, 0]

register = run_program(ip, register, True)
print("Part 2 program output:", register[0])
