'''
  Raspberry Pi GPIO Status and Control
'''
from flask import Flask, render_template, request, jsonify
import time
import Sensor as ss
import RPi.GPIO as GPIO
import numpy 
import threading 
import requests
from subprocess import check_output
from tuning import Tuning
import usb.core
import usb.util
from flask_cors import CORS
import sys, getopt
sys.path.append('.')
import RTIMU
import math
import socket
import sys
import os
from PIL import Image, ImageOps, ImageEnhance, ImageFont, ImageDraw
lock = threading.Lock()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Mic_direction = 0
fusionPose=[0,0,0]
def make_linear_ramp():
    # putpalette expects [r,g,b,r,g,b,...]
    ramp = [
    0,0,0,
    0,0,16,
    0,0,33,
    0,0,42,
    0,0,49,
    0,0,56,
    0,0,63,
    0,0,70,
    0,0,77,
    0,0,83,
    1,0,87,
    2,0,91,
    3,0,95,
    4,0,99,
    5,0,103,
    7,0,106,
    9,0,110,
    11,0,115,
    12,0,116,
    13,0,118,
    16,0,120,
    19,0,122,
    22,0,124,
    25,0,127,
    28,0,129,
    31,0,131,
    34,0,133,
    38,0,135,
    42,0,137,
    45,0,138,
    48,0,140,
    52,0,141,
    55,0,143,
    58,0,144,
    61,0,146,
    63,0,147,
    65,0,148,
    68,0,149,
    71,0,149,
    74,0,150,
    76,0,150,
    79,0,151,
    82,0,151,
    85,0,152,
    88,0,152,
    92,0,153,
    94,0,154,
    97,0,155,
    101,0,155,
    104,0,155,
    107,0,155,
    110,0,156,
    112,0,156,
    114,0,156,
    117,0,157,
    121,0,157,
    124,0,157,
    126,0,157,
    129,0,157,
    132,0,157,
    135,0,157,
    137,0,157,
    140,0,156,
    143,0,156,
    146,0,155,
    149,0,155,
    152,0,155,
    154,0,155,
    157,0,155,
    159,0,155,
    161,0,155,
    164,0,154,
    166,0,154,
    168,0,153,
    170,0,153,
    172,0,152,
    174,0,152,
    175,1,151,
    177,1,151,
    178,1,150,
    180,1,149,
    182,2,149,
    183,3,149,
    185,4,148,
    186,4,147,
    188,5,147,
    189,5,146,
    190,5,146,
    191,6,145,
    192,7,144,
    193,9,143,
    194,10,142,
    195,11,141,
    197,12,139,
    198,13,138,
    200,15,136,
    201,17,134,
    202,18,133,
    203,20,131,
    204,21,129,
    206,23,126,
    207,24,123,
    208,26,121,
    208,27,118,
    209,28,116,
    210,30,113,
    211,32,111,
    212,34,108,
    213,36,104,
    214,38,101,
    216,40,98,
    217,42,95,
    218,44,91,
    219,46,87,
    220,47,81,
    221,49,76,
    222,51,70,
    223,53,65,
    223,54,59,
    224,56,54,
    224,57,48,
    225,59,42,
    226,61,37,
    227,63,31,
    228,65,28,
    228,67,25,
    229,69,23,
    230,71,21,
    231,72,19,
    231,74,17,
    232,76,15,
    233,77,13,
    234,78,11,
    234,80,10,
    235,82,9,
    235,84,8,
    236,86,8,
    236,87,7,
    236,89,7,
    237,91,6,
    237,92,5,
    238,94,4,
    238,95,4,
    239,97,3,
    239,99,3,
    240,100,3,
    240,102,3,
    241,103,2,
    241,104,2,
    241,106,1,
    241,107,1,
    242,109,1,
    242,111,1,
    243,113,1,
    243,114,0,
    243,115,0,
    244,117,0,
    244,119,0,
    244,121,0,
    244,124,0,
    245,126,0,
    245,128,0,
    246,129,0,
    246,131,0,
    247,133,0,
    247,134,0,
    248,136,0,
    248,137,0,
    248,139,0,
    248,140,0,
    249,142,0,
    249,143,0,
    249,144,0,
    249,146,0,
    249,148,0,
    250,150,0,
    250,153,0,
    251,155,0,
    251,157,0,
    252,159,0,
    252,161,0,
    253,163,0,
    253,166,0,
    253,168,0,
    253,170,0,
    253,172,0,
    253,174,0,
    254,176,0,
    254,177,0,
    254,178,0,
    254,181,0,
    254,183,0,
    254,185,0,
    254,186,0,
    254,188,0,
    254,190,0,
    254,191,0,
    254,193,0,
    254,195,0,
    254,197,0,
    254,199,0,
    254,200,0,
    254,202,1,
    254,203,1,
    254,205,2,
    254,206,3,
    254,207,4,
    254,209,6,
    254,211,8,
    254,213,10,
    254,215,11,
    254,216,12,
    254,218,14,
    255,219,16,
    255,220,20,
    255,221,24,
    255,222,28,
    255,224,32,
    255,225,36,
    255,227,39,
    255,228,44,
    255,229,50,
    255,230,56,
    255,231,62,
    255,233,67,
    255,234,73,
    255,236,79,
    255,237,85,
    255,238,92,
    255,238,98,
    255,239,105,
    255,240,111,
    255,241,119,
    255,241,127,
    255,242,135,
    255,243,142,
    255,244,149,
    255,244,156,
    255,245,164,
    255,245,171,
    255,246,178,
    255,247,184,
    255,247,190,
    255,248,195,
    255,248,201,
    255,249,206,
    255,250,212,
    255,251,218,
    255,252,224,
    255,253,229,
    255,253,235,
    255,254,240,
    255,254,244,
    255,255,249,
    255,255,252,
    255,255,255]

    return ramp

