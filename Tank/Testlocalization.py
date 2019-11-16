import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

xdata = []
ydata = []
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
d_yaw = np.array([0,0])
d = 0
dl = 0
xn = 0 
yn = 0 
def animate(i):
    global xdata
    global ydata
    global d_yaw
    global d
    global xn
    global yn
    x = d*math.cos(d_yaw[1])
    y = d*math.sin(d_yaw[1]) 
    xn += x
    yn += y
    #print(dl,d_yaw[0])
    xdata.append(xn)
    ydata.append(yn)
    ax1.clear()
    ax1.plot(xdata,ydata
if __name__ == "__main__":    
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()