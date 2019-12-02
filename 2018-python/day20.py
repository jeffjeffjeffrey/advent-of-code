from queue import Queue
from re import match

data = input().strip()

def get_neighbor(room, direction):
  dx = 0
  dy = 0
  if direction == 'N':
    dy = -1
  elif direction == 'S':
    dy = 1
  elif direction == 'E':
    dx = 1
  else: # 'W'
    dx = -1
  return (room[0] + dx, room[1] + dy)

def add_neighbor(grid, room, direction):
  neighbor = get_neighbor(room, direction)
  grid[room]['neighbors'].add(neighbor)
  if neighbor not in grid:
    grid[neighbor] = {'distance': grid[room]['distance'] + 1, 'neighbors': set(())}
  grid[neighbor]['neighbors'].add(room)
  return neighbor

def get_branches(directions):
  if len(directions) == 0 or directions[0] != '(':
    return [[], directions]
  parens_depth = 1
  branches = []
  branch = ''
  i = 1
  while parens_depth > 0:
    char = directions[i]
    if parens_depth == 1 and char == '|':
      branches.append(branch)
      branch = ''
    elif parens_depth == 1 and char == ')':
      branches.append(branch)
    else:
      branch += char

    i += 1

    if char == '(':
      parens_depth += 1
    elif char == ')':
      parens_depth -= 1
  return [branches, directions[i:]]

def explore(grid, room, directions):
  for direction in directions:
    room = add_neighbor(grid, room, direction)
  return room

directions = data[1:-1]


# First technique: track distances using a queue, where we split up forks as we go

room = (0, 0)
grid = {room: {'distance': 0, 'neighbors': set(())}}
q = Queue()
q.put([room, directions])
while not q.empty():
  room, directions = q.get()
  head, tail = match('([NSEW]*)(.*)', directions).groups()
  room = explore(grid, room, head)
  branches, tail = get_branches(tail)
  if len(tail) > 0:
    for branch in branches:
      explore(grid, room, branch[:int(len(branch) / 2)])
    q.put([room, tail])
  else:
    for branch in branches:
      q.put([room, branch])

print("Part 1 (queue):", max([grid[room]['distance'] for room in grid]))
print("Part 2 (queue):", len([room for room in grid if grid[room]['distance'] >= 1000]))


# Second technique: build an adjacency map during the previous step
# and use that result to find absolute shortest paths.
# This technique ought to guard against paths that can be reached in multiple ways

room = (0, 0)
distances = {room: 0}
q = Queue()
q.put(room)
while not q.empty():
  room = q.get()
  for neighbor in grid[room]['neighbors']:
    if neighbor not in distances or distances[room] + 1 < distances[neighbor]:
      distances[neighbor] = distances[room] + 1
      q.put(neighbor)

print("Part 1 (dfs):", max([distances[room] for room in distances]))
print("Part 2 (dfs):", len([room for room in distances if distances[room] >= 1000]))


# Third technique: do it all in one quick pass using a stack.
# Credit to the subreddit for this simple approach

# Note that this shortcut approacch doesn't work for some edge cases, like these:
# data = '^NNNNNEEEEESS(E|WSS)S$'
# data = '^NNNNNEEEEESSES$'

directions = data[1:-2]

positions = []
room = (0, 0)
distances = {room: 0}
for c in directions:
  if c == '(':
    positions.append(room)
  elif c == '|':
    room = positions[-1]
  elif c == ')':
    room = positions.pop()
  else:
    neighbor = get_neighbor(room, c)
    if neighbor not in distances or distances[room] + 1 < distances[neighbor]:
      distances[neighbor] = distances[room] + 1
    room = neighbor

print("Part 1 (stack):", max([distances[room] for room in distances]))
print("Part 2 (stack):", len([room for room in distances if distances[room] >= 1000]))
