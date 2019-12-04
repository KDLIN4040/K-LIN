import time
import Sensor as s
import Movement as mv
import RPi.GPIO as GPIO
import numpy as np
import threading 

sweetspot_upperbond = 50
sweetspot_lowerbond = 30

### get the obstacle distance 
# Define GPIO for ultrasonic Front
front1_trigger_pin = 31
front1_echo_pin = 33
GPIO.setup(front1_trigger_pin, GPIO.OUT)
GPIO.setup(front1_echo_pin, GPIO.IN)

# Define GPIO for ultrasonic Right
front2_trigger_pin = 35
front2_echo_pin = 37
GPIO.setup(front2_trigger_pin, GPIO.OUT)
GPIO.setup(front2_echo_pin, GPIO.IN)

# Define GPIO for ultrasonic Left
left_trigger_pin = 38 
left_echo_pin = 40
GPIO.setup(left_trigger_pin, GPIO.OUT)
GPIO.setup(left_echo_pin, GPIO.IN)

# Define GPIO for wallfollowing 
wallfollowing_1_trigger_pin = 7 
wallfollowing_1_echo_pin = 11
GPIO.setup(wallfollowing_1_trigger_pin, GPIO.OUT)
GPIO.setup(wallfollowing_1_echo_pin, GPIO.IN)
wallfollowing_2_trigger_pin = 13
wallfollowing_2_echo_pin = 15
GPIO.setup(wallfollowing_2_trigger_pin, GPIO.OUT)
GPIO.setup(wallfollowing_2_echo_pin, GPIO.IN)

def right1_distance():
    distance = s.get_distance(wallfollowing_1_trigger_pin,wallfollowing_1_echo_pin)
    return distance

def right2_distance():
    distance = s.get_distance(wallfollowing_2_trigger_pin,wallfollowing_2_echo_pin)
    return distance

def front1_distance():
    frontobstacle_distacne_cm = s.get_distance(front1_trigger_pin,front1_echo_pin)
    return(frontobstacle_distacne_cm)

def front2_distance():
    rightobstacle_distance_cm = s.get_distance(front2_trigger_pin,front2_echo_pin)
    return(rightobstacle_distance_cm)

def left_distance():
    leftobstacle_distance_cm  = s.get_distance(left_trigger_pin, left_echo_pin)
    return(leftobstacle_distance_cm )


class wallfollower(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:    
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
                
                mv.goforward()
                
                if (front1 < 20) or (front2 < 20):
                    mv.stopmotors()
                    mv.goback()
                    time.sleep(1)
                    mv.turn_left()
                    time.sleep(0.5)
                elif right1 < 30 :
                    mv.turn_left()
                elif left < 30 :
                    mv.turn_right()
                elif sweetspot_lowerbond < right1 < sweetspot_upperbond :
                    mv.goforward()
                else:
                    mv.move_arc()  
                
                time.sleep(0.01)

        except KeyboardInterrupt:
            GPIO.cleanup()
            time.sleep(1)
            print("stop")        

if __name__ == "__main__":
    threads = []
    t = wallfollower()
    t.start()
    time.sleep(1)