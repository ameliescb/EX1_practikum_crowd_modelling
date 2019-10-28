# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 10:18:48 2019

@author: danie
"""

import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk

#%% ################## DETERMINATION OF VALID NEIGHBOORS CELLS ##################################
    
def neighboors_computation(loc, grid_size, env) :
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
                 [loc[0],loc[1]+1],
                 [loc[0], loc[1]]]
            
    ####### CORNER CONSIDERTION : ######################
#If one direct adjacent cell is an obstacle, then the corners directkly adjaent are not neighboors
    
    possible = [0 for j in range(9)]
    
    if loc[1] < grid_size[1]-1:
        neigh = neighboors[7]
        if env[neigh[0], neigh[1]] == 2:
            possible[2] = 1
            possible[5] = 1
            possible[7] = 1
    else:
        possible[2] = 1
        possible[5] = 1
        possible[7] = 1
            
    if loc[0] < grid_size[0]-1:
        neigh = neighboors[4]
        if env[neigh[0], neigh[1]] == 2:
            possible[4] = 1
            possible[5] = 1
            possible[3] = 1
    else:
        possible[3] = 1
        possible[4] = 1
        possible[5] = 1
            
    if loc[0] > 0:
        neigh = neighboors[1]
        if env[neigh[0], neigh[1]] == 2:
            possible[0] = 1
            possible[1] = 1
            possible[2] = 1
    else:
        possible[2] = 1
        possible[1] = 1
        possible[0] = 1
            
    if loc[1] > 0:
        neigh = neighboors[6]
        if env[neigh[0], neigh[1]] == 2:
            possible[6] = 1
            possible[0] = 1
            possible[3] = 1
    else:
        possible[6] = 1
        possible[0] = 1
        possible[3] = 1
            
    count = 0
    for i in range(9):
        if possible[i] == 1:
            del neighboors[i-count]
            count += 1
    
    return neighboors


#%% ################## COMPUTE THE MATRIX DISTANCE ##################################

def distance_matrix(env, grid_size, target):
    dist = -1*np.ones(np.shape(env))
    dist[target[0], target[1]] = 0
        # Initialize the distance matrix with -1 everywhere, then start with the target
    
    count = 0
    while count in dist:
        at_dist = np.argwhere(dist==count)
        count += 1
        # Until every empty cell from which the target is reachable has a distance to the target
        
        for loc in at_dist:
            neighboors = neighboors_computation(loc, grid_size, env)
            for neigh in neighboors:
                if env[neigh[0],neigh[1]] != 2 and dist[neigh[0],neigh[1]] == -1:
                    dist[neigh[0],neigh[1]] = count
        # For every neighboor to a cell that is distant from the last computed distance from the target
        # Assign distance + 1 for its neigboors
     
    
    for line in range(grid_size[0]):
        for column in range(grid_size[1]):
            if dist[line, column] != -1:
                dist[line, column] += np.sqrt((line - target[0])**2 + (column - target[1])**2)/(2*grid_size[0]*grid_size[1])
    # Add a decima taking euclidian distance into consideration
    # This helps to difference the distance to the target between two cells with same Djikstra distance
    
    return dist



#%% ################## MOVES OF A PEDESTRIAN ##################################

def one_step(env, pedestrian_ID, X, distance_matrix, grid_size) :
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""

    loc = X[pedestrian_ID] #pedestrian location
    neighboors = neighboors_computation(loc, grid_size, env)
    possible_moves = []
    for neigh in neighboors:
        if [neigh[0], neigh[1]] in X:
            possible_moves.append(-1)
        else:
            possible_moves.append(distance_matrix[neigh[0], neigh[1]])
    possible_moves[-1] = distance_matrix[neigh[0], neigh[1]]
    best_move = len(possible_moves)-1
    for neigh in range(len(possible_moves)):
        print(neigh, possible_moves[neigh])
        if possible_moves[neigh] < possible_moves[best_move] and possible_moves[neigh] != -1:
            best_move = neigh
        print('donc ', best_move, possible_moves[best_move])
                   
    X[pedestrian_ID] = neighboors[best_move]
            
    return X


#%%                               Graphic simulation


##################### Initialization of graphic interface ###################
def simulation(n, pedestrian_number, obstacle_number, env, grid_size, X, target):
    
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










