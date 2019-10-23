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
PI = 3.141592653589793238462643383279502884
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
while True:
    try:
        while True:  
            accel = mpu9250.readAccel()
            '''
            print(" ax = " , ( accel['x'] ))
            print(" ay = " , ( accel['y'] ))
            print(" az = " , ( accel['z'] ))
            '''
            gyro = mpu9250.readGyro()
            '''
            print(" gx = " , ( gyro['x'] ))
            print(" gy = " , ( gyro['y'] ))
            print(" gz = " , ( gyro['z'] ))
            '''
            mag = mpu9250.readMagnet()
            '''
            print(" mx = " , ( mag['x'] ))
            print(" my = " , ( mag['y'] ))
            print(" mz = " , ( mag['z'] ))
            print()
            '''
            ax = accel['x']
            ay = accel['y']
            az = accel['z']
            mx = mag['x']
            my = mag['y']
            mz = mag['z']

            pitch = 180 * math.atan2(ax, math.sqrt(ay*ay + az*az))/PI
            roll = 180 * math.atan2(ay, math.sqrt(ax*ax + az*az))/PI
            
            mag_x = mx*math.cos(pitch) + my*math.sin(roll)*math.sin(pitch) + mz*math.cos(roll)*math.sin(pitch)
            mag_y = my*math.cos(roll) - mz*math.sin(roll)
            yaw = 180 * math.atan2(-mag_y,mag_x)/PI
            
            if(yaw < 0):
                yaw  += 360.0
            

            print("yaw angle:%f" %yaw)

            time.sleep(0.1)


    except KeyboardInterrupt:
        sys.exit()

    except :
        pass


