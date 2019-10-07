import GPIO_Setup as setup
import RPi.GPIO as GPIO
import time
# Functions for driving
def goforward():
        GPIO.output(setup.right_motor_pin1,1)
        GPIO.output(setup.right_motor_pin2,0)
        GPIO.output(setup.left_motor_pin1 ,1)
        GPIO.output(setup.left_motor_pin2 ,0)
        setup.r.start(50)
        setup.l.start(50)
        #print("goforward")

def turnright(value):
    goforward()
    setup.l.ChangeDutyCycle(value)
    setup.r.ChangeDutyCycle(0)
    time.sleep(0.5)
    #print("turn_right(%f)"%value)

def turnleft(value):
    goforward()
    setup.r.ChangeDutyCycle(value)
    setup.l.ChangeDutyCycle(0)
    time.sleep(0.5)
    #print("turn_left(%f)"%value)
def stopmotors():
    GPIO.output(setup.right_motor_pin1, False)
    GPIO.output(setup.right_motor_pin2, False)
    GPIO.output(setup.left_motor_pin1, False)
    GPIO.output(setup.left_motor_pin2, False)
    time.sleep(1)