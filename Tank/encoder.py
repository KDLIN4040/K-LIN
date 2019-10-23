import RPi.GPIO as GPIO
import time  

A_ = 11
dt = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(clk, GPIO.IN)
GPIO.setup(dt, GPIO.IN)
counter = 0
clkLastState = GPIO.input(clk)
try:
        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                #print("clkState: {0}, dtState: {1}".format(clkState, dtState))
                if clkState != clkLastState:
                        dtState = GPIO.input(dt)
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print counter
                        clkLastState = clkState
                time.sleep(0.01)
finally:
        GPIO.cleanup()