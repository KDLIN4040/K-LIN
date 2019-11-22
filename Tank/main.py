import GPIO_Setup
import RPi.GPIO as GPIO
import Movement as mv
import Sensor as s
import Obstacle_Avoidance as oa
import path_planning as pp
import slam_test as st
import RobotPosition as rp
import Lidar 
import numpy as np
import threading
from pylive import live_plotter
def main():
    try:
    
        threads = []
        t1 = pp.wallfollowing("wallfollowing")
        t2 = oa.obstacle_avoidance("obstacle_avoidance")
        t3 = rp.MARG()
        t4 = rp.encoder()
        t5 = rp.RobotPosition()
        t6 = Lidar.Lidar_Scan()
        t7 = st.ekf_slam_start()
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)
        threads.append(t5)
        threads.append(t6)
        threads.append(t7)
        for t in threads:
            t.start()
            
        

    except KeyboardInterrupt:
        GPIO.cleanup()
        time.sleep(1)
        print("stop")


if __name__ == "__main__":
    main()
