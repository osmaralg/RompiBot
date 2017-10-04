# coding=utf-8
from Tkinter import *
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
file_test = open("testfile.dat","w") # abrir archivo donde se va a guardar las lecturas del sensor de vrep
MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10
LIDAR_DEVICE            = '/dev/ttyACM0'

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import URG04LX as LaserModel
from breezylidar import URG04LX as Lidar

class Application(Frame):

    def __init__(self, master=None):
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
        x_inicial=0
        y_incial=0
        x_actual=0
        y_actual=0
        x_meta=200



def task(): 
    import vrep
    clientID = app.clientID.get()
    name_hokuyo_data = "hokuyo_data"
    print("Leyendo string")
    root.after(6, task)  # reschedule event in 2 seconds
    #returnCode, data = vrep.simxGetIntegerParameter(clientID, vrep.sim_intparam_mouse_x, vrep.simx_opmode_buffer)  # Try to retrieve the streamed data
    print("The clientID is:",clientID)
    e, lrf_bin = vrep.simxGetStringSignal(clientID, name_hokuyo_data, vrep.simx_opmode_buffer)
    print("this is data:", lrf_bin)
    #print("this is return code:", returnCode)
    print("return ok?", vrep.simx_return_ok)
    #if returnCode == vrep.simx_return_ok:  # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
    #    print ('Mouse position x: ', data)  # Mouse position x is actualized when the cursor is over V-REP's window
    lrf_raw = vrep.simxUnpackFloats(lrf_bin)
    lrf = np.array(lrf_raw).reshape(-1, 3)
    magnitud = np.arange(683)
    sec, msec = vrep.simxGetPingTime(clientID)
    print "Ping time: %f" % (sec + msec / 1000.)
    timesim = int(time.clock() * 1000000)
    timesim = str(timesim)
    file_test.write(timesim + "0 0 0 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 0 0 0 0")
    for i in range(0, 682):
        magnitud[i] = 1000 * math.sqrt(lrf[i, 0] * lrf[i, 0] + lrf[i, 1] * lrf[i, 1])
        magnitud[i] = int(magnitud[i])
        magnitud1 = np.array2string(magnitud[i])
        file_test.write(magnitud1 + " ")
    file_test.write("\n")
root = Tk()
app = Application(master=root)
root.after(300, task) # repetir la función task cada 300 ms 
app.mainloop()


root.destroy()
file_test.close()
import vrep
# Now close the connection to V-REP:
vrep.simxFinish(-1)






