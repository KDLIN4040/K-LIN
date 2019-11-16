import sys, getopt
import GPIO_Setup
import RPi.GPIO as GPIO
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import threading  
import numpy as np
import Encoder
import Lidar
import observation
def main():
    try:
        
        threads = []
        t2 = Lidar.Lidar_Scan()
        t1 = Encoder.encoder()
        t3 = observation.observation()
        threads.append(t1)
        threads.append(t2) 
        threads.append(t3)
        for t in threads:
            t.start()


    except KeyboardInterrupt:
        GPIO_Setup.cleargpios()
        time.sleep(1)
        print("stop")


if __name__ == "__main__":
    main()