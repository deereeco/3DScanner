def record_z_line(z_step, height, step_dir_pin, step_dir_state, step_step_pin):

    import VL53L1X as lidar
    import RPi.GPIO as IO
    import time as t

    IO.setwarnings(False)         #ignore what the pins were doing before

    #CONSTANTS FOR STEPPER MOTOR
    high = 1
    low = 0
    i_end = 80 * z_step
    delay = 0.0001

    #CONSTANTS FOR FILE ACCESS
    z_location = 0
    write_flag = 1
    curr_points_file = 'curr_points.txt'

    #GPIO SETUP
    IO.setmode(IO.BCM)              #declare naming convention for IO pins
    IO.setup(step_dir_pin, IO.OUT)        #set pins as output
    IO.setup(step_step_pin, IO.OUT)
    IO.output(step_dir_pin, step_dir_state)     #set state of dirpin

    #LIDAR SETUP
    tof = lidar.VL53L1X(i2c_bus=1,i2c_address=0x29)
    tof.open()
    tof.start_ranging(1)   #1,2,3 = short,med,long

    for i in range(height):
        
        x = str(tof.get_distance()) + ','
        y = '0,'
        z = str(z_location) + '\n'

        if write_flag == 1:
            f = open(curr_points_file, 'w')
            f.write(x+y+z)
            write_flag = 0
            f.close()
        else:
            f = open(curr_points_file, 'a')
            f.write(x+y+z)
            f.close()

        i_start = 1
        while i_start <= i_end:         #turn stepper by sending pulses
            IO.output(step_step_pin, high)
            t.sleep(delay)
            IO.output(step_step_pin, low )
            t.sleep(delay)
            i_start += 1

        z_location += z_step
        

    
 
