# coding=utf-8
from Tkinter import *
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
import sys
#from sdk import *
sys.setrecursionlimit(10000) # 10000 is an example, try with different values
file_test = open("testfile.dat","w") # abrir archivo donde se va a guardar las lecturas del sensor de vrep
MAP_SIZE_PIXELS         = 300
MAP_SIZE_METERS         = 30


from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import RPLidar as LaserModel
#from breezylidar import URG04LX as Lidar
from pltslamshow import SlamShow
from PIL import Image
from rrt_with_pathsmoothing import *

global slam
global display
global mapbytes
slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS,1)
# Set up a SLAM display
display = SlamShow(MAP_SIZE_PIXELS, MAP_SIZE_METERS * 1000 / MAP_SIZE_PIXELS, 'SLAM')
# Initialize empty map
mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)



class Application(Frame):

    def __init__(self, master=None):  #Correr esta aplicación cuando se inicializa la ventana FRAME


        try:
            import vrep
        except:
            print ('--------------------------------------------------------------')
            print ('"vrep.py" could not be imported. This means very probably that')
            print ('either "vrep.py" or the remoteApi library could not be found.')
            print ('Make sure both are in the same folder as this file,')
            print ('or appropriately adjust the file "vrep.py"')
            print ('--------------------------------------------------------------')
            print ('')
        Frame.__init__(self, master)
        self.pack()  #inicializar variables globales
        self.createWidgets()

        self.name_hokuyo_data = StringVar()

        print ('Program started')


    def createWidgets(self):
        self.QUIT = Button(self)         ######## Boton para cerrar el programa ########
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self) ######## Boton mover hacia adelante ########
        self.hi_there["text"] = "Avanzar",
        self.hi_there["command"] = self.setvelocity
        self.hi_there.pack({"side": "left"})

        self.hi_there1 = Button(self)######## Boton mover el carro hacia atras ########
        self.hi_there1["text"] = "Atras",
        self.hi_there1["command"] = self.setvelocity_back
        self.hi_there1.pack({"side": "right"})

        self.hi_there2 = Button(self)######## Boton para girar a la derecha####
        self.hi_there2["text"] = "Derecha",
        self.hi_there2["command"] = self.setvelocity_right
        self.hi_there2.pack({"side": "right"})

        self.hi_there2 = Button(self)  ######## Boton para girar a la izquierda ########
        self.hi_there2["text"] = "Izquierda",
        self.hi_there2["command"] = self.setvelocity_left
        self.hi_there2.pack({"side": "right"})

        self.hi_there2 = Button(self)  ######## Boton para detener el carro ########
        self.hi_there2["text"] = "Detener",
        self.hi_there2["command"] = self.setvelocity_stop
        self.hi_there2.pack({"side": "right"})

        self.hi_there2 = Button(self)  ######## Boton para crear un trayectoria hay que espeficiar punto de partida y meta ########
        self.hi_there2["text"] = "Crear_Trayectoria",
        self.hi_there2["command"] = self.creartrayectoria
        self.hi_there2.pack({"side": "right"})

        self.hi_there2 = Button(self)  ######## Boton para seguir dos puntos o una sucesión de puntos ########
        self.hi_there2["text"] = "Seguir_Trayectoria",
        self.hi_there2["command"] = self.seguir
        self.hi_there2.pack({"side": "right"})

    def setvelocity(self):
        x=2
    def setvelocity_left(self):
        x="1"
    def setvelocity_right(self):
        x=2
    def setvelocity_stop(self):
        x=22
    def setvelocity_back(self):
        x=22
    def seguir(self):
        #usar la nueva funcion

        x=22
    def creartrayectoria(self):

        x=22

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

root = Tk()
app = Application(master=root)
root.after(2000, task) # repetir la función task cada 300 ms
app.mainloop()
root.destroy()
file_test.close()
save_movie("animationRplidar.gif",0.1)
# Now close the connection to V-REP:







