# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:35:59 2019

@author: amelie
"""

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as manimation
from scipy.integrate import odeint
import scipy
import glob
import pandas as pd

#%%
#Load the two data bases

p = 30 #number of pedestrian of the scenario


######################### GNM/Model Database
final_split = []
last_time_step = 0

path_of_output = glob.glob("outputGNM-"+str(p)+"/task5_*/postvis.trajectories")

for path in path_of_output : 
    file = open(path,'r').read()
    split = file.split('\n')
    split = split[1:-1]
    
    for l in split : 
        row = l.split(' ')
        row = [str(float(row[0])+ last_time_step)] + row[1:]
        final_split.append(row)
    last_time_step = float(row[0])
    
global gnm
gnm = pd.DataFrame(final_split, columns = ["timeStep","Id","x","y","target_id"] )
gnm = gnm.astype(float)
print(gnm)

############################# OSM / Ground Truth Database
path_of_output = glob.glob("outputOSM-"+str(p)+"/task5_*/postvis.trajectories")
final_split = [] #we keep this value, we use it then in the functions
last_time_step = 0

for path in path_of_output : 
    file = open(path,'r').read()
    split = file.split('\n')
    split = split[1:-1]
    
    for l in split : 
        row = l.split(' ')
        row = [str(float(row[0])+ last_time_step)] + row[1:]
        final_split.append(row)
    last_time_step = float(row[0])
    
global osm
osm = pd.DataFrame(final_split, columns = ["timeStep","Id","x","y","target_id"] )
osm = osm.astype(float)
print(osm)
#%%

def f_true(x,dt) :
    output = []
    global osm
    global output_time_out
    
    
    
    for i in range(0,x.shape[1],2) : 
        init_row = osm.loc[ (osm['x'] == x[0][i])  &  (osm['y'] == x[0][i+1]) ]
        
        
        if (init_row.empty) : #we look for the value with minimal distance
            #at this time step
            
            possible_values_x = osm.loc[(osm['timeStep'] == dt ) ]['x'].values.tolist()
            possible_values_y = osm.loc[(osm['timeStep'] == dt ) ]['y'].values.tolist()
            
            
            if possible_values_x == [] : #no more pedestrians
                return output_time_out
            
            else : 
                distances = [(x[0][i] - possible_values_x[k])**(2)
                             +(x[0][i+1] - possible_values_y[k])**(2)
                             for i in range(len(possible_values_x))]
                
    
                xd = possible_values_x[np.argmin(distances)]
                yd = possible_values_y[np.argmin(distances)]
                init_row = osm.loc[ (osm['x'] == xd)  &  (osm['y'] == yd) ]
      
        
        #pedestrian id of interest
        p_id = init_row['Id'].values[0]
        
        next_row = osm.loc[(osm['Id'] == p_id)& (osm['timeStep'] == dt ) ]
        
        #if a pedestrian is on target, we keep the same location
        dt1 = dt
        if (next_row.empty) : 
            dt1 -= 1
            row_to_be_pasted = osm.loc[(osm['Id'] == p_id)& (osm['timeStep'] == dt1 ) ]
            idex = osm.index.get_loc(row_to_be_pasted.iloc[0].name)
            for i in range(dt,NT) : 
                row_to_be_pasted.at[idex,'timeStep'] = i
                osm = osm.append(row_to_be_pasted)
                
            next_row = osm.loc[(osm['Id'] == p_id)& (osm['timeStep'] == dt ) ]
        
        xc1 = next_row['x'].values.tolist()
        xc2 = next_row['y'].values.tolist()
    
        output.append(xc1[0])
        output.append(xc2[0])
        output_time_out = output
        
    return np.array(output)



def f_model(x,dt,b) :
    global gnm
    output = []

    
    
    for i in range(0,x.shape[1],2) :
        
        init_row = gnm.loc[ (gnm['x'] == x[0][i])  &  (gnm['y'] == x[0][i+1]) ]
        #pedestrian id of interest
        
        
        
        if (init_row.empty) : #we look for the value with minimal distance
            #at this time step
            possible_values_x = gnm.loc[(gnm['timeStep'] == dt ) ]['x'].values.tolist()
            possible_values_y = gnm.loc[(gnm['timeStep'] == dt ) ]['y'].values.tolist()
            distances = [(x[0][i] - possible_values_x[k])**(2)
                         +(x[0][i+1] - possible_values_y[k])**(2)
                         for i in range(len(possible_values_x))]
            
            xd = possible_values_x[np.argmin(distances)]
            yd = possible_values_y[np.argmin(distances)]
            init_row = gnm.loc[ (gnm['x'] == xd)  &  (gnm['y'] == yd) ]
            
            
    
        p_id = init_row['Id'].values[0]
        next_row = gnm.loc[(gnm['Id'] == p_id)& (gnm['timeStep'] == dt ) ]
        
        
        dt1 = dt
        if (next_row.empty) : 

            dt1 -= 1
            row_to_be_pasted = gnm.loc[(gnm['Id'] == p_id)& (gnm['timeStep'] == dt1 ) ]
            idex = gnm.index.get_loc(row_to_be_pasted.iloc[0].name)
            for i in range(dt,NT) : 
                row_to_be_pasted.at[idex,'timeStep'] = i
                gnm = gnm.append(row_to_be_pasted)
            next_row = gnm.loc[(gnm['Id'] == p_id)& (gnm['timeStep'] == dt ) ]
            
            
        
        xc1 = next_row['x'].values.tolist()
        xc2 = next_row['y'].values.tolist()
    
        output.append(xc1[0])
        output.append(xc2[0])
        
    
        
    return np.array(output)
#%%
def normal_draw(cov):
    """ draw an n-dimensional point from a Gaussian distribution with given covariance. """
    return np.random.multivariate_normal(cov[:,0],cov,1)


    
# compute ensemble Kalman smoothing
def algorithm1_enks(z_data, error_covariance_M, error_covariance_Q):
    t = z_data.shape[0]
    print(z_data.shape)
    ML = (error_covariance_M)
    QL = (error_covariance_Q)
    
# initialize the initial guess for the model state with random numbers
# normally, one would probably have a better guess
    xk = z_data.copy()
    for k in range(1,t):
        print('k' + str(k))
        zk = np.zeros((z_data.shape[1],))
        for i in range(m):
            print('i' + str(i))
            mkm1 = normal_draw(ML)
            xk[k,(i*nd):((i+1)*nd)] = f_model(xk[k-1,(i*nd):((i+1)*nd)].reshape(1,-1),k,0.1) +mkm1 
            qk = normal_draw(QL)
            zk[(i*nd):((i+1)*nd)] = f_true(xk[k,(i*nd):((i+1)*nd)].reshape(1,-1),k) + qk
            
        zkhat = 1/m*np.sum([zk[i::nd] for i in range(nd)],axis=1)
        zdiff = np.row_stack([(zk[(i*nd):((i+1)*nd)]-zkhat) for i in range(m)])
        Zk = np.cov(zdiff.T)
        
        for j in range(1,k+1):
            xjbar = np.array(1/m*np.sum([xk[j,i::nd] for i in range(nd)],axis=1))
            xdiff = np.row_stack([(xk[j,(i*nd):((i+1)*nd)]-xjbar) for i in range(m)])
            zdiff = np.row_stack([(zk[(i*nd):((i+1)*nd)]-zkhat) for i in range(m)])
            sigmaj = 1/(m-1) * (xdiff.T @ zdiff)
            matk = sigmaj @ np.linalg.pinv(Zk,rcond=1e-10)
            
            for i in range(m):
                xk[j,(i*nd):((i+1)*nd)] = xk[j,(i*nd):((i+1)*nd)] + matk @(z_data[k,(i*nd):((i+1)*nd)]-zk[(i*nd):((i+1)*nd)])
    return xk



def max_likelihood(xk):
    t = xk.shape[0]
    data = []
    for k in range(1, t-1):
        for i in range(m):
            fhat = f_model(xk[k,(i*nd):((i+1)*nd)].reshape(1,-1),k,0.1)
            xhat = xk[k+1,(i*nd):((i+1)*nd)]
            data.append((xhat-fhat))
            
     
    data = np.row_stack(np.array(data))

# note that we do not compute it "per agent", as in the paper guy-2019b,
# but for all coordinates of the state (we only consider one "agent" in this code)
    return np.cov(data.T)




def entropy(M):
    return 1/2 * n * np.log((2*np.pi*np.exp(1))**d * np.linalg.det(M))

#%%

random_seed = 1 # used throughout the example

np.random.seed(random_seed)

# Number of time steps for the given simulation
NT = 70
# Physical time that passes in the given number of time steps
T = 5
dt = T / NT
time = np.linspace(0,T,NT)


#model_error = 1e-0 # very noisy, entropy > 0
model_error = 1e-1 # very smooth, entropy < 0

# Initial state of the true and simulated data
x_gnm = gnm.loc[gnm['timeStep'] == 1]['x'].values.tolist()
y_gnm = gnm.loc[gnm['timeStep'] == 1]['y'].values.tolist()

x_osm = osm.loc[osm['timeStep'] == 1]['x'].values.tolist()
y_osm = osm.loc[osm['timeStep'] == 1]['y'].values.tolist()

# this is the error in the true model, and also in the observations. You do not
# need to change this.

true_error = 1e-4
m = 10 # ensemble runs
n = len(x_gnm) # number of agents. Note that the models f_true and f_model only work for n=1.
d = 2 # dimension per "agent" (we only have one here)
nd = n*d # total state dimension
xt = np.zeros((NT, (nd*m)))
x0_gnm = []
x0_osm = []
for i in range(n) :
    x0_gnm.append(x_gnm[i])
    x0_gnm.append(y_gnm[i])
    
    x0_osm.append(x_osm[i])
    x0_osm.append(y_osm[i])


x0_gnm = np.array(x0_gnm+x0_gnm+x0_gnm+x0_gnm+x0_gnm
                 +x0_gnm+x0_gnm+ x0_gnm + x0_gnm+x0_gnm)




# initialize the ensembles with randomly perturbed states
# in this example, this is not necessary because the model itself introduces errors

xt[0,:m*nd] = np.column_stack(x0_gnm) #let's use the mathematical model first
#state as initialisation
xm = xt.copy()


# this is the initial guess for the entropy matrix. can be pretty arbitrary
M = np.identity(nd) 
# this is the guess for the true error in the observations. should be small here.
Q = np.identity(nd) * true_error**2

N_ITER = 4 # number of iterations of algorithm1_enks and max_likelihood
Mhat = M
entropy_list =[]
zk = np.zeros(np.shape(xt))
zk[0,:] = f_true(xt[1:,:],1).reshape(1,-1)
xm_hat = 0
xm_hat_prev = 0
for k in range(N_ITER):
    
    print(k)
    xm_hat = algorithm1_enks(zk, Mhat, Q);
    print(xm_hat)
    Mhat = max_likelihood(xm_hat)
    print('current det(M)', np.linalg.det(Mhat))
    print('error change ', np.linalg.norm(xm_hat - xm_hat_prev))
    xm_hat_prev = xm_hat
    
    entropy_list.append(entropy(Mhat))


#%%
print('entropy(M estimated) ', entropy(Mhat))









