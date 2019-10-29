# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 23:43:29 2019

@author: amelie
"""


import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk
from ex1_functions import * #be careful to be in the right current folder
import time

#%%                                     TEST 1 - Version step by step

#Pedestrians
pedestrian_number = 1
X = [[2,0]]

#target and shape
grid_size = [5,100]
obstacle_number = 0
target = 2,99 
env = np.zeros((grid_size[0],grid_size[1])) #matrix of the non moving objects
env[target[0]][target[1]] = 3

    
#speed and time
speed = [0.66 for i in range(pedestrian_number)] #speed of each pedestrian.
#unit case/click, should be <= 1
# Here 1 click is 0.2 seconds and 1 case is 0.40 meters
# so 1.33 m/s is a speed of 0.66

waiting_list = [0 for i in range(pedestrian_number)] #time each pedestrian had
#wait since its last move
global time
time = 0

#Graphic interface
persistance = True #to see the path of the pedestrian

run_graphic(n, pedestrian_number,obstacle_number,grid_size, 
            env,X,target,speed,waiting_list,persistance) 



                                            # Test not passed
                                            
                                            
#%%                                      TEST 1 - Version real time
                                            

#Pedestrians
pedestrian_number = 1
X = [[2,0]]

#target and shape
grid_size = [5,100]
target = 2,99 
env = np.zeros((grid_size[0],grid_size[1])) #matrix of the non moving objects
env[target[0]][target[1]] = 3

    
#speed and time
pedestrian_speed = [1.33] #speed of each pedestrian.


#Graphic interface
duration = 40 #Duration of the simulation

run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration)



                                            # Test passed
                                            
                                            
#%%                                      TEST 3 - Version real time
         

# Pedestrians
pedestrian_number = 20
X = [[lin,col] for lin in range(25,30) for col in range(4)]                                            
    
# Target and shape
grid_size = [30,30]
target = 0,27 
env = 2*np.ones((grid_size[0],grid_size[1]))
env[target[0]][target[1]] = 3


# Obstacles
for lin in range(25,30):
    for col in range(30):
        env[lin][col] = 0

for col in range(25,30):
    for lin in range(25):
        env[lin][col] = 0
        
# Speed and time
pedestrian_speed = [1.33 for k in range(40)] #speed of each pedestrian.

#Graphic interface
duration = 40 #Duration of the simulation

run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration)                                          
