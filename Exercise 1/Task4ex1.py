# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 23:19:40 2019

@author: daniel
reorganised by Amélie
"""



import matplotlib.pyplot as plt
from tkinter import * 
import numpy as np
import tkinter.font as tkFont
import tkinter as tk
from ex1_functions import * #be careful to be in the right current folder


#%% To compute this task, we found it useful to change the way we calcul neighboors
# IN THIS SECTION : we compute a matrix of distances, we say that neighboors that are in the 
# corner or on an obstacle are not anymore neighboors


 ################## DETERMINATION OF VALID NEIGHBOORS CELLS ##################################
    
 
# In order to compute the movement arround a corner and deal with the issue of scratching/going threw a wall:
# We recompute the neighboors function, considering that if a diagonal case is next to an adjacent obstacle, it is no more a neighboor.
 # This scenario will also be applied to the distance computation so that it does not slow down the pedestrian
 
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
            
    ####### AVOID OBSTACLES + CORNER CONSIDERTION : ######################
# If one direct adjacent cell is an obstacle, then the corners directly adjacent are not neighboors
    
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


 ################## COMPUTE THE MATRIX DISTANCE ##################################

# Use of Dijkstra algorithm and additional euclidian distance feature

def distance_matrix(env, grid_size, target):
    dist = -1*np.ones(np.shape(env)) # start considering all cells are to infinite distance of the target
    dist[target[0], target[1]] = 0
        # The target is distance 0 from the target
    
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
    # This helps to difference the distance to the target between two cells with same Dijkstra distance
    
    
    # We realise the obstacle avoidance in the computation of the neighboors above
    return dist



 ################## MOVES OF A PEDESTRIAN ##################################


# Now the function one_step implemented to simulate one step of all the pedestrians has to be updated
# This is in order to incorporate the distance matrix and avoid obstacles to make it safely to the target
 
def one_step(env,pedestrian_number,X,distance_matrix, speed, waiting_list,grid_size,target) : 
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""

    for i in range(pedestrian_number):
        loc = X[i] # pedestrian location
        neighboors = neighboors_computation(loc, grid_size, env)
        possible_moves = []

        if ((waiting_list[i]+1) *speed[i])   < 1: #the pedestrian should wait
            waiting_list[i] += 1
        
            
        else : 
            waiting_list[i] = 0 # the pedestrian will move at this time
            for neigh in neighboors:
                if [neigh[0], neigh[1]] in X: # if one adjacent cell is busy with another pedestrian, 
                    possible_moves.append(-1) # then this cell is not reachable
                else:
                    possible_moves.append(distance_matrix[neigh[0], neigh[1]]) # else it is
            
            possible_moves[-1] = distance_matrix[neigh[0], neigh[1]] 
   # staying still is a possible move even though the cell is occupied (because it is by this very pedestrian)
   # thus we add it
   
            best_move = len(possible_moves)-1 #By default, the best move is staying still
            
            for neigh in range(len(possible_moves)): # check all possibilities and see which is the closest to the target
                print(neigh, possible_moves[neigh])
                if possible_moves[neigh] < possible_moves[best_move] and possible_moves[neigh] != -1: 
    # the best move is the one with the closest distance to the target, -1 is infinity
                    best_move = neigh
                        
            X[i] = neighboors[best_move] # move towards the best cell
            
    return X, waiting_list



    
#%%############################## DJIKSTRA ALGORITHM

#grid
n = 2500 #number of cases of the grid
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))] #size of 1 side of the grid

#Pedestrians
pedestrian_number = 5
X = [[4,24],[44,24],[24,4],[24,44],[13,6]]

#target
target = 24,24 
env = np.zeros((grid_size[0],grid_size[1])) #matrix of the non moving objects
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

run_graphic(n, pedestrian_number,obstacle_number,grid_size,env,X,target,speed,waiting_list,persistance)

#%%##############################  Initialization TASK 4 - Chicken test 

#grid
n = 2500 #number of cases of the grid
grid_size = [int(np.sqrt(n)),int(np.sqrt(n))]    
#pedestrian 
pedestrian_number = 1
X = [[24,4]]

#target
target = 24,24 
env = np.zeros((grid_size[0],grid_size[1])) #matrix of the non moving objects
env[target[0]][target[1]] = 3

#obstacles
for i in range(24) : 
    env[12+i][20] = 2

for i in range(10) :
    env[12][10+i] = 2
    env[35][10+i] = 2

#speed and time
speed = [1 for i in range(pedestrian_number)] #speed of each pedestrian
#unit case/click, should be <= 1
waiting_list = [0 for i in range(pedestrian_number)] #time each pedestrian had
#wait since its last move
#global time
#time = 0

#Graphic interface
persistance = True #to see the path of the pedestrian
run_graphic(n, pedestrian_number,obstacle_number,grid_size, 
            env,X,target,speed,waiting_list,persistance) 





