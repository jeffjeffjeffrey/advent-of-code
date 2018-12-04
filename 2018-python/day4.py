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
      asleep_times[current_guard] = asleep_times.get(current_guard, {})
      asleep_times[current_guard][m] = asleep_times[current_guard].get(m, 0) + 1
  else:
    current_guard = int(re.match('Guard #(\d*) begins shift', row['action']).groups()[0])

# Part 1
guard_totals = {}
for guard in asleep_times:
  guard_totals[guard] = sum(v for v in asleep_times[guard].values())

def key_of_max_value(dictionary):
  return max(dictionary.keys(), key = (lambda k: dictionary[k]))

sleepiest_guard = key_of_max_value(guard_totals)
sleepiest_minute = key_of_max_value(asleep_times[sleepiest_guard])

print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)

# Part 2
sleepiest_minutes = {}
for guard in asleep_times:
  sleepiest_minute = key_of_max_value(asleep_times[guard])
  sleepiest_minutes[guard] = (sleepiest_minute, asleep_times[guard][sleepiest_minute])

sleepiest_guard = max(sleepiest_minutes.keys(), key = (lambda k: sleepiest_minutes[k][1]))
sleepiest_minute = sleepiest_minutes[sleepiest_guard][0]

print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)
