import sys
import re

stars = []
for row in sys.stdin.readlines():
  x, y, dx, dy = re.match('.*<\s*(.*),\s*(.*)>.*<\s*(.*),\s*(.*)>', row.strip()).groups()
  stars += [{'x': int(x), 'y': int(y), 'dx': int(dx), 'dy': int(dy)}]

def get_rectangle(stars):
  min_x = min([star['x'] for star in stars])
  max_x = max([star['x'] for star in stars])
  min_y = min([star['y'] for star in stars])
  max_y = max([star['y'] for star in stars])
  return [min_x, max_x, min_y, max_y]

def print_stars(stars):
  min_x, max_x, min_y, max_y = get_rectangle(stars)
  sky = [['.'] * (max_x - min_x + 1) for i in range(max_y - min_y + 1)]
  for star in stars:
    sky[star['y'] - min_y][star['x'] - min_x] = '#'
  for row in sky:
    print(''.join(row))

sky_size = None
previous_sky_size = None
seconds = 0
while not previous_sky_size or sky_size < previous_sky_size:
  min_x, max_x, min_y, max_y = get_rectangle(stars)
  previous_sky_size = sky_size
  sky_size = (max_x - min_x) * (max_y - min_y)
  seconds += 1
  for star in stars:
    star['x'] += star['dx']
    star['y'] += star['dy']

for star in stars:
  star['x'] -= star['dx'] * 2
  star['y'] -= star['dy'] * 2

print("After " + str(seconds - 2) + " seconds:")
print_stars(stars)
