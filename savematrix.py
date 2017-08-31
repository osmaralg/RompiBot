filename = 'testfile.dat' # (datadir, dataset)
print('Loading data from %s...' % filename)
    
fd = open(filename, 'rt')
    
timestamps = []
scans = []
odometries = []
    
while True:  #leer todas las lineas a menos que esten vacias y seperarlas en un vector toks[1xn] 
        
    s = fd.readline() #leer linea
        
    if len(s) == 0: # si no hay nada en la linea salir 
            break       
            
    toks = s.split()[0:-1] # ignore '' #usar espacio como separador desde el inicio 0 al final -1

    timestamp = int(toks[0]) # timestap = primer columna string to integer 

    odometry = timestamp, int(toks[2]), int(toks[3])
                        
    lidar = [int(tok) for tok in toks[24:]] 

    timestamps.append(timestamp) #crear columna
    scans.append(lidar) #matriz lidar [nx400]
    odometries.append(odometry) #matriz odometry [nx3]
    #print(scans)
    length=len(lidar)
    print(length)    
fd.close()
