# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 17:51:15 2019

@author: danie
"""

import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk
from ex1_code_new import *

#%%                                TEST SCENARIO 1

n = 500 #number of cases of the grid
pedestrian_number = 1
obstacle_number = 0
grid_size = [5,100]
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size[0],grid_size[1]))

env[2][99] = 3
target = 2,99 
X = [[2,0]]

pedestrian_speed = [1.33]
duration = 30

simulation(n, pedestrian_number, obstacle_number, env, grid_size, X, target, pedestrian_speed, duration)



#%%                                TEST SCENARIO 6

n = 30*30 #number of cases of the grid
pedestrian_number = 20
obstacle_number = 0
grid_size = [30,30]
env = 2*np.ones((grid_size[0],grid_size[1]))
    
  ##################      PLACING THE WALLS #########
for lin in range(25,30):
    for col in range(30):
        env[lin][col] = 0

for col in range(25,30):
    for lin in range(25):
        env[lin][col] = 0
        
  ##################      PLACING THE TARGET #########

env[0][27] = 3
target = 0,27 
X = [[lin,col] for lin in range(25,30) for col in range(4)]

pedestrian_speed = [1.33 for k in range(40)]
duration = 30

simulation(n, pedestrian_number, obstacle_number, env, grid_size, X, target, pedestrian_speed, duration)