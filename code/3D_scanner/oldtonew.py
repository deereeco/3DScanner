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


