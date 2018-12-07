import sys
import re

graph = [re.match('Step (.).*step (.).*', row).groups() for row in sys.stdin.readlines()]

# Part 1

# Step 1: create dicts of targets and dependency counts for each node in the directed graph
targets = {}
dependency_counts = {}
for source, target in graph:
  if source not in targets:
    targets[source] = set(())
  targets[source].add(target)
  dependency_counts[source] = dependency_counts.get(source, 0)
  dependency_counts[target] = dependency_counts.get(target, 0) + 1

ordering = ''
while len(dependency_counts) > 0:
  current_step = sorted(dependency_counts.keys(), key = (lambda k: (dependency_counts[k], k)))[0]
  del dependency_counts[current_step]
  for target in targets.pop(current_step, []):
    dependency_counts[target] -= 1
  ordering += current_step

print(ordering)

# Part 2

# Step 1: create dicts of targets and dependency counts for each node in the directed graph
targets = {}
dependency_counts = {}
for source, target in graph:
  if source not in targets:
    targets[source] = set(())
  targets[source].add(target)
  dependency_counts[source] = dependency_counts.get(source, 0)
  dependency_counts[target] = dependency_counts.get(target, 0) + 1

def step_duration(step):
  return ord(step) - ord('A') + 1 + 60

time = -1
ordering = ''
total_steps = len(dependency_counts)
workers = [{'time_left': 0, 'step': None} for i in range(5)]

while len(ordering) < total_steps:
  time += 1
  # See who is done with their jobs
  for worker in workers:
    if worker['step'] and worker['time_left'] == 0: # if worker is done with their job, then remove it from the targets dict and reduce its dependent steps
      for target in targets.pop(worker['step'], []):
        dependency_counts[target] -= 1
      ordering += worker['step']
      worker['step'] = None

  # Now assign available steps to available workers and increment time left for all workers
  for worker in workers:
    if worker['time_left'] == 0 and len(dependency_counts) > 0:
      current_step = sorted(dependency_counts.keys(), key = (lambda k: (dependency_counts[k], k)))[0]
      if dependency_counts[current_step] == 0: # If the next step is available, put the worker to work
        del dependency_counts[current_step]
        worker['time_left'] = step_duration(current_step) - 1
        worker['step'] = current_step
    elif worker['step']: # If the worker is still working, increment their time left
      worker['time_left'] -= 1

print(time)
