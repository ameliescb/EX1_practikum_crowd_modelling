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
import time


#%%
#env represent a matrix with fix objects (target and X)
#X is a list of the coordinates of the pedestrians during the simulation

#We store the speed of the pedestrians in the list "speed", and create a waiting
#list for them in the list "waiting_list" which stores the time of the last 
#move of each pedestrian. 


def randomly_initialize(n, pedestrian_number,obstacle_number) : 
    
    """ Initialize the position of the target, the pedestrians and the obstacles
    RANDOMLY
    env is the matrix of non-moving objects, X the current location of pedestrianc
     Code : (for env) 0 = empty cell, 2 = obstacle, 3 = Target """
    
    #grid
    grid_side = int(np.sqrt(n))
    
    ###################non moving objects
    env = np.zeros((grid_side,grid_side)) #obstacles and target : in a matrix
    #target 
    h,v  = np.random.randint(grid_side), np.random.randint(grid_side)
    env[h][v] = 3
    target = h,v 
    #obstacles:
    obstacles_location = []
    for i in range(obstacle_number) : 
        h,v  = np.random.randint(grid_side), np.random.randint(grid_side)
        while env[h][v] > 0 : #don't put 2 ped. in the same place, don't put them in the target
            h,v  = np.random.randint(grid_side), np.random.randint(grid_side)
        env[h][v] = 2
        obstacles_location.append([h,v])
        
    ########################moving objects 
    #pedestrians 
    X =  [[] for i in range(pedestrian_number)] 
    for i in range(pedestrian_number) : 
        h,v  = np.random.randint(grid_side), np.random.randint(grid_side)
        while env[h][v] > 0 : #don't put 2 ped. in the same place, don't put them in the target
            h,v  = np.random.randint(grid_side), np.random.randint(grid_side)
        X[i] = [h,v]
    
    #speed and time
    speed = [1 for i in range(pedestrian_number)] #speed of each pedestrian
    #unit case/click, should not be >1
    waiting_list = [0 for i in range(pedestrian_number)] #time each pedestrian had
    #wait since its last move
    global mytime
    mytime = 0 #initialisation, time set to zero
    
    return(grid_side, env, X,target,speed,waiting_list)
    
#%%                               Graphic simulation
##################### Initialization of graphic interface ###################
#Graphic interface inspired from : https://stackoverflow.com/questions/23709154/displaying-square-tkinter-buttons




def run_graphic(n, pedestrian_number,obstacle_number,grid_size, env,X,target,speed,waiting_list,persistance,pixel=15) : 

    global mytime
    mytime = 0 
    
    dist = distance_matrix(env, grid_size, target)
    
    master = tk.Tk()
    grid_frame = tk.Frame( master) 
    for i in range(grid_size[0]) : 
        for j in range(grid_size[1]) : 
    
            if env[i][j] == 3 : #target
    
                frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "red")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=i, column=j) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
    
            elif env[i][j] == 2 : 
                frame = tk.Frame(grid_frame, width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "black")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=i, column=j) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
                
            else : 
                frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "white")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=i, column=j) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
            
            
    #####################    PEDESTRIANS
    for l in range(pedestrian_number) : 
        i,j = X[l]
        frame = tk.Frame(grid_frame, width=pixel, height=pixel) #their units in pixels
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
    global timer 
    timer = tk.Label(master, text="Time : " + str(mytime))
    timer.pack(side = RIGHT)
    
    
    def get_X() :  
        return X, X.copy()
    
    
    def get_waiting_list() :
        return waiting_list
    
    def get_time() : 
        
        return mytime
    
    def update_time() : 
        global mytime
        mytime += 1
        return mytime
      
    
    def leftclick(event):
        
        X,old_X = get_X()
        waiting_list = get_waiting_list()
        X,waiting_list = one_step(env,pedestrian_number,X,dist,speed,waiting_list,grid_size,target) 
        
        for p in range(pedestrian_number) : 
            if old_X[p] != X[p] : 
                #change the old location to white : 
                frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                if persistance == True : 
                    button1 = tk.Button(frame, bg = "cyan")
                else : 
                    button1 = tk.Button(frame, bg = "white")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=old_X[p][0], column=old_X[p][1]) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
                
                #put the new location to blue :
                frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "blue")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=X[p][0], column=X[p][1]) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
                
        
        mytime = get_time()
        mytime = update_time()
        
        global timer
        timer.pack_forget()
        timer = tk.Label(master, text="Time : " + str(mytime))
        timer.pack(side = RIGHT)
    
        
        
        
    button.bind("<Button-1>", leftclick)
    button.pack(side=RIGHT)
    
    
    
    tk.mainloop()
    
    return 0 

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
    
#%% ################## MOVES OF A PEDESTRIAN ##################################

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
            
            for neigh in range(len(possible_moves)): #check all possibilities and see which is the closest to the target
                print(neigh, possible_moves[neigh])
                if possible_moves[neigh] < possible_moves[best_move] and possible_moves[neigh] != -1:
                    best_move = neigh
                        
            X[i] = neighboors[best_move] # move towards the best cell
            
    return X, waiting_list
        