a =1 
def thermal():
    global a
    
    HeatMap = make_linear_ramp() 

    lock.acquire()    
    os.system("./agcenable.exe")
    lock.release()
    #font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf",6)

    text = 1
    tcolor = (255,255,0)
    text_pos = (0,0)
    framecounter = 0
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    # Bind the socket to the port
    server_address = ('', 8080)
    #print 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    sock.listen(1)
    #a = 0
    try:

        while True:
                print ('waiting for a connection')
                connection, client_address = sock.accept()
                connection.sendall("HTTP/1.1 200 OK\n".encode())
                connection.sendall("Content-Type: multipart/x-mixed-replace;boundary=--informs\n".encode())
                #connection.sendall("Transfer-Encoding: chunked\n".encode()) 
                
                while(True):
                    lock.acquire()
                    var = os.system("./frame.exe")
                    lock.release()
                    if (var == 0 ): 
                        
                      
                        data = numpy.loadtxt("/run/shm/Numpey.dat", numpy.uint8)

                        framecounter = framecounter + 1
                        #print ("frame: " + str(framecounter))

                        image = Image.fromarray(data)
                        
                        image.putpalette(HeatMap)
                        image = image.convert('RGB')
                        
                        #image = image.rotate(90).resize((80*5, 60*5), Image.ANTIALIAS)
                        image = image.resize((80*5, 60*5))

                        #draw = ImageDraw.Draw(image)
                        #draw.text(text_pos, str(framecounter), fill=tcolor, font=font)

                        TmpFileName = "/dev/shm/latest.jpg"

                        quality_val = 80
                        image.save(TmpFileName, quality=quality_val)
                        connection.sendall("\n--informs\n".encode())
                        connection.sendall("Content-Type: image/jpeg\n".encode())
                        test=str(os.stat(TmpFileName).st_size)
                        connection.sendall("Content-Length: ".encode() + test.encode() + "\n\n".encode())
                        #print ("Image Size: ",test)
                        
                        with open(TmpFileName, 'rb') as f:
                            data = f.read()
                            f.close()

                        connection.sendall(data)
                        connection.sendall("\n".encode())
                        connection.sendall("".encode())
                        #time.sleep(0.01)
                        
                    else:
                      print ("\nWarning failed read")
                      time.sleep(1)
                    
    finally:
            #Clean up the connection
            connection.close()
            
app = Flask(__name__)
CORS(app)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Mic_direction = 0
fusionPose=[0,0,0]

##the thermal image has something error 3/23
@app.route('/getattitude',methods=['GET'])

def getattitude():
  global fusionPose
  data = fusionPose
  roll =int(math.degrees(data[0]))
  pitch = int(math.degrees(data[1]))
  yaw = int(math.degrees(data[2]))
  attitude=''
  attitude=str(roll)+','+str(-pitch)+','+str(-yaw)
  time.sleep(0.01)
  return  str(attitude)
 
