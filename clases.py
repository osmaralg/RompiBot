
# coding=utf-8

def load_data(datadir, dataset):
    filename = '%s/%s' % (datadir, dataset)
    print('Loading data from %s...' % filename)

    fd = open(filename, 'rt')
    while True:

        s = fd.readline()

        if len(s) == 0:
            break
        toks = s.split()[0:-1]  # ignore ''
        lidar = [int(tok) for tok in toks[0:300]]
        size = len(lidar)
    fd.close()

    return lidar, size

def task():  #Esta función se llama cada 300 ms que es el tiempo de ping entre el scrpit de python y V-REP

    root.after(101, task)
    # Load the data from the file, ignoring timestamps
    lidar,size = load_data('.', "example.txt")

    slam.update(lidar) #voy aqui convertir la lista de sting a una lista
    # Get current robot position
    x, y, theta = slam.getpos()

    # Get current map bytes as grayscale
    slam.getmap(mapbytes)
    print "slam.getmap"
    display.displayMap(mapbytes)
    print "display"
    display.setPose(x, y, theta)
    print "displaypose"
    image = Image.frombuffer('L', (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), mapbytes, 'raw', 'L', 0, 1)
    image.save('hola.png')
    save_frame()
    save_last_frame()
    # Exit on ESCape
    key = display.refresh()
    if key != None and (key & 0x1A):
        exit(0)
