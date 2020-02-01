####################################################################################################
def cylindricalToCartesian(cylindrical_points_file, cartesian_points_file):

    import math as m
    import timeit

    start = timeit.default_timer()

    flag = 1                    #this is to only write to the new file once, then after, append to the file
    with open(cylindrical_points_file, 'r') as fnew:       #open file to read from 
        numrows = fnew.readlines()                     #take all lines
        numOfPoints = len(numrows)
        for i in numrows:                           #iterate through each row

            mystring = str(i).strip()               #take off the \n at the end
            row = mystring.split(',')               #make into list between ','s

            r = float(row[0])                       #read point from file
            theta = float(row[1])
            z = row[2] + '\n'

            x = str(r*m.cos(theta)) + ','                     #convert point from cylindrical to cartesian
            y = str(r*m.sin(theta)) + ','

            if flag == 1:                           #overwite for the first go around
                with open(cartesian_points_file, 'w') as fold:
                    fold.write(x+y+z)  #write new point
                    flag = flag + 1                 #update so we append next time
                    fold.close()
            else:
                with open(cartesian_points_file, 'a') as fold: #append for all the rest
                    fold.write(x+y+z)      
                    fold.close()
        fnew.close()
    stop = timeit.default_timer()    #this will return time in seconds
    execution_time = (stop - start)    

    print("It took "+ str(execution_time) + ' seconds to convert ' + str(numOfPoints) + ' points from cylindrical to cartesian coordinates' ) 
####################################################################################################
def oldtonew(curr_points, rotated_points):

    flag = 1                    #this is to only write to the new file once, then after, append to the file
    with open(rotated_points, 'r') as fnew:       #open file to read from 
        numrows = fnew.readlines()                     #take all lines
        for i in numrows:                           #iterate through each row

            if flag == 1:                           #if we want to erase the file and write to a fresh one
                with open(curr_points, 'w') as fold:
                    fold.write(i)  #write new point
                    flag = flag + 1                 #update so we append next time
                    fold.close()
            else:
                with open(curr_points, 'a') as fold: #append write
                    fold.write(i)      #append the rest
                    fold.close()
        fnew.close()
###################################################################################################
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
###################################################################################################
def rotate_all_points(old_file, new_file, input_angle):          #in cylindrical coordinates

    import math as m
    import numpy as np
    import array as a
    
    flag = 1                                                     #this is to only write to the new file once, then after, append to the file

    with open(old_file, 'r') as f:                              #open file to read from 
        numrows = f.readlines()                                #take all lines
        for i in numrows:                                     #iterate through each row
            mystring = str(i).strip()                            #take off the \n at the end
            row = mystring.split(',')                            #make into list between ','s

            theta = float(row[1])

            r = row[0] + ','
            theta_prime = str( theta + input_angle) + ','          #add angle step
            z = row[2] + '\n'                      #about z axis

            if flag == 1:                                    #if we want to erase the file and write to a fresh one
                with open(new_file, 'w') as fprime:
                    fprime.write(r + theta_prime + z)  #write new point
                    flag = flag + 1                          #update so we append next time
                    fprime.close()
            else:
                with open(new_file, 'a') as fprime:         #append write
                    fprime.write(r + theta_prime + z)      #append the rest
                    fprime.close()
                    
        f.close()

