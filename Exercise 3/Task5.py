#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:13:01 2019

@author: mayau
"""


import json
import os
import glob
import shutil
import random
import numpy as np
import matplotlib.pyplot as plt
 

#%% Scenario reading, editing and running

def scenario(y):
    with open('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Bottleneck bifurcation.scenario', 'r') as f:
        scenario = json.load(f)
    
    scenario["scenario"]['topography']['obstacles'][0]["shape"]["y"] = y
    
    with open("/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Bottleneck bifurcation.scenario", 'w') as outfile:
	    json.dump(scenario, outfile, indent=2)    
    
    run_scenario = 'java -jar /u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/vadere-console.jar scenario-run --scenario-file "/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Bottleneck bifurcation.scenario" --output-dir="/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output"'
    os.system(run_scenario)
    
    #finds the most recently created file and reads it line by line
    postvis = open(glob.glob('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output/Bottleneck bifurcation_*/postvis.trajectories')[-1], "r")
    
    output = []
    
    for line in postvis:
        l_arr = line.split()
        output.append(l_arr)
        
    shutil.rmtree('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output', ignore_errors=True)
        
    return output


#%% Data getting
    
#data = []
#
#for y in [2.5 + 0.25*i for i in range(11)]:
#    data.append(scenario(y))
    
#%% Data analyses    

idp = random.randint(1,100)
# Pick a random pedestrian among the 100 ones




sc25 = scenario(2.5)

positions = []
for step in sc25:
    if step[1] == str(idp):
        positions.append([float(step[2]), float(step[3])])
positions = np.array(positions)

plt.figure(figsize = (18, 12))
plt.plot([0.4*i for i in range(len(positions))], positions[:,0], label = "x position")
plt.plot([0.4*i for i in range(len(positions))], positions[:,1], label = "y position")
plt.title("Scenario for obstacle position at y = 2,5 m and pedestrian " + str(idp))
plt.legend()

plt.show()


sc35 = scenario(4)

positions35 = []
for step in sc35:
    if step[1] == str(idp):
        positions35.append([float(step[2]), float(step[3])])
positions35 = np.array(positions35)

plt.figure(figsize = (18, 12))
plt.plot([0.4*i for i in range(len(positions35))], positions35[:,0], label = "x position")
plt.plot([0.4*i for i in range(len(positions35))], positions35[:,1], label = "y position")
plt.title("Scenario for obstacle position at y = 4 m and pedestrian " + str(idp))
plt.legend()


plt.show()




sc40 = scenario(2.625)

positions40 = []
for step in sc40:
    if step[1] == str(idp):
        positions40.append([float(step[2]), float(step[3])])
positions40 = np.array(positions40)

plt.figure(figsize = (12, 6))
plt.plot([0.4*i for i in range(len(positions40))], positions40[:,0], label = "x position")
plt.plot([0.4*i for i in range(len(positions40))], positions40[:,1], label = "y position")
plt.title("Scenario for obstacle position at y = 2,625 m and pedestrian " + str(idp))
plt.legend()

plt.show()

print(sc25==sc40)

#    if str(l_arr[1]) == str(idp):
#        positions.append([float(l_arr[2]), float(l_arr[3])])
##plt.figure()
#print(positions) #you initiate positions array inside for loop
#break
#plt.plot(positions[:][0], positions[:][1])


#%%

idp = random.randint(1,100)

#scenar = scenario(3)

positions = []
for step in scenar:
    if step[1] == str(idp):
        positions.append([float(step[2]), float(step[3])])
positions = np.array(positions)
for dt in [1+ 10*i for i in range(0,11)]:
    
    plt.figure(figsize = (5, 2))
    plt.plot(positions[:-dt,0], positions[dt:,0])
    plt.title("dt is " + str(dt*0.4) + " s")
        
#    plt.plot([0.4*i for i in range(len(positions))], positions[:,0], label = "x position")





















    
    
    