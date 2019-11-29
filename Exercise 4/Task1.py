#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:57:29 2019

@author: mayau
"""

import numpy.linalg as la
import numpy as np

def normalize(X):
    N, n = X.shape
    print(N, n)
    x_ = [0 for i in range(n)]
    for j in range(n):
        print(X[:, j], np.sum(X[:, j])/N)
        x_[j] = np.sum(X[:, j])/N
    
    print(x_)
    
    for i in range(N):
        for j in range(n):
            X[i, j] = X[i, j] - x_[j]
            print(X)
    return X