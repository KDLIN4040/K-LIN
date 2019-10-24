import RPi.GPIO as GPIO
import time  
counter = 0
flag_backward = True
def encoder():
    try:
        A_Wave = 11
        B_Wave = 13
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(A_Wave, GPIO.IN)
        GPIO.setup(B_Wave, GPIO.IN)
        ALastState = GPIO.input(A_Wave)

        while True:
            
            global counter
            global flag_backward
            if flag_backward == False:
                A = GPIO.input(A_Wave)
                B = GPIO.input(B_Wave)
                if A != ALastState:
                        B = GPIO.input(B_Wave)
                        if B != A:
                                counter += 1
                        else:
                                counter -= 1
                        print counter
                        ALastState = A
                time.sleep(0.01)
            elif flag_backward == True:
                counter = 0
                A = GPIO.input(A_Wave)
                B = GPIO.input(B_Wave)
                if A != ALastState:
                        B = GPIO.input(B_Wave)
                        if B != A:
                                counter += 1                    
                        else:
                                counter -= 1
                        -counter
                        print counter
                        ALastState = A
                time.sleep(0.01)
    finally:
            GPIO.cleanup()          

def main():
    encoder()

if __name__ == "__main__":
    main()