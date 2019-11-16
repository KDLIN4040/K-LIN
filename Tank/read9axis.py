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
PI = 3.141
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

#magclibration
mag_scale = np.array([0,0,0])
mag_bias  = np.array([0,0,0])
accel_bias = np.array([0,0,0])
gyro_bias = np.array([0,0,0])

def magcalibration():
    #magclibration
    global mag_scale
    global mag_bias
    mag_temp = np.array([0,0,0],dtype=np.float16)
    mag_bias = np.array([0,0,0],dtype=np.float16)
    mag_scale = np.array([0,0,0],dtype=np.float16)
    mag_max = np.array([-32767, -32767, -32767],dtype=np.float16)
    mag_min = np.array([32767, 32767, 32767],dtype=np.float16)
    dest1 = np.array([0,0,0],dtype=np.float16)
    dest2 = np.array([0,0,0],dtype=np.float16)
    print("mag ==>calibration")
    for i in range (0,20) :
        mag = mpu9250.readMagnet()
        mag_temp[0] = mag['x']
        mag_temp[1] = mag['y']
        mag_temp[2] = mag['z']
        print(mag_temp[0],mag_temp[1],mag_temp[2])
        for j in range (0,3):
            if(mag_temp[j] > mag_max[j]) and (mag_temp[j]!=0):
                mag_max[j] = mag_temp[j]
            if(mag_temp[j] < mag_min[j]) and (mag_temp[j]!=0):
              mag_min[j] = mag_temp[j]
        #print(mag_temp)
        time.sleep(0.5)
    mag_bias[0]  = round((mag_max[0] + mag_min[0])/2.0,3)  #get average x mag bias in counts
    mag_bias[1]  = round((mag_max[1] + mag_min[1])/2.0,3)  #get average y mag bias in counts
    mag_bias[2]  = round((mag_max[2] + mag_min[2])/2.0,3)  #get average z mag bias in counts
    '''
    dest1[0] = mag_bias[0]*mRes*magCalibration[0]  #save mag biases in G for main program
    dest1[1] = mag_bias[1]*mRes*magCalibration[1]   
    dest1[2] = mag_bias[2]*mRes*magCalibration[2]  
    ''' 
    #Get soft iron correction estimate
    mag_scale[0]  = (mag_max[0] - mag_min[0])/2.0  #get average x axis max chord length in counts
    mag_scale[1]  = (mag_max[1] - mag_min[1])/2.0  #get average y axis max chord length in counts
    mag_scale[2]  = (mag_max[2] - mag_min[2])/2.0  #get average z axis max chord length in counts

    avg_rad = mag_scale[0] + mag_scale[1] + mag_scale[2]
    avg_rad /= 3.0

    mag_scale[0] = round(avg_rad/(mag_scale[0]),3)
    mag_scale[1] = round(avg_rad/(mag_scale[1]),3)
    mag_scale[2] = round(avg_rad/(mag_scale[2]),3)
  
    print("Mag Calibration done!")
    print("mag_bias:{},mag_scale:{}".format(mag_bias,mag_scale))
    time.sleep(5)
def gyro_and_accel_calibration():

    cal = 100
    global gyro_bias
    global accel_bias
    accel_temp = np.array([0,0,0],dtype=np.float16)
    gyro_temp = np.array([0,0,0],dtype=np.float16)
    for i in range(100):  
        accel = mpu9250.readAccel() 
        gyro = mpu9250.readGyro()
        
        ax = accel['x']
        accel_temp[0] += ax
        ay = accel['y']
        accel_temp[1] += ay
        az = accel['z']
        accel_temp[2] += az
        
        gx = gyro['x']
        gyro_temp[0] += gx
        gy = gyro['y']
        gyro_temp[1] += gy
        gz = gyro['z']
        gyro_temp[2] += gz
        time.sleep(0.1)
        print(accel_temp,gyro_temp)
    
    accel_temp /= cal
    gyro_temp /= cal

    accel_bias[0] = round(accel_temp[0],3)
    accel_bias[1] = round(accel_temp[1],3)
    accel_bias[2] = round(accel_temp[2],3)
    gyro_bias[0] = round(gyro_temp[0],3)
    gyro_bias[0] = round(gyro_temp[0],3)
    gyro_bias[0] = round(gyro_temp[0],3)
    print("accel&gyroscope Calibration done!")
    print("accel_bias:{},gyro_bias:{}".format(accel_bias,gyro_bias))
    time.sleep(5)

