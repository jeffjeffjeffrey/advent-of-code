import sys

data = [int(row.strip()[1:]) * (-1 if row[0] == "-" else 1) for row in sys.stdin.readlines()]

# Part 1
print(sum(data))

# Part 2
i = 0
freqs = {}
total = 0
while freqs.get(total, 0) < 2:
  total += data[i % len(data)]
  freqs[total] = freqs.get(total, 0) + 1
  i += 1

print(total)
