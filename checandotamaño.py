# Method to load all from file ------------------------------------------------
# Each line in the file has the format:
#
#  TIMESTAMP  ... Q1  Q1 ... Distances
#  (usec)                    (mm)
#  0          ... 2   3  ... 24 ...
#
# where Q1, Q2 are odometry values


filename = '%s/%s.dat' % (datadir, dataset)
print('Loading data from %s...' % filename)

fd = open(filename, 'rt')

timestamps = []
scans = []
odometries = []

while True:

    s = fd.readline()

    if len(s) == 0:
        break

    toks = s.split()[0:-1]  # ignore ''

    timestamp = int(toks[0])

        odometry = timestamp, int(toks[2]), int(toks[3])

        lidar = [int(tok) for tok in toks[24:]]

        timestamps.append(timestamp)
        scans.append(lidar)
        odometries.append(odometry)

    fd.close()

    return timestamps, scans, odometries