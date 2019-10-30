import numpy as np  
import matplotlib.pyplot as plt  


x= []
y= []
z= []
x = np.loadtxt('magneticdata.txt',usecols=(0,))
y = np.loadtxt('magneticdata.txt',usecols=(1,))
z = np.loadtxt('magneticdata.txt',usecols=(2,))
ax = plt.subplot()

offset_x = (max(x)+min(x))/2
offset_y = (max(y)+min(y))/2
offset_z = (max(z)+min(z))/2

###hard iron distortion
corrected_x = x[:] - offset_x
corrected_y = y[:] - offset_y
corrected_z = z[:] - offset_z


'''
###soft iron distortion
avg_delta =(offset_x+offset_y+offset_z)/3
scale_x = avg_delta/offset_x
scale_y = avg_delta/offset_y
scale_z = avg_delta/offset_z
corrected_x = (x[:]-offset_x)*scale_x
corrected_y = (y[:]-offset_y)*scale_y
corrected_z = (z[:]-offset_z)*scale_z
'''

ax.scatter(corrected_y,corrected_z,c='blue')
ax.scatter(corrected_x,corrected_z,c='red')
ax.scatter(corrected_x,corrected_y,c='green')

print(offset_x,offset_y,offset_z)


plt.show()