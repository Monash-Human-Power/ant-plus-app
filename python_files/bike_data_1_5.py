
# Bike data for V1.5, all units in SI
# Updated 27/7/18

rho = 1.20  #Air Density, kg/m^3
cdA = 0.0294 #old wind tunnel 0.0294corrected data ~0.032, decreases to ~0.03 at 60km/h

# Now have a function, cdA_function, to calculate CdA as it varies with
# speed]
rider_mass = 80
bike_mass = 55 #including weight of fairing
m = rider_mass + bike_mass # % Total Mass
g = 9.81302 #Gravity
mu = 0.00532 #Co-efficient of Rolling Resistance, +20% for smaller wheel
grad = 0 #Road Gradient
dtloss = 18.1 #Power lost in the drivetrain, due to friction in the chain
intensityfactor = 0.6 #Percent of P_GET in initial inrun
P_GET = 200 #Max Aerobic Power, used for 3min segment
P_MAX = 400 #Max Anaerobic Power, used for peak power burst
rateconst = -0.153 #Rate of increase for In-run Power
srateconst = -0.0494 #Rate of increase for Sprint Power
sdist = 500
ts = 180 #Time when sprint starts
xs = 4200 #distance when sprint starts
xi = 1500 #distance when inrun starts
P_IN = 200 #Constant 
Crr1_1 = mu #0.0055 #zero speed rolling resistance front wheel
Crr1_2 = 0*(4.1*10**-5)*3.6 # rolling resistance speed factor front wheel
N1 = m*g # normal force front wheel 
Crr2_1 = mu #0.0055  #zero speed rolling resistance back wheel
Crr2_2 = 0*(4.1*10**-5)*3.6 # rolling resistance speed factor back wheel
N2 = 0*57.1*g #normal force back wheel
I1 = 0*0.0233 #moment of inertia front wheel 
I2 = 0*0.0233 #%moment of inertia back wheel
d1 = 0.52 #%diameter front wheel
d2 = 0.64 #%diameter of back wheel

