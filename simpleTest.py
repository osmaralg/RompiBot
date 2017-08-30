# Copyright 2006-2017 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
# 
# -------------------------------------------------------------------
# THIS FILE IS DISTRIBUTED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY. THE USER WILL USE IT AT HIS/HER OWN RISK. THE ORIGINAL
# AUTHORS AND COPPELIA ROBOTICS GMBH WILL NOT BE LIABLE FOR DATA LOSS,
# DAMAGES, LOSS OF PROFITS OR ANY OTHER KIND OF LOSS WHILE USING OR
# MISUSING THIS SOFTWARE.
# 
# You are free to use/modify/distribute this file for whatever purpose!
# -------------------------------------------------------------------
#
# This file was automatically created for V-REP release V3.4.0 rev. 1 on April 5th 2017

# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import math
import time
import numpy as np
import matplotlib.pyplot as plt
file_test = open("testfile.txt","w")
def draw_lrf(lrf):
    lrf = np.asarray(lrf)
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.plot(0, 0, 'r>', markersize=10)
    ax.scatter(lrf[:, 0], lrf[:, 1])
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.grid()
    plt.show()

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



print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
    returnCode,back_left=vrep.simxGetObjectHandle(clientID,'back_left_motor',vrep.simx_opmode_blocking)	
    returnCode,back_right=vrep.simxGetObjectHandle(clientID,'back_right_motor',vrep.simx_opmode_blocking)
    returnCode,front_left=vrep.simxGetObjectHandle(clientID,'front_left_motor',vrep.simx_opmode_blocking)
    returnCode,front_right=vrep.simxGetObjectHandle(clientID,'front_right_motor',vrep.simx_opmode_blocking)
  

    if returnCode==vrep.simx_return_ok:
        print ('Corrio bien la lectura del handle')
    else:
        print ('Remote API function call returned with error code: ',returnCode)
    print ('No sirvio el returnCode')    
    print ('left_motor handle is:',back_left)
    print ('left_motor handle is:',front_left)
    print ('right_motor handle is:',back_right)
    print ('right_motor handle is:',front_right)
	
    if res==vrep.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(1)

    # Now retrieve streaming data (i.e. in a non-blocking fashion):
    startTime=time.time()

    name_hokuyo_data = "hokuyo_data"
    vrep.simxGetStringSignal(clientID, name_hokuyo_data,
                             vrep.simx_opmode_streaming)
    vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming) # Initialize streaming
    while time.time()-startTime < 10:
        returnCode,data=vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_buffer) # Try to retrieve the streamed data
        e, lrf_bin = vrep.simxGetStringSignal(clientID, name_hokuyo_data,                                  vrep.simx_opmode_buffer)
        #print ('hola sensor',lrf)
        
        if returnCode==vrep.simx_return_ok: # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
            print ('Mouse position x: ',data) # Mouse position x is actualized when the cursor is over V-REP's window
            lrf_raw = vrep.simxUnpackFloats(lrf_bin)
            lrf = np.array(lrf_raw).reshape(-1, 3)
            magnitud = np.arange(399.000)
            for i in range (0,399):        
                magnitud[i]=math.sqrt(lrf[i,0]*lrf[i,0]+lrf[i,1]*lrf[i,1])
            print ('la magnitud es:',magnitud)
            magnitud= magnitud.tostring()
            file_test.write(magnitud)
            #draw_lrf(lrf)
			#returnCode,Sensor_motor_pos=vrep.simxGetJointPosition(clientID,Sensor_motor,vrep.simx_opmode_blocking)
			#print('La posicion del motor es:',Sensor_motor_pos)
			
				
        time.sleep(0.05)

    # Now send some data to V-REP in a non-blocking fashion:
    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    file_test.close()
    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
