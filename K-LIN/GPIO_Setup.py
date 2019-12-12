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
left_motorEB_pin = 26
left_motor_pin1 = 22
left_motor_pin2 = 24
GPIO.setup(left_motor_pin1,GPIO.OUT)
GPIO.setup(left_motor_pin2,GPIO.OUT)
GPIO.setup(left_motorEB_pin,GPIO.OUT)
l = GPIO.PWM(left_motorEB_pin, 50) # GPIO for PWM with 50Hz

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

# Define GPIO for encoder
Ar_Wave = 11
Br_Wave = 13   
Al_Wave = 16
Bl_Wave = 18 
GPIO.setup(Ar_Wave, GPIO.IN)
GPIO.setup(Br_Wave, GPIO.IN)
GPIO.setup(Al_Wave, GPIO.IN)
GPIO.setup(Bl_Wave, GPIO.IN)

#cleargpios