SETTINGS_FILE="RTIMULib"
print("Using settings file" + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
 print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
 print("IMU Init Failed")
 #sys.exit(1)
else:
 print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval : %dms\n" % poll_interval)

def readimu():
    global i2cflag
    global fusionPose
    
    while True:
      if imu.IMURead() :
        lock.acquire()
        data = imu.getIMUData()
        lock.release()
        fusionPose = data["fusionPose"]
        #print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
        time.sleep(poll_interval*1.0/1000.0)
      else:pass
        
@app.route('/askangle',methods=['GET'])
def askangle():  
  global Mic_direction
  sound()
  angle= Mic_direction
  time.sleep(0.01)
  return str(angle)
  
                           
def sound():
  global Mic_direction
  #lock.acquire()
  dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
  #lock.release()
  if dev :
    #lock.acquire()
    Mic_tuning = Tuning(dev)
    #while True:
    try:
       Mic_direction = Mic_tuning.direction
       print(Mic_direction)
       time.sleep(1)
    except KeyboardInterrupt:
       pass
    #lock.release()
#define bee

GPIO.setup(7,GPIO.OUT)
def bee():
  p=GPIO.PWM(7,659)
  for i in range (5):
    p.start(100)
    time.sleep(0.5)
    p.stop()
    time.sleep(0.5)
  
#define actuators motor GPIOs
right_motorEA_pin=12
right_motor_pin1 = 16
right_motor_pin2 = 18
left_motorEB_pin = 22
left_motor_pin1 = 32
left_motor_pin2 = 24

#initialize GPIO status variables
forwardSts = 0
movement = 0
forwardSts = 0
backwardSts = 0
turnrightSts = 0
turnleftSts = 0

#Define motor pins as output
GPIO.setup(right_motor_pin1,GPIO.OUT)
GPIO.setup(right_motor_pin2,GPIO.OUT)
GPIO.setup(right_motorEA_pin,GPIO.OUT)
r = GPIO.PWM(right_motorEA_pin,50) # GPIO for PWM with 50Hz
GPIO.setup(left_motor_pin1,GPIO.OUT)
GPIO.setup(left_motor_pin2,GPIO.OUT)
GPIO.setup(left_motorEB_pin,GPIO.OUT)
l = GPIO.PWM(left_motorEB_pin,50) # GPIO for PWM with 50Hz


#define car movement
def backward():
  GPIO.output(right_motor_pin1,1)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,1)
  GPIO.output(left_motor_pin2 ,0)
  r.start(100)
  l.start(100)
  print("backward")
def forward():
  GPIO.output(right_motor_pin1,0)
  GPIO.output(right_motor_pin2,1)
  GPIO.output(left_motor_pin1 ,0)
  GPIO.output(left_motor_pin2, 1)
  r.start(100)
  l.start(100)
  print("forward")

def turnright():
  GPIO.output(right_motor_pin1,0)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,1)
  GPIO.output(left_motor_pin2, 0)
  r.start(100)
  l.start(100)
  print("turnright")

def turnleft():
  GPIO.output(right_motor_pin1,1)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,0)
  GPIO.output(left_motor_pin2, 0)
  r.start(100)
  l.start(100)
  print("turnleft")
def movearc():
  GPIO.output(right_motor_pin1,0)
  GPIO.output(right_motor_pin2,1)
  GPIO.output(left_motor_pin1,0)
  GPIO.output(left_motor_pin2,1)
  r.start(30)
  l.start(100)
  print("movearc")
def stopmotors():
  GPIO.output(right_motor_pin1, False)
  GPIO.output(right_motor_pin2, False)
  GPIO.output(left_motor_pin1, False)
  GPIO.output(left_motor_pin2, False)
  time.sleep(1)


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
left_trigger_pin = 13 
left_echo_pin = 15
GPIO.setup(left_trigger_pin, GPIO.OUT)
GPIO.setup(left_echo_pin, GPIO.IN)

# Define GPIO for wallfollowing 
right_trigger_pin = 38 
right_echo_pin = 40
GPIO.setup(right_trigger_pin, GPIO.OUT)
GPIO.setup(right_echo_pin, GPIO.IN)

def right_distance():
    distance = ss.get_distance(right_trigger_pin,right_echo_pin)
    return distance

def front1_distance():
    frontobstacle_distacne_cm = ss.get_distance(front1_trigger_pin,front1_echo_pin)
    return(frontobstacle_distacne_cm)

def front2_distance():
    rightobstacle_distance_cm = ss.get_distance(front2_trigger_pin,front2_echo_pin)
    return(rightobstacle_distance_cm)

def left_distance():
    leftobstacle_distance_cm  = ss.get_distance(left_trigger_pin, left_echo_pin)
    return(leftobstacle_distance_cm )

