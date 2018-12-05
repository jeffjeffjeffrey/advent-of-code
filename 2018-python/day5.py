import sys

data = input().strip()

# Part 1
def remove_reaction(s):
  for i in range(len(s) - 1):
    if s[i] != s[i + 1] and s[i].lower() == s[i + 1].lower():
      return s[:i] + s[(i+2):]
  return s

def react(s):
  while True:
    new_s = remove_reaction(s)
    if new_s == s:
      break
    else:
      s = new_s
  return s

print(len(react(data)))

# Part 2
def remove_letter(string, letter):
  return "".join([char for char in string if char.lower() != letter])

pruned_strings = [remove_letter(data, letter) for letter in 'abcdefghijklmnopqrstuvwxyz']

print(min([len(react(string)) for string in pruned_strings]))
