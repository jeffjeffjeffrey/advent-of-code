import sys
import re

# Parse the input
data = []
for row in sys.stdin.readlines():
  fields = re.match('\[1518-(\d\d)-(\d\d) (\d\d):(\d\d)\] (.*)', row).groups()
  data += [{'month': int(fields[0]), 'day': int(fields[1]), 'hour': int(fields[2]), 'minute': int(fields[3]), 'action': fields[4]}]

# Sort the rows by date and time
log = sorted(data, key = lambda r: (r['month'], r['day'], r['hour'], r['minute']))

# Create minute-by-minute sleep log
current_guard = None
sleep_start_minute = None
asleep_times = {}
for row in log:
  if row['action'] == 'falls asleep':
    sleep_start_minute = row['minute']
  elif row['action'] == 'wakes up':
    for m in range(sleep_start_minute, row['minute']):
      if current_guard not in asleep_times:
        asleep_times[current_guard] = [0] * 60
      asleep_times[current_guard][m] += 1
  else:
    current_guard = int(re.match('Guard #(\d*) begins shift', row['action']).groups()[0])

# Part 1: Find the guard with the most total minutes asleep, and then find his sleepiest minute
sleepiest_guard = max(asleep_times.keys(), key = (lambda k: sum(asleep_times[k])))
sleepiest_minute = max(range(60), key = (lambda k: asleep_times[sleepiest_guard][k]))

print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)

# Part 2: Find the guard asleep most often in a single minute, and then find his sleepiest minute
sleepiest_guard = max(asleep_times.keys(), key = (lambda k: max(asleep_times[k])))
sleepiest_minute = max(range(60), key = (lambda k: asleep_times[sleepiest_guard][k]))

print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)
