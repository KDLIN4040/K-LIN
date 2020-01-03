import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import RPi.GPIO as GPIO
import threading
import numpy as np
import datetime
import matplotlib.pyplot as plt
yaw = 0
yaw_flag = False

SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
poll_interval = 0

def init_MARG():
    ### setting IMU
    GPIO.setmode(GPIO.BOARD) 
    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
      print("Settings file does not exist, will be created")
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
    global poll_interval  
    global yaw
    if imu.IMURead():
        data = imu.getIMUData()
        fusionPose = data["fusionPose"]
        #roll = math.degrees(fusionPose[0])
        #pitch = math.degrees(fusionPose[1])
        #print("r: %f p: %f y: %f" % (roll, pitch, yaw))
        yaw = math.degrees(fusionPose[2])
        if yaw < 0:
            yaw += 360
        time.sleep(poll_interval*1.0/1000.0)
    
class MARG(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        init_MARG()
        global yaw
        while True:
            get_yaw()
            print(yaw)
#!/usr/bin/python
#-------------------------------------------------------------------------------
# FileName:     Rotary_Encoder-1a.py
# Purpose:      This program decodes a rotary encoder switch.
#

#
# Note:         All dates are in European format DD-MM-YY[YY]
#
# Author:       Paul Versteeg
#
# Created:      23-Nov-2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#-------------------------------------------------------------------------------

import RPi.GPIO as GPIO
from time import sleep


# Global constants & variables
# Constants
__author__ = 'Paul Versteeg'

counter = 0  # starting point for the running directional counter

# GPIO Ports
Enc_A = 11  # Encoder input A: input GPIO 23 (active high)
Enc_B = 13  # Encoder input B: input GPIO 24 (active high)


def init_encoder():
    '''
    Initializes a number of settings and prepares the environment
    before we start the main program.
    '''
    print ("Rotary Encoder Test Program")

    GPIO.setwarnings(True)

    # Use the Raspberry Pi BOARD pins
    GPIO.setmode(GPIO.BOARD)

    # define the Encoder switch inputs
    GPIO.setup(Enc_A, GPIO.IN) # pull-ups are too weak, they introduce noise
    GPIO.setup(Enc_B, GPIO.IN)

    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=50) # bouncetime in mSec
    #
    return


def rotation_decode(Enc_A):
    '''
    This function decodes the direction of a rotary encoder and in- or
    decrements a counter.

    The code works from the "early detection" principle that when turning the
    encoder clockwise, the A-switch gets activated before the B-switch.
    When the encoder is rotated anti-clockwise, the B-switch gets activated
    before the A-switch. The timing is depending on the mechanical design of
    the switch, and the rotational speed of the knob.

    This function gets activated when the A-switch goes high. The code then
    looks at the level of the B-switch. If the B switch is (still) low, then
    the direction must be clockwise. If the B input is (still) high, the
    direction must be anti-clockwise.

    All other conditions (both high, both low or A=0 and B=1) are filtered out.

    To complete the click-cycle, after the direction has been determined, the
    code waits for the full cycle (from indent to indent) to finish.

    '''

    global counter

    sleep(0.05) # extra 50 mSec de-bounce time

    # read both of the switches
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        counter += 1
        print ("direction -> ", counter)
        # at this point, B may still need to go high, wait for it
        while Switch_B == 0:
            Switch_B = GPIO.input(Enc_B)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(Enc_B)
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        counter -= 1
        print ("direction <- ", counter)
         # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(Enc_A)
        return

    else: # discard all other combinations
        return
        
class encoder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        init_encoder()
        global encoder_flag
        while True:
            rotation_decode(Enc_A)

position_flag = False            
position = (0.0,0.0, 0.0)
class RobotPosition(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global yaw
        global yaw_flag
        global counter
        global encoder_flag
        global position
        global position_flag
        dl = 0
        vector = np.array([0.0,0.0])
        xn = 0
        yn = 0
        while True:
                dl = counter
                yawl = yaw
                time.sleep(0.1)
                vector[0] =  counter
                vector[1] =  yaw
                d = vector[0] - dl
                dyaw = int(vector[1] -yawl)
                #x = d*math.cos(vector[1])
                #y = d*math.sin(vector[1])
                #xn += x
                #yn += y
                if dyaw >330:
                    dyaw = 0
                position = [d*1000, dyaw, 0.1]
                position_flag = True
if __name__ == "__main__":
    threads = []
    t1 = RobotPosition()
    t2 = encoder()
    t3 = MARG()
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    for t in threads:
     t.start()
