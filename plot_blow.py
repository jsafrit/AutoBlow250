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
    data_pt = DataPoint._make(line)
    dp.append(data_pt)

# discard headers
dp.pop(0)

# get s/n from last entry
serial_number = dp[0].serial_number
print(serial_number)

# separate into each blow by timestamp
blows = []
x = []
y = []
for p in dp:
    sample_time = datetime.datetime.strptime(p.timestamp, "%H:%M:%S.%f")
    try:
        delta_time = sample_time - x[-1]
        if delta_time > datetime.timedelta(seconds=10):
            blows.append([x.copy(), y.copy()])
            x.clear()
            y.clear()
        elif delta_time > datetime.timedelta(microseconds=60000):
            print('Boo!', delta_time)
    except IndexError:
        pass

    x.append(sample_time)
    y.append(p.pressure)
blows.append([x, y])

# convert all datetime to time
# for x, y in blows:
#     x = list(map(lambda z: z.time(), x))
#     y = list(map(int, y))
#     print(x)
#     print(y)

# find avg
for i, blow in enumerate(blows):
    length = len(blow[0])
    y = list(map(int, blow[1]))
    blow_max = max(y)
    blow_min = min(y)
    threshold = blow_max * 0.75
    peak = [x for x in y if x > threshold]
    print(peak[:8], peak[-8:])
    print(len(peak))
    peak_avg = np.mean(peak)

    print('Sample {}:  length={}  max={}  min={} threshold={} avg={}'.format(i, length, blow_max, blow_min,
                                                                             threshold, peak_avg))


# do the plotting
fig, ax = plt.subplots()
colors = ['b', 'g', 'r', 'y', 'k']
plt.title(serial_number)
plt.legend()
x = range(len(blows[0][0]))
for i, blow in enumerate(blows):
    ax.plot(x, blow[1], label='Blow %d' % i)
    ax.legend(loc='lower center')

plt.show()

exit(1)

# x = np.linspace(0, 2*np.pi, 50)
# y = np.sin(x)
# y2 = y + 0.1 * np.random.normal(size=x.shape)

# fig, ax = plt.subplots()
# ax.plot(x, y, 'k--')
# # ax.plot(x, y2, 'ro')
#
# # set ticks and tick labels
# ax.set_xlim((0, 2*np.pi))
# ax.set_xticks([0, np.pi, 2*np.pi])
# ax.set_xticklabels(['0', '$\pi$','2$\pi$'])
# ax.set_ylim((-1.5, 1.5))
# ax.set_yticks([-1, 0, 1])
#
# # Only draw spine between the y-ticks
# ax.spines['left'].set_bounds(-1, 1)
# # Hide the right and top spines
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# # Only show ticks on the left and bottom spines
# ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_ticks_position('bottom')
#
# plt.show()
