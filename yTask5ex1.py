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

#%%                                TEST SCENARIO 1

pixel = 5
density = 1
n = 5*500 #number of cases of the grid
pedestrian_number = 2400
obstacle_number = 0
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
'''
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
            env,X,target,speed,waiting_list,persistance, pixel, 1)
'''