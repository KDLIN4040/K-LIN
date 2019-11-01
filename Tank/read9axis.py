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
import kalman_filter as kf
# plot 
plot_i = 0
size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
yawangle_array = np.zeros(101)
line1 = []

#save data
accelArr = []
magneticArr = []
PI = 3.141592653589793238462643383279502884
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
savedata_i = 0

#kalman filter
measurements = []
measurements_yaw = []
kalman_accel = []
kalman_ax = 0
kalman_ay = 0
kalman_az = 0
yawlist = []
kalman_yaw = 0
i = 0
while True:

    try:
        while True:  
            ### get raw data
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
            mx = mag['x']-29.59
            my = mag['y']-15.60
            mz = mag['z']-2.35
            
            #print(" mx = " , ( mx ))
            #print(" my = " , ( my ))
            #print(" mz = " , ( mz ))
            
            ###Kalman_filter 
            rawdata_array = [ax,ay,az]
            measurements.append(rawdata_array)
            kalman_accel = kf.example(measurements,'accel')

            if len(kalman_accel)>=3:
                kalman_ax = kalman_accel[0]
                kalman_ay = kalman_accel[1]
                kalman_az = kalman_accel[2]
                #print(kalman_ax,kalman_ay,kalman_az)
                
                '''
                ### calculate pitch roll yaw
                pitch = math.atan2 (kalman_ax ,( math.sqrt ((kalman_ax * kalman_ax) + (kalman_az * kalman_az))))
                roll = math.atan2(kalman_ay ,( math.sqrt((kalman_ay * kalman_ay) + (kalman_az * kalman_az))))

                Yh = (my * math.cos(roll)) - (mz * math.sin(roll))
                Xh = (mx * math.cos(pitch))+(my * math.sin(roll)*math.sin(pitch)) + (mz * math.cos(roll) *math.sin(pitch))
                yaw =  math.atan2(Yh, Xh)


                
                roll = roll*57.3
                pitch = pitch*57.3
                yaw = yaw*70
                if yaw != 0  : 
                    measurements_yaw.append(yaw)
                    kalman_yaw = kf.example(measurements_yaw,'yaw')
        
                '''            

            #plot yawangle
            '''
            yawangle_array[plot_i] = pitch
            y_vec = yawangle_array[0:-1]
            line1 = live_plotter(x_vec,y_vec,line1)
            plot_i += 1
            if plot_i == 100:
                plot_i = 0
            '''
            
            
            #Correct accel data
            '''
            correct_accel = ([1.391,0.022,-0.028],[0.022,1.43,-0.075],[-0.028,-0.075,0.505])  
            correct_accel = np.array(correct_accel)
            accel = [ax,ay,az]
            accel = np.array(accel)
            #FIXaccel = accel.dot(correct_accel)         
            accelArr.append(accel)
            ''' 
            
            #Correct magnetic data
            '''
            magnetic = [mx,my,mz]
            magnetic = np.array(magnetic)
            magneticArr.append(magnetic)
            '''
            
            # save sensor data to txt
            '''
            savedata_i+=1
            print (savedata_i)
            if savedata_i == 500:
                np.savetxt('acceldata.txt',accelArr)
                np.savetxt('magneticdata.txt',magneticArr)
                sys.exit()
            '''
        
            


    except KeyboardInterrupt:
        sys.exit()



