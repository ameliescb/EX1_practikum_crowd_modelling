#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:13:01 2019

@author: mayau
"""


import json
import os
import glob

def scenario(y):
    with open('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Bottleneck bifurcation.scenario', 'r') as f:
        scenario = json.load(f)
    
    scenario["scenario"]['topography']['obstacles'][0]["shape"]["y"] = y
    
    with open("/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Bottleneck bifurcation.scenario", 'w') as outfile:
	    json.dump(scenario, outfile, indent=2)    
    
    run_scenario = 'java -jar /u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/vadere-console.jar scenario-run --scenario-file "/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/Bottleneck bifurcation.scenario" --output-dir="/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3/output"'
    os.system(run_scenario)
    
    #finds the most recently created file and reads it line by line
    postvis = open(glob.glob('/u/halle/mayau/home_at/Downloads/vadere.v1.0.linux/EX1_practikum_crowd_modelling-master/Exercise 3//output/Bottleneck bifurcation_*/postvis.trajectories')[-1], "r")
    return postvis



#for line in postvis:
#	l_arr = line.split()
#	pedos[l_arr[1]] = l_arr[0]
#for key in pedos.keys():
#	print(str(key) + "  =  " + str(pedos[key]))

#%%
    

    
    
    
    
    
    