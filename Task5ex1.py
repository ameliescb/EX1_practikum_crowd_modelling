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

#%% TEST 1 

#Pedestrians
pedestrian_number = 5
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]

#target
target = 24,24 
env = np.zeros((grid_size,grid_size)) #matrix of the non moving objects
env[target[0]][target[1]] = 3

#obstacles
obstacles_location = [[24,9],[24,20],[10,24],[20,24],[10,24],[40,24],[10,3],
                      [24,40],[ 24,30],[30,24],[10,3]]
obstacle_number = len(obstacles_location)

for i in range(obstacle_number) : 
    obst = obstacles_location[i]
    env[obst[0]][obst[1]] = 2
    
    
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
