 # Libraries for file path
import os
import sys

# functions for power model that exclude interpolation***
#import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
#import numpy as np

from math import sin,atan,exp
#from scipy.interpolate import UnivariateSpline
from bike_data_1_5 import *
import _pickle as pickle

from math import floor

saved_interpolation_file_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "saved_interp.pkl")
with open(saved_interpolation_file_path, 'rb') as y:
    interps_loaded = pickle.load(y)

slope = interps_loaded[0]
fcda = interps_loaded[1]


def p_air(rho,cda,v):
    return 0.5 * rho * cda * v**3

def p_roll(m,g,mu,v):    
    return m * g * mu * v 

def p_slope(m,g,grad,v):
    return m * g * sin(atan(grad)) * v


def p_in(intensityfactor,P_GET,rateconst,P_MAX,sdist,x,xs,xi):
    if x<xi+1:
        return intensityfactor*P_GET*(1-exp(rateconst*0.1*x))
    elif x<xi+((1)*(xs-xi))/(3):
        return 1*P_GET*(1-exp(rateconst*0.1*(x-xi+60)))
    elif x<xi+((2)*(xs-xi))/(3):
        return 1*P_GET*(1-exp(rateconst*0.1*(x-xi+60)))
    elif x<xi+((8)*(xs-xi))/(9):
        return 1*P_GET*(1-exp(rateconst*0.1*(x-xi+60)))
    elif x<xs+1:
        return 1.0*P_GET*(1-exp(rateconst*0.1*(x-xi+60)))
    elif x<xs+1:
        c = P_MAX - P_GET
        a = ((sdist)**(4)) / (16*c)
        b = ((a*c)**(1/4))+xs
        return (-1/a)*(x-b)**(4) + c + P_GET
    else:
        return intensityfactor*P_GET




        
# slope data for each track must use slope
#def p_slope(m,g,slope,v):
#    return m*g*slope(x)*v
startAdjust = 93

def slopef(x):
    xa = x - startAdjust 
    n = floor(xa/4782)
    xb = xa - 4782*n
    return slope(xb)

#plt.plot(vk, ck, 'o', vnew, f(vnew), '-', vnew, f2(vnew), '--',vnew,f3(vnew),':')

#plt.show()

#using f2 for cda

def cdaf(v):
    if v<5.765:
        return 0.03154635
    elif 5.765<=v<=30.46:
        return fcda(v)
    else:
        return 0.028759387

# mass function intended to be used as Pinput/mass_f
#print (cdaf(1))
#print (cdaf(5.8))
#print (cdaf(32))

def mass_f(d1,d2,i1,i2,v,m):
    r1 = d1/2
    r2 = d2/2
    w1 = v/(r1)
    w2 = v/(r2)
    I = i1*w1/r1 + i2*w2/r2
    return I+m*v

# variable rolling resistance

def p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,v):
    return (Crr1_1+1/3*Crr1_2*v)*v*N1 + (Crr2_1+1/3*Crr2_2*v)*v*N2  
        
        


        
        

