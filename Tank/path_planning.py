import time
import sensor as s
import movement as mv
import GPIO_Setup as setup
import RPi.GPIO as GPIO
from simple_pid import PID
import numpy as np
import threading 
import Obstacle_Avoidance as oa
from pylive import live_plotter

#pid algorithm
pid = PID(20, 2, 0.5, setpoint=1)
pid.output_limits = (-1, 1)
pid.auto_mode = True

# plot 
i = 0
size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
wallangle_array = np.zeros(101)
line1 = []
def wallfollowing1_distance():
    distance = s.get_distance(setup.wallfollowing_1_trigger_pin,setup.wallfollowing_1_echo_pin)
    return distance

def wallfollowing2_distance():
    distance = s.get_distance(setup.wallfollowing_2_trigger_pin,setup.wallfollowing_2_echo_pin)
    return distance

def wallangle():
    wall1 = wallfollowing1_distance()
    wall2 = wallfollowing2_distance()
    print("wall1 = %f wall2 = %f " %(wall1,wall2) )
    if (wall1 < 10) or (wall2 < 10):
        global flag_obstacle
        flag_obstacle = True
        mv.stopmotors()
        mv.turnleft(50)
        mv.goforward()
        flag_obstacle = False 
    wallangle = wall1/wall2
    return wallangle

def driving(value):
    setup.r.ChangeDutyCycle(30+value)
    setup.l.ChangeDutyCycle(30-value)
    time.sleep(0.1)

class wallfollowing(threading.Thread):
    def __init__(self, name):
        super(wallfollowing, self).__init__()
        self.name = name

    def run(self):
        mv.goforward()
        time.sleep(0.5)
        global i
        global line1
        while True:
            time.sleep(0.01)
            if  (oa.flag == False) :
                rotation = pid(wallangle())
                value = 20*(rotation)
                print("output :%f" %(30+value))
                driving(value)
    	        
                '''
                wallangle_array[i] = wallangle()
                y_vec = wallangle_array[0:-1]
                line1 = live_plotter(x_vec,y_vec,line1)
                i = i+1
                if i == 100:
                    i = 0
                '''
                if (wallfollowing1_distance() > 100 and wallfollowing2_distance() > 100) :
                    mv.stopmotors()
                    mv.turnright(50)
                