autoflag = False

def wallfollower():
        try:    
            right1 = 40
            right2 = 40
            front1 = 40
            front2 = 40
            left   = 40
            global autoflag
            while True:
                if (autoflag == True):
                    right = right_distance()
                    front1 = front1_distance()
                    front2 = front2_distance()
                    left   = left_distance()           
                    print("right:{},front1:{},front2:{},left:{}".format(right,front1,front2,left))
                                                            
                    if (front1 <20 ) or (front2 < 20):
                        stopmotors()
                        backward()
                        time.sleep(0.5)
                        turnleft()
                        time.sleep(0.3)
                    elif right < 20 :
                        turnleft()
                        time.sleep(0.2)
                    elif left < 20 :
                        turnright()
                        time.sleep(0.2)
                    elif sweetspot_lowerbond < right < sweetspot_upperbond :
                        forward()
                        time.sleep(0.2)
                    else:
                        forward() 
                        time.sleep(0.2)  
                    time.sleep(0.1)
                 
        except KeyboardInterrupt:
            stopmotors()
            GPIO.cleanup()
            time.sleep(1)
            print("stop") 


def check_WiFi():
    global autoflag
    while True:

      try:   
         wifi_ip=check_output(['hostname','-I'])
         if wifi_ip != b'\n':
           print('connected {}'.format(wifi_ip))
         else:
           print('not connected')
           autoflag=False
           stopmotors()
           bee() 
   
      except:
           pass
      
      time.sleep(3)   


app = Flask(__name__)
CORS(app)


##the thermal image has something error 3/23
@app.route('/getattitude',methods=['GET'])

def getattitude():
  global fusionPose
  data = fusionPose
  roll =int(math.degrees(data[0]))
  pitch = int(math.degrees(data[1]))
  yaw = int(math.degrees(data[2]))
  attitude=''
  attitude=str(roll)+','+str(-pitch)+','+str(-yaw)
  time.sleep(0.01)
  return  str(attitude)
  
@app.route('/askangle',methods=['GET'])
def askangle():  
  global Mic_direction
  sound()
  angle= Mic_direction
  time.sleep(0.01)
  return str(angle)


@app.route("/")
def index():
  global forwardSts
  global backwardSts
  global turnrightSts
  global turnleftSts
  templateData = {
              'title' : 'GPIO output Status!',
              'forward'  : forwardSts,
              'turnright'  : turnrightSts,
              'turnleft'  : turnleftSts,
              'backward'  : backwardSts,
                  }
  return render_template('index.html', **templateData)
  
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
  global forwardSts
  global backwardSts
  global turnrightSts
  global turnleftSts
  global autoflag  
  
  if deviceName == 'auto':
    movement = 'auto'
  elif deviceName == 'forward':
    movement = 'forward'
  elif deviceName == 'turnright':
    movement = 'turnright'
  elif deviceName == 'turnleft':
    movement = 'turnleft'
  elif deviceName == 'backward':
    movement = 'backward'
  elif deviceName == 'stopmotors':
    movement = 'stopmotors'

  if action == "on":
    if movement == "auto" :
      autoflag = True  
    elif movement == "forward" :
      forward()
    elif movement == "turnright":
      turnright()
    elif movement == "turnleft":
      turnleft()
    elif movement == "backward":
      backward()
    elif movement == "stopmotors":
      stopmotors()

  if action == "off":
    if movement == "auto" :
      autoflag = False
      stopmotors()
      print("change to manual mode")
    elif movement == "forward" :
      stopmotors()
    elif movement == "turnright":
      stopmotors()
    elif movement == "turnleft":
      stopmotors()
    elif movement == "backward":
      stopmotors()


  templateData = {
              'forward'  : forwardSts,
              'turnright'  : turnrightSts,
              'turnleft'  : turnleftSts,
              'backward'  : backwardSts,
  }
  return render_template('index.html', **templateData)

            
if __name__ == "__main__":
   #app.run(host='0.0.0.0',port=81,threaded=True,debug=True)
   t1=threading.Thread(target=thermal)
   t1.start()
   time.sleep(0.1)
   t2=threading.Thread(target=readimu)
   #t2.start()
   time.sleep(0.1)
   t3=threading.Thread(target=wallfollower)
   t3.start()
   time.sleep(0.1)
   t4=threading.Thread(target=check_WiFi)
   #t4.start()
   time.sleep(0.1)
   app.run(host='0.0.0.0',port=81,threaded=True,debug=False)
     
