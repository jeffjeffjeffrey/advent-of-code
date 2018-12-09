import re

num_players, highest_marble = [int(value) for value in re.match('(\d+).* (\d+).*', input().strip()).groups()]

# Part 1: Create a new array representing the circle of marbles at each turn

scores = [0] * num_players

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

player = 0
marbles = [0]
current_index = 0
for marble in range(1, highest_marble + 1):
  marbles, current_index, score = take_turn(marbles, current_index, marble)
  scores[player % len(scores)] += score
  player += 1

print(max(scores))

# Part 2: Modify a doubly linked list at each turn of the marble game

scores = [0] * num_players

class Marble:
  def __init__(self, value):
    self.value = value
    self.next = None
    self.previous = None

def insert_after(marble, value):
  new_marble = Marble(value)
  new_marble.next = marble.next
  new_marble.previous = marble
  new_marble.previous.next = new_marble
  new_marble.next.previous = new_marble
  return new_marble

def remove(marble):
  next_marble = marble.next
  next_marble.previous = marble.previous
  next_marble.previous.next = next_marble
  removed_score = marble.value
  del(marble)
  return [next_marble, removed_score]

player = 0
current_marble = Marble(0)
current_marble.next = current_marble
current_marble.previous = current_marble
for marble_value in range(1, highest_marble * 100 + 1):
  if marble_value % 23 == 0:
    [current_marble, removed_score] = remove(current_marble.previous.previous.previous.previous.previous.previous.previous)
    scores[player % len(scores)] += marble_value + removed_score
  else:
    current_marble = insert_after(current_marble.next, marble_value)
  player += 1

print(max(scores))
