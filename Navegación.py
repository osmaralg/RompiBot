# coding=utf-8
from Tkinter import *
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
import sys
sys.setrecursionlimit(10000) # 10000 is an example, try with different values
file_test = open("testfile.dat","w") # abrir archivo donde se va a guardar las lecturas del sensor de vrep
MAP_SIZE_PIXELS         = 300
MAP_SIZE_METERS         = 30


from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import URG04LX as LaserModel
from rompibot import RompiBot
#from breezylidar import URG04LX as Lidar
from pltslamshow import SlamShow

global slam
global display
global mapbytes
global robot

robot = RompiBot()


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
            _, simtime = vrep.simxGetFloatSignal(clientID, "mySimulationTime", vrep.simx_opmode_streaming)
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
            print ("Stopping all motors, waiting 2 seconds for sensor data streaming")
            velocity = 0
            vrep.simxSetJointTargetVelocity(clientID, back_left, velocity, vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, back_right, velocity, vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, front_right, velocity, vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, front_left, velocity, vrep.simx_opmode_blocking)
            global left_inicial
            global right_inicial
            _,left_inicial = vrep.simxGetJointPosition(clientID,back_left,vrep.simx_opmode_blocking)
            _,right_inicial = vrep.simxGetJointPosition(clientID,back_right,vrep.simx_opmode_blocking)
            left_inicial = math.degrees(left_inicial)
            right_inicial = math.degrees(right_inicial)

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

        self.hi_there2 = Button(self)  ######## Boton para seguir dos puntos o una sucesión de puntos ########
        self.hi_there2["text"] = "Explorar",
        self.hi_there2["command"] = self.navegar
        self.hi_there2.pack({"side": "right"})

    def setvelocity(self):
        import vrep
        velocity = 2
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
        velocity = 2
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
        velocity = 2
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
        velocity = -2
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
        #print "seguir trayectoria!!!!!!!!!!!!!!!!!!!!!!!!!"
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
	
        x_actual=x
        y_actual=y
        theta1 = theta

        division = theta / 360
        theta1 = theta - math.floor(division)*360
        theta_actual=math.radians(theta1)
        print "x actual",x
        print "y actual",y
        print "theta actual es radianes", theta_actual
        print "theta actual es en grados", theta1


	
        x_meta=16000
        y_meta=15000
        k=1 #ganancia de velocidad
	
        theta_meta=math.atan2((y_meta-y_actual+.00001),(x_meta-x_actual))+math.pi/2 # -menos posicion inicial
        print "theta meta es en radianes", theta_meta
        print "theta meta es en grados", math.degrees(theta_meta    )
        errotheta=theta_meta-theta_actual
        v=k*errotheta
        velocity_left=-v
        velocity_right=v

        error_pos = math.sqrt((x_meta - x_actual) * (x_meta - x_actual) + (y_meta - y_actual) * (y_meta - y_actual))

        if errotheta< .1:
            if errotheta> -.1:

                print "error en pos es:", error_pos
                velocity_left=k*error_pos
                velocity_right=k*error_pos
        limit = .2
        if velocity_left > limit:
            velocity_left=limit

        if velocity_left<-limit:
            velocity_left=-limit
        if velocity_right>limit:
            velocity_right=limit
        if velocity_right<-limit:
            velocity_right=-limit
        print "error theta es: ", errotheta
        print "velocity es :", velocity_right
		

	#print "velocidad left: ", velocity_left
	#print "velocidad right: ", velocity_right
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity_left, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity_left, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity_right, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity_right, vrep.simx_opmode_blocking)
        if error_pos > 150:
        	root.after(80,self.seguir)
        else:
            self.setvelocity_stop()
    def creartrayectoria(self):
        x_inicial=0
        y_incial=0
        x_actual=0
        y_actual=0
        x_meta=200

    # calidad del mapa, anchura del hoyo  calidad del mapa = persistencia del mapa que tan rapido cambio de no hay obstaculo a si hay obstaculo, numero maximo de iteraciones, aumentando el numero de iteraciones, RMHC

    def navegar(self):

        print magnitud[3]
        if magnitud[2]>3000:
            self.setvelocity()

        print "estoy navegando"
        time.sleep(3)
        root.after(1000,self.navegar())



