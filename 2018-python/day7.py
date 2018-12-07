import sys
import re

# Part 1

# Create a dict mapping each task to a list of the tasks that depend on it, excluding tasks with no dependencies
dependencies = {}
for step, dependent in [re.match('Step (.).*step (.).*', row).groups() for row in sys.stdin.readlines()]:
  dependencies[step] = dependencies.get(step, []) + [dependent]

# Create a dict of prereq counts for each task, including tasks with no prerequisites
def get_prereq_counts(dependencies):
  prereq_counts = {}
  for step in dependencies:
    for dependent in dependencies[step]:
      prereq_counts[step] = prereq_counts.get(step, 0)
      prereq_counts[dependent] = prereq_counts.get(dependent, 0) + 1
  return prereq_counts

def get_first_step(prereq_counts):
  return sorted(prereq_counts.keys(), key = (lambda k: (prereq_counts[k], k)))[0]

prereq_counts = get_prereq_counts(dependencies)
total_steps = len(prereq_counts)
ordering = ''

# Find the topological ordering by popping the first available step, decrementing its dependents' prereq counts, and repeating
while len(ordering) < total_steps:
  step = get_first_step(prereq_counts)
  del prereq_counts[step]
  for dependent in dependencies.get(step, []):
    prereq_counts[dependent] -= 1
  ordering += step

print(ordering)

# Part 2

def step_duration(step):
  return ord(step) - ord('A') + 1 + 60

# Create workers with state that tracks the step they're working on and how much time they have left to complete it
workers = [{'step': None, 'time_left': 0} for i in range(5)]
prereq_counts = get_prereq_counts(dependencies)
time = -1
ordering = ''

while len(ordering) < total_steps:
  time += 1
  # See which occupied workers are done with their steps, and add completed steps to the overall ordering
  for worker in workers:
    if worker['step'] and worker['time_left'] == 0:
      for dependent in dependencies.get(worker['step'], []):
        prereq_counts[dependent] -= 1
      ordering += worker['step']
      worker['step'] = None

  # Assign available steps to available workers and decrement time left for all occupied workers
  for worker in workers:
    if worker['time_left'] == 0 and len(prereq_counts) > 0:
      step = get_first_step(prereq_counts)
      if prereq_counts[step] == 0:
        del prereq_counts[step]
        worker['step'] = step
        worker['time_left'] = step_duration(step) - 1
    elif worker['step']:
      worker['time_left'] -= 1

print(time)
