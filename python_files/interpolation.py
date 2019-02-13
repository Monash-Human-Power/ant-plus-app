#This script saves inteprolation files as a pickle file
# ford track slope data + cda data save interpolations

from scipy.interpolate import interp1d
import scipy.interpolate as spinterp # to calcualte the slope fit
import numpy as np 
import csv
import matplotlib.pyplot as plt # for debugging/testing only
from math import floor
import os
import _pickle as pickle
# Get path of file
current_script_location = os.path.dirname(os.path.realpath(__file__))
ford_slope_filename = 'YYPG_Track_Survey_Data.csv'

 # Read CSV file
with open(os.path.join(current_script_location, ford_slope_filename)) as csvfile: 
    data = list(csv.reader(csvfile))
data = np.array(data)
distance = data[1:-1,1]
distance = [float(i) for i in data[1:-1,1]]
height = [float(j) for j in data[1:-1,2]]

# Display data
#print (data)
#print (distance)
#print(height)

#plt.plot(distance,height)
#plt.show()
    
hfit = spinterp.UnivariateSpline(distance,height,s=0.03,k=3)
slope = hfit.derivative()

# cda data 
  
vk = [5.765, 8.5784, 11.53, 14.136, 16.89, 19.51, 22.307, 25.106, 27.794, 30.46]
ck = [0.03154635, 0.032188888, 0.03226118, 0.03153383, 0.030963788, 0.030108619, 0.029681334, 0.029214234, 0.028967576, 0.028759387]



fcda = interp1d(vk, ck, kind='cubic', fill_value = 'extrapolate')

#vv = range(41)
#plt.plot(vv,fcda(vv),'-',vk,ck,'x')
#plt.show

interps = [slope, fcda]
with open('saved_interp.pkl', 'wb') as f:
    pickle.dump(interps, f)

#print(slope(distance))
#plt.plot(distance,slope(distance))


