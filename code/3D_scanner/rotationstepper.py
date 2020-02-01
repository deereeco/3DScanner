#This function assumes a GT2 belt with a 20T pulley at each end with 1/16 stepping
def rotationstepper(steps, dirpin, dirstate, steppin):
    import RPi.GPIO as IO
    import time as t

    IO.setwarnings(False)         #ignore what the pins were doing before

    #CONSTANTS
    high = 1
    low = 0
    i_start = 1
    i_end = 16 * steps             # 1.8degrees/16steps 
    delay = 0.0001

    #GPIO SETUP
    IO.setmode(IO.BCM)              #declare naming convention for IO pins
    IO.setup(dirpin, IO.OUT)        #set pins as output
    IO.setup(steppin, IO.OUT)
    IO.output(dirpin, dirstate)     #set state of dirpin

    #LOOP
    while i_start <= i_end:         #turn stepper by sending pulses
        IO.output(steppin, high)
        t.sleep(delay)
        IO.output(steppin, low )
        t.sleep(delay)
        i_start += 1
