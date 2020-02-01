
import RPi.GPIO as IO
import time as t
IO.setwarnings(False)         #ignore what the pins were doing before

dist = 200
dirpin = 23
dirstate = 1
steppin = 24

#CONSTANTS
high = 1
low = 0
i_start = 1
i_end = dist * 16
delay = 0.00001

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

IO.cleanup()