def task():  #Esta función se llama cada 300 ms que es el tiempo de ping entre el scrpit de python y V-REP

    # Connect to Lidar unit
    # lidar = Lidar(LIDAR_DEVICE)
    # Create an RMHC SLAM object with a laser model and optional robot model



    import vrep
    clientID = app.clientID.get()
    name_hokuyo_data = "hokuyo_data"
    print("Leyendo string")

    #returnCode, data = vrep.simxGetIntegerParameter(clientID, vrep.sim_intparam_mouse_x, vrep.simx_opmode_buffer)  # Try to retrieve the streamed data
    print("The clientID is:",clientID)
    _, back_left = vrep.simxGetObjectHandle(clientID, 'back_left_motor', vrep.simx_opmode_blocking)
    _, back_right = vrep.simxGetObjectHandle(clientID, 'back_right_motor', vrep.simx_opmode_blocking)
    e, lrf_bin = vrep.simxGetStringSignal(clientID, name_hokuyo_data, vrep.simx_opmode_buffer)
    _,pos_left = vrep.simxGetJointPosition(clientID,back_left,vrep.simx_opmode_blocking)
    _,pos_right = vrep.simxGetJointPosition(clientID,back_right,vrep.simx_opmode_blocking)
    _, simtime = vrep.simxGetFloatSignal(clientID, "mySimulationTime", vrep.simx_opmode_buffer)
    print "Simulation time from Vrep is:", simtime
    print("return ok?", vrep.simx_return_ok)
    #if returnCode == vrep.simx_return_ok:  # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
    #    print ('Mouse position x: ', data)  # Mouse position x is actualized when the cursor is over V-REP's window
    lrf_raw = vrep.simxUnpackFloats(lrf_bin)
    lrf = np.array(lrf_raw).reshape(-1, 3) #lrf da un vector de 3x683 que contiene un v=[vx vy vz]*683 la distancia vectorial del carro a un objetivo, siendo el carro el origen
    global magnitud
    magnitud = np.arange(683)
    sec, msec = vrep.simxGetPingTime(clientID)
    print "Ping time: %f" % (sec + msec / 1000.)
    timesim=simtime
    pos_left= -math.degrees(pos_left)
    pos_right = math.degrees(pos_right)
    if(pos_left<0):
        pos_left=pos_left+360
    if(pos_right<0):
        pos_right=pos_right+360


    print "pos left is:", pos_left
    print "pos right is:", pos_right


    odometries  = [timesim,pos_right,pos_left]
    print odometries
    timesim = str(timesim)
    pos_right = str(pos_right)
    pos_left = str(pos_left)
    file_test.write(timesim +" "+pos_left+" "+pos_right+"0 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 0 0 0")
    s=""
    for i in range(0, 683):
        magnitud[i] = 1000 * math.sqrt(lrf[i, 0] * lrf[i, 0] + lrf[i, 1] * lrf[i, 1])
        magnitud[i] = int(magnitud[i])
        if magnitud[i]>4500:
            magnitud[i]=0
        magnitud1 = np.array2string(magnitud[i])
        file_test.write(magnitud1 + " ")
        s = s + magnitud1 + " "
    file_test.write("\n")
    scans = []

    #print s

    toks = s.split()[0:-1]  # ignore ''
    #print toks
    lidar = [int(tok) for tok in toks[0:]]
    lengthlidar=len(lidar)
    print lengthlidar
    dxy,dtheta,dt =robot.computeVelocities(odometries)
    slam.update(lidar,(dxy,dtheta,dt)) #voy aqui convertir la lista de sting a una lista
    global x
    global y
    global theta
    # Get current robot position
    x, y, theta = slam.getpos()
    print "theta is: ", theta
    # Get current map bytes as grayscale
    slam.getmap(mapbytes)

    display.displayMap(mapbytes)

    display.setPose(x, y, theta)
    
    # Exit on ESCape
    key = display.refresh()
    if key != None and (key & 0x1A):
        exit(0)
    root.after(10, task)  # reschedule event in 1 ms

root = Tk()
app = Application(master=root)
root.after(1000, task) # repetir la función task cada 300 ms
app.mainloop()


root.destroy()
file_test.close()
import vrep
# Now close the connection to V-REP:
vrep.simxFinish(-1)



