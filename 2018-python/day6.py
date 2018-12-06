import sys
import re

nodes = [(int(coords[0]), int(coords[1])) for coords in [row.split(", ") for row in sys.stdin.readlines()]]

# Part 1

# Step 1: Put a bounding box around the coordinates

max_x = max(node[0] for node in nodes)
min_x = min(node[0] for node in nodes)
max_y = max(node[1] for node in nodes)
min_y = min(node[1] for node in nodes)

# Step 2: Find the nearest node to each location in the grid using Manhattan distance: |x - a| + |y - b|
# Note infinite nodes along the way so we can avoid them in the end

def distance(first, second):
  return abs(first[0] - second[0]) + abs(first[1] - second[1])

nearest_nodes = {}
infinite_nodes = set(())
for x in range(min_x, max_x + 1):
  for y in range(min_y, max_y + 1):
    nearest_node, next_node = sorted(nodes, key = (lambda k: distance((x, y), k)))[0:2]
    if distance((x, y), nearest_node) < distance((x, y), next_node):
      nearest_nodes[nearest_node] = nearest_nodes.get(nearest_node, 0) + 1
      if x == min_x or x == max_x or y == min_y or y == max_y:
        infinite_nodes.add(nearest_node)

print(max([nearest_nodes[node] for node in nearest_nodes if node not in infinite_nodes]))

# Part 2

def distance_sum(location, nodes):
  return sum([distance(location, node) for node in nodes])

# Step 1: Find the centroid of the nodes

centroid = (int(sum([node[0] for node in nodes]) / len(nodes)), int(sum([node[1] for node in nodes]) / len(nodes)))

# Step 2: Starting at the centroid, work our way outward radially until we stop finding safe locations

safe_distance = 10000
safety_zone = set(())
safety_zone_complete = False
radius = -1
while not safety_zone_complete:
  safety_zone_complete = True
  radius += 1
  for x in range(-1 * radius, radius + 1):

    current_location = (centroid[0] + x, centroid[1] - radius)
    if distance_sum(current_location, nodes) < safe_distance:
      safety_zone.add(current_location)
      safety_zone_complete = False

    current_location = (centroid[0] + x, centroid[1] + radius)
    if distance_sum(current_location, nodes) < safe_distance:
      safety_zone.add(current_location)
      safety_zone_complete = False

  for y in range(-1 * radius + 1, radius):

    current_location = (centroid[0] - radius, centroid[1] + y)
    if distance_sum(current_location, nodes) < safe_distance:
      safety_zone.add(current_location)
      safety_zone_complete = False

    current_location = (centroid[0] + radius, centroid[1] + y)
    if distance_sum(current_location, nodes) < safe_distance:
      safety_zone.add(current_location)
      safety_zone_complete = False

print(len(safety_zone))
