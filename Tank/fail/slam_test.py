import sys, getopt
import GPIO_Setup
import RPi.GPIO as GPIO
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import matplotlib.pyplot as plt
import threading  
import numpy as np
import Lidar
import observation as ov
import RobotPosition as rp

#EKF state covariance 
#Cx = np.diag([0.5, 0.5, np.deg2rad(30.0)]) ** 2
Cx = np.diag([0.1, 0.1, 0.1])

# Simulation parameter
#Q_sim = np.diag([0.2, np.deg2rad(1.0)]) ** 2
#R_sim = np.diag([1.0, np.deg2rad(10.0)]) ** 2
Q_sim = np.diag([0.1, 0.1])
R_sim = np.diag([0.1, 0.1])


DT = 0.1 # time ticl [s]
SIM_TIME = 10.0 # simulation time [s]
MAX_RANGE = 360 # maximum observation range 
M_DIST_TH = 2.0  # Threshold of Mahalanobis distance for data association.
STATE_SIZE = 3 # state size [x, y, yaw]
LM_SIZE = 2 # LM state size [x, y]

show_animation = True

def ekf_slam(xEst, PEst, u, z):
    # Predict 
    S = STATE_SIZE
    xEst[0:S] = motion_model(xEst[0:S],u)
    G, Fx = jacob_motion(xEst[0:S],u)
    PEst[0:S, 0:S] = G.T * PEst[0:S, 0:S] * G + Fx.T* Cx   
    initP = np.eye(2)

    # Update 
    for iz in range(len(z[:,0])): # for each observation (in this case it is landmark's distance & angle measured by the lidar)
        minid = search_correspond_landmark_id(xEst, PEst, z[iz, 0:2])

        nLM = calc_n_lm(xEst)
        if minid == nLM:
            print("New LM")
            # Extend state and covariance matrix
            xAug = np.vstack((xEst, calc_landmark_position(xEst, z[iz, :])))
            PAug = np.vstack((np.hstack((PEst, np.zeros((len(xEst), LM_SIZE)))),
                              np.hstack((np.zeros((LM_SIZE, len(xEst))), initP))))
            xEst = xAug
            PEst = PAug
        lm = get_landmark_position_from_state(xEst, minid)
        y, S, H = calc_innovation(lm, xEst, PEst, z[iz, 0:2], minid)
        K = (PEst @ H.T) @ np.linalg.inv(S)
        xEst = xEst #+ (K @ y)
        PEst = (np.eye(len(xEst)) - (K @ H)) @ PEst

    #xEst[2] = pi_2_pi(xEst[2])
    return xEst, PEst

def calc_input(position1,theta,rp_position,rp_theta):
    # it will be the global x,y,yaw from path_planning 
    #v = 1.0 #[m/s]
    
    x1 = position1[0]
    y1 = position1[0]
    theta1 = theta
    x2 = rp_position[0]
    y2 = rp_position[1]
    theta2 = rp_theta
    trans = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    rot1 = rp_theta
    rot2 = math.radians(68) 
    print(rot1)
    # yawrate = difference of right wheel and left wheel speed  
    #yawrate = 0 #[rad/s]
    u = np.array([[rot1, trans, rot2]]).T
    return u , rp_position, rp_theta     


def motion_model(x,u):
    F = np.array([[1.0, 0, 0],
                 [0, 1.0, 0],
                 [0, 0, 1.0]])
    
    Bu = np.array([u[1] * math.cos( u[0]), u[1] * math.sin( u[0]), u[0] + u[2]])
    x = (F @ x) + Bu
    return x

def observation(xTrue, xd, u, LIDAR):
    #xTrue in here would be change by encoder and imu measurement
    xTrue = motion_model(xTrue, u)

    # add noise to gps x-y 
    # in my suggest it is not needed in pritical
    z = np.zeros((0, 3))

    for i in range(len(LIDAR[:, 0])):

        dx = LIDAR[i, 0] - xTrue[0, 0]
        dy = LIDAR[i, 1] - xTrue[1, 0]
        d = math.sqrt(dx ** 2 + dy ** 2)
        angle = pi_2_pi(math.atan2(dy, dx) - xTrue[2, 0])
        if d <= MAX_RANGE:
            dn = d + np.random.randn() * Q_sim[0, 0] ** 0.5  # add noise
            anglen = angle + np.random.randn() * Q_sim[1, 1] ** 0.5  # add noise
            zi = np.array([dn, anglen, i])
            z = np.vstack((z, zi))

    # add noise to input
    # you don't need to add noise in pritical actually
    '''
    ud = np.array([[
        u[0, 0] + np.random.randn() * R_sim[0, 0] ** 0.05,
        u[1, 0] + np.random.randn() * R_sim[1, 1] ** 0.05]]).T
    '''
    ud = u 
    xd = motion_model(xd, ud)
    return xTrue, z, xd, ud

def jacob_motion(x, u):
    #align landmark information to match the state matrix x
    Fx = np.hstack((np.eye(STATE_SIZE), np.zeros(
        (STATE_SIZE, LM_SIZE * calc_n_lm(x)))))
    # jacobian of the Motion so cos --> -sin
    jF = np.array([[1.0, 0.0, -u[1] * math.sin(x[2] + u[0])],
                   [0.0, 0.0, -u[1] * math.cos(x[2] + u[0])],
                   [0.0, 0.0, 1.0]])

    G = np.eye(STATE_SIZE) + Fx.T * jF * Fx
    return G, Fx

def calc_n_lm(x):
    n = int((len(x) - STATE_SIZE )/LM_SIZE)
    return n

