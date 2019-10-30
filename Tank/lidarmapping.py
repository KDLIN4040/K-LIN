import math
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians, pi

def file_read(f):
    """
    Reading LIDAR laser beams (angles and corresponding distance data)
    """
    measures = []
    measures = np.loadtxt(f,usecols=(2,3))
    print (measures)
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances

ang, dist = file_read("out.txt")
ox = np.sin(ang) * dist
oy = np.cos(ang) * dist
plt.figure(figsize=(6,10))
plt.plot([oy, np.zeros(np.size(oy))], [ox, np.zeros(np.size(oy))], "ro-") # lines from 0,0 to the 
plt.axis("equal")
bottom, top = plt.ylim()  # return the current ylim
plt.ylim((top, bottom)) # rescale y axis, to match the grid orientation
plt.grid(True)
plt.show()