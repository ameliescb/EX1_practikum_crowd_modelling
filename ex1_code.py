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

#We store the speed of the pedestrians in the list "speed", and create a waiting
#list for them in the list "waiting_list" which stores the time of the last 
#move of each pedestrian. 


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
    
    #speed : here the pedestrians have all the same speed of 1case/s
    speed = [1 for i in range(pedestrian_number)] #cannot be > 1case/s
    waiting_list = [0 for i in range(pedestrian_number)] #howlong the pedestrian are in this position
    time = 0 #initialisation, time set to zero
    
    
    
    
    
    
    for i in range(pedestrian_number) : 
        h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
        while env[h][v] > 0 : #don't put 2 ped. in the same place, don't put them in the target
            h,v  = np.random.randint(grid_size), np.random.randint(grid_size)
        X[i] = [h,v]
        
        
    
    return(grid_size, env, X,target,speed,waiting_list)

    
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


def one_step(env,pedestrian_number,X, speed, waiting_list) :
    
    """ Simulation of 1 step of all pedestrians given the target and obstacles, 
    and the pedestrians locations"""

    for i in range(pedestrian_number):
        loc = X[i] #pedestrian location
        
        if env[loc[0],loc[1]] == 3 :  #stop when the first pedestrian is on the target
            return X,waiting_list
        
        elif ((waiting_list[i]+1) *speed[i])   < 1: #the pedestrian should wait
            waiting_list[i] += 1
        
            
        else : 
            waiting_list[i] = 0 #the pedestrian will move at this time

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
            
    return X,waiting_list
        

def simulation(env,pedestrian_number,X,N, speed, waiting_list) : 
    """ Simulate all the positions of the pedestrians N times 
    or until on of them reaches destination"""
    
    positions = []
    for step in range(N) : 
        M = env.copy()
        X = one_step(env,pedestrian_number,X,speed, waiting_list)
    
    
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
grid_size, env,X,target,speed,waiting_list=  initialization(n, pedestrian_number,obstacle_number)

global time
time = 0 

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


########################### MOVING PEDESTRIANS ############################
button = tk.Button(master, text = "Simulate one step ")

global timer 
timer = tk.Label(master, text="Time : " + str(time))
timer.pack(side = RIGHT)



def get_X() :  
    return X, X.copy()


def get_waiting_list() :
    return waiting_list

def get_time() : 
    
    return time

def update_time() : 
    global time
    time += 1
    return time
  

def leftclick(event):
    
    X,old_X = get_X()
    waiting_list = get_waiting_list()
    X,waiting_list = one_step(env,pedestrian_number,X,speed,waiting_list) 

    
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
            
    
    time = get_time()
    time = update_time()
    
    global timer
    timer.pack_forget()
    timer = tk.Label(master, text="Time : " + str(time))
    timer.pack(side = RIGHT)
    #timer.labelText = "Time : " + str(time)
    
    
    
button.bind("<Button-1>", leftclick)
button.pack(side=RIGHT)



tk.mainloop()

#%%                               TASK 2



############################## INITIALIZATION ########################
n = 2500 #number of cases of the grid
pedestrian_number = 2
grid_size = int(np.sqrt(n))
    
  ##################      PLACING THE TARGET #########
env = np.zeros((grid_size,grid_size)) 
env[24][24] = 3
target = 24,24 
X = [[4,24],[24,4]]
speed = [1,0.3334]
waiting_list = [0,0]
global time
time = 0

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


########################### MOVING PEDESTRIANS ############################
button = tk.Button(master, text = "Simulate one step ")

global timer 
timer = tk.Label(master, text="Time : " + str(time))
timer.pack(side = RIGHT)



def get_X() :  
    return X, X.copy()


def get_waiting_list() :
    return waiting_list

def get_time() : 
    
    return time

def update_time() : 
    global time
    time += 1
    return time
  

def leftclick(event):
    
    X,old_X = get_X()
    waiting_list = get_waiting_list()
    X,waiting_list = one_step(env,pedestrian_number,X,speed,waiting_list) 

    
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
            
    
    time = get_time()
    time = update_time()
    
    global timer
    timer.pack_forget()
    timer = tk.Label(master, text="Time : " + str(time))
    timer.pack(side = RIGHT)
    #timer.labelText = "Time : " + str(time)
    
    
    
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

speed = [1 for i in range(pedestrian_number)]
waiting_list = [0 for i in range(pedestrian_number)]
global time
time = 0

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


########################### MOVING PEDESTRIANS ############################
button = tk.Button(master, text = "Simulate one step ")

global timer 
timer = tk.Label(master, text="Time : " + str(time))
timer.pack(side = RIGHT)



def get_X() :  
    return X, X.copy()


def get_waiting_list() :
    return waiting_list

def get_time() : 
    
    return time

def update_time() : 
    global time
    time += 1
    return time
  

def leftclick(event):
    
    X,old_X = get_X()
    waiting_list = get_waiting_list()
    X,waiting_list = one_step(env,pedestrian_number,X,speed,waiting_list) 

    
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
            
    
    time = get_time()
    time = update_time()
    
    global timer
    timer.pack_forget()
    timer = tk.Label(master, text="Time : " + str(time))
    timer.pack(side = RIGHT)
    #timer.labelText = "Time : " + str(time)
    
    
    
button.bind("<Button-1>", leftclick)
button.pack(side=RIGHT)



tk.mainloop()


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


speed = [1 for i in range(pedestrian_number)]
waiting_list = [0 for i in range(pedestrian_number)]
global time
time = 0

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


########################### MOVING PEDESTRIANS ############################
button = tk.Button(master, text = "Simulate one step ")

global timer 
timer = tk.Label(master, text="Time : " + str(time))
timer.pack(side = RIGHT)



def get_X() :  
    return X, X.copy()


def get_waiting_list() :
    return waiting_list

def get_time() : 
    
    return time

def update_time() : 
    global time
    time += 1
    return time
  

def leftclick(event):
    
    X,old_X = get_X()
    waiting_list = get_waiting_list()
    X,waiting_list = one_step(env,pedestrian_number,X,speed,waiting_list) 

    
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
            
    
    time = get_time()
    time = update_time()
    
    global timer
    timer.pack_forget()
    timer = tk.Label(master, text="Time : " + str(time))
    timer.pack(side = RIGHT)
    #timer.labelText = "Time : " + str(time)
    
    
    
button.bind("<Button-1>", leftclick)
button.pack(side=RIGHT)



tk.mainloop()

    