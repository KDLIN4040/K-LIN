import GPIO_Setup as setup
import RPi.GPIO as GPIO
import time
# Functions for driving
def goforward():
    GPIO.output(setup.right_motor_pin1,1)
    GPIO.output(setup.right_motor_pin2,0)
    GPIO.output(setup.left_motor_pin1 ,1)
    GPIO.output(setup.left_motor_pin2 ,0)
    setup.r.start(100)
    setup.l.start(100)
    print("goforward")

def goback():
    GPIO.output(setup.right_motor_pin1,0)
    GPIO.output(setup.right_motor_pin2,1)
    GPIO.output(setup.left_motor_pin1 ,0)
    GPIO.output(setup.left_motor_pin2, 1)
    setup.r.start(100)
    setup.l.start(100)
    print("goback")

def turn_right():
    GPIO.output(setup.right_motor_pin1,0)
    GPIO.output(setup.right_motor_pin2,0)
    GPIO.output(setup.left_motor_pin1 ,1)
    GPIO.output(setup.left_motor_pin2, 0)
    setup.r.start(100)
    setup.l.start(100)
    print("turn_right")
def turn_left():
    GPIO.output(setup.right_motor_pin1,1)
    GPIO.output(setup.right_motor_pin2,0)
    GPIO.output(setup.left_motor_pin1 ,0)
    GPIO.output(setup.left_motor_pin2, 0)
    setup.r.start(100)
    setup.l.start(100)
    print("turn_left")
def move_arc():
    GPIO.output(setup.right_motor_pin1,1)
    GPIO.output(setup.right_motor_pin2,0)
    GPIO.output(setup.left_motor_pin1 ,1)
    GPIO.output(setup.left_motor_pin2 ,0)
    setup.r.start(50)
    setup.l.start(100)
    print("move_arc")
'''    
def turnright(value):
    goforward()
    setup.l.ChangeDutyCycle(value)
    setup.r.ChangeDutyCycle(0)
    time.sleep(0.3)
    print("turn_right")

def turnleft(value):
    goforward()
    setup.r.ChangeDutyCycle(value)
    setup.l.ChangeDutyCycle(0)
    time.sleep(0.3)
    print("turn_left")
'''

def stopmotors():
    GPIO.output(setup.right_motor_pin1, False)
    GPIO.output(setup.right_motor_pin2, False)
    GPIO.output(setup.left_motor_pin1, False)
    GPIO.output(setup.left_motor_pin2, False)
    time.sleep(1)