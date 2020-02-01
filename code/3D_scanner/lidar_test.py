import VL53L1X
import RPi.GPIO as IO
import time

IO.setwarnings(False)               #ignore what the pins were doing before

shutpin = 4

IO.setmode(IO.BCM)
IO.setup(shutpin, IO.OUT)
IO.output(shutpin, 1)

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open() # Initialise the i2c bus and configure the sensor
tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

while 1:
    distance = tof.get_distance() # Grab the range in mm
    print(distance)
    
