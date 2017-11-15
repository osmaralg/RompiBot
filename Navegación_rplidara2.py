# coding=utf-8
from Tkinter import *
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
import sys

import random
import json
import datetime
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint
import time
import os
import re
from dateutil import tz
from datetime import datetime
from gpsdData2 import GpsPoller
import os


from_zone=tz.tzutc()
to_zone=tz.tzlocal()



script_dir=sys.path[0]
img_path=os.path.join(script_dir,'/home/osmaralg/Desktop/RompiBot/hola.png')

import serial
import socket
UDP_IP="192.168.1.51"
UDP_PORT=10202
UDP_SENDIP="192.168.1.50"
UDP_SENDPORT=10003

udpSock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpSock.bind((UDP_IP,UDP_PORT))
paymentTypes = ["cash", "tab", "visa","mastercard","bitcoin"]
namesArray = ['Ben', 'Jarrod', 'Vijay', 'Aziz']
global centralTime
centralTime=0 

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


class WebSocketHandler(websocket.WebSocketHandler):
           
    def check_origin(self, origin):
        return True

    #on open of this socket
    def open(self):
        print ('Connection established.')
        #ioloop to wait for 3 seconds before starting to send data
        ioloop.IOLoop.instance().add_timeout(timedelta(seconds=3), self.send_data)
    #close connection
    def on_close(self):
        print ('Connection closed.')
    # Our function to send new (random) data for charts
    def send_data(self):
        #print ("Sending Data")
        img_path=os.path.join(script_dir,'/home/osmaralg/Desktop/RompiBot/hola.png')
        img_file=open(img_path,'r')      
        #read the image file
        data=img_file.read()
        #data has to be encoded base64
        #outjson['img']=data.encode('base64')
        #create a bunch of random data for various dimensions we want
        #qty = random.randrange(1,4)
        #total = random.randrange(30,1000)
        #tip = random.randrange(10, 100)
        #payType = paymentTypes[random.randrange(0,4)]
        #name = namesArray[random.randrange(0,4)]
        #spent = random.randrange(1,150);
        #year = random.randrange(2012,2016)
        """
        All the UDP data received from the TITech M4 board is stored in the
        variable udp, it is received as string with each sensor/data value
        separated by a coma. The split method is then used to separate the data in
        its components.
        THE DATA MUST BE RECEIVED AS FOLLOWS:
        data0,data1,....,datan
        """
        try:
            udp,addr=udpSock.recvfrom(1024)
        
            udp=udp.split(",") #UDP data is splitted
            yaw=str(udp[0])
            roll=str(udp[1])
            pitch=str(udp[2])
            battery=str(udp[3])
	    llanta1 = str(udp[4])
	    llanta2 = str(udp[5])
            print yaw,roll,pitch,battery,llanta1,llanta2

        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print "\nKilling Socket..."
            udpSock.close()
         
        #print("Time: ", gpsp.gpsd.utc)
        if(gpsp.gpsd.utc is not None):
            utcEncoded=gpsp.gpsd.utc.encode("ASCII")
            utcSplited=re.split(r'[T.]',utcEncoded)
            if(len(utcSplited)>1):
                utcTime=datetime.strptime(utcSplited[0]+utcSplited[1], '%Y-%m-%d%H:%M:%S')

                utcTime=utcTime.replace(tzinfo=from_zone)
                global centralTime
                centralTime =utcTime.astimezone(to_zone)
        else:
            
            centralTime='No Data'

        if(math.isnan(gpsp.gpsd.fix.latitude) ==False ):
            latitude=gpsp.gpsd.fix.latitude
        else:
            latitude='No Data'

        if(math.isnan(gpsp.gpsd.fix.longitude)==False):
            longitude=gpsp.gpsd.fix.longitude
        else:
            longitude='No Data'


        if(math.isnan(gpsp.gpsd.fix.altitude)==False):
            altitude=gpsp.gpsd.fix.altitude
        else:
            altitude='No Data'

               
        #print ("Time", centralTime)
        
        #print("latitude",gpsd.fix.latitude)
        #print(parseGPS(gpsRead))
        #print(gps.msg)        
        #print(gps_ser.readGPS())
        #print "latitude ", gpsc.fix.latitude           
        #print(udp[3])
        #print(udp)
        #yaw=ser.readline().decode('ascii').strip().split(',')#.decode('ascii').strip().split(',')
        #print(yaw)
        #print(data)
        point_data = {
        #'quantity': qty,
        #'total' : total,
        #'tip': tip,
        #'payType': payType,
        #'Name': name,
        #'Spent': spent,
        #'Year' : year,
        #'x': time.time(),
        #'yaw':str(ser.readline())
        #'yaw':str(yaw),
        'yaw':yaw,
        'roll':roll,
        'pitch':pitch,
        'battery':battery,
        'image1':data.encode('base64'),
        'central':str(centralTime),
        'latitude':str(latitude),
        'longitude':str(longitude),
        'altitude':str(altitude)
        }
        #print "latitude",str(latitude)
        #print "longitude",str(longitude)
        #print "altitude",str(altitude)

        #data=ser.readline().decode('ascii').strip().split(',')
        #print(data)
        #print (point_data)
        #write the json object to the socket
        self.write_message(json.dumps(point_data))
        #create new ioloop instance to intermittently publish data
        
        ioloop.IOLoop.instance().add_timeout(timedelta(seconds=.01), self.send_data)


    def on_message(self,message):


        #200ms enviar un mensaje al MCU independientemente de la interfaz.

        #interfaz: estar siempre mandando evitar que cada que se presione se envien el mensaje,
        #enviar periodicamente.

        #En MCU encabezado:@C,tres numeros para diferentes estados: 0-detenido,1,2 dos mensajes uno para el motor derecho y otro para motor izquierdo.
        #En MCU convertir los numeros para cada motor en condicional.

        #En la interfaz 
        
        print('Message received: {}'.format(message))
       
        
        if message=='1':
            udpSock.sendto("@1",(UDP_SENDIP,UDP_SENDPORT))
            
        if message=='2':
            udpSock.sendto("@2",(UDP_SENDIP,UDP_SENDPORT))
            
        if message=='3':
            udpSock.sendto("@3",(UDP_SENDIP,UDP_SENDPORT))

        if message=='4':
            udpSock.sendto("@4",(UDP_SENDIP,UDP_SENDPORT))
            
        if message=='0':
            udpSock.sendto("@0",(UDP_SENDIP,UDP_SENDPORT))
        '''
        if message=='hold':
            udpSock.sendto("@UDEM",(UDP_SENDIP,UDP_SENDPORT))
         '''

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


os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")
    
from gpsdData2 import GpsPoller
#create new web app w/ websocket endpoint available at /websocket

print ("Starting websocket server program. Awaiting client requests to open websocket ...")

application = web.Application([(r'/websocket', WebSocketHandler)])
    
application.listen(8001)
  
gpsp=GpsPoller()
    #try:
gpsp.start()

    #except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
     #   print "\nKilling Thread..."
      #  gpsp.running = False
       # gpsp.join() # wait for the thread to finish what it's doing
    

    #gps_ser=gps(serGPS)
    #gpsc=GpsController()
    #gpsc.start()
    #gps=GPSReader()
ioloop.IOLoop.instance().start()
root = Tk()
app = Application(master=root)
root.after(2000, task) # repetir la función task cada 300 ms
app.mainloop()
root.destroy()
file_test.close()
save_movie("animationRplidar.gif",0.1)


# Now close the connection to V-REP:







