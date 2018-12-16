import sys
import re

# Parse input
input_part = 0
opcode_experiment_part = 0
opcode_experiment_index = 0
opcode_experiments = []
program = []
for row in sys.stdin.readlines():
  row = row.strip()
  if input_part == 0:
    if opcode_experiment_part == 0:
      if row == '':
        input_part = 1
      else:
        before = [int(register) for register in re.match('Before: \[(\d), (\d), (\d), (\d).*', row).groups()]
        opcode_experiments.append({'before': before})
    elif opcode_experiment_part == 1:
      instruction = [int(code) for code in re.match('(\d*) (\d) (\d) (\d)', row).groups()]
      opcode_experiments[opcode_experiment_index]['opcode'] = instruction[0]
      opcode_experiments[opcode_experiment_index]['A'] = instruction[1]
      opcode_experiments[opcode_experiment_index]['B'] = instruction[2]
      opcode_experiments[opcode_experiment_index]['C'] = instruction[3]
    elif opcode_experiment_part == 2:
      after = [int(register) for register in re.match('After:  \[(\d), (\d), (\d), (\d).*', row).groups()]
      opcode_experiments[opcode_experiment_index]['after'] = after
      opcode_experiment_index += 1
    opcode_experiment_part = (opcode_experiment_part + 1) % 4
  else:
    if row != '':
      program.append([int(code) for code in re.match('(\d*) (\d) (\d) (\d)', row).groups()])

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

# Part 1

# Get possible opcode names for ids based on experiment results
experiment_results = []
possible_op_names = {}
for x in opcode_experiments:
  possible_ops = set(())
  for op in ops:
    if ops[op](x['before'], x['A'], x['B'], x['C']) == x['after']:
      possible_ops.add(op)
  experiment_results.append(possible_ops)
  if x['opcode'] in possible_op_names:
    possible_op_names[x['opcode']] = possible_op_names[x['opcode']] & possible_ops
  else:
    possible_op_names[x['opcode']] = possible_ops

# Print the number of experiments that could correspond to 3 or more opcodes
print(len([result for result in experiment_results if len(result) >= 3]))


# Part 2

# Use process of elimination to figure out unique mapping of opcode ids to names
op_names = {} # mapping from op ids to names
while len(op_names) < len(ops):
  for id in range(len(ops)):
    if id not in possible_op_names:
      continue
    elif len(possible_op_names[id]) == 1:
      op_names[id] = list(possible_op_names[id])[0]
      del possible_op_names[id]
    else:
      possible_op_names[id] = possible_op_names[id].difference(op_names.values())

# Execute the program
register = [0, 0, 0, 0]
for instruction in program:
  register = ops[op_names[instruction[0]]](register, instruction[1], instruction[2], instruction[3])

print(register)
