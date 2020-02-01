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
