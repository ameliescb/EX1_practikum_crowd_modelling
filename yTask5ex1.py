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

#%%                                TEST SCENARIO 4

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


#%%                                TEST SCENARIO 7


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
#for k in range(pedestrian_number): #1.33
#	pedestrian_speed[k] += np.random.normal(0, 0.2, 1)


#for i in range(pedestrian_number):
#    for j in range(0, pedestrian_number-i-1):
#        if pedestrian_speed[j] > pedestrian_speed[j+1] :
#        	pedestrian_speed[j], pedestrian_speed[j+1] = pedestrian_speed[j+1], pedestrian_speed[j]#

#print(pedestrian_speed)

duration = 15

run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration, pixel=10)
