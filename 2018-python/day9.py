import re

num_players, highest_marble = [int(value) for value in re.match('(\d+).* (\d+).*', input().strip()).groups()]

# Part 1: Create a new array representing the circle of marbles at each turn

def take_turn(marbles, current_index, new_marble):
  if new_marble % 23 == 0:
    remove_index = (current_index - 7) % len(marbles)
    score = new_marble + marbles[remove_index]
    marbles = marbles[:remove_index] + marbles[remove_index + 1:]
    return [marbles, remove_index, score]
  else:
    insert_index = (current_index + 2) % len(marbles)
    marbles = marbles[:insert_index] + [new_marble] + marbles[insert_index:]
    return [marbles, insert_index, 0]

scores = [0] * num_players
player = 0
marbles = [0]
current_index = 0
for marble in range(1, highest_marble + 1):
  marbles, current_index, score = take_turn(marbles, current_index, marble)
  scores[player % len(scores)] += score
  player += 1

print(max(scores))

# Part 2: Modify a doubly linked list at each turn of the marble game, tracking the scores as we go

class Marble:
  def __init__(self, value, previous = None, next = None):
    self.value = value
    self.previous = previous
    self.next = next

def insert_after(marble, value):
  new_marble = Marble(value, marble, marble.next)
  new_marble.previous.next = new_marble
  new_marble.next.previous = new_marble
  return new_marble

def remove(marble):
  marble.previous.next = marble.next
  marble.next.previous = marble.previous
  return [marble.next, marble.value]

scores = [0] * num_players
player = 0
current_marble = Marble(0)
current_marble.next = current_marble
current_marble.previous = current_marble
for marble_value in range(1, highest_marble * 100 + 1):
  if marble_value % 23 == 0:
    [current_marble, removed_value] = remove(current_marble.previous.previous.previous.previous.previous.previous.previous)
    scores[player % len(scores)] += marble_value + removed_value
  else:
    current_marble = insert_after(current_marble.next, marble_value)
  player += 1

print(max(scores))
