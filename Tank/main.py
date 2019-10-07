import GPIO_Setup
import RPi.GPIO as GPIO
import movement as mv
import sensor as s
import Obstacle_Avoidance 
import path_planning as pp
import numpy
import threading

def main():
    try:
        #define plot 
        '''size = 100
        x_vec = np.linspace(0,1,size+1)[0:-1]
        y_vec = np.random.randn(len(x_vec))
        line1 = []
        '''
        threads = []
        t1 = pp.wallfollowing("wallfollowing")
        threads.append(t1)
        t2 = pp.obstacle_avoidance("obstacle_avoidance")
        threads.append(t2)        
        for t in threads:
            t.start()
        #pp.wallfollowing("wallfollowing",test).start()
        #pp.obstacle_avoidance("obstacle_avoidance").start()
        #print("456")
        '''    
            time.sleep(1)
            rand_val = np.random.randn(1)
            y_vec[-1] = rand_val 	
            line1 = live_plotter(x_vec,y_vec,line1)
            y_vec = np.append(y_vec[1:],0.0)
        '''
            

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("stop")

if __name__ == "__main__":
    main()