def main():
    

    try:
        global roll
        global pitch
        global yaw
        global mag_scale
        global mag_bias
        global accel_bias
        global gyro_bias
        magcalibration()
        gyro_and_accel_calibration()
        while True:  
            last_angle_gx = roll
            last_angle_gy = pitch
            #last_angle_gz = yaw
        

            
            ### get raw data
            accel = mpu9250.readAccel() 
            ax = accel['x']-accel_bias[0]
            ay = accel['y']-accel_bias[1]
            az = accel['z']-accel_bias[2]

            

            start_time = datetime.datetime.now()
            gyro = mpu9250.readGyro()
            endtime = datetime.datetime.now()
            dt = (endtime - start_time).microseconds

            gx = gyro['x']-gyro_bias[0]
            gy = gyro['y']-gyro_bias[1]
            gz = gyro['z']-gyro_bias[2]
            

            
            mag = mpu9250.readMagnet()
            mx = (mag['x']-mag_bias[0])*mag_scale[0]
            my = (mag['y']-mag_bias[1])*mag_scale[1]
            mz = (mag['z']-mag_bias[2])*mag_scale[2]
            
            
            '''    
            mx = (mx-bas_mx)*scale_x
            my = (my-bas_my)*scale_y
            mz = (mz-bas_mz)*scale_z
            #print("mx:{},my:{},mz:{}".format(mx,my,mz))
        
            '''
    

            #angle_gz = (gz*dt)/1000 + last_angle_gz 


            
            
            #### calculate  roll pitch  by accel
            angle_ax = 180*math.atan2(ay ,math.sqrt(round(ax*ax,3) + round(az*az),3))/PI
            angle_ay = 180*math.atan2(ax ,math.sqrt(round(ay*ay,3) + round(az*az),3))/PI

            angle_gx = (gx*dt)/1000000 + last_angle_gx
            angle_gy = (gy*dt)/1000000 + last_angle_gy
            
            print(angle_ax,angle_ay)

            dt = 0.000
            alpha = 0.96
            roll = alpha*angle_gx + (1.000-alpha)*angle_ax
            pitch = alpha*angle_ay + (1.000-alpha)*angle_ay
            #yaw = angle_gz 
            
            ###use kalman filter to fuse pitch & roll which calculated by accel and gyro 
            rawdata_array = [roll,pitch]
            measurements.append(rawdata_array)
            kalman_angle = kf.example(measurements)
            
            if len(kalman_angle) >=2 :
                kalman_roll = kalman_angle [0]
                kalman_pitch = kalman_angle[1]
                if mx*my*mz != 0:
                    Xh = (mx * math.cos(kalman_pitch))+(my * math.sin(kalman_roll)*math.sin(kalman_pitch)) + (mz * math.cos(kalman_roll) *math.sin(kalman_pitch))
                    Yh = (my * math.cos(kalman_roll)) - (mz * math.sin(kalman_roll))
                    yaw =  180*(math.atan2(-Yh, Xh)/PI)
                    if yaw < 0:
                        yaw+=360
                    yawlist.append(yaw)
                    kalman_yaw =  kf.example(yawlist)
            #print("x:{},y:{},yaw:{}".format(roll,pitch,yaw)) 
              
        
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
            time.sleep(0.5)
                
    except KeyboardInterrupt:
            sys.exit()

if __name__ == '__main__':
    main() 
