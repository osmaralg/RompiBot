# coding=utf-8
from Tkinter import *
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
import sys


import random
import copy
from scipy import misc
import glob
import subprocess
from rrt_with_pathsmoothing import *

iframe = 0

class RRT():
    u"""
    Class for RRT Planning
    """

    def __init__(self, start, goal, obstacleList, randArea, expandDis=20, goalSampleRate=5, maxIter=300):
        u"""
        Setting Parameter

        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]

        """
        self.start = Node(start[0], start[1])
        self.end = Node(goal[0], goal[1])
        self.minrand = randArea[0]
        self.maxrand = randArea[1]
        self.expandDis = expandDis
        self.goalSampleRate = goalSampleRate
        self.maxIter = maxIter

    def Planning(self, animation=True):
        u"""
        Pathplanning

        animation: flag for animation on or off
        """

        self.nodeList = [self.start]
        while True:
            # Random Sampling
            if random.randint(0, 100) > self.goalSampleRate:
                rnd = [random.uniform(self.minrand, self.maxrand), random.uniform(self.minrand, self.maxrand)]
            else:
                rnd = [self.end.x, self.end.y]

            # Find nearest node
            nind = self.GetNearestListIndex(self.nodeList, rnd)
            # print(nind)

            # expand tree
            nearestNode = self.nodeList[nind]
            theta = math.atan2(rnd[1] - nearestNode.y, rnd[0] - nearestNode.x)

            newNode = copy.deepcopy(nearestNode)
            newNode.x += self.expandDis * math.cos(theta)
            newNode.y += self.expandDis * math.sin(theta)
            newNode.parent = nind

            if not self.__CollisionCheck(newNode, obstacleList):
                continue

            self.nodeList.append(newNode)

            # check goal
            dx = newNode.x - self.end.x
            dy = newNode.y - self.end.y
            d = math.sqrt(dx * dx + dy * dy)
            if d <= self.expandDis:
                print("Goal!!")
                break

            if animation:
                self.DrawGraph(rnd)

        path = [[self.end.x, self.end.y]]
        lastIndex = len(self.nodeList) - 1
        while self.nodeList[lastIndex].parent is not None:
            node = self.nodeList[lastIndex]
            path.append([node.x, node.y])
            lastIndex = node.parent
        print path
        return path

    def DrawGraph(self, rnd=None):
        import matplotlib.pyplot as plt
        plt.clf()
        if rnd is not None:
            plt.plot(rnd[0], rnd[1], "^k")
        for node in self.nodeList:
            if node.parent is not None:
                plt.plot([node.x, self.nodeList[node.parent].x], [node.y, self.nodeList[node.parent].y], "-g")
                # save_frame()  # save each frame
                plt.axis([0, 800, 0, 800])  ####################################### aqui
                plt.grid(True)
        for (x, y, size) in obstacleList:
            self.PlotCircle(x, y, size)

        plt.plot(self.start.x, self.start.y, "xr")
        plt.plot(self.end.x, self.end.y, "xr")
        # plt.axis([0, 800, 0, 800])
        plt.grid(True)
        plt.pause(0.001)

    def PlotCircle(self, x, y, size):
        deg = range(0, 360, 5)
        deg.append(0)
        xl = [x + size * math.cos(math.radians(d)) for d in deg]
        yl = [y + size * math.sin(math.radians(d)) for d in deg]
        plt.plot(xl, yl, "-k")

    def GetNearestListIndex(self, nodeList, rnd):
        dlist = [(node.x - rnd[0]) ** 2 + (node.y - rnd[1]) ** 2 for node in nodeList]
        minind = dlist.index(min(dlist))
        return minind

    def __CollisionCheck(self, node, obstacleList):

        for (ox, oy, size) in obstacleList:
            dx = ox - node.x
            dy = oy - node.y
            d = math.sqrt(dx * dx + dy * dy)
            if d <= size:
                return False  # collision

        return True  # safe
