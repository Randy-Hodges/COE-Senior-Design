import csv
import numpy as np
import pandas as pd

coordinate_arr = np.array([["img number","object class","x1","y1","x2","y2"]])
next_object_arr = np.array([[0, 1, 0.614121, 0.779235, 0.0394089, 0.063388]])

coordinate_arr = np.concatenate((coordinate_arr,next_object_arr), axis = 0)
coordinate_arr = np.concatenate((coordinate_arr,next_object_arr), axis = 0)

#coordinate_arr = coordinate_arr[0:2]

print(coordinate_arr)
#print("again:")
#coordinate_arr = coordinate_arr[1:3]

#print(coordinate_arr)

# convert array into dataframe
DF = pd.DataFrame(coordinate_arr)
 

#print(DF)
# save the dataframe as a csv file
DF.to_csv("test.csv")

#pd.read_csv("test.csv")


#coordinate_arr.tofile("text2.csv",sep=',',format='%10.5f')

#np.savetxt("text3.csv", coordinate_arr, delimiter=",")

with open("text4.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(coordinate_arr)


print("done")