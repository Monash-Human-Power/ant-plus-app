# Rider Simulator
Uses power data from ant_plus sensors to estimate speed on a given bike

# Motivation
Can be used as a training tool for riders and for analysis

# Installation
- Requires python and node to be installed
- Requires index.js to be installed follow https://github.com/Monash-Human-Power/ant-plus-app

### Modules needed from python
Install the following modulues from python using pip install MODULE.
The Modules needed are: os, sys, math, _pickle, argparse, scipy, numpy, json, csv, matplotlib

# Steps to run
1. Ensure a saved.interp.pkl is in the directory otherwise run interpolation.py
2. run index.js  by typing: node index.js in terminal
3. type: http://localhost:3000 in browser to view live data

# Customization
1. Changing rider mass
  - Go to bike_data_1_5.py and edit the variable rider_mass
2. Changing location of riding
  - Go to interpolation.py and edit the variable ford_slope_filename
  - You must rerun interpolation after making this change

# Accuracy tests for solving model
Run python_verification.py to check accuracy of model

