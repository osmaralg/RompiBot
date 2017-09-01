from Tkinter import *
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
file_test = open("testfile.dat","w")


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
        self.pack()
        self.createWidgets()
        self.clientID = IntVar()
        self.back_left = IntVar()
        self.back_right = IntVar()
        self.front_left = IntVar()
        self.front_right = IntVar()
        print ('Program started')
        vrep.simxFinish(-1)  # just in case, close all opened connections
        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP
        self.clientID.set(clientID)
        if clientID != -1:
            print ('Connected to remote API server')
            # Now try to retrieve data in a blocking fashion (i.e. a service call):
            res, objs = vrep.simxGetObjects(clientID, vrep.sim_handle_all, vrep.simx_opmode_blocking)
            returnCode, back_left = vrep.simxGetObjectHandle(clientID, 'back_left_motor', vrep.simx_opmode_blocking)
            returnCode, back_right = vrep.simxGetObjectHandle(clientID, 'back_right_motor', vrep.simx_opmode_blocking)
            returnCode, front_left = vrep.simxGetObjectHandle(clientID, 'front_left_motor', vrep.simx_opmode_blocking)
            returnCode, front_right = vrep.simxGetObjectHandle(clientID, 'front_right_motor', vrep.simx_opmode_blocking)
            self.back_left.set(back_left)
            self.back_right.set(back_right)
            self.front_left.set(front_left)
            self.front_right.set(back_right)

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

        self.hi_there = Button(self) ######## Boton empezar conexion ########
        self.hi_there["text"] = "Avanzar",
        self.hi_there["command"] = self.setvelocity
        self.hi_there.pack({"side": "left"})

        self.hi_there1 = Button(self)######## Boton mover el carro ########
        self.hi_there1["text"] = "Atras",
        self.hi_there1["command"] = self.say_hi
        self.hi_there1.pack({"side": "right"})

        self.hi_there2 = Button(self)######## Boton para imprimir un texto ########
        self.hi_there2["text"] = "Derecha",
        self.hi_there2["command"] = self.say_hi
        self.hi_there2.pack({"side": "right"})

        self.hi_there2 = Button(self)  ######## Boton para imprimir un texto ########
        self.hi_there2["text"] = "Izquierda",
        self.hi_there2["command"] = self.say_hi
        self.hi_there2.pack({"side": "right"})
    def setvelocity(self):
        import vrep
        velocity = 100
        clientID = self.clientID.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
        vrep.simxSetJointTargetVelocity(clientID, self.back_left.get(), velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right, velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left, velocity, vrep.simx_opmode_blocking)
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()