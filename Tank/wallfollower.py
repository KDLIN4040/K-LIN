import time
import Sensor as s
import Movement as mv
import GPIO_Setup as setup
import RPi.GPIO as GPIO
from simple_pid import PID
import numpy as np
import threading 
import Obstacle_Avoidance as oa

sweetspot_upperbond = 50
sweetspot_lowerbond = 30

### get the obstacle distance 
def right1_distance():
    distance = s.get_distance(setup.wallfollowing_1_trigger_pin,setup.wallfollowing_1_echo_pin)
    return distance

def right2_distance():
    distance = s.get_distance(setup.wallfollowing_2_trigger_pin,setup.wallfollowing_2_echo_pin)
    return distance

def front1_distance():
    frontobstacle_distacne_cm = s.get_distance(setup.front1_trigger_pin,setup.front1_echo_pin)
    return(frontobstacle_distacne_cm)

def front2_distance():
    rightobstacle_distance_cm = s.get_distance(setup.front2_trigger_pin,setup.front2_echo_pin)
    return(rightobstacle_distance_cm)

def left_distance():
    leftobstacle_distance_cm  = s.get_distance(setup.left_trigger_pin, setup.left_echo_pin)
    return(leftobstacle_distance_cm )


class wallfollower(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        right1 = 40
        right2 = 40
        front1 = 40
        front2 = 40
        left   = 40
        while True:
            right1 = right2_distance()
            front1 = front1_distance()
            front2 = front2_distance()
            left   = left_distance()           
            print("right1:{},front1:{},front2:{},left:{}".format(right1,front1,front2,left))
            
            if right1 < 30 :
                mv.turn_left()
            elif (front1 < 30) or (front2 < 30):
                mv.stopmotors()
                mv.goback()
                time.sleep(0.5)
                mv.turn_left()
                time.sleep(0.5)
            elif left < 30 :
                mv.turn_right()
            elif sweetspot_lowerbond < right1 < sweetspot_upperbond :
                mv.goforward()
            else:
                mv.move_arc()    
            
            time.sleep(0.05)


'''
#pid wallfollowing
pid = PID(20, 2, 0.5, setpoint=1)
pid.output_limits = (-1, 1)
pid.auto_mode = True


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

class pidwallfollowing(threading.Thread):
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
            if  (oa.flag_obstacle == False) :
                rotation = pid(wallangle())
                value = 20*(rotation)
                print("output :%f" %(30+value))
                driving(value)
                
                if (wallfollowing1_distance() > 100 and wallfollowing2_distance() > 100) :
                    mv.stopmotors()
                    mv.turnright(50)
'''
if __name__ == "__main__":
    threads = []
    t = wallfollower()
    t.start()