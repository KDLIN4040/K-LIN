# -*- coding: utf8 -*-
import socket
import RobotPosition as rp
from rplidar import RPLidar as Lidar
import threading
import numpy as np
import struct
import time
def pose_read(pose):
    if rp.position_flag == True:
        #print(rp_position,rp_theta)
        pose = rp.position
    return pose

class rpslam(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        host = '192.168.11.29'  # 對server端為主機位置
        port = 2222
        address = (host, port)

        socket02 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET:默認IPv4, SOCK_STREAM:TCP

        socket02.connect(address)  # 用來請求連接遠程服務器
        
        LIDAR_DEVICE = '/dev/ttyUSB0'
        # Connect to Lidar unit
        lidar = Lidar(LIDAR_DEVICE)
        # Create an iterator to collect scan data from the RPLidar
        iterator = lidar.iter_scans(max_buf_meas=1000)
        # First scan is crap, so ignore it
        next(iterator)
        pose = [0.0, 0.0, 0.0]
        bufsize = 4096
        data_mix = []
        lock = threading.Lock()
        while True:
            
            pose = pose_read(pose)            
            # Extract (quality, angle, distance) triples from current scan
            items = [item for item in next(iterator)]
            distances = [item[2] for item in items]
            angles = [item[1] for item in items]

            items_size = [float(len(items))]
            data_mix.extend(pose)
            data_mix.extend(items_size)
            data_mix.extend(distances)
            data_mix.extend(angles)
            data = struct.pack('%sf'%(len(data_mix)),*data_mix)
            print(len(items))
            socket02.send(data)
            
            data = socket02.recv(bufsize)
            if not data : 
                print('Server say:', data)

            

            
            data_mix.clear()
            time.sleep(0.001)
        socket02.close()  # 關閉
        print('client close')

def main():
    try:
    
        threads = []
        t1 = rp.MARG()
        t2 = rp.encoder()
        t3 = rp.RobotPosition()
        t4 = rpslam()
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)
        for t in threads:
            t.start()
            
        

    except KeyboardInterrupt:
        GPIO.cleanup()
        time.sleep(1)
        print("stop")

if __name__ == '__main__':

    main()