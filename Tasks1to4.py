# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 10:59:30 2019

@author: danie
"""

import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk
from ex1_code_new import *

'''
n, pedestrian_number, obstacle_number = 100, 1, 25
grid_size, env, X, target = initialization(n, pedestrian_number, obstacle_number)
dist = distance_matrix(env, grid_size, target)

print(grid_size, '\n\n', X, '\n\n', target, '\n\n', env, '\n\n', dist)
plt.figure()
plt.imshow(env)

plt.figure()
plt.imshow(dist)

X = one_step(env, pedestrian_number, X, dist, grid_size)
'''

#%%                               Initialization TASK 2



############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 1
obstacle_number = 0
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))]
duration = 10
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0],grid_size[1]))
print(env)
env[24][24] = 3
target = 24,24 
X = [[24,2]]
pedestrian_speed = [1]

simulation(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration)


#%%                                     Initialization TASK 3


############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 5
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))]
pedestrian_speed = [0.1, 0.5, 1, 0.2, 2]
duration = 10

  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0],grid_size[1]))
target = 24,24 
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]
duration = 10

simulation(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration)


#%%##############################  Initialization TASK 4 

############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 5
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))]
pedestrian_speed = [0.1, 0.5, 1, 0.2, 2]
duration = 10
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0],grid_size[1])) 
env[24][24] = 3
target = 24,24 
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]

######################## PLACING THE OBSTACLES########################

obstacles_location = [[24,9],[24,20],[10,24],[20,24],[10,24],[40,24],[10,3],
                      [24,40],[ 24,30],[30,24],[10,3]]
obstacle_number = len(obstacles_location)

for i in range(obstacle_number) : 
    obst = obstacles_location[i]
    env[obst[0]][obst[1]] = 2
    
simulation(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration)  


#%%##############################  Initialization TASK 4 - Chicken test 

############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 1
pedestrian_speed = [1.33]
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))]
duration = 20
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0], grid_size[1])) 
env[24][24] = 3
target = 24,24 
X = [[24,0]]

######################## PLACING THE OBSTACLES########################

for i in range(24) : 
    env[12+i][20] = 2

for i in range(10) :
    env[12][10+i] = 2
    env[35][10+i] = 2
    

simulation(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration)