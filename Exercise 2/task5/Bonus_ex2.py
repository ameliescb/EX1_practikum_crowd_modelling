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
 
def dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, situation, dt):
    
    X = np.around(X)
    X.astype(int)
    X = X.tolist()

    for ped in range(pedestrian_number):
        situation[ped] += speed[ped]/0.4*dt
        while situation[ped] > 1:
            X = single_step(env, ped, X, dist, grid_size)
            situation[ped] -= 1
    return X, situation


#%%                                        Simplification for comparison

pedestrian_number, X, n, grid_size, obstacle_number, target, env, speed, dt, dist, situation = envir_init()

#%%                                         Simulation
    
master = tk.Tk()
grid_frame = tk.Frame( master) 
for i in range(grid_size[0]) : 
    for j in range(grid_size[1]) : 

        if env[i][j] == 3 : #target

            frame = tk.Frame(grid_frame,  width=15, height=15) #their units in pixels
            button1 = tk.Button(frame, bg = "red")
            frame.grid_propagate(False) #disables resizing of frame
            frame.columnconfigure(0, weight=1) #enables button to fill frame
            frame.rowconfigure(0,weight=1) #any positive number would do the trick
            frame.grid(row=i, column=j) #put frame where the button should be
            button1.grid(sticky="wens") #makes the button expand

        elif env[i][j] == 2 : 
            frame = tk.Frame(grid_frame, width=15, height=15) #their units in pixels
            button1 = tk.Button(frame, bg = "black")
            frame.grid_propagate(False) #disables resizing of frame
            frame.columnconfigure(0, weight=1) #enables button to fill frame
            frame.rowconfigure(0,weight=1) #any positive number would do the trick
            frame.grid(row=i, column=j) #put frame where the button should be
            button1.grid(sticky="wens") #makes the button expand
            
        else : 
            frame = tk.Frame(grid_frame,  width=15, height=15) #their units in pixels
            button1 = tk.Button(frame, bg = "white")
            frame.grid_propagate(False) #disables resizing of frame
            frame.columnconfigure(0, weight=1) #enables button to fill frame
            frame.rowconfigure(0,weight=1) #any positive number would do the trick
            frame.grid(row=i, column=j) #put frame where the button should be
            button1.grid(sticky="wens") #makes the button expand
        
        
#####################    PEDESTRIANS
for l in range(pedestrian_number) : 
    i,j = X[l]
    frame = tk.Frame(grid_frame, width=15, height=15) #their units in pixels
    button2 = tk.Button(frame, bg = "blue")
    frame.grid_propagate(False) #disables resizing of frame
    frame.columnconfigure(0, weight=1) #enables button to fill frame
    frame.rowconfigure(0,weight=1) #any positive number would do the trick
    frame.grid(row=i, column=j) #put frame where the button should be
    button2.grid(sticky="wens") #makes the button expand

grid_frame.pack(side=LEFT)


########################### MOVING PEDESTRIANS ############################



button = tk.Button(master, text = "Simulate one step ")
button.pack(side=RIGHT)

def get_X() : 
    return X, X.copy()


def get_situation() :
    return situation

def get_time() : 
    
    return time

def update_time() : 
    global time
    time += 1
    return time
  

def leftclick(event):
        
    X,old_X = get_X()
    situation = get_situation()
    X, situation = dt_step(pedestrian_number, dist, env, grid_size, X, target, speed, situation, dt) 

    
    for p in range(pedestrian_number) :
        if old_X[p] != X[p] : 
            #change the old location to white : 
            frame = tk.Frame(grid_frame,  width=15, height=15) #their units in pixels
            button1 = tk.Button(frame, bg = "white")
            frame.grid_propagate(False) #disables resizing of frame
            frame.columnconfigure(0, weight=1) #enables button to fill frame
            frame.rowconfigure(0,weight=1) #any positive number would do the trick
            frame.grid(row=old_X[p][0], column=old_X[p][1]) #put frame where the button should be
            button1.grid(sticky="wens") #makes the button expand
            
            #put the new location to blue :
            frame = tk.Frame(grid_frame,  width=15, height=15) #their units in pixels
            button1 = tk.Button(frame, bg = "blue")
            frame.grid_propagate(False) #disables resizing of frame
            frame.columnconfigure(0, weight=1) #enables button to fill frame
            frame.rowconfigure(0,weight=1) #any positive number would do the trick
            frame.grid(row=X[p][0], column=X[p][1]) #put frame where the button should be
            button1.grid(sticky="wens") #makes the button expand    
    
    
button.bind("<Button-1>", leftclick)
button.pack(side=RIGHT)



tk.mainloop()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 