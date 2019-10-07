import serial
import RPi.GPIO as GPIO
import time
import threading
ser = serial.Serial('/dev/ttyACM0',9600)
trigger_pin = 11 
echo_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

global distance_cm		
distance_cm = 0
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.001)
    GPIO.output(trigger_pin, False)
def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count = count - 1
def get_distance():
	global distance_cm
	while 1 :
		send_trigger_pulse()
		wait_for_echo(True, 5000)
		start = time.time()
		wait_for_echo(False, 5000)
		finish = time.time()
		pulse_len = finish - start
		distance_cm = pulse_len * 340 *100 /2
		time.sleep(0.1)

t = threading.Thread(target = get_distance)
t.start()	
while 1:
	data = ser.readline()
	int distance = -7*10^-9*data^6 + 3*10^-6*data^5 - -0.0007*data^4 + 0.0636*data^3 - 2.9596*data^2 + 53.298*data + 211.34 
	print("infraded:{0} \nultrasonic:{1}".format(distance,distance_cm))	
	
	
