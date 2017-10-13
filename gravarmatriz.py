

def load_data(datadir, dataset):
    filename = '%s/%s' % (datadir, dataset)
    print('Loading data from %s...' % filename)

    fd = open(filename, 'rt')
    while True:

        s = fd.readline()

        if len(s) == 0:
            break

        toks = s.split()[0:-1]  # ignore ''


        lidar = [int(tok) for tok in toks[0:330]]
        size = len(lidar)




    fd.close()

    return lidar, size


def main():
    lidar,size = load_data(".","exp1.txt")
    print "lidar is "
    print lidar
    print "lidar size is "
    print size

main()
