import sys
from collections import defaultdict

data = {}
for y, row in enumerate(sys.stdin.readlines()):
  for x, char in enumerate(row.strip()):
    data[(x, y)] = char

grid = data.copy()

def print_grid(grid):
  for y in range(max(square[1] for square in grid) + 1):
    row = ''
    for x in range(max(square[0] for square in grid) + 1):
      row += grid[(x, y)]
    print(row)

def get_surrounding_units(grid, square):
  unit_counts = defaultdict(int)
  for x in range(-1,2):
    for y in range(-1,2):
      neighbor = (square[0] + x, square[1] + y)
      if neighbor in grid and neighbor != square:
        unit_counts[grid[neighbor]] += 1
  return unit_counts

def get_next_state(state, surrounding_units):
  if state == '.':
    if surrounding_units['|'] >= 3:
      return '|'
    else:
      return '.'
  elif state == '|':
    if surrounding_units['#'] >= 3:
      return '#'
    else:
      return '|'
  elif state == '#':
    if surrounding_units['#'] >= 1 and surrounding_units['|'] >= 1:
      return '#'
    else:
      return '.'

def get_resource_value(grid):
  num_trees = len([square for square in grid if grid[square] == '|'])
  num_mills = len([square for square in grid if grid[square] == '#'])
  return num_trees * num_mills

# Part 1: Let the forest evolve for 10 minutes

minutes = 10
for i in range(minutes):
  new_grid = {}
  for square in grid:
    new_grid[square] = get_next_state(grid[square], get_surrounding_units(grid, square))
  grid = new_grid
  print("After", i + 1, "minutes:")
  print_grid(grid)

print("Resource value after", minutes, "minutes:", get_resource_value(grid))

# Part 2

def get_forest_hash_key(grid):
  key = ''
  for y in range(max(square[1] for square in grid) + 1):
    for x in range(max(square[0] for square in grid) + 1):
      key += grid[(x, y)]
  return key

grid = data.copy()

# Keep track of which forest arrangements we've already seen via a hash
# Once we detect a repeated arrangement, continue for the length of the cycle and break

initial_forests = set(())
forest_hash = {}
i = 0
while True:
  forest_hash_key = get_forest_hash_key(grid)
  if forest_hash_key not in initial_forests:
    initial_forests.add(forest_hash_key)
  elif forest_hash_key not in forest_hash:
    forest_hash[forest_hash_key] = {'minutes': i, 'resource_value': get_resource_value(grid)}
  else:
    break
  new_grid = {}
  for square in grid:
    new_grid[square] = get_next_state(grid[square], get_surrounding_units(grid, square))
  grid = new_grid
  i += 1

  # Un-comment these lines to watch the forest evolve
  # print("After", i, "minutes:")
  # print_grid(grid)

# Extrapolate to 1,000,000,000 minutes now that we know the cycle structure

minutes = 1000000000
cycle_length = len(forest_hash)
print("After", i - cycle_length, "minutes the forest begins a", cycle_length, "minute cycle")
for forest in forest_hash:
  if (minutes - forest_hash[forest]['minutes']) % cycle_length == 0:
    print("Resource value after", minutes, "minutes:", forest_hash[forest]['resource_value'])
