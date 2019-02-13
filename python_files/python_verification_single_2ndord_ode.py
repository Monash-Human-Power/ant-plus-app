#Power model verification
import scipy.integrate as spi
import scipy.interpolate as spinterp # to calcualte the slope fit
import numpy as np 
import csv
import matplotlib.pyplot as plt # for debugging/testing only
from math import floor
import os

from functions import *

#get run data to verify against

# Get path of file
current_script_location = os.path.dirname(os.path.realpath(__file__))
ford_slope_filename = 'Data_18_3_31_9_39.csv'

np.warnings.filterwarnings('ignore')
#adjustment to when rider starts
adjust = 113
 # Read CSV file
with open(os.path.join(current_script_location, ford_slope_filename)) as csvfile: 
    data = list(csv.reader(csvfile))
data = np.array(data)
#distance = data[1:-1,1]
time = [float(i)-float(data[adjust,0]) for i in data[adjust:-1,0]]
distance = [float(i)*1000-float(data[adjust,3])*1000 for i in data[adjust:-1,3]]
speed = [float(i)/3.6 for i in data[adjust:-1,4]]
power = [float(i) for i in data[adjust:-1,6]]

#create power function with respect to time
fpint = spinterp.interp1d(time, power, kind='linear', fill_value="extrapolate")
#dr = np.linspace(0,5000,500)
fpinx = spinterp.interp1d(distance, power, kind='linear', fill_value="extrapolate")
#plt.plot(distance , power, 'o', dr, fp(dr), '-')

#plt.show()

#def power model
def pend(t,y):
    x,v = y    
    dydt = [v, ((1/(mass_f(d1,d2,I1,I2,v,m))) * ( fpint(t)*(1-(dtloss/100)) - p_air(rho,cdaf(v),v) - p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,v) - p_slope(m,g,slopef(x),v)  ))]
 
    return dydt


#initial condition [starting distance, speed]
y0 = [0,speed[0]]

#time over which to solve
dt = [time[0],time[-1]]

#ode methods
sol = spi.solve_ivp(pend, dt, y0, max_step=1)
#sol = spi.odeint(pend, y0, dt, tfirst=True)


# gets results for solve_ivp
estimated_dist = sol.y[0,:]
estimated_speed = sol.y[1,:]

# gets results for odeint
#x = sol[-1,0]
#v = sol[-1,1]


fig = plt.figure()    
plt.plot(distance, speed, 'g-', label='real')
plt.plot(estimated_dist, estimated_speed, 'b-', label='estimated')
fig.suptitle('speed vs distance')
plt.xlabel('distance')
plt.ylabel('speed')
plt.legend(loc='upper left')





