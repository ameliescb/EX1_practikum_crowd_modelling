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

n, pedestrian_number, obstacle_number = 100, 1, 25
grid_size, env, X, target = initialization(n, pedestrian_number, obstacle_number)
dist = distance_matrix(env, grid_size, target)

print(grid_size, '\n\n', X, '\n\n', target, '\n\n', env, '\n\n', dist)
plt.figure()
plt.imshow(env)

plt.figure()
plt.imshow(dist)

X = one_step(env, pedestrian_number, X, dist, grid_size)


#%%                               Initialization TASK 2



############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 1
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target = 24,24 
X = [[24,2]]



#%%                                     Initialization TASK 3




############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 5
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target = 24,24 
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]


#%%##############################  Initialization TASK 4 

############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 5
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target_location = 24,24 
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]

######################## PLACING THE OBSTACLES########################

obstacles_location = [[24,9],[24,20],[10,24],[20,24],[10,24],[40,24],[10,3],
                      [24,40],[ 24,30],[30,24],[10,3]]
obstacle_number = len(obstacles_location)

for i in range(obstacle_number) : 
    obst = obstacles_location[i]
    env[obst[0]][obst[1]] = 2
    
    
#%%##############################  Initialization TASK 4 - Chicken test 

############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 1
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target_location = 24,24 
X = [[24,4]]

######################## PLACING THE OBSTACLES########################

for i in range(24) : 
    env[12+i][20] = 2

for i in range(10) :
    env[12][10+i] = 2
    env[35][10+i] = 2
    



#%%                               Graphic simulation


##################### Initialization of graphic interface ###################

master = tk.Tk()
grid_frame = tk.Frame( master) 
for i in range(grid_size) : 
    for j in range(grid_size) : 

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

dist = distance_matrix(env, grid_size, target)

def get_X() :  
    return X, X.copy()
  

def leftclick(event):
    X,old_X = get_X()
    X = X = one_step(env, pedestrian_number, X, dist, grid_size)


    
    for p in range(pedestrian_number) : 
        if old_X[p] != X[p] : 
            #change the old location to white : 
            frame = tk.Frame(grid_frame,  width=15, height=15) #their units in pixels
            button1 = tk.Button(frame, bg = "cyan")
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
