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
import random 

#%%                                     TEST 1 - Version step by step

#Pedestrians
pedestrian_number = 1
X = [[2,0]]

#target and shape
n = 5*500
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

#%%                                	TEST 2 - MEASUREMENT OF THE FUNDAMENTAL DIAGRAM

pixel = 5
density = 1
n = 5*500 #number of cases of the grid
pedestrian_number = 2400
grid_size = [5,500]
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0],grid_size[1]))

env[2][499] = 3
target = 2,499

X =  [[] for i in range(pedestrian_number)]
for i in range(pedestrian_number) :
	h,v  = np.random.randint(grid_size[0]), np.random.randint(grid_size[1])
	while env[h][v] > 0 : #don't put 2 ped. in the same place, don't put them in the target
		h,v  = np.random.randint(grid_size[0]), np.random.randint(grid_size[1])
	X[i] = [h,v]
pedestrian_speed = [1.33 for k in range(pedestrian_number)] #1.33
duration = 80

run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration, pixel, density)

                                            
                                            
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


#%%                                TEST 4 - ALLOCATION OF DEMOGRAPHOC PARAMETERS


n = 100*100 #number of cases of the grid
pedestrian_number = 50
grid_size = [100,100]
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0],grid_size[1]))

env[50][99] = 3
target = 50,99

# Obstacles
for row in range(1,100,2):
    for col in range(99):
        env[row][col] = 2

X = [[row,0] for row in range(0,100,2)]

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

pedestrian_speed = [0.6+gaussian(i/50+0.7, 1.2, 0.2) for i in range(50)]
velocity = 0.5
increase_velocity = 0.03

duration = 15

run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration, pixel=10)
