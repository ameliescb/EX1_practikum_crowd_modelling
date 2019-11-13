#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 18:28:44 2019

@author: mayau
"""

from ex1_functions import *
import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk
import time
import random

#%%                                       Bonus Question exercice 2: model adaptation.

#def our_model(env, x, dt):
    

#Pedestrians
def envir_init():
    pedestrian_number = 25
    X = []
    while len(X) < 25:
        ped = [random.randint(19,28), random.randint(1,8)]
        if ped not in X:
            X.append(ped)
    #for i in range(pedestrian_number): to be implemented
        
    
    #target and shape
    n = 47*72
    grid_size = [47,72]
    obstacle_number = 3*44
    target = 24,70 
    env = np.zeros((grid_size[0],grid_size[1])) #matrix of the non moving objects
    env[target[0]][target[1]] = 3
    
    for i in range(36,39):
        for j in range(22):
            env[j,i] = 2
        for j in range(25,47):
            env[j,i] = 2
            
    speed = np.random.normal(1.33, 0.1, 25)
    duration = 30
    dt = 0.2   
    
    dist = distance_matrix(env, grid_size, target)
    situation = [0 for i in range(25)]
    
    return pedestrian_number, X, n, grid_size, obstacle_number, target, env, speed, dt, dist, situation
#run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, speed, duration)
#speed and time
 #speed of each pedestrian.
 
 
 
#%%                                        Additional functions
 
def nested_change(item, func):
    if isinstance(item, list):
        return [nested_change(x, func) for x in item]
    return func(item)
 
def dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt):
    
    Y = X.copy()
    Y = np.around(Y)
    Y = Y.tolist()
    Y = nested_change(Y, int)
    
    print(Y)

    for ped in range(pedestrian_number):
        move= speed[ped]/0.4*dt
        Y = single_step(env, ped, Y, dist, grid_size)
        norm = np.sqrt((Y[ped][0]-X[ped][0])**2 + (Y[ped][1]-X[ped][1])**2)
        sum = abs(Y[ped][0]-X[ped][0]) + abs(Y[ped][1]-X[ped][1])
#        print(X,"\n\n\n",Y)
        X[ped][0] += (Y[ped][0]-X[ped][0])/norm/sum
        X[ped][1] += (Y[ped][1]-X[ped][1])/norm/sum
    return X


#%%                                        Simplification for comparison

pedestrian_number, X, n, grid_size, obstacle_number, target, env, speed, dt, dist, situation = envir_init()

X = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt)
print("yes")
X = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt)
X = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt)
X = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt)

X = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt)

X = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, dt)



print(X, "\n\n\n\n\n\n\n\n")

