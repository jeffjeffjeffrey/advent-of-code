import sys

data = [row.strip() for row in sys.stdin.readlines()]

# Part 1
def get_char_counts(string):
  char_counts = {}
  for char in string:
    char_counts[char] = char_counts.get(char, 0) + 1
  return char_counts

char_counts = [get_char_counts(string) for string in data]
twos   = [2 in char_count.values() for char_count in char_counts]
threes = [3 in char_count.values() for char_count in char_counts]

print(sum([int(x) for x in twos]) * sum([int(x) for x in threes]))

# Part 2
def get_common_chars(first, second):
  return [first[i] for i in range(len(first)) if first[i] == second[i]]

for i in range(len(data)):
  for j in range(i):
    common_chars = get_common_chars(data[i], data[j])
    if len(common_chars) == len(data[i]) - 1:
      print(''.join(common_chars))
      break
