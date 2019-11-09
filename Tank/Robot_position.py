import sys, getopt
import GPIO_Setup
import RPi.GPIO as GPIO
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import threading  
import numpy as np
import Encoder
flag_backward = False
GPIO.setmode(GPIO.BOARD)
Ar_Wave = 11
Br_Wave = 13   
Al_Wave = 16
Bl_Wave = 18   
### setting IMU
SETTINGS_FILE = "RTIMULib"
print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

def get_yaw():  
    if imu.IMURead():

        data = imu.getIMUData()
        fusionPose = data["fusionPose"]
        #roll = math.degrees(fusionPose[0])
        #pitch = math.degrees(fusionPose[1])
        #print("r: %f p: %f y: %f" % (roll, pitch, yaw))
        yaw = math.degrees(fusionPose[2])
        time.sleep(poll_interval*1.0/1000.0)
        return yaw
    
    else :
        return 500

#def Llidarscan():

#def get_distance():


def Robot_position(): 
    value = get_yaw()
    distance = Encoder.rturns
    if value != 500:
        yaw = round(value,3)
        print(yaw)
        print("distance:{}".format(distance))




class observation(threading.Thread):
    def __init__(self, name):
        super(observation, self).__init__()
        self.name = name
    
    def run(self):
        while True:
            Robot_position()




def main():
    try:
        
        threads = []
        t1 = Encoder.encoder()
        t2 = observation("observation")
        threads.append(t1)
        threads.append(t2) 
       
        for t in threads:
            t.start()


    except KeyboardInterrupt:
        GPIO_Setup.cleargpios()
        time.sleep(1)
        print("stop")


if __name__ == "__main__":
    main()