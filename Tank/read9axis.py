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
import datetime
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
PI = 3.14
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
savedata_i = 0

#kalman filter
measurements = []
kalman_accel = []
kalman_ax = 0
kalman_ay = 0
kalman_az = 0
yawlist = []
kalman_yaw = 0
kalman_angle = 0
i = 0
roll = 0
pitch = 0
yaw = 0

def calibrate():
    totalmx = []
    totalmy = []
    totalmz = []
    totalax = 0
    totalay = 0
    totalaz = 0
    totalgx = 0
    totalgy = 0
    totalgz = 0
    cal = 20
    
    global bas_mx
    global bas_my 
    global bas_mz
    global scale_x
    global scale_y
    global scale_z
    global bas_ax
    global bas_ay
    global bas_az
    global bas_gx
    global bas_gy
    global bas_gz



    for i in range(1,10):  
        accel = mpu9250.readAccel() 
        gyro = mpu9250.readGyro()
        '''
        mag = mpu9250.readMagnet()     
        mx = mag['x']
        totalmx.append(mx)
        my = mag['y']
        totalmy.append(my)
        mz = mag['z']
        totalmz.append(mz)
        '''
        ax = accel['x']
        totalax += ax
        ay = accel['y']
        totalay += ay
        az = accel['z']
        totalaz += az
        gx = gyro['x']
        gy = gyro['y']
        gz = gyro['z']
   
        
    '''
    offset_x = (max(totalmx)-min(totalmx))/2
    offset_y = (max(totalmy)-min(totalmy))/2
    offset_z = (max(totalmz)-min(totalmz))/2
    avg_delta = (offset_x+offset_y+offset_z)/3
    if offset_x*offset_y*offset_z != 0:    
        scale_x = avg_delta / offset_x
        scale_y = avg_delta / offset_y
        scale_z = avg_delta / offset_z
    '''
    totalax /= cal
    totalay /= cal
    totalaz /= cal
    totalgx /= cal
    totalgy /= cal
    totalgz /= cal

    #bas_mx = offset_x
    #bas_my = offset_y
    #bas_mz = offset_z
    bas_ax = totalax
    bas_ay = totalay
    bas_az = totalaz
    bas_gx = totalgx
    bas_gy = totalgy
    bas_gz = totalgz

while True:

    try:
        while True:  
            '''
            mag = mpu9250.readMagnet()
            mx = mag['x']
            my = mag['y']
            mz = mag['z']
            print("mx:{},my:{},mz:{}".format(mx,my,mz))
            '''
            last_angle_gx = roll
            last_angle_gy = pitch
            #last_angle_gz = yaw


            calibrate()

            ### get raw data
            accel = mpu9250.readAccel() 
            ax = accel['x']-bas_ax
            ay = accel['y']-bas_ay
            az = accel['z']-bas_az

            
            gyro = mpu9250.readGyro()
            start_time = datetime.datetime.now()
            gx = gyro['x']-bas_gx
            gy = gyro['y']-bas_gy
            gz = gyro['z']-bas_gz
            endtime = datetime.datetime.now()
            dt = (endtime - start_time).microseconds

            
            mag = mpu9250.readMagnet()
            mx = mag['x']
            my = mag['y']
            mz = mag['z']
            
            #if mx*my*mz != 0:
            '''    
            mx = (mx-bas_mx)*scale_x
            my = (my-bas_my)*scale_y
            mz = (mz-bas_mz)*scale_z
            #print("mx:{},my:{},mz:{}".format(mx,my,mz))
        
            '''
    
            angle_gx = (gx*dt)/1000 + last_angle_gx
            angle_gy = (gy*dt)/1000 + last_angle_gy
            #angle_gz = (gz*dt)/1000 + last_angle_gz 


    
            
            #### calculate  roll pitch  by accel
            angle_ax = 180*math.atan2(ay ,( math.sqrt((ax * ax) + (az * az))))/PI
            angle_ay = 180*math.atan2 (ax ,( math.sqrt ((ay * ay) + (az * az))))/PI
            
            dt = 0.000
            alpha = 0.96
            roll = alpha*angle_gx + (1-alpha)*angle_ax
            pitch = alpha*angle_ay + (1-alpha)*angle_ay
            #yaw = angle_gz 
            
            ###use kalman filter to fuse pitch & roll which calculated by accel and gyro 
            rawdata_array = [roll,pitch]
            measurements.append(rawdata_array)
            kalman_angle = kf.example(measurements)
            
            if len(kalman_angle) >=2 :
                kalman_roll = kalman_angle [0]
                kalman_pitch = kalman_angle[1]

                Xh = (mx * math.cos(kalman_pitch))+(my * math.sin(kalman_roll)*math.sin(kalman_pitch)) + (mz * math.cos(kalman_roll) *math.sin(kalman_pitch))
                Yh = (my * math.cos(kalman_roll)) - (mz * math.sin(kalman_roll))
                yaw =  180*(math.atan2(-Yh, Xh)/PI)
                if yaw < 0:
                    yaw+=360
                #yawlist.append(yaw)
                #kalman_yaw =  kf.example(yawlist)
                print("x:{},y:{},z:{},yaw:{}".format(mx,my,mz,yaw)) 
                
        
            #plot yawangle
            '''
            yawangle_array[plot_i] = yaw
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


