grid_size = 300
grid_serial_number = int(input())

# Part 1

def get_power(x, y):
  return int(((x + 10) * y + grid_serial_number) * (x + 10) / 100) % 10 - 5

# 300x300 grid with values equal to each square's power
grid = [[0] * grid_size for i in range(grid_size)]

# Start at the bottom-right and iterate through the grid,
# computing the single-square power along with the 3x3 subsquare power along the way
optimal_subsquare = {'point': None, 'power': None}
for i in range(grid_size):
  for j in range(grid_size):
    x = grid_size - i - 1
    y = grid_size - j - 1
    grid[x][y] = get_power(x, y)
    if x + 3 <= grid_size and y + 3 <= grid_size:
      subsquare_power = 0
      for a in range(3):
        for b in range(3):
          subsquare_power += grid[x + a][y + b]
      if not optimal_subsquare['power'] or optimal_subsquare['power'] < subsquare_power:
        optimal_subsquare['point'] = (x, y)
        optimal_subsquare['power'] = subsquare_power

print(optimal_subsquare)

# Part 2

# 300x300 grid of dictionaries: top-left coordinates -> subsquare size -> total power
grid = [[{0:0, -1:0} for j in range(grid_size)] for i in range(grid_size)]

# Start at the bottom-right and iterate through the grid,
# computing the all subsquare powers along the way
# using inclusion-exclusion on previously-computed subsquares
optimal_subsquare = {'point': None, 'size': None, 'power': None}
for i in range(grid_size):
  for j in range(grid_size):
    x = grid_size - i - 1
    y = grid_size - j - 1
    for square_size in range(1, min(grid_size - x, grid_size - y) + 1):
      if square_size == 1:
        grid[x][y][square_size] = get_power(x, y)
      else:
        grid[x][y][square_size] = \
          grid[x][y][1] + \
          grid[x + 1][y][square_size - 1] + \
          grid[x][y + 1][square_size - 1] - \
          grid[x + 1][y + 1][square_size - 2] + \
          grid[x + square_size - 1][y + square_size - 1][1]
      if not optimal_subsquare['power'] or optimal_subsquare['power'] < grid[x][y][square_size]:
        optimal_subsquare['point'] = (x, y)
        optimal_subsquare['size'] = square_size
        optimal_subsquare['power'] = grid[x][y][square_size]

print(optimal_subsquare)

# Another implementation of Part 2, same time complexity but lower space complexity:

# 300x300 grid of rectangular power totals.
# Each point (x, y) is the sum of powers within the rectangle bounded by (x, y) in the northwest and (299, 299) in the southeast.
rect = {}

# Start at the bottom-right and iterate through the grid,
# computing the values of rect and
# computing the all subsquare powers along the way
# using inclusion-exclusion on rect
best_square = {'point': None, 'size': None, 'power': None}
for i in range(grid_size):
  for j in range(grid_size):
    x = grid_size - i - 1
    y = grid_size - j - 1
    rect[(x, y)] = \
      get_power(x, y) + \
      rect.get((x + 1, y), 0) + \
      rect.get((x, y + 1), 0) - \
      rect.get((x + 1, y + 1), 0)
    for square_size in range(1, min(grid_size - x, grid_size - y) + 1):
      power = \
        rect.get((x, y), 0) - \
        rect.get((x + square_size, y), 0) - \
        rect.get((x, y + square_size), 0) + \
        rect.get((x + square_size, y + square_size), 0)
      if not best_square['power'] or best_square['power'] < power:
        best_square['point'] = (x, y)
        best_square['size'] = square_size
        best_square['power'] = power

print(best_square)

