# coding: utf-8
## @package faboMPU9250
#  This is a library for the FaBo 9AXIS I2C Brick.
#
#  http://fabo.io/202.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import FaBo9Axis_MPU9250 
import time
import sys
import numpy as np
import math
from pylive import live_plotter

# plot 
i = 0
size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
yawangle_array = np.zeros(101)
line1 = []


accelArr = []
magneticArr = []
PI = 3.141592653589793238462643383279502884
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
i = 0

while True:
    try:
        
        while True:  
            accel = mpu9250.readAccel() 
            ax = accel['x']
            ay = accel['y']
            az = accel['z']
            #print(" ax = " , ( ax ))
            #print(" ay = " , ( ay ))
            #print(" az = " , ( az ))
            

            gyro = mpu9250.readGyro()
            gx = gyro['x']
            gy = gyro['y']
            gz = gyro['z']
            #print(" gx = " , ( gx ))
            #print(" gy = " , ( gy ))
            #print(" gz = " , ( gz ))
           
            mag = mpu9250.readMagnet()
            mx = mag['x']
            my = mag['y']
            mz = mag['z']
            
            print(" mx = " , ( mx ))
            print(" my = " , ( my ))
            print(" mz = " , ( mz ))
          


            pitch = math.atan2 (ay ,( math.sqrt ((ax * ax) + (az * az))))
            roll = math.atan2(-ax ,( math.sqrt((ay * ay) + (az * az))))

            Yh = (my * math.cos(roll)) - (mz * math.sin(roll))
            Xh = (mx * math.cos(pitch))+(my * math.sin(roll)*math.sin(pitch)) + (mz * math.cos(roll) *math.sin(pitch))

            yaw =  math.atan2(Yh, Xh)


            roll = roll*180
            pitch = pitch*180
            yaw = yaw*180
    
            print(yaw)

            '''
            #plot yawangle
            yawangle_array[i] = pitch
            y_vec = yawangle_array[0:-1]
            line1 = live_plotter(x_vec,y_vec,line1)
            i = i+1
            if i == 100:
                i = 0
            '''
            
            '''
            #Correct accel data
            correct_accel = ([1.391,0.022,-0.028],[0.022,1.43,-0.075],[-0.028,-0.075,0.505])  
            correct_accel = np.array(correct_accel)
            accel = [ax,ay,az]
            accel = np.array(accel)
            FIXaccel = accel.dot(correct_accel)         
            accelArr.append(FIXaccel)
            ''' 
            '''
            #Correct magnetic data
            magnetic = [mx,my,mz]
            magnetic = np.array(magnetic)
            magneticArr.append(magnetic)
            
            #test save sensor data to txt
        
            i+=1
            print (i)
            if i == 100:
                np.savetxt('acceldata.txt',accelArr)
                np.savetxt('magneticdata.txt',magneticArr)
                sys.exit()
            '''
            
        
            time.sleep(0.2)


    except KeyboardInterrupt:
        sys.exit()



