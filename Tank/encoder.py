import RPi.GPIO as GPIO
import time  
import threading
import numpy as np
flag_backward = False
GPIO.setmode(GPIO.BOARD)
Ar_Wave = 11
Br_Wave = 13   
Al_Wave = 16
Bl_Wave = 18   
rcounter = 0
lcounter = 0
rturns = 0 
lturns = 0
class encoder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self): 
        GPIO.setup(Ar_Wave, GPIO.IN)
        GPIO.setup(Br_Wave, GPIO.IN)
        GPIO.setup(Al_Wave, GPIO.IN)
        GPIO.setup(Bl_Wave, GPIO.IN)
        ArLastState = GPIO.input(Ar_Wave)
        AlLastState = GPIO.input(Al_Wave)
        global rcounter
        global lcounter
        global rturns
        global lturns 

        while True:
            
            global flag_backward
            
            ### right wheel encoder 
            if flag_backward == False:
                Ar = GPIO.input(Ar_Wave)
                Br = GPIO.input(Br_Wave)
                Al = GPIO.input(Al_Wave)
                Bl = GPIO.input(Bl_Wave)
                
                if Ar != ArLastState:
                        Br = GPIO.input(Br_Wave)
                        if Br != Ar:
                                rcounter += 1
                        else:
                                rcounter -= 1
                        ArLastState = Ar
                        rturns = int(rcounter/50)
                        #print ("right:{}".format(rturns))
                if Al != AlLastState:
                        Bl = GPIO.input(Bl_Wave)
                        if Bl != Al:
                                lcounter += 1
                        else:
                                lcounter -= 1
                        AlLastState = Al
                        lturns = int(lcounter/50)
                        #print ("left:{}".format(lturns))        
          

            elif flag_backward == True:
                Ar = GPIO.input(Ar_Wave)
                Br = GPIO.input(Br_Wave)
                Al = GPIO.input(Al_Wave)
                Bl = GPIO.input(Bl_Wave)
                if Ar != ArLastState:
                        Br = GPIO.input(Br_Wave)
                        if Br != Ar:
                                rcounter += 1
                        else:
                                rcounter -= 1
                        -rcounter
                        rturns = int(rcounter/50)
                        #print ("right:{}".format(rturns))
                        ArLastState = Ar
                if Al != AlLastState:
                        Bl = GPIO.input(Bl_Wave)
                        if Bl != Al:
                                lcounter += 1
                        else:
                                lcounter -= 1
                        -lcounter
                        lturns = int(lcounter/50)
                        #print ("left:{}".format(lturns))       
                        AlLastState = Al   
            time.sleep(0.05)     
            print (rcounter)
        
def main():
    try:
        threads = []
        t1 = encoder()
        threads.append(t1)       
        for t in threads:
            t.start()

    except KeyboardInterrupt:
        GPIO_Setup.cleargpios()
        time.sleep(1)
        print("stop")

if __name__ == "__main__":
    main()