import numpy as np
import matplotlib.pyplot as plt
import collections
import csv
import datetime

DataPoint = collections.namedtuple("DataPoint", ["timestamp", "pressure", "serial_number",
                                                 "handset_state", "cellheater_state"])

# read in data file
dp = []
for line in csv.reader(open("UUT1-3.csv", "r"), skipinitialspace=True):
    data = DataPoint._make(line)
    dp.append(data)

# discard headers
dp.pop(0)

# get s/n from last entry
serial_number = data.serial_number
print(serial_number)

# separate into each blow by timestamp
blows = []
x = []
y = []
for p in dp:
    sample_time = datetime.datetime.strptime(p.timestamp, "%H:%M:%S.%f")

    try:
        if (sample_time - x[-1]) > datetime.timedelta(seconds=10):
            blows.append([x.copy(), y.copy()])
            x.clear()
            y.clear()
    except IndexError:
        pass

    x.append(sample_time)
    y.append(p.pressure)
blows.append([x, y])

# convert all datetime to time
for x, y in blows:
    x = list(map(lambda z: z.time(), x))
    print(x)

fig, ax = plt.subplots()

colors = ['b', 'g', 'r', 'y', 'k']
x = range(len(blows[0][0]))
for i, blow in enumerate(blows):
    ax.plot(x, blow[1])
plt.show()
exit(1)

# x = np.linspace(0, 2*np.pi, 50)
# y = np.sin(x)
# y2 = y + 0.1 * np.random.normal(size=x.shape)

fig, ax = plt.subplots()
ax.plot(x, y, 'k--')
# ax.plot(x, y2, 'ro')

# set ticks and tick labels
ax.set_xlim((0, 2*np.pi))
ax.set_xticks([0, np.pi, 2*np.pi])
ax.set_xticklabels(['0', '$\pi$','2$\pi$'])
ax.set_ylim((-1.5, 1.5))
ax.set_yticks([-1, 0, 1])

# Only draw spine between the y-ticks
ax.spines['left'].set_bounds(-1, 1)
# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.show()
