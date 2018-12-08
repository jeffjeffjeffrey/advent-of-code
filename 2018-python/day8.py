data = [int(token) for token in input().strip().split()]

class Node:
  def __init__(self):
    self.children = []
    self.metadata = []

def build_tree(numbers):
  num_children, num_metadata = numbers[0:2]
  node = Node()
  remaining_numbers = numbers[2:]
  for i in range(num_children):
    new_child, remaining_numbers = build_tree(remaining_numbers)
    node.children += [new_child]
  node.metadata = remaining_numbers[0:num_metadata]
  return [node, remaining_numbers[num_metadata:]]

tree = build_tree(data)[0]

def sum_metadata(node):
  return(sum(node.metadata) + sum(sum_metadata(child) for child in node.children))

print(sum_metadata(tree))

def get_value(node):
  if len(node.children) == 0:
    return sum(node.metadata)
  value = 0
  for index in node.metadata:
    if index <= len(node.children):
      value += get_value(node.children[index - 1])
  return value

print(get_value(tree))
