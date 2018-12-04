import sys
import re

# Record the number of times each guard is asleep for each minute of the midnight hour
guard = None
sleep_start_minute = None
asleep_times = {}
for row in sorted([row.strip() for row in sys.stdin.readlines()]):
  minute = int(re.match('.*:(\d\d)\].*', row).groups()[0])
  action = re.match('.*\] (.*)', row).groups()[0]
  if action == 'falls asleep':
    sleep_start_minute = minute
  elif action == 'wakes up':
    for m in range(sleep_start_minute, minute):
      if guard not in asleep_times:
        asleep_times[guard] = [0] * 60
      asleep_times[guard][m] += 1
  else:
    guard = int(re.match('.*#(\d*) .*', action).groups()[0])

# Part 1: Find the guard with the most total minutes asleep, and then find their sleepiest minute
sleepiest_guard = max(asleep_times.keys(), key = (lambda k: sum(asleep_times[k])))
sleepiest_minute = max(range(60), key = (lambda k: asleep_times[sleepiest_guard][k]))
print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)

# Part 2: Find the guard asleep most often in a single minute, and then find their sleepiest minute
sleepiest_guard = max(asleep_times.keys(), key = (lambda k: max(asleep_times[k])))
sleepiest_minute = max(range(60), key = (lambda k: asleep_times[sleepiest_guard][k]))
print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)
