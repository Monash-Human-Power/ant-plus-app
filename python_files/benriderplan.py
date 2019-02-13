# ben power input using ftp
#finds optimised power plan and otputs power function

import numpy as np
from functions import *
import scipy.integrate as spi
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import _pickle as pickle

ftp = 188
xi = 1500 #when to transition to aerobic limit
tvo = 180 #max time in vo2 max range
tvoin = 0 #time elabsped in vo2
tsprint = 30 #max anerobic capacity
tspin = 0 #time in anerobic
tmaxp = 5 # max time in max power
tmaxpin = 0 #time in max power

def benpin(x,ftp,xi,tvo,tvoin,tsprint,tspin,tmaxp,tmaxpin):
    if x<xi:
        return 0.5*ftp #power for inrun
        
    elif xi<x and tvoin< tvo:
        return 1.1*ftp #power for vo2
     
    elif tvoin>= tvo and tspin< tsprint:
        return 1.3*ftp #power for anerobic sprint (should be 1.3)
        
    elif tspin>= tsprint and tmaxpin< tmaxp:
        return 1.5*ftp
    
    else:
        return 0.5*ftp

# finding optimised xi

t = np.arange(0,501,1)

def pend(t,y):
    x,v = y  
    dydt = [v, ((1/(mass_f(d1,d2,I1,I2,v,m))) * (benpin(x,ftp,xi,tvo,tvoin,tsprint,tspin,tmaxp,tmaxpin) *(1-(dtloss/100)) - p_air(rho,cdaf(v),v) - p_roll_res(Crr1_1,Crr1_2,N1,Crr2_1,Crr2_2,N2,v) - p_slope(m,g,slopef(x),v)  ))]
 
    return dydt

x = [0]
v = [2]

tstart = []
tspstart = []
tmaxpstart = []
benpower = [0]
for i in range(len(t)-1):
    dt = [t[i],t[i+1]]
    sol = spi.solve_ivp(pend, dt, [x[i],v[i]])
# gets results
    tx = sol.y[0,-1]
    tv = sol.y[1,-1]
    
    benpower.append(benpin(x[i],ftp,xi,tvo,tvoin,tsprint,tspin,tmaxp,tmaxpin))
    
    x.append(tx)
    v.append(tv)

    if xi < x[-1]:
        tstart.append(t[i+1])
        tvoin = tstart[-1] - tstart[0]
        
    if tvoin >= tvo:
        tspstart.append(t[i+1])
        tspin = tspstart[-1] - tspstart[0]
        
    if tspin >= tsprint:
        tmaxpstart.append(t[i+1])
        tmaxpin = tspstart[-1] - tspstart[0]
        
        


bpp = interp1d(x, benpower, kind='linear')
    
       
plt.plot(x,bpp(x))
plt.show()

#plt.plot(x,v)
#plt.show()

with open('ben_power_plan', 'wb') as f:
    pickle.dump(bpp, f)




