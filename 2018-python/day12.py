import sys
import re

# Make a string for the pots, and a dict for all the cultivation notes
pots = None
notes = {}
for row in sys.stdin.readlines():
  row = row.strip()
  if not pots:
    pots = re.match('initial state: (.*)', row).groups()[0]
  elif len(row) > 0:
    key, value = re.match('(.*) => (.)', row).groups()
    notes[key] = value

# Compute each successive generation of plants as a string of . and #
# Trim empty pots on the ends and keep track of the index of the "zero" pot as we go
zero_index = 0
for i in range(150):
  pots = '....' + pots + '....'
  zero_index += 2
  new_pots = ''
  first_plant_found = False
  for j in range(2, len(pots) - 2):
    key = pots[j - 2 : j + 3]
    new_pot = notes.get(key, '.')
    new_pots += new_pot
    if not first_plant_found and new_pot == '.':
      zero_index -= 1
    else:
      first_plant_found = True

  pots = new_pots.replace('.', ' ').strip().replace(' ', '.')

  print("day:", i+1, "score:", sum([i - zero_index for i in range(len(pots)) if pots[i] == '#']), pots)

# For Part 1, just look at the value in the printout at day 20: 1,991
# For Part 2, observe the garden until it stabilizes, then extrapolate via the apparent linear function from there:
# plant_score(day) = (day + 1 - 120) * 22 + 3151
# plant_score(50,000,000,000) = 1,100,000,000,511
