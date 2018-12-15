input_value = input()

# Create a Node class for representing a circular linked list of elf recipes

class Node:
  def __init__(self, score, next = None):
    self.score = score
    if next:
      self.next = next
    else:
      self.next = self

  def add(self, score):
    node = Node(score, self.next)
    self.next = node
    return node

  def next_n(self, n):
    node = self.next
    for i in range(n - 1):
      node = node.next
    return node

  def match(self, pattern, last_node):
    if len(pattern) == 0:
      return True
    elif len(pattern) > 1 and self == last_node:
      return False
    elif pattern[0] == self.score:
      return self.next.match(pattern[1:], last_node)
    else:
      return False

  def print_n(self, n):
    output_string = ''
    node = self
    for i in range(n):
      output_string += str(node.score)
      node = node.next
    print(output_string)

# Part 1

last_node = Node(3).add(7)
elf1 = last_node.next
elf2 = elf1.next

min_recipes = int(input_value)
length = 2

while length < min_recipes + 10:
  for digit in str(elf1.score + elf2.score):
    last_node = last_node.add(int(digit))
    length += 1
  elf1 = elf1.next_n(1 + elf1.score)
  elf2 = elf2.next_n(1 + elf2.score)

last_node.next_n(min_recipes + 1).print_n(10)

# Part 2

last_node = Node(3).add(7)
elf1 = last_node.next
elf2 = elf1.next

pattern = [int(digit) for digit in input_value]
seq_start = last_node
length = 2
length_before_match = None

while not length_before_match:
  for digit in str(elf1.score + elf2.score):
    seq_start = seq_start.next
    last_node = last_node.add(int(digit))
    length += 1
    if length < len(pattern):
      seq_start = last_node
    if seq_start.match(pattern, last_node):
      length_before_match = length - len(pattern)
  elf1 = elf1.next_n(1 + elf1.score)
  elf2 = elf2.next_n(1 + elf2.score)

print(length_before_match)
