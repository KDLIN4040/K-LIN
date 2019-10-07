import GPIO_Setup
import RPi.GPIO as GPIO
import movement as mv
import sensor as s
import Obstacle_Avoidance as oa
import path_planning as pp
import numpy
import threading

def main():
    try:
    
        threads = []
        t1 = pp.wallfollowing("wallfollowing")
        threads.append(t1)
        t2 = oa.obstacle_avoidance("obstacle_avoidance")
        threads.append(t2)        
        for t in threads:
            t.start()

            

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("stop")

if __name__ == "__main__":
    main()