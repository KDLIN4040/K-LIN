import time
from numpy import *
import numpy as np
import xlrd
import serial 
ser  = serial.Serial('/dev/ttyACM1',9600)
data = xlrd.open_workbook('infraded-sensor.xlsx')
table = data.sheets()[0]
nrows = table.nrows 
ncols = table.ncols 
c1=arange(0,nrows,1)
datamatrix=zeros((nrows,ncols))
for x in range(ncols):
    cols = np.matrix(table.col_values(x))
    datamatrix[:,x] = cols
while 1:
    try:
        data = ser.readline()
        voltage = data.decode()
        start = time.time()
        for i in range(1,150):
            try:
                front = datamatrix[i-1,1]
                behind = datamatrix[i+1,1]
                if (front>int(voltage)) and (int(voltage)>behind):
                    distance = datamatrix[i,0]
                    print (distance)
                    end = time.time()
                    elapsed = end- start
                    print ("Time taken: ", elapsed, "seconds.")
                    break 
            except:           
                pass
                    
    except: 
        pass