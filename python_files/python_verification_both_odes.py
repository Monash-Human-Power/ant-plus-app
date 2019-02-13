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
#plt.plot(distance , power, 'o', )

#plt.show()

#def power model
def pend(t,y):
    x,v = y    
    dydt = [v, ((1/(mass_f(d1,d2,I1,I2,v,m))) * ( fpint(t)*(1-(dtloss/100)) - p_air(rho,cdaf(v),v) - p_roll(m,g,mu,v) - p_slope(m,g,slopef(x),v)  ))]
 
    return dydt

def dvdxt(x,v):
    return ((1/(mass_f(d1,d2,I1,I2,v,m)*v)) * ( fpinx(x)*(1-(dtloss/100)) - p_air(rho,cdaf(v),v) - p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,v) - p_slope(m,g,slopef(x),v)  ))

# guess initial velocity
vi = [speed[0]]

# solve for specified distance
xi = 0
xspan=[xi,5000]

# ode solving can change parameters to execute faster
solx = spi.solve_ivp(dvdxt,xspan, vi,dense_output=True,max_step=10,rtol=1e-8)

# the list of distance and velocity which can be exported
xlist = solx.t
vlist = solx.y[0]


#initial condition [starting distance, speed]
y0 = [0,speed[0]]

#time over which to solve
dt = [time[0],time[-1]]
#evaluate at time 
ts = time[1:-2]
sol = spi.solve_ivp(pend, dt, y0, max_step=1)
#odesol = spi.odeint(pend, y0, time)

# gets results
estimated_dist = sol.y[0,:]
estimated_speed = sol.y[1,:]

#estd = odesol.y[0,:]
#estv = odesol.y[1,:]

#plt.plot(distance, speed, 'x', estimated_dist, estimated_speed, '-')

ya = [0,speed[0]]
xa = [0]
va = [speed[0]]
for tn in time:
    
    input_power = fpint(tn)
    input_estimated_speed = ya[-1]
    input_estimated_distance = ya[0]
    input_data_rate = 1000/1000
    ya = [input_estimated_distance, input_estimated_speed]
#avoids ode failing if speed close to 0
    if input_estimated_speed < 0.01:
        input_estimated_speed = 0.01
        y0 = [input_estimated_distance, input_estimated_speed]

#time over which ode solves
    dt = [0, input_data_rate]
    
# solving theoretical velocity based on theoretical power map
    def penda(t,y):
        x,v = y  
        dydt = [v, ((1/(mass_f(d1,d2,I1,I2,v,m))) * ( input_power*(1-(dtloss/100)) - p_air(rho,cdaf(v),v) - p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,v) - p_slope(m,g,slopef(x),v)  ))]
 
        return dydt


#solve the ode
#sol = spi.odeint(pend, y0, dt)
    sol = spi.solve_ivp(penda, dt, ya)
# gets results
    x = sol.y[0,-1]
    v = sol.y[1,-1]
    ya = [x,v]
    xa.append(x)
    va.append(v)
speed = [x*3.6 for x in speed]   
estimated_speed  = [x*3.6 for x in estimated_speed] 
va = [x*3.6 for x in va]   
plt.plot(distance, speed, 'x', estimated_dist, estimated_speed, '-',xa,va,'b')

tv = 5
print(p_air(rho,cdaf(tv),tv))

print(p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,tv) )

print(p_slope(m,g,slopef(3000),tv))