def calc_landmark_position(x, z):
    zp = np.zeros((2, 1))

    zp[0, 0] = x[0, 0] + z[0] * math.cos(x[2, 0] + z[1])
    zp[1, 0] = x[1, 0] + z[0] * math.sin(x[2, 0] + z[1])
    # zp[0, 0] = x[0, 0] + z[0, 0] * math.cos(x[2, 0] + z[0, 1])
    # zp[1, 0] = x[1, 0] + z[0, 0] * math.sin(x[2, 0] + z[0, 1])

    return zp

def get_landmark_position_from_state(x, ind):
    lm = x[STATE_SIZE + LM_SIZE * ind : STATE_SIZE + LM_SIZE * (ind + 1), :]
    return lm

def calc_innovation(lm, xEst, PEst, z, LMid):
    delta = lm - xEst[0:2]
    q = (delta.T @ delta)[0, 0]
    zangle = math.atan2(delta[1, 0], delta[0, 0]) - xEst[2, 0]
    zp = np.array([[math.sqrt(q), pi_2_pi(zangle)]])
    y = (z - zp).T
    y[1] = pi_2_pi(y[1])
    H = jacob_h(q, delta, xEst, LMid + 1)
    S = H @ PEst @ H.T + Cx[0:2, 0:2]

    return y, S, H

def search_correspond_landmark_id(xAug, PAug, zi):
    """
    Landmark association with Mahalanobis distance
    """
    nLM = calc_n_lm(xAug)

    mdist = []

    for i in range(nLM):
        lm = get_landmark_position_from_state(xAug, i)
        y, S, H = calc_innovation(lm, xAug, PAug, zi, i)
        mdist.append(y.T @ np.linalg.inv(S) @ y)

    mdist.append(M_DIST_TH)  # new landmark

    minid = mdist.index(min(mdist))

    return minid
def pi_2_pi(angle):
    angle = math.radians(angle)
    return angle

def jacob_h(q, delta, x, i):
    sq = math.sqrt(q)
    G = np.array([[-sq * delta[0, 0], - sq * delta[1, 0], 0, sq * delta[0, 0], sq * delta[1, 0]],
                  [delta[1, 0], - delta[0, 0], - 1.0, - delta[1, 0], delta[0, 0]]])

    G = G / q
    nLM = calc_n_lm(x)
    F1 = np.hstack((np.eye(3), np.zeros((3, 2 * nLM))))
    F2 = np.hstack((np.zeros((2, 3)), np.zeros((2, 2 * (i - 1))),
                    np.eye(2), np.zeros((2, 2 * nLM - 2 * i))))

    F = np.vstack((F1, F2))

    H = G @ F

    return H

def position_read(rp_position,rp_theta):
    if rp.position_flag == True:
        #print(rp_position,rp_theta)
        rp_position = rp.position
        rp_theta = rp_position[2]
    return rp_position,rp_theta

def measurement_read(LIDAR):
    if Lidar.scan_flag == True:
        LIDAR = []
        LIDAR = Lidar.lidar_data
    return LIDAR

class ekf_slam_start(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print(__file__ + " start!!")
        np.seterr(divide='ignore', invalid='ignore')
        time = 0.0

        # LIDAR positions [x, y]
        ## Lidar measurement
        LIDAR = np.array([[1, 1],
                         [1, 1],
                         [1, 1],
                         [1, 1]])

        # State Vector [x y yaw v]'
        xEst = np.zeros((STATE_SIZE, 1))
        xTrue = np.zeros((STATE_SIZE, 1))
        PEst = np.eye(STATE_SIZE)

        xDR = np.zeros((STATE_SIZE, 1))  # Dead reckoning
        position1 = np.array([0,0])
        rp_position = np.array([0,0])
        theta = 0
        rp_theta = 0
        # history
        hxEst = xEst
        hxTrue = xTrue
        hxDR = xTrue  
        
        #while SIM_TIME >= time:
        while True:
                            
        
            #time += DT
            rp_position, rp_theta = position_read(rp_position,rp_theta)
            LIDAR = measurement_read(LIDAR)
            print(LIDAR)
            u, position1, theta = calc_input(position1,theta,rp_position,rp_theta)
            #xTrue, z, xDR, ud = observation(xTrue, xDR, u, LIDAR)
            xEst, PEst = ekf_slam(xEst, PEst, u, LIDAR)

            x_state = xEst[0:STATE_SIZE]

            # store data history
            hxEst = np.hstack((hxEst, x_state))
            hxDR = np.hstack((hxDR, xDR))
            hxTrue = np.hstack((hxTrue, xTrue))
            
            if show_animation:  # pragma: no cover
                plt.cla()

                #plt.plot(LIDAR[:, 0], LIDAR[:, 1], "*k")
                #plt.plot(xEst[0], xEst[1], ".r")
                '''

                
                plt.plot(hxTrue[0, :],
                         hxTrue[1, :], "-b")
                plt.plot(hxDR[0, :],
                         hxDR[1, :], "-k")
                '''
                # plot landmark
                for i in range(calc_n_lm(xEst)):
                    plt.plot(xEst[STATE_SIZE + i * 2],
                             xEst[STATE_SIZE + i * 2 + 1], "xg")
                plt.plot(hxEst[0, :],
                         hxEst[1, :], "-r")
                
                plt.axis("equal")
                plt.grid(True)
                plt.pause(0.001)  

def main():
    try:
        
        threads = []
        t1 = rp.encoder()
        t2 = rp.MARG()
        t3 = rp.RobotPosition()
        t4 = Lidar.Lidar_Scan()
        t5 = ekf_slam_start()
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
        print("stop")


if __name__ == "__main__":
    main()