import GPIO_Setup as setup
import movement as mv
import sensor   as s
import threading 
import main
import time
flag = False
#Functions for Obstacle Avoidance
def frontobstacle():
    frontobstacle_distacne_cm = s.get_distance(setup.front_trigger_pin,setup.front_echo_pin)
    return(frontobstacle_distacne_cm)

def rightobstacle():
    rightobstacle_distance_cm = s.get_distance(setup.right_trigger_pin,setup.right_echo_pin)
    return(rightobstacle_distance_cm)

def leftobstacle():
    leftobstacle_distance_cm  = s.get_distance(setup.left_trigger_pin, setup.left_echo_pin)
    return(leftobstacle_distance_cm )

def checkanddrivefront():
    distance = frontobstacle()
    global flag 
    if distance < 30:
        flag = True
        mv.stopmotors()
        mv.turnleft(100)
        print("***front***:%f" %distance)
        mv.goforward()
        flag = False
def checkanddriveright(): 
    distance = rightobstacle()
    global flag
    if distance < 30:
        flag = True
        mv.stopmotors()
        mv.turnleft(100)
        print("***right***:%f" %distance )
        mv.goforward()
        flag = False
 


def checkanddriveleft():
    distance = leftobstacle()
    global flag 
    if distance < 30:
        flag = True
        mv.stopmotors()
        mv.turnright(100)
        print("***left***:%f" %distance )
        mv.goforward()
        flag = False