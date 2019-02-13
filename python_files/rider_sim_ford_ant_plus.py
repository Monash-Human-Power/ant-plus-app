##!/usr/local/bin/python
#import os, sys
#...

import argparse
import sys
import scipy.integrate as spi
import numpy as np
import json
# import slope data of specific track this also includes the slope function (slopef())
# code may change depending on location of file 

from functions import *

# setup variables **only power is compulsory
parser = argparse.ArgumentParser()
parser.add_argument("-input_power", type=float, help="power input")
parser.add_argument("-input_estimated_speed", "--input_estimated_speed", default=2, type=float,
                    help="estimated speed with initial speed 2m/s")
parser.add_argument("-input_estimated_distance", "--input_estimated_distance", default=0, type=float,
                    help="estimated distance with initial distance 0m")
parser.add_argument("-data_rate", "--data_rate", default=1000, type=float,
                    help="data sampling rate in milliseconds default 1second")


args = parser.parse_args()

input_power = args.input_power
input_estimated_speed = args.input_estimated_speed
input_estimated_distance = args.input_estimated_distance
input_data_rate = args.data_rate/1000

#avoids ode failing if speed close to 0
if input_estimated_speed < 0.01:
    input_estimated_speed = 0.01
y0 = [input_estimated_distance, input_estimated_speed]

#time over which ode solves
dt = [0, input_data_rate]
    


#define ode
def pend(t,y):
    x,v = y  
    dydt = [v, ((1/(mass_f(d1,d2,I1,I2,v,m))) * ( input_power*(1-(dtloss/100)) - p_air(rho,cdaf(v),v) - p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,v) - p_slope(m,g,slopef(x),v)  ))]
 
    return dydt


#solve the ode
sol = spi.odeint(pend, y0, dt, tfirst=True)
#sol = spi.solve_ivp(pend, dt, y0)

# gets results solve_ivp
#x = sol.y[0,-1]
#v = sol.y[1,-1]

# gets results for odeint
x = sol[-1,0]
v = sol[-1,1]

# outputs results

output_data = {}
output_data["estimated_speed"] = v
output_data["estimated_distance"] = x

print(json.dumps(output_data))


#plt.plot(xlist, vlist, )

#plt.xlabel('Distance (m)')
#plt.ylabel('Speed (m/s)')

#plt.title("Speed vs Distance")

#plt.legend()

#plt.show()
