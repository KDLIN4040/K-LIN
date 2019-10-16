import GPIO_Setup as setup
import movement as mv
import sensor   as s
import threading 
import time
flag = False
#Functions for Obstacle Avoidance
def front1obstacle():
    frontobstacle_distacne_cm = s.get_distance(setup.front1_trigger_pin,setup.front1_echo_pin)
    return(frontobstacle_distacne_cm)

def front2obstacle():
    rightobstacle_distance_cm = s.get_distance(setup.front2_trigger_pin,setup.front2_echo_pin)
    return(rightobstacle_distance_cm)

def leftobstacle():
    leftobstacle_distance_cm  = s.get_distance(setup.left_trigger_pin, setup.left_echo_pin)
    return(leftobstacle_distance_cm )

def checkanddrivefront():
    distance1 = front1obstacle()
    distance2 = front2obstacle()
    global flag 
    if (distance < 30) and (distance2 < 30) :
        flag = True
        mv.stopmotors()
        mv.goback()
        time.sleep(0.5)
        mv.turnleft(80)
        print("***front***:%f" %distance)
        mv.goforward()
        flag = False

'''
def checkanddriveright(): 
    distance = rightobstacle()
    global flag
    if distance < 10:
        flag = True
        mv.stopmotors()
        mv.turnleft(50)
        print("***right***:%f" %distance )
        mv.goforward()
        flag = False 
'''

def checkanddriveleft():
    distance = leftobstacle()
    global flag 
    if distance < 25:
        flag = True
        mv.stopmotors()
        mv.turnright(50)
        print("***left***:%f" %distance )
        mv.goforward()
        flag = False

class obstacle_avoidance(threading.Thread):
    def __init__(self,name):
        super(obstacle_avoidance, self).__init__()
        self.name = name

    def run(self):
        while True:
            #checkanddriveright()
            checkanddriveleft()
            checkanddrivefront()
            time.sleep(0.001)