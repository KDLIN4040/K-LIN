import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

#define GPIO For Driver motors Right
right_motorEA_pin = 12
right_motor_pin1 = 16
right_motor_pin2 = 18
GPIO.setup(right_motor_pin1,GPIO.OUT)
GPIO.setup(right_motor_pin2,GPIO.OUT)
GPIO.setup(right_motorEA_pin,GPIO.OUT)
r = GPIO.PWM(right_motorEA_pin, 50) # GPIO for PWM with 50Hz

#define GPIO For Driver motors Left
left_motorEB_pin = 32
left_motor_pin1 = 22
left_motor_pin2 = 24
GPIO.setup(left_motor_pin1,GPIO.OUT)
GPIO.setup(left_motor_pin2,GPIO.OUT)
GPIO.setup(left_motorEB_pin,GPIO.OUT)
l = GPIO.PWM(left_motorEB_pin, 50) # GPIO for PWM with 50Hz

# Define GPIO for ultrasonic Front
front_trigger_pin = 31
front_echo_pin = 33
GPIO.setup(front_trigger_pin, GPIO.OUT)
GPIO.setup(front_echo_pin, GPIO.IN)

# Define GPIO for ultrasonic Right
right_trigger_pin = 35
right_echo_pin = 37
GPIO.setup(right_trigger_pin, GPIO.OUT)
GPIO.setup(right_echo_pin, GPIO.IN)

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

#cleargpios
def cleargpios():
    GPIO.output(7 , False)
    GPIO.output(13, False)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(18, False)
    GPIO.output(22, False)
    GPIO.output(24, False)
    GPIO.output(31, False)
    GPIO.output(32, False)
    GPIO.output(35, False)
    GPIO.output(38, False)   