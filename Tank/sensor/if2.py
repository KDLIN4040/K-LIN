import time

from numpy import *
import numpy as np
import xlrd
import serial 
ser  = serial.Serial('/dev/ttyACM0',9600)
data = xlrd.open_workbook('infraded-sensor.xlsx')
table = data.sheets()[0]
nrows = table.nrows #行数
ncols = table.ncols #列数
c1=arange(0,nrows,1)
datamatrix=zeros((nrows,ncols))
for x in range(ncols):
    cols = np.matrix(table.col_values(x))
    datamatrix[:,x] = cols
while 1:
    data = ser.readline()
    voltage = data.decode()
    start = time.time()
    try:    
        voltage2 = int(voltage)
        distance = 8*pow(10,-9)*pow(voltage2,4) - 1*pow(10,-5)*pow(voltage2,3) + 0.007*pow(voltage2,2) - 1.8855*voltage2 + 238.53
        print (distance)
        end = time.time()
        elapsed = end - start
        print ("Time taken: ", elapsed, "seconds.")
    except:
        pass
                
