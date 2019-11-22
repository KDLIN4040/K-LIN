#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:

$ ./record_measurments.py out.txt'''
### 10-40 ms
import sys
from rplidar import RPLidar
import math
import numpy as np
import threading
import datetime
PORT_NAME = '/dev/ttyUSB0'
lidar_measurement = []
lidar_data = np.array(lidar_measurement)
lidar_data2 = np.array(lidar_measurement)
lidar_rawdata = np.array([0,0])
scan_flag = False

class Lidar_Scan(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            '''Main function'''
            lidar = RPLidar(PORT_NAME)
             
            #outfile = open('out.txt', 'w')
            global lidar_measurement
            global lidar_rawdata
            global lidar_data
            global scan_flag
            global lidar_data2
            try:

                print('Recording measurments... Press Crl+C to stop.')
                
                for measurment in lidar.iter_measurments():
                    line = '\t'.join(str(v) for v in measurment)
                    angle = int(measurment[2]) 
                    distance = int(measurment[3])
                    lidar_rawdata = [distance,angle]
                    lidar_measurement.append(lidar_rawdata)
                    lidar_data = np.array(lidar_measurement)
                    length = len(lidar_data)
                    #print(length)
                    if length > 10:
                        lidar_data2 = lidar_data
                        scan_flag = True
                        lidar_measurement = []
                        lidar_data = np.array(lidar_measurement)
                        #print(lidar_data2)
                       
                 
                    '''
                    print('Recording measurments... Press Crl+C to stop.')
                    for measurment in lidar.iter_measurments():
                        line = '\t'.join(str(v) for v in measurment)
                        outfile.write(line + '\n')
                    '''
                               
                                                        
            except KeyboardInterrupt:
                print('Stoping.')
            lidar.stop()
            lidar.disconnect()
            outfile.close()
              
            time.sleep(0.01) 
