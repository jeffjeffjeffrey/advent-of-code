import sys

carts = {}
cart_locations = {}
grid = {}
cart_id = 0
y = 0
for row in sys.stdin.readlines():
  x = 0
  for char in row:
    if char in ['<', '>']:
      grid[(x, y)] = '-'
      carts[cart_id] = {'location': (x, y), 'orientation': char, 'turn': 0}
      cart_locations[(x, y)] = cart_id
      cart_id += 1
    elif char in ['^', 'v']:
      grid[(x, y)] = '|'
      carts[cart_id] = {'location': (x, y), 'orientation': char, 'turn': 0}
      cart_locations[(x, y)] = cart_id
      cart_id += 1
    elif char in ['|', '-', '\\', '/', '+']:
      grid[(x, y)] = char
    x += 1
  y += 1

def print_grid(grid, carts):
  width = max([location[0] for location in grid]) + 1
  height = max([location[1] for location in grid]) + 1
  arr_grid = [[' '] * width for i in range(height)]
  for location in grid:
    arr_grid[location[1]][location[0]] = grid[location]
  for cart_id in carts:
    arr_grid[carts[cart_id]['location'][1]][carts[cart_id]['location'][0]] = carts[cart_id]['orientation']
  for row in arr_grid:
    print(''.join(row))

# print_grid(grid, carts)

def next_location(location, orientation):
  if orientation == '^':
    return (location[0], location[1] - 1)
  elif orientation == '>':
    return (location[0] + 1, location[1])
  elif orientation == 'v':
    return (location[0], location[1] + 1)
  elif orientation == '<':
    return (location[0] - 1, location[1])

# dict of (orientation, track_char, turn) -> new_orientation
next_orientation = {
  ('^', '|'):  '^',
  ('^', '\\'): '<',
  ('^', '/'):  '>',
  ('>', '-'):  '>',
  ('>', '\\'): 'v',
  ('>', '/'):  '^',
  ('v', '|'):  'v',
  ('v', '\\'): '>',
  ('v', '/'):  '<',
  ('<', '-'):  '<',
  ('<', '\\'): '^',
  ('<', '/'):  'v',
  ('^', '+', 0): '<',
  ('^', '+', 1): '^',
  ('^', '+', 2): '>',
  ('>', '+', 0): '^',
  ('>', '+', 1): '>',
  ('>', '+', 2): 'v',
  ('v', '+', 0): '>',
  ('v', '+', 1): 'v',
  ('v', '+', 2): '<',
  ('<', '+', 0): 'v',
  ('<', '+', 1): '<',
  ('<', '+', 2): '^',
}

first_crash = None
remaining_carts = set(carts.keys())
while len(remaining_carts) > 1:
  for cart_id in sorted(carts.keys(), key = (lambda k: (carts[k]['location'][1], carts[k]['location'][0]))):
    if cart_id not in remaining_carts:
      continue
    cart = carts[cart_id]
    cart_locations.pop(cart['location'])
    cart['location'] = next_location(cart['location'], cart['orientation'])
    if cart['location'] in cart_locations:
      if not first_crash:
        first_crash = cart['location']
      remaining_carts.remove(cart_locations[cart['location']])
      remaining_carts.remove(cart_id)
      cart_locations.pop(cart['location'])
      continue
    cart_locations[cart['location']] = cart_id
    if grid[cart['location']] == '+':
      cart['orientation'] = next_orientation[(cart['orientation'], '+', cart['turn'])]
      cart['turn'] = (cart['turn'] + 1) % 3
    else:
      cart['orientation'] = next_orientation[(cart['orientation'], grid[cart['location']])]

# Part 1
print(first_crash)
# Part 2
print(carts[list(remaining_carts)[0]]['location'])
