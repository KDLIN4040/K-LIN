import time
import threading  
import numpy as np
import RobotPosition as rp
import Lidar
class observation(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        
        while True :
            if rp.position_flag == True:
                position = rp.position
                print("position:{}".format(position))

            if Lidar.scan_flag == True:
                range_and_bearing = Lidar.lidar_data2
                if len(range_and_bearing)>1:
                    print("range_and_bearing{}".format(range_and_bearing))
                    
            time.sleep(0.1)

def main():
    try:
        
        threads = []
        t1 = rp.encoder()
        t2 = rp.MARG()
        t3 = rp.RobotPosition()
        t4 = Lidar.Lidar_Scan()
        t5 = observation() 
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)
        threads.append(t5)
        for t in threads:
            t.start()


    except KeyboardInterrupt:
        GPIO_Setup.cleargpios()
        time.sleep(1)
        print('Stoping.')
        lidar.stop()
        lidar.disconnect()
        outfile.close()
        print("stop")



if __name__ == "__main__":
    main()