def simulation(env,pedestrian_number,X,N, speed, waiting_list) : 
    """ Simulate all the positions of the pedestrians N times 
    or until one of them reaches destination, returns a matrix"""
    
    positions = []
    for step in range(N) : 
        M = env.copy()
        X = one_step(env,pedestrian_number,X,speed, waiting_list,grid_size)
    
    
        for i in range(len(X)) : 
            M[X[i][0]][X[i][1]] = 1
            positions.append(M)
            if np.sum(np.sum(M)) == pedestrian_number : 
                return positions

            
    return positions














#%%                     Other possible implementation, considering a speed in real time
    

def single_step(env, pedestrian_id, X, distance_matrix, grid_size) :
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""

    ped = pedestrian_id
    loc = X[ped] #pedestrian location
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
        if possible_moves[neigh] < possible_moves[best_move] and possible_moves[neigh] != -1:
            best_move = neigh
                    
    X[ped] = neighboors[best_move]
            
    return X



def run_real_time_graphic(n, pedestrian_number, env, grid_size, X, target, pedestrian_speed, duration, pixel=15, measure_flow=0):
    
    master = tk.Tk()
    grid_frame = tk.Frame( master)
    for i in range(grid_size[0]) : 
        for j in range(grid_size[1]) : 
    
            if env[i][j] == 3 : #target
    
                frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "red")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=i, column=j) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
    
            elif env[i][j] == 2 : 
                frame = tk.Frame(grid_frame, width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "black")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=i, column=j) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
                
            else : 
                frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                button1 = tk.Button(frame, bg = "white")
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=i, column=j) #put frame where the button should be
                button1.grid(sticky="wens") #makes the button expand
            
            
    #####################    PEDESTRIANS
    for l in range(pedestrian_number) : 
        i,j = X[l]
        frame = tk.Frame(grid_frame, width=pixel, height=pixel) #their units in pixels
        button2 = tk.Button(frame, bg = "blue")
        frame.grid_propagate(False) #disables resizing of frame
        frame.columnconfigure(0, weight=1) #enables button to fill frame
        frame.rowconfigure(0,weight=1) #any positive number would do the trick
        frame.grid(row=i, column=j) #put frame where the button should be
        button2.grid(sticky="wens") #makes the button expand
    
    grid_frame.pack(side=LEFT)
    
    timing_text = tk.Label(master, text="  Simulation time in s:     ")
    timing_text.pack(side=TOP)
    
    timing_display = tk.Label(master, text="       0 s")
    timing_display.pack(side=TOP)
    
    flow_display = tk.Label(master, text="flow = speed * density")
    flow_display.pack(side=TOP)
    
    
    ########################### MOVING PEDESTRIANS ############################
    button = tk.Button(master, text = "Start simulation ")
    
    dist = distance_matrix(env, grid_size, target)
    
    def get_X() :  
        return X, X.copy()
      
    
    def leftclick(event):
        m1, m2, m3 = 0, 0, 0
        start = time.perf_counter()
        pedestrian_waiting = [0.4/pedestrian_speed[i] + start for i in range(pedestrian_number)]
        while time.perf_counter()-start<duration:
            timed = time.perf_counter()
            if timed>np.min(pedestrian_waiting):
                X,old_X = get_X()
                for p in range(pedestrian_number):
                    if pedestrian_waiting[p] < timed:
                        X = single_step(env, p, X, dist, grid_size)
                        pedestrian_waiting[p] += 0.4/pedestrian_speed[p]
                    if old_X[p] != X[p] :
                        #counts pedesterains who walks throught the measuring points
                        if ((start+10 <= time.perf_counter()) and (time.perf_counter() <= start+70)):
                            if (X[p][0] == 2 and X[p][1] == 225):
                                m1 += 1
                            if (X[p][0] == 2 and X[p][1] == 250):
                                m2 += 1
                            if (X[p][0] == 1 and X[p][1] == 250):
                                m3 += 1
                        #change the old location to white :
                        frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                        button1 = tk.Button(frame, bg = "cyan")
                        frame.grid_propagate(False) #disables resizing of frame
                        frame.columnconfigure(0, weight=1) #enables button to fill frame
                        frame.rowconfigure(0,weight=1) #any positive number would do the trick
                        frame.grid(row=old_X[p][0], column=old_X[p][1]) #put frame where the button should be
                        button1.grid(sticky="wens") #makes the button expand
                        
                        #put the new location to blue :
                        frame = tk.Frame(grid_frame,  width=pixel, height=pixel) #their units in pixels
                        button1 = tk.Button(frame, bg = "blue")
                        frame.grid_propagate(False) #disables resizing of frame
                        frame.columnconfigure(0, weight=1) #enables button to fill frame
                        frame.rowconfigure(0,weight=1) #any positive number would do the trick
                        frame.grid(row=X[p][0], column=X[p][1]) #put frame where the button should be
                        button1.grid(sticky="wens") #makes the button expand
                        
                        timing_display.configure(text="       " + str(int((timed-start)*100)/100) + "s")
                        #displays the amount of people passed from the control points
                        flow_display.configure(text="Control1: " + str(m1) + " Main: " + str(m2) + " Control2: " + str(m3))
                        button1.update()
                    
        
        
    button.bind("<Button-1>", leftclick)
    button.pack(side=RIGHT)
    
    

    tk.mainloop()











