import numpy as np
import matplotlib.pyplot as plt
import collections
import csv
import datetime
import glob
import sys

DataPoint = collections.namedtuple("DataPoint", ["timestamp", "pressure", "serial_number",
                                                 "handset_state", "cellheater_state"])
Point = collections.namedtuple('Point', ['x', 'y'])

blows = []

class Blow(object):
    def __init__(self, serial_number=None, volume=0, rate=0, samples=None, seq=0):
            """
            Blow object
            """
            self.volume = volume
            self.rate = rate
            self.samples = samples
            self.serial_number = serial_number
            self.seq = seq


def process_file(fn):
    global blows

    # read in data file
    dp = []
    for line in csv.reader(open(fn, "r"), skipinitialspace=True):
        data_pt = DataPoint._make(line)
        dp.append(data_pt)

    # discard headers
    dp.pop(0)

    # get s/n from last entry
    serial_number = dp[0].serial_number
    flow_rate = fn.split('-')[2][0]
    flow_rate = int(flow_rate)/10.0
    vol = float(fn.split('-')[1])
    print('Serial Number: {}   Volume: {}   Flow Rate: {}'.format(serial_number, vol, flow_rate))

    # separate into each blow by timestamp
    # x = []
    pts = []
    seq = 0
    for p in dp:
        sample_time = datetime.datetime.strptime(p.timestamp, "%H:%M:%S.%f")
        try:
            delta_time = sample_time - pts[-1].x
            if delta_time > datetime.timedelta(seconds=10):
                blows.append(Blow(serial_number, vol, flow_rate, pts.copy(), seq))
                seq += 1
                # x.clear()
                pts.clear()
            elif delta_time > datetime.timedelta(microseconds=60000):
                print('Boo!', delta_time)
        except IndexError:
            pass

        # x.append(sample_time)
        # y.append(p.pressure)
        pts.append(Point(x=sample_time, y=p.pressure))

    blows.append(Blow(serial_number, vol, flow_rate, pts, seq))
    print('Number of blows processed: {}'.format(seq+1))
    print(blows[0])

    # convert all datetime to time
    # for x, y in blows:
    #     x = list(map(lambda z: z.time(), x))
    #     y = list(map(int, y))
    #     print(x)
    #     print(y)

    # find avg
    return

def run_stats():
    out_data = []
    start_ts = 0
    end_ts = 0
    for i, blow in enumerate(blows):
        length = len(blow[0])
        y = list(map(int, blow[1]))
        blow_max = max(y)
        blow_min = min(y)
        threshold = blow_max * 0.7
        peak = [x for x in y if x > threshold]
        # print(peak[:8], peak[-8:])
        # print(len(peak))
        peak_avg = np.mean(peak)
        for j, pt in enumerate(y):
            if pt > threshold:
                start_ts = blow[0][j]
        for k, pt in enumerate(y[::-1]):
            if pt > threshold:
                end_ts = blow[0][length-k-1]

        blow_time = start_ts-end_ts

        # this kludge because no formatting for timedelta
        # print(blow_time)
        sec, us = str(blow_time).split(':')[2].split('.')
        sec = int(sec)
        us = int(us[:3])
        # print('{:d}.{:d},'.format(sec, us))

        blow_time = sec + us/1000.0
        report_str = 'Sample {}:  length={}  max={}  min={} threshold={:.3f} avg={:.3f} time={:.3f}'
        print(report_str.format(i, length, blow_max, blow_min, threshold, peak_avg, blow_time))
        out_data.append([serial_number, flow_rate, i, peak_avg, blow_time, blow_max, blow_min])

    total = 0
    for x in out_data[1:]:
        total += x[3]

    out_summary = [serial_number, flow_rate, total / 4.0]

    with open('out.csv', 'a', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(out_summary)


def plot_it(blows, serial_number='None'):
    # do the plotting
    fig, ax = plt.subplots()
    # colors = ['b', 'g', 'r', 'y', 'k']
    plt.title(serial_number)
    plt.legend()
    for i, blow in enumerate(blows):
        x = range(len(blow[0]))
        ax.plot(x, blow[1], label='Blow %d' % i)
        ax.legend(loc='lower center')
    plt.show()


# region plotting stuff
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
# endregion

def correct_missing_samples():
    global blows

    for blow in blows:
        new_samples = blow.samples.copy()
        print('Starting samples: {}'.format(len(new_samples)))
        clean = False
        while not clean:
            clean, new_samples = fix_missing(new_samples)
        print('Ending samples: {}'.format(len(new_samples)))
        blow.samples = new_samples


def fix_missing(blow):
    new_samples = []
    original_samples = blow
    # print('Starting samples: {}'.format(len(original_samples)))
    clean = True
    for i, point in enumerate(original_samples):
        try:
            delta_time = point.x - original_samples[i - 1].x
            if delta_time > datetime.timedelta(microseconds=60000):
                print('Boo!', delta_time)
                pt = Point(original_samples[i - 1].x + delta_time/2.0,
                           str((float(original_samples[i - 1].y) + float(original_samples[i].y))/2.0))
                new_samples.append(pt)
                new_samples.append(point)
                clean = False
            else:
                new_samples.append(point)
        except IndexError:
            pass
    return clean, new_samples


def out_file(limit=None):
    for blow in blows:
        fn = '{}-{}-{}_{}.csv'.format(blow.serial_number, blow.volume, blow.rate, blow.seq)
        with(open(fn, 'w')) as f:
            for pt in blow.samples:
                if limit is None:
                    print('{},{}'.format(pt.x, pt.y), file=f)
                elif float(pt.y) > limit:
                    print('{},{}'.format(pt.x, pt.y), file=f)


def main():
    # for arg in sys.argv:
    #    print(arg)

    args = glob.glob(sys.argv[1])
    for file in args:
        print(file)
        process_file(file)
        
    correct_missing_samples()
    out_file(20000)
    # run_stats()

if __name__ == '__main__':
    main()
