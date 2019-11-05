# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 23:09:32 2019

@author: amelie
"""

import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk
from ex1_functions import * #be careful to be in the right current folder

#%% #TASK 3 5 PEDESTRIANS, ALL THE SAME SPEED, NO OBSTACLE


#grid
n = 2500 #number of cases of the grid
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))] #size of both side of the grid

#Pedestrians
pedestrian_number = 5
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]

#target
target = 24,24 
env = np.zeros((grid_size[0],grid_size[1])) #matrix of the non moving objects
env[target[0]][target[1]] = 3

#obstacles
obstacles_location = []
obstacle_number = len(obstacles_location)
    
#speed and time
speed = [1 for i in range(pedestrian_number)] #speed of each pedestrian
#unit case/click, should be <= 1
waiting_list = [0 for i in range(pedestrian_number)] #time each pedestrian had
#wait since its last move
global time
time = 0

#Graphic interface
persistance = True #to see the path of the pedestrian

run_graphic(n, pedestrian_number,obstacle_number,grid_size, 
            env,X,target,speed,waiting_list,persistance) 