###################################################################################################
def record_z_line(z_step, height, step_dir_pin, step_dir_state, step_step_pin, write_flag, file_to_write_to, lidar_to_origin_dist, z_dir_indicator, tof):

    #import VL53L1X as lidar
    import RPi.GPIO as IO
    import time as t

    IO.setwarnings(False)         #ignore what the pins were doing before


    dist_from_lidar_to_origin = lidar_to_origin_dist

    #CONSTANTS FOR STEPPER MOTOR
    high = 1
    low = 0
    i_end = 80 * z_step
    delay = 0.0002

    #CONSTANTS FOR FILE ACCESS
    curr_points_file = file_to_write_to

    #GPIO SETUP
    IO.setmode(IO.BCM)              #declare naming convention for IO pins
    IO.setup(step_dir_pin, IO.OUT)        #set pins as output
    IO.setup(step_step_pin, IO.OUT)
    IO.output(step_dir_pin, step_dir_state)     #set state of dirpin

    if z_dir_indicator == 1: #This means the lidar is going up

        z_location = 0 #start from zero and climb

        for i in range(1,height+1):
            
            r = str(dist_from_lidar_to_origin - tof.get_distance()) + ','
            theta = '0,'
            z = str(z_location) + '\n'

            if write_flag == 1:
                f = open(curr_points_file, 'w')
                f.write(r+theta+z)
                write_flag = 0
                f.close()
            else:
                f = open(curr_points_file, 'a')
                f.write(r+theta+z)
                f.close()

            i_start = 1
            while i_start <= i_end:         #turn stepper by sending pulses
                IO.output(step_step_pin, high)
                t.sleep(delay)
                IO.output(step_step_pin, low )
                t.sleep(delay)
                i_start += 1

            z_location += z_step
            #input('z is: '+str(z_location)+', i is: '+str(i))

    else: #This means the lidar is going up

        z_location = height   #start from top and go down

        for i in range(1,height+1):
            
            r = str(dist_from_lidar_to_origin - tof.get_distance()) + ','
            theta = '0,'
            z = str(z_location) + '\n'

            if write_flag == 1:
                f = open(curr_points_file, 'w')
                f.write(r+theta+z)
                write_flag = 0
                f.close()
            else:
                f = open(curr_points_file, 'a')
                f.write(r+theta+z)
                f.close()

            i_start = 1
            while i_start <= i_end:         #turn stepper by sending pulses
                IO.output(step_step_pin, high)
                t.sleep(delay)
                IO.output(step_step_pin, low )
                t.sleep(delay)
                i_start += 1

            z_location -= z_step
            #input('z is: '+str(z_location)+', i is: '+str(i))
        
        
###################################################################################################
def main():

    import VL53L1X as lidar
    #LIDAR SETUP
    tof = lidar.VL53L1X(i2c_bus=1,i2c_address=0x29)
    tof.open()
    tof.start_ranging(1)   #1,2,3 = short,med,long



    import time as t
    import timeit

    start = timeit.default_timer()

    #CONSTANTS .MAIN()
    ANGLE_STEP = 1  #the actual angle the stepper turns is this time 1.8 degrees
    FINAL_ANGLE = 360
    HEIGHT = 150
    LIDAR_TO_ORIGIN_DIST = 300
    Z_STEP = 1
    Z_STEP_DIR_PIN = 23
    Z_STEP_DIR_STATE = 1
    Z_STEP_STEP_PIN = 24
    THETA_STEP_DIR_PIN = 22
    THETA_STEP_DIR_STATE = 1
    THETA_STEP_STEP_PIN = 27
    old_file = 'cylindrical_points_v3.txt'
    new_file = 'rotated_points_v3.txt'
    cartesian_file = 'cartesian_points_v3.txt'
    
    angle = 0
    write_flag = 1

    i = 0
    z_dir = 1                       #1 = going up, 0 = going down

    while int(angle) < FINAL_ANGLE:   #until part has turned an angle of FINAL_ANGLE

        i += 1

        if write_flag == 1:   #this means overwrite
            record_z_line(Z_STEP, HEIGHT, Z_STEP_DIR_PIN, Z_STEP_DIR_STATE, Z_STEP_STEP_PIN, write_flag, old_file, LIDAR_TO_ORIGIN_DIST, z_dir, tof) 
            write_flag = 0
        else:                 #this means append
            record_z_line(Z_STEP, HEIGHT, Z_STEP_DIR_PIN, Z_STEP_DIR_STATE, Z_STEP_STEP_PIN, write_flag, old_file, LIDAR_TO_ORIGIN_DIST, z_dir, tof)

        rotationstepper(ANGLE_STEP, THETA_STEP_DIR_PIN, THETA_STEP_DIR_STATE, THETA_STEP_STEP_PIN)

        angle += ANGLE_STEP * 1.8

        start_rotation_time = t.time()
        
        if int(angle) != FINAL_ANGLE - 1: #to stop the last point from getting rotated,
            rotate_all_points(old_file, new_file, float(ANGLE_STEP * 1.8))

        oldtonew(old_file, new_file)

        end_rotation_time = t.time()
        rotation_time = end_rotation_time - start_rotation_time
        print('Theta rotation of all points took ' + str(rotation_time) + ' seconds')

        print(str(i) + 'th pass done')

        z_dir ^= 1     #change direction of z flag with XOR
        Z_STEP_DIR_STATE ^= 1     #change motor direction

    stop = timeit.default_timer()
    execution_time = (stop - start) / 60

    cylindricalToCartesian(old_file, cartesian_file)

    tof.stop_ranging()

    print("Program Executed in "+ str(execution_time) + 'minutes') #It returns time in sec

main()



