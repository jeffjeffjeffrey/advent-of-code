import sys
from queue import Queue

data = []
for row in sys.stdin.readlines():
  data.append(row.strip())

class Unit:
  def __init__(self, species, location, hp = 200, ap = 3):
    self.species = species
    self.location = location
    self.hp = hp
    self.ap = ap

  def print(self):
    print(self.species, self.position, self.hp, self.ap)


def get_neighbors(square):
  return [(square[0] + 1, square[1]), (square[0] - 1, square[1]), (square[0], square[1] + 1), (square[0], square[1] - 1)]

def find_distances(start, cavern):
  distances = {start: 0}
  queue = Queue()
  queue.put(start)
  while not queue.empty():
    square = queue.get()
    for neighbor in get_neighbors(square):
      if neighbor in cavern and (neighbor not in distances or distances[neighbor] > distances[square] + 1):
        distances[neighbor] = distances[square] + 1
        queue.put(neighbor)
  return distances

def get_closest_target(square, targets, cavern):
  distances = find_distances(square, cavern)
  reachable_targets = set(distances.keys()) & set(targets)
  if len(reachable_targets) == 0:
    return None
  return min(reachable_targets, key = (lambda target: (distances[target], target)))

def print_grid(height, width, units, fill):
  rows = []
  for y in range(grid_height):
    row = []
    for x in range(grid_width):
      row += str(fill.get((y, x), '#'))
    rows += [row]

  for unit in units:
    if unit.hp > 0:
      rows[unit.location[0]][unit.location[1]] = unit.species

  for row in rows:
    print(''.join(row))


casualty = True
ap = {'E': 2, 'G': 3}
while casualty:
  ap['E'] += 1

  total_units = {'E': 0, 'G': 0}
  units = []
  cavern = {}
  grid_width = 0
  grid_height = 0
  for y, row in enumerate(data):
    grid_height = y + 1
    for x, square in enumerate(row):
      grid_width = x + 1
      if square == '.':
        cavern[(y, x)] = '.'
      if square in ['E', 'G']:
        units.append(Unit(species = square, location = (y, x), ap = ap[square]))
        total_units[square] += 1

  combat_round = 0
  completed_full_rounds = 0
  combat_active = True
  casualty = False

  while combat_active: # rounds
    for unit in sorted(units, key = lambda unit: unit.location): # turns

      if total_units['E'] == 0 or total_units['G'] == 0:
        combat_active = False
        completed_full_rounds = combat_round
        break

      # skip dead units
      if unit.hp <= 0:
        continue

      # get all target neighbors
      neighbors = set(())
      for other_unit in units:
        if other_unit.species != unit.species and other_unit.hp > 0:
          neighbors.update(get_neighbors(other_unit.location))

      # find the closest reachable neighbor, if one exists
      closest_neighbor = get_closest_target(square = unit.location, targets = neighbors, cavern = cavern)
      if closest_neighbor and closest_neighbor != unit.location:
        # take a step toward the closest neighbor
        step = get_closest_target(square = closest_neighbor, targets = get_neighbors(unit.location), cavern = cavern)

        del cavern[step]
        cavern[unit.location] = '.'

        unit.location = step

      # see if enemies are adjacent
      targets = [other_unit for other_unit in units if other_unit.hp > 0 and other_unit.species != unit.species and other_unit.location in get_neighbors(unit.location)]

      # if so, attack!
      if len(targets) > 0:
        target = sorted(targets, key = lambda target: (target.hp, target.location))[0]
        target.hp -= unit.ap
        if target.hp <= 0:
          cavern[target.location] = '.'
          total_units[target.species] -= 1
          if target.species == 'E':
            casualty = True

    combat_round += 1
    print("\nAfter round ", combat_round)
    print_grid(grid_height, grid_width, units, cavern)

  # Uncomment the following line to solve Part 1 instead of Part 2
  # casualty = False

print("Combat ended after ", completed_full_rounds, " completed rounds")
print("Elf attack power:", ap['E'])
remaining_hp = sum([unit.hp for unit in units if unit.hp > 0])
print("Remaining hp: ", remaining_hp)
print("Outcome: ", completed_full_rounds * remaining_hp)
