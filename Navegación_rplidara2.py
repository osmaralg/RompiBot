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

global slam
global display
global mapbytes
slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
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
        self.clientID = IntVar()
        self.back_left = IntVar()
        self.back_right = IntVar()
        self.front_left = IntVar()
        self.front_right = IntVar()
        self.name_hokuyo_data = StringVar()

        print ('Program started')
        vrep.simxFinish(-1)  # just in case, close all opened connections

        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP

        print("el clientId es %d", clientID)
        self.clientID.set(clientID)
        if clientID != -1:
            print ('Connected to remote API server')
            # Now try to retrieve data in a blocking fashion (i.e. a service call):
            res, objs = vrep.simxGetObjects(clientID, vrep.sim_handle_all, vrep.simx_opmode_blocking)
            returnCode, back_left = vrep.simxGetObjectHandle(clientID, 'back_left_motor', vrep.simx_opmode_blocking)
            returnCode, back_right = vrep.simxGetObjectHandle(clientID, 'back_right_motor', vrep.simx_opmode_blocking)
            returnCode, front_left = vrep.simxGetObjectHandle(clientID, 'front_left_motor', vrep.simx_opmode_blocking)
            returnCode, front_right = vrep.simxGetObjectHandle(clientID, 'front_right_motor', vrep.simx_opmode_blocking)

            name_hokuyo_data = "hokuyo_data"
            vrep.simxGetStringSignal(clientID, name_hokuyo_data, vrep.simx_opmode_streaming)

            self.back_left.set(back_left)
            self.back_right.set(back_right)
            self.front_left.set(front_left)
            self.front_right.set(front_right)


            if returnCode == vrep.simx_return_ok:
                print ('Corrio bien la lectura del handle')
            else:
                print ('Remote API function call returned with error code: ', returnCode)
                print ('No sirvio el returnCode')
            print ('left_motor handle is:', back_left)
            print ('left_motor handle is:', front_left)
            print ('back right_motor handle is:', back_right)
            print ('right_motor handle is:', front_right)
    def say_hi(self):
        print "hi there, everyone estoy usando variables globales!"
        print ("back right motor handle is",self.back_right.get())
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
        import vrep
        velocity = 10
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity, vrep.simx_opmode_blocking)
    def setvelocity_left(self):
        import vrep
        velocity = 10
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        vrep.simxSetJointTargetVelocity(clientID, back_left,   -velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  -velocity, vrep.simx_opmode_blocking)
    def setvelocity_right(self):
        import vrep
        velocity = 10
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  -velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, -velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity, vrep.simx_opmode_blocking)
    def setvelocity_stop(self):
        import vrep
        velocity = 0
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity, vrep.simx_opmode_blocking)
    def setvelocity_back(self):
        import vrep
        velocity = -10
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity, vrep.simx_opmode_blocking)
    def seguir(self):
        import vrep
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        x_inicial=0
        y_incial=0
        x_actual=0
        y_actual=0
        theta_actual=0;
        x_meta=200
        y_meta=200
        k=10 #ganancia de velocidad
        v=k*theta
        theta_meta=math.atan((y_meta-y_incial)/(x_meta-x_inicial))
        errotheta=theta_meta-theta
        v=k*errotheta
        velocity_left=v
        velocity_right=-v
        if errotheta<.5:
            if errotheta>-.5:
                v=math.sqrt((x_meta-x_actual)^2+(y_meta-y_actual)^2)
                velocity_left=v
                velocity_right=v
               
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity_left, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity_left, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity_right, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity_right, vrep.simx_opmode_blocking)
        
    def creartrayectoria(self):


        x_meta=200
        y_meta = 200
        x, y, theta = slam.getpos()





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
import vrep
# Now close the connection to V-REP:







