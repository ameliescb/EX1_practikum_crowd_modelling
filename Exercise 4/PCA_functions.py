#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:57:29 2019

@author: mayau
"""

import numpy.linalg as la
import numpy as np
import glob
import matplotlib.pyplot as plt
  
# Function to normalize X

def normalize(X):   
    
    N, n = X.shape
    x_ = [0 for i in range(n)]
    for j in range(n):
        x_[j] = np.sum(X[:, j])/N
        
    for i in range(N):
        for j in range(n):
            X[i, j] = X[i, j] - x_[j]
    return X, n ,N

# Apply PCA to the data

def PCA_Energy(X, L):
    
    X, n, N = normalize(X)
    U, S, Vt = la.svd(X)
    
    energy = np.sum(S[:L])/np.sum(S)
    
    print("Energy for dimension " + str(L) + " = " + str(energy))
    
    return energy, U, S, Vt, n, N, X


def PCA_Reduce(U, S, Vt, N, n, L):
    Smat = np.zeros((N,n))
    for i in range(L):
        Smat[i, i] = S[i]
    return U.dot(Smat.dot(Vt))
    
