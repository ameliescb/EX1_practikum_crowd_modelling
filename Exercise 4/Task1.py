#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:02:39 2019

@author: mayau
"""

import numpy.linalg as la
import numpy as np
import glob
import matplotlib.pyplot as plt
from PCA_functions import *
import scipy.misc

#%%  Part 1

X = []

# Charge the data and set the type as float in a matrix X

file = open(glob.glob('pca_dataset.txt')[-1], "r")
for line in file:
    l_arr = line.split()
    for i in range(len(l_arr)):
        l_arr[i] = float(l_arr[i])
    X.append(l_arr)
    
X = np.array(X)    
Y = X.copy()

plt.figure(figsize=(18,6))
plt.subplot(1,3,1)
plt.scatter(Y[:, 0], Y[:, 1])
plt.title("Original data") 

L = 1
energy, U, S, Vt, n, N, X = PCA_Energy(X, L)

Reduce = PCA_Reduce(U, S, Vt, N, n, L)

plt.subplot(1,3,2)
plt.scatter(X[:, 0], X[:, 1])
plt.title("Normalized data")    

plt.subplot(1,3,3)
plt.scatter(Reduce[:, 0], Reduce[:, 1])
plt.title("Reduced data")




#%%  Part 2

racoon = scipy.misc.face()
shape = racoon.shape

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

racoon = rgb2gray(racoon)


plt.figure(figsize=(18,12))
plt.subplot(2,2,1)
plt.title("all principal components")
L = shape[0]
energy, U, S, Vt, n, N, X = PCA_Energy(racoon, L)
Reduce = PCA_Reduce(U, S, Vt, N, n, L)
plt.imshow(Reduce, cmap=plt.get_cmap('gray'))

plt.subplot(2,2,2)
plt.title("120 principal components")
L = 120
energy, U, S, Vt, n, N, X = PCA_Energy(racoon, L)
Reduce = PCA_Reduce(U, S, Vt, N, n, L)
plt.imshow(Reduce, cmap=plt.get_cmap('gray'))

plt.subplot(2,2,3)
plt.title("50 principal components")
L = 50
energy, U, S, Vt, n, N, X = PCA_Energy(racoon, L)
Reduce = PCA_Reduce(U, S, Vt, N, n, L)
plt.imshow(Reduce, cmap=plt.get_cmap('gray'))

plt.subplot(2,2,4)
plt.title("10 principal components")
L = 10
energy, U, S, Vt, n, N, X = PCA_Energy(racoon, L)
Reduce = PCA_Reduce(U, S, Vt, N, n, L)
plt.imshow(Reduce, cmap=plt.get_cmap('gray'))


#for i in range(shape[0]):
#    energy = PCA_Energy(racoon, i)
#    print("\n\n", energy[0])
#    if energy[0] > 0.99:
#        break
#    
#print(i)


#%%  Part 3

X = []
file = open(glob.glob('data_DMAP_PCA_vadere.txt')[-1], "r")
for line in file:
    l_arr = line.split()
    for i in range(len(l_arr)):
        l_arr[i] = float(l_arr[i])
    X.append(l_arr)

X = np.array(X)

plt.figure(figsize = (18,9))

plt.subplot(1,2,1)
plt.title("First pedestrian")
plt.plot(X[:, 0], X[:, 1])

plt.subplot(1,2,2)
plt.title("Second pedestrian")
plt.plot(X[:, 2], X[:, 3])

X = X.T
L = 3
energy, U, S, Vt, n, N, X = PCA_Energy(X, L)
Reduce = PCA_Reduce(U, S, Vt, N, n, L)
Reduce = Reduce.T

plt.figure(figsize = (18,9))

plt.subplot(1,2,1)
plt.title("First pedestrian with 2 principal components")
plt.plot(Reduce[:, 0], Reduce[:, 1])

plt.subplot(1,2,2)
plt.title("Second pedestrian with 2 principal components")
plt.plot(Reduce[:, 2], Reduce[:, 3])













