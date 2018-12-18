import sys
from queue import Queue

grid = {}
for row in sys.stdin.readlines():
  coords = [xy.split('=')[1].split('..') for xy in sorted(row.strip().split(', '))]
  x_range = [int(coord) for coord in coords[0]]
  y_range = [int(coord) for coord in coords[1]]
  if len(x_range) == 1:
    x_range.append(x_range[0])
  if len(y_range) == 1:
    y_range.append(y_range[0])
  for x in range(x_range[0], x_range[1] + 1):
    for y in range(y_range[0], y_range[1] + 1):
      grid[(x, y)] = '#'

min_x = min([square[0] for square in grid])
max_x = max([square[0] for square in grid])
min_y = min([square[1] for square in grid])
max_y = max([square[1] for square in grid])

def print_grid(grid):
  for y in range(min_y, max_y + 1):
    row = ''
    for x in range(min_x, max_x + 1):
      row += grid.get((x, y), ' ')
    print(row)

def is_wall_ahead(grid, square, x_direction):
  if grid.get(square, '.') == '#':
    return True
  if grid.get((square[0], square[1] + 1), '|') == '|':
    return False
  return is_wall_ahead(grid, (square[0] + x_direction, square[1]), x_direction)

def fill_to_wall(grid, square, x_direction):
  if grid.get(square, '.') == '#':
    return
  grid[square] = '~'
  fill_to_wall(grid, (square[0] + x_direction, square[1]), x_direction)

def fill_reservoir(grid, square):
  if is_wall_ahead(grid, square, -1) and is_wall_ahead(grid, square, 1):
    fill_to_wall(grid, square, -1)
    fill_to_wall(grid, square, 1)
    return fill_reservoir(grid, (square[0], square[1] - 1))
  else:
    return square

def flow(grid, square, x_direction = 0):
  # stop flowing if we've hit a wall or gone off the map
  if square[1] > max_y or grid.get(square, '.') in ['#', '~']:
    return None

  # always flow downward if possible
  if grid.get((square[0], square[1] + 1), '|') == '|':
    grid[square] = '|'
    return flow(grid, (square[0], square[1] + 1))

  # keep flowing horizontally if we are already doing so
  elif x_direction != 0:
    grid[square] = '|'
    return flow(grid, (square[0] + x_direction, square[1]), x_direction)

  # fill the reservoir if we've fallen onto the floor
  else:
    return fill_reservoir(grid, square)

q = Queue()
q.put([(500, 1), 0])
while not q.empty():
  square, x_direction = q.get()
  optional_square = flow(grid, square, x_direction)
  if optional_square:
    q.put([optional_square, -1])
    q.put([optional_square, 1])

print_grid(grid)

print("Part 1: Total wet squares =", len([square for square in grid if square[1] <= max_y and square[1] >= min_y and grid[square] in ['|', '~']]))
print("Part 2: Total standing water =", len([square for square in grid if square[1] <= max_y and square[1] >= min_y and grid[square] == '~']))
