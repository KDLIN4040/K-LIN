import time
import sensor as s
import movement as mv
import GPIO_Setup as setup
import RPi.GPIO as GPIO
from simple_pid import PID
import numpy
import threading 
import Obstacle_Avoidance as oa

#pid algorithm
pid = PID(1, 0.1, 0.5, setpoint=1)
pid.output_limits = (-1, 1)

def wallfollowing1_distance():
    distance = s.get_distance(setup.wallfollowing_1_trigger_pin,setup.wallfollowing_1_echo_pin)
    return distance

def wallfollowing2_distance():
    distance = s.get_distance(setup.wallfollowing_2_trigger_pin,setup.wallfollowing_2_echo_pin)
    return distance

def wallangle():
    wall1 = wallfollowing1_distance()
    wall2 = wallfollowing2_distance()
    wallangle = wall1/wall2
    return wallangle
def driving(value):
    setup.r.ChangeDutyCycle(value)
    setup.l.ChangeDutyCycle(100-value)
    time.sleep(0.1)

class wallfollowing(threading.Thread):
    def __init__(self, name):
        super(wallfollowing, self).__init__()
        self.name = name

    def run(self):
        mv.goforward()

        while True:
            time.sleep(0.001)
            if  (oa.flag == False) :
                rotation = pid(wallangle())
                print("rotation:%f" %rotation)
                value = 50 + 20*rotation
                print("value:%f" %value)
                driving(value)

class obstacle_avoidance(threading.Thread):
    def __init__(self,name):
        super(obstacle_avoidance, self).__init__()
        self.name = name

    def run(self):
        while True:
            oa.checkanddriveright()
            oa.checkanddriveleft()
            oa.checkanddrivefront()
            time.sleep(0.001)