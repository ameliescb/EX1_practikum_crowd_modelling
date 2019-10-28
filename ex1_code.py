# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 16:08:36 2019

@author: amelie
"""

#importations 

import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk

#%% ######################### INITIALISATION ################################

 
#env represent a matrix with fix objects (target and X)
#X is a list of the coordinates of the pedestrians during the simulation


def initialization(n, pedestrian_number,obstacle_number) : 
    
    """ Initialize the position of the target, the pedestrians and the obstacles
    RANDOMLY
     Code : 0 = empty cell, 1 = pedestrian, 2 = obstacle, 3 = Target """
    
    ##################     GETTING THE GRID HEIGHT AND WIDNESS ###########
    grid_size = int(np.sqrt(n))
    
    ##################      PLACING THE TARGET AND THE OBSTACLES #########
    env = np.zeros((grid_size,grid_size)) #obstacles and target
    #target 
    h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
    env[h][v] = 3
    target = h,v 
    
    #obstacles:
    obstacles_location = []
    for i in range(obstacle_number) : 
        h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
        while env[h][v] > 0 : #don't put 2 ped. in the same place, don't put them in the target
            h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
        env[h][v] = 2
        obstacles_location.append([h,v])
        
    ####################        PLACING THE PEDESTRIANS  ######################
        
      #pedestrian place :
    X =  [[] for i in range(pedestrian_number)] 
    for i in range(pedestrian_number) : 
        h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
        while env[h][v] > 0 : #don't put 2 ped. in the same place, don't put them in the target
            h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
        X[i] = [h,v]
        
        
    
    return(grid_size, env, X,target)

    
#%% ################## MOVES OF A PEDESTRIAN ##################################
    
def neighboors_computation(loc, grid_size) :
    """ Compute the index of neighbooring cases of a pedestrian given the location of the 
    pedestrian and the grid size 
    loc = index of the pedestrian location"""
    
    ######## ALL POSSIBILITIES OF NEIGHBOORS : ##############################
    neighboors = [[loc[0]-1, loc[1]-1],
                 [loc[0]-1, loc[1]],        #list of all neighboors coordinates
                 [loc[0]-1, loc[1]+1],
                          
                 [loc[0]+1, loc[1]-1],
                 [loc[0]+1, loc[1]],
                 [loc[0]+1, loc[1]+1],
                          
                 [loc[0], loc[1]-1],
                 [loc[0],loc[1]+1]]
            
    
    ################## ELEMINATION OF THE NON-EXISTING NEIGHBOORING CASES ####
    if loc[0] >= grid_size-1 or loc[1] >= grid_size-1 or loc[0] == 0 or loc[1] == 0:
    
        #down and right boundaries
        l = 0
        while l < len(neighboors) :
            if neighboors[l][0] >= grid_size or neighboors[l][1] >= grid_size : 
                del neighboors[l]
                l -= 1
            l += 1

        #up and left boundaries
        l = 0
        while l <len(neighboors) :
            if neighboors[l][0] < 0 or neighboors[l][1] < 0 : 
                del neighboors[l]
                l -= 1
            l += 1
            
    
    return neighboors


def one_step(env,pedestrian_number,X) :
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""

    for i in range(pedestrian_number):
        loc = X[i] #pedestrian location
        
        if env[loc[0],loc[1]] == 3 :  #stop when the first pedestrian is on the target
            return X
        
        
        else : 
            #get the list of index of the neighboors
            neighboors = neighboors_computation(loc, grid_size)
            
            
            dist = [] #list of all distances per neighboor
            for k in range(len(neighboors)) :
                neigh = neighboors[k]

                if env[neigh[0]][neigh[1]] == 2 : #obstacle : set d to infinite 
                    d = 10*n 
                    
                if neigh in X : # other pedestrian neighboor : set d to infinite 
                    d = 10*n 
                else : 
                    d = np.sqrt((target[0]-neigh[0])**(2) + (target[1]-neigh[1])**(2))
                
                dist.append(-d)
        
            to_be_changed = neighboors[np.argmax(dist)] #go to the closest path
            X[i] = to_be_changed 
            
    return X
        

def simulation(env,pedestrian_number,X,N) : 
    """ Simulate all the positions of the pedestrians N times 
    or until on of them reaches destination"""
    
    positions = []
    for step in range(N) : 
        M = env.copy()
        X = one_step(env,pedestrian_number,X)
    
    
        for i in range(len(X)) : 
            M[X[i][0]][X[i][1]] = 1
            positions.append(M)
            if np.sum(np.sum(M)) == pedestrian_number : 
                return positions

            
    return positions
#%%                                     TASK 1



#Graphic interface inspired from : https://stackoverflow.com/questions/23709154/displaying-square-tkinter-buttons


############################## RANDOM INITIALIZATION ########################
n = 25 #number of cases of the grid
pedestrian_number = 1
obstacle_number = 2
grid_size, env, X,target =  initialization(n, pedestrian_number,obstacle_number)



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

def get_X() :  
    return X, X.copy()
  

def leftclick(event):
    X,old_X = get_X()
    X = one_step(env,pedestrian_number,X) 

    
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

#%%                               TASK 2



############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 1
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target = 24,24 
X = [[4,24]]



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

def get_X() :  
    return X, X.copy()
  

def leftclick(event):
    X,old_X = get_X()
    X = one_step(env,pedestrian_number,X) 

    
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

#%%                                     TASK 3




############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 5
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target = 24,24 
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]

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



########################### MOVING PEDESTRIANS WHEN CLICKING ############################
button = tk.Button(master, text = "Simulate one step ")

def get_X() :  
    """Returns X and a copy of it to be stored in order to compare the movement
    """
    return X, X.copy() 
  

def leftclick(event):
    X,old_X = get_X()
    X = one_step(env,pedestrian_number,X) 

    
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
tk.mainloop() #loop to detect a new click


#%%############################## TASK 4 
#For this task, it is better to change the function of simulation and to compute
# the distance of all fields. 

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

obstacles_location = [[24,10],[24,20],[10,24],[20,24],[10,24],[40,24],[10,3],
                      [24,40],[ 24,30],[30,24],[10,3]]
obstacle_number = len(obstacles_location)

for i in range(obstacle_number) : 
    obst = obstacles_location[i]
    env[obst[0]][obst[1]] = 2
    
    


def initialize_distances(grid_size, obstacles_location, target_location) :  
    distances = np.zeros((grid_size,grid_size))
    
    for i in range(grid_size) : 
        for j in range(grid_size) : 
            
            d = int(np.sqrt((target[0]-i)**(2) + (target[1]-j)**(2)))
            distances[i][j] = d
    
    
    
    for k in range(len(obstacles_location)) : #set obstacles to zero. 
        distances[obstacles_location[k][0]][obstacles_location[k][0]] = grid_size**(3)
    
    
    return distances

distances_environnement = initialize_distances(grid_size, obstacles_location, target_location)

def update_distances(distances_environnement,pedestrian_location,grid_size) : 
    d = distances_environnement.copy()
    for i in range(len(pedestrian_location)) : 
        loc = pedestrian_location[i]
        d[loc[0]][loc[1]] = grid_size**(3)
    return d


def one_step(env,pedestrian_number,X) :
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""
    distances = update_distances(distances_environnement,X,grid_size)
    for i in range(pedestrian_number):
        loc = X[i] #pedestrian location
        
        if env[loc[0],loc[1]] == 3 :  #stop when pedestrian is on the target
            return X
        
        
        else : 
            #get the list of index of the neighboors
            neighboors = neighboors_computation(loc, grid_size)
            
            
            dist = [] #list of all distances per neighboor
            for k in range(len(neighboors)) :
                neigh = neighboors[k]

                d = distances[neigh[0]][neigh[1]]
                
                dist.append(-d)
        
            to_be_changed = neighboors[np.argmax(dist)] #go to the closest path
            X[i] = to_be_changed 
            
    return X

#%%
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



########################### MOVING PEDESTRIANS WHEN CLICKING ############################
button = tk.Button(master, text = "Simulate one step ")

def get_X() :  
    """Returns X and a copy of it to be stored in order to compare the movement
    """
    return X, X.copy() 
  

def leftclick(event):
    X,old_X = get_X()
    X = one_step(env,pedestrian_number,X) 

    
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
tk.mainloop() #loop to detect a new click

#%%
    