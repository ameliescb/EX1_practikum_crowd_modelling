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

    
#%% ################## DETERMINATION OF VALID NEIGHBOORS CELLS ##################################
    
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
                 [loc[0],loc[1]+1],
                 [loc[0], loc[1]]]
            
    
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
            neighboors = neighboors_computation(loc, grid_size)
            for neigh in neighboors:
                if env[neigh[0],neigh[1]] != 2 and dist[neigh[0],neigh[1]] == -1:
                    dist[neigh[0],neigh[1]] = count
        # For every neighboor to a cell that is distant from the last computed distance from the target
        # Assign distance + 1 for its neigboors
     
    
    for line in range(grid_size):
        for column in range(grid_size):
            if dist[line, column] != -1:
                dist[line, column] += np.sqrt((line - target[0])**2 + (column - target[1])**2)/(2*grid_size**2)
    # Add a decima taking euclidian distance into consideration
    # This helps to difference the distance to the target between two cells with same Djikstra distance
    
    return dist



#%% ################## MOVES OF A PEDESTRIAN ##################################

def one_step(env, pedestrian_number, X, distance_matrix, grid_size) :
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""

    for ped in range(pedestrian_number):
        loc = X[ped] #pedestrian location
        neighboors = neighboors_computation(loc, grid_size)
        possible_moves = []
        for neigh in neighboors:
            if [neigh[0], neigh[1]] in X:
                possible_moves.append(-1)
            else:
                possible_moves.append(distance_matrix[neigh[0], neigh[1]])
        possible_moves[-1] = distance_matrix[neigh[0], neigh[1]]



        print('\n\n', neighboors, '\n', possible_moves, '\n')
        best_move = len(possible_moves)-1
        for neigh in range(len(possible_moves)):
            print(neigh, possible_moves[neigh])
            if possible_moves[neigh] < possible_moves[best_move] and possible_moves[neigh] != -1:
                best_move = neigh
            print('donc ', best_move, possible_moves[best_move])
                    
        X[ped] = neighboors[best_move]
            
    return X










