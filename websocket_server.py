import time
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
import math


from_zone=tz.tzutc()
to_zone=tz.tzlocal()

from gpsdData2 import GpsPoller

import sys, os

script_dir=sys.path[0]
img_path=os.path.join(script_dir,'/home/osmaralg/Desktop/image1.jpg')

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
        img_path=os.path.join(script_dir,'/home/osmaralg/Desktop/image1.jpg')
        img_file=open(img_path,'r')      
        #read the image file
        data=img_file.read()
        
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

               
       
        point_data = {
       
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
        
        self.write_message(json.dumps(point_data))
        
        
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

if __name__ == "__main__":
    main()
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

manager.shutdown()
