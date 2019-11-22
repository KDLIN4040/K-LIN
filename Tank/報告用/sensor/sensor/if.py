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
    try:
        data = ser.readline()
        voltage = data.decode()
        start = time.time()
        minus = 0
        for k in range(0,100,5):
            for i in range(0,150):
                try:
                    compare = datamatrix[i,1]
                    minus = int(voltage) - int(compare)
                    if(abs(minus) < k):
                        distance = datamatrix[i,0]
                        print (distan
                            ce)
                        end = time.time()
                        elapsed = end - start
                        print ("Time taken: ", elapsed, "seconds.")
                        break 
                except:
                    pass
                    
    
            else:
                continue
            break
    except:
                    pass
           
    