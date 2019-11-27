#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 17:14:09 2019

@author: mayau
"""

import json
import os
import glob
import shutil
import random
import numpy as np
import matplotlib.pyplot as plt

alpha = 2

with open('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Scenario_Moving_Walls.scenario', 'r') as f:
    scenario = json.load(f)

scenario["scenario"]['topography']["obstacles"][2]["shape"]["x"] = 50 - alpha - 0.5
scenario["scenario"]['topography']["obstacles"][3]["shape"]["x"] = 50 + alpha - 0.5


with open("/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Scenario_Moving_Walls.scenario", 'w') as outfile:
    json.dump(scenario, outfile, indent=2)    

run_scenario = 'java -jar /u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/vadere-console.jar scenario-run --scenario-file "/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Scenario_Moving_Walls.scenario" --output-dir="/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output"'
os.system(run_scenario)

#finds the most recently created file and reads it line by line
postvis = open(glob.glob('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output/Task5part2_*/postvis.trajectories')[-1], "r")

output = []

for line in postvis:
    l_arr = line.split()
    output.append(l_arr)

shutil.rmtree('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output', ignore_errors=True)

#%%
plt.figure(figsize = (9, 6))
plt.title(r'$\alpha$ = ' + str(alpha))
plt.xlabel("time in s")
plt.ylabel("value of x")


for idp in range(3,31):
    
    positions = []
    for step in output:
        if step[1] == str(idp):
            positions.append([float(step[2]), float(step[3])])
    positions = np.array(positions)
    plt.plot([0.4*i for i in range(len(positions))], positions[:,0])
    
#%%
    
alpha = [-10 + 0.1*i for i in range(400)]
zeros = [0 for i in range(400)]
up = [alpha[i]*(alpha[i]>1.5) for i in range(400)]
down = [-alpha[i]*(alpha[i]>1.5) for i in range(400)]

plt.figure()
plt.plot(alpha, up, color = "k")
plt.plot(alpha, down, color = "k")
plt.plot(alpha, zeros, color = "k")
plt.xlabel(r'$\alpha$')

    
    
    
    
    
    
    
    
    