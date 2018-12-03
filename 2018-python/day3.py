import sys
import re

data = []
for row in sys.stdin.readlines():
  fields = re.match('#(\d*) @ (\d*),(\d*): (\d*)x(\d*)', row).groups()
  data += [{'id': int(fields[0]), 'x': int(fields[1]), 'y': int(fields[2]), 'width': int(fields[3]), 'height': int(fields[4])}]

fabric = [[0] * 1000 for i in range(1000)]

# Part 1
for rectangle in data:
  for i in range(rectangle['width']):
    for j in range(rectangle['height']):
      fabric[rectangle['x'] + i][rectangle['y'] + j] += 1

print(sum([1 for row in fabric for value in row if value > 1]))

# Part 2

for rectangle in data:
  rectangle_size = rectangle['width'] * rectangle['height']
  total_claims = 0
  for i in range(rectangle['width']):
    for j in range(rectangle['height']):
      total_claims += fabric[rectangle['x'] + i][rectangle['y'] + j]
  if total_claims == rectangle_size:
    print(rectangle['id'])
    break