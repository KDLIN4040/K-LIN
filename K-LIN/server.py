# -*- coding: utf8 -*-
#!/usr/bin/env python3

'''
rpslam.py : BreezySLAM Python with SLAMTECH RP A1 Lidar
                 
Copyright (C) 2018 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

MAP_SIZE_PIXELS         = 250
MAP_SIZE_METERS         = 10


# Ideally we could use all 250 or so samples that the RPLidar delivers in one 
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES   = 150

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from roboviz import MapVisualizer
import threading
import numpy as np
import socket
import struct
def main():
    try:
        host = '192.168.11.29'  # 對server端為主機位置
        port = 2222
        address = (host, port)

        socket01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET:默認IPv4, SOCK_STREAM:TCP

        socket01.bind(address)  # 讓這個socket要綁到位址(ip/port)
        socket01.listen(5)  # listen(backlog)
        # backlog:操作系統可以掛起的最大連接數量。該值至少為1，大部分應用程序設為5就可以了
        print('Socket Startup')

        conn, addr = socket01.accept()  # 接受遠程計算機的連接請求，建立起與客戶機之間的通信連接
        # 返回（conn,address)
        # conn是新的套接字對象，可以用來接收和發送數據。address是連接客戶端的地址
        print('Connected by', addr)

        # Create an RMHC SLAM object with a laser model and optional robot model
        slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

        # Set up a SLAM display
        viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')

        # Initialize an empty trajectory
        trajectory = []

        # Initialize empty map
        mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

        # We will use these to store previous scan in case current scan is inadequate
        previous_distances = None
        previous_angles    = None
        bufsize = 4096  # 指定要接收的數據大小
        distances = []
        angles = []
        pose = []
        while True:
            
            
            
            data = conn.recv(bufsize)  # 接收遠端主機傳來的數據(distance)
            data_mix = struct.unpack('%sf' %(len(data)//4),data)
            pose[0:3] = data_mix[0:3]
            item_size = int(data_mix[3])
            distances[0:item_size] = data_mix[1:item_size+1]
            angles[0:item_size] = data_mix[item_size+1:2*item_size+1]
            

            string = 'distance' 
            conn.send(bytes(string, encoding = "utf8"))  # 發送數據給指定的遠端主機
            


            # Update SLAM with current Lidar scan and scan angles if adequate
            if (len(distances) > MIN_SAMPLES) and (len(distances) == len(angles)):
                slam.update(distances,scan_angles_degrees=angles)
                previous_distances = distances.copy()
                previous_angles    = angles.copy()

            # If not adequate, use previous
            elif previous_distances is not None:
                slam.update(previous_distances, scan_angles_degrees=previous_angles)
 

            # Get current robot position
            x, y, theta = slam.getpos()
            print(theta)
            # Get current map bytes as grayscale
            slam.getmap(mapbytes)
            distances.clear()
            angles.clear()
            # Display map and robot pose, exiting gracefully if user closes it
            if not viz.display(x/1000., y/1000., theta, mapbytes):
                exit(0)
            

    except KeyboardInterrupt:
        print("stop")
        conn.close()  # 關閉
        print('server close')
if __name__ == '__main__':

    main()