class Node():
    u"""
    RRT Node
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
def GetPathLength(path):
    l = 0
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        d = math.sqrt(dx * dx + dy * dy)
        l += d

    return l
def GetTargetPoint(path, targetL):
    l = 0
    ti = 0
    lastPairLen = 0
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        d = math.sqrt(dx * dx + dy * dy)
        l += d
        if l >= targetL:
            ti = i - 1
            lastPairLen = d
            break

    partRatio = (l - targetL) / lastPairLen
    #  print(partRatio)
    #  print((ti,len(path),path[ti],path[ti+1]))

    x = path[ti][0] + (path[ti + 1][0] - path[ti][0]) * partRatio
    y = path[ti][1] + (path[ti + 1][1] - path[ti][1]) * partRatio
    #  print((x,y))

    return [x, y, ti]
def LineCollisionCheck(first, second, obstacleList):
    # Line Equation

    x1 = first[0]
    y1 = first[1]
    x2 = second[0]
    y2 = second[1]

    try:
        a = y2 - y1
        b = -(x2 - x1)
        c = y2 * (x2 - x1) - x2 * (y2 - y1)
    except ZeroDivisionError:
        return False

    # print(first)
    #  print(second)

    for (ox, oy, size) in obstacleList:
        d = abs(a * ox + b * oy + c) / (math.sqrt(a * a + b * b))
        #  print((ox,oy,size,d))
        if d <= (size):
            #  print("NG")
            return False

    # print("OK")

    return True  # OK
def PathSmoothing(path, maxIter, obstacleList):
    #  print("PathSmoothing")

    l = GetPathLength(path)

    for i in range(maxIter):
        # Sample two points
        pickPoints = [random.uniform(0, l), random.uniform(0, l)]
        pickPoints.sort()
        #  print(pickPoints)
        first = GetTargetPoint(path, pickPoints[0])
        #  print(first)
        second = GetTargetPoint(path, pickPoints[1])
        #  print(second)

        if first[2] <= 0 or second[2] <= 0:
            continue

        if (second[2] + 1) > len(path):
            continue

        if second[2] == first[2]:
            continue

        # collision check
        if not LineCollisionCheck(first, second, obstacleList):
            continue

        # Create New path
        newPath = []
        newPath.extend(path[:first[2] + 1])
        newPath.append([first[0], first[1]])
        newPath.append([second[0], second[1]])
        newPath.extend(path[second[2] + 1:])
        path = newPath
        l = GetPathLength(path)

    return path


sys.setrecursionlimit(10000) # 10000 is an example, try with different values
file_test = open("testfile.dat","w") # abrir archivo donde se va a guardar las lecturas del sensor de vrep
MAP_SIZE_PIXELS         = 800
MAP_SIZE_METERS         = 30


from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import URG04LX as LaserModel
from rompibot import RompiBot
#from breezylidar import URG04LX as Lidar
from pltslamshow import SlamShow
from PIL import Image

global slam
global display
global mapbytes
global robot
global obstacleList
global donothing
global iframe




obstacleList=[]
iframe = 0
donothing = False


robot = RompiBot()


slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS,8)
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
        self.contador = IntVar()
        self.lenpath = IntVar()
        self.flag = IntVar()   # Variable para que la primera vez que se llame navegar espere 1 s despues cada 100 ms
        flag = 1
        self.flag2 = IntVar() # Variable para detener la navegación y cambiar a manual
        flag2 = 1
        self.flag1 = IntVar()
        print ('Program started')
        vrep.simxFinish(-1)  # just in case, close all opened connections

        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 30)  # Connect to V-REP

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
            self.flag.set(flag)
            self.flag2.set(flag2)
            self.contador.set(0)
            self.lenpath.set(0)

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
        self.flag2.set(1)
        velocity = 1
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
        velocity = .2
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
        velocity = .2
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
        self.flag2.set(0)
        self.flag1.set(1)
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
        velocity = -1
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
        print path
        lenpath = self.lenpath.get()
        contador = self.contador.get()
        #print "seguir trayectoria!!!!!!!!!!!!!!!!!!!!!!!!!"
        clientID = self.clientID.get()
        back_left = self.back_left.get()
        back_right = self.back_right.get()
        front_left = self.front_left.get()
        front_right = self.front_right.get()
	
        x_actual=x
        y_actual=y
        theta1 = theta
        print "la equis es", x_actual

        division = theta / 360
        theta1 = theta - math.floor(division)*360
        theta_actual=theta1
        print "x actual",x
        print "y actual",y
        print "theta actual es en grados", theta1

        print "el primer elemento de path es:"

        print path[contador]
        primero = path[contador]
        print "el segudno elemento del primer elementos es:"
        x_meta=primero[0]*30000/800
        y_meta=primero[1]*30000/800
        k=1 #ganancia de velocidad
	
        theta_meta=math.atan2((y_meta-y_actual+.00001),(x_meta-x_actual))+math.pi/2 # -menos posicion inicial
        theta_meta = math.degrees(theta_meta)
        if theta_meta<0:
            theta_meta=theta_meta+360
        print "theta meta es en grados", theta_meta
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

        for i in range(165,175):
            if magnitud[i]<1000:
                print "hay que girar"



        limit = .2
        if velocity_left > limit:
            velocity_left=limit

        if velocity_left<-.2:
            velocity_left=-.2
            velocity_right=.2
        if velocity_right>limit:
            velocity_right=limit
        if velocity_right<-.2:
            velocity_right=-.2
            velocity_left=.2
        print "error theta es: ", errotheta
        print "velocity es :", velocity_right
		

	#print "velocidad left: ", velocity_left
	#print "velocidad right: ", velocity_right
        vrep.simxSetJointTargetVelocity(clientID, back_left,   velocity_left, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_left,  velocity_left, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, back_right,  velocity_right, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, front_right, velocity_right, vrep.simx_opmode_blocking)
        if error_pos > 150:      # si ya llego al primer segmento de la trayectoria entonces caminar hacia el siguiente
        	root.after(80,self.seguir)  # si ha llegado al segmento entonces hay que volver a llamar la funcion
        else:
            contador = contador - 1   # si ya no hay más segmentos dentener el carro y ya no llamar más a esta funcion
            self.contador.set(contador)
            if contador < 1:
                self.setvelocity_stop
            else:
                root.after(80,self.seguir)


    def creartrayectoria(self):
        print "voy a crear una trayectoria"
        print "la x es :", x
        print "la y actual es :", y
        x_inicial=x*800/30000
        y_incial=y*800/30000
        x_meta = 400   #en pixeles
        y_meta = 400   #en pixeles
        print "la equis en pixeles es " ,x_inicial
        print "la y inicial es en pixeles:", y_incial
        import matplotlib.pyplot as plt
        # ====Search Path with RRT====
        # Parameter
        iframe = 0
        donothing = False
        for image_path in glob.glob("/home/osmaralg/Desktop/PythonRobotics/PathPlanning/RRT/hola.png"):
            image = misc.imread(image_path)
        print (image.shape)
        print (image.dtype)

        png = []
        for image_path in glob.glob("/home/osmaralg/Desktop/PythonRobotics/PathPlanning/RRT/hola.png"):
            png.append(misc.imread(image_path))

        im = np.asarray(png)

        ocupado = []
        print 'Importing done...', im.shape

        print im
        size = 800  # number of the pixels of the image
        pixel_inicial = 0 # apartir de que pixel tomar los puntos de ocupación
        resolution = 2  # step size pixel, if 1 evaluates every pixel if 4  every 4 pixels obstacle sambple
        obstaclesize = 13  # radious of the obstacle circle
        darkness = 127  # gray scale if 127 gray equals obstacle if 0 only black equals obstacle
        for j in range(pixel_inicial, size, resolution):
            for i in range(pixel_inicial, size, resolution):
                if im[0, i, j] < darkness:
                    im[0, i, j] = obstaclesize
                    coordenada = j, i, obstaclesize
                    ocupado.append(coordenada)
                else:
                    im[0, i, j] = 0
                    # print "espacio libre ",i,j

        obstacleList = ocupado
        print "la lenght de ocupado es : "
        print len(ocupado)
        global path
        rrt = RRT(start=[x_inicial, y_incial], goal=[x_meta, y_meta], randArea=[0, size], obstacleList=obstacleList)
        path = rrt.Planning(animation=False)
        print "lenght de path es :" ,len(path)
        self.lenpath.set(len(path))
        self.contador.set(len(path)-1)
        print path

    # calidad del mapa, anchura del hoyo  calidad del mapa = persistencia del mapa que tan rapido cambio de no hay obstaculo a si hay obstaculo, numero maximo de iteraciones, aumentando el numero de iteraciones, RMHC

    def navegar(self):
        flag = self.flag.get()
        flag2 = self.flag2.get()
        print flag
        print "esta es la distancia al frente"
        print magnitud[171]
        print "esta es la distancia a la derecha: ", magnitud[0]
        print "estoy navegando"


        self.setvelocity()

        if magnitud[171]<2000:
            self.setvelocity_right()
            print "hay un obstaculo a dos metros al frente"
            if magnitud[1]>600 or magnitud[1]==0:
                self.setvelocity_right()
            else:
                self.setvelocity()

                print "estamos muy pegados a la derecha vamos al frente un poco mas"





        if magnitud[171]==0:
            #checar que no hay nada a la izquierda si no que siga girando
            self.setvelocity()

        if flag ==1:
            time.sleep(1)
            self.flag.set(0)

        if flag2 == 1:
            root.after(100,self.navegar)



def task():  #Esta función se llama cada 300 ms que es el tiempo de ping entre el scrpit de python y V-REP

    # Connect to Lidar unit
    # lidar = Lidar(LIDAR_DEVICE)
    # Create an RMHC SLAM object with a laser model and optional robot model



    import vrep
    import matplotlib as plt
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
    timesim=simtime
    pos_left= -math.degrees(pos_left)
    pos_right = math.degrees(pos_right)
    if(pos_left<0):
        pos_left=pos_left+360
    if(pos_right<0):
        pos_right=pos_right+360


    print "pos left is:", pos_left
    print "pos right is:", pos_right


    odometries  = [timesim,pos_right,pos_left]  # odometries  = [timesim,pos_right,pos_left]
    print odometries
    timesim = str(timesim)
    pos_right = str(pos_right)
    pos_left = str(pos_left)
    file_test.write(timesim +" "+pos_left+" "+pos_right+"0 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 0 0 0")
    s=""
    for i in range(0, 683):
        magnitud[i] = 1000 * math.sqrt(lrf[i, 0] * lrf[i, 0] + lrf[i, 1] * lrf[i, 1])
        magnitud[i] = int(magnitud[i])
        if magnitud[i]>5700:
            magnitud[i]=0
        #print magnitud[i]
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
    dxy,dtheta,dt =robot.computeVelocities(odometries)
    slam.update(lidar) #voy aqui convertir la lista de sting a una lista (dxy,dtheta,dt)
    # Get current robot position
    global x
    global y
    global theta
    x, y, theta = slam.getpos()

    # Get current map bytes as grayscale
    slam.getmap(mapbytes)
    image = Image.frombuffer('L', (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), mapbytes, 'raw', 'L', 0, 1)
    image.save('hola.png' )
    display.displayMap(mapbytes)

    display.setPose(x, y, theta)
    save_frame()
    save_last_frame()
    # Exit on ESCape
    key = display.refresh()
    if key != None and (key & 0x1A):
        exit(0)
    root.after(1, task)  # reschedule event in 1 ms

root = Tk()
app = Application(master=root)
root.after(1000, task) # repetir la función task cada 300 ms
app.mainloop()


root.destroy()
save_movie("animation.gif", 0.1)
file_test.close()
import vrep
# Now close the connection to V-REP:
vrep.simxFinish(-1)



