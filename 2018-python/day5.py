data = input().strip()

# Build a fully-reacted stack of letters in one pass through the polymer, optionally ignoring a given letter
def react(polymer, removable_letter = ' '):
  reacted = ''
  for letter in polymer:
    if letter.lower() == removable_letter.lower():
      continue
    elif len(reacted) > 0 and reacted[-1] != letter and reacted[-1].lower() == letter.lower():
      reacted = reacted[:-1]
    else:
      reacted += letter
  return reacted

# Part 1: React the polymer as-is and find its resultant length
print(len(react(data)))

# Part 2: React the polymer while ignoring a specific letter of the alphabet. Find the shortest resultant length
print(min([len(react(data, letter)) for letter in 'qwertyuiopasdfghjklzxcvbnm']))
