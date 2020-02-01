def rotate_all_points(old_file, new_file, input_angle):

    import math as m
    import numpy as np
    import array as a

    angle = input_angle * (m.pi/180)    #convert to radians

    flag = 1                    #this is to only write to the new file once, then after, append to the file

    with open(old_file, 'r') as f:       #open file to read from 
        numrows = f.readlines()                     #take all lines
        for i in numrows:                           #iterate through each row
            mystring = str(i).strip()               #take off the \n at the end
            row = mystring.split(',')               #make into list between ','s

            x = float(row[0])                       #coordinates of point 
            y = float(row[1])
            z = float(row[2])

            xprime = str(x*m.cos(angle) + y*m.sin(angle)) + ','     #matrix
            yprime = str(y*m.cos(angle) - x*m.sin(angle)) + ','     #mulciplication
            zprime = str(z) + '\n'                                  #about z axis

            if flag == 1:                           #if we want to erase the file and write to a fresh one
                with open(new_file, 'w') as fprime:
                    fprime.write(xprime + yprime + zprime)  #write new point
                    flag = flag + 1                 #update so we append next time
                    fprime.close()
            else:
                with open(new_file, 'a') as fprime: #append write
                    fprime.write(xprime + yprime + zprime)      #append the rest
                    fprime.close()
                    
        f.close()

