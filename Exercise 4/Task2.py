# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:43:03 2019

@author: amelie
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_swiss_roll
from sklearn.decomposition import PCA
from sklearn import preprocessing
import glob

#%%

def diffusion_map(X,L,scalar = False) : 
    N = len(X)
    
    if scalar == False :
        n = len(X[0])
    else : 
        n = 1
    
    #1 form D
    D = np.zeros((N,N))
    for i in range(N) : 
        for j in range(N) : 
            for k in range(n) : 
                D[i][j] += np.abs(X[i][k]-X[j][k])
    
    #2
    
    eps = 0.05*np.amax(D)
    #3
    W = np.zeros((N,N))
    for i in range(N) : 
        for j in range(N) : 
            W[i][j] = np.exp(-D[i][i]**(2)/eps)
    
    #4
    P = np.diag(np.sum(W,axis = 0))
    
    #5
    K = np.dot(np.linalg.inv(P),np.dot(W,np.linalg.inv(P)))
    
    #6
    Q = np.diag(np.sum(K,axis = 0))
    
    #7
    T_hat = np.linalg.inv(np.power(Q,0.5))@K@np.linalg.inv(np.power(Q,0.5))
    
    #8
    a,v = np.linalg.eig(T_hat)
    sort_indeces = np.argsort(a)[::-1]
    
    a_L = [a[i] for i in sort_indeces]
    v_L =[v[i] for i in sort_indeces]

    a_L = a_L[:L]
    v_L = v_L[:L]

    #9
    lambdas = [a_L[i]**(1/(2*eps)) for i in range(L)] 
    
    #
    phis = np.linalg.inv(np.power(Q,0.5)) @ np.array(v_L).T
    
    return lambdas, phis.T

#%% PART ONE 
    
N = 1000

t = [2*np.pi*k / (N+1) for k in range(N)]
X = [(np.cos(t[k]),np.sin(t[k])) for k in range(N)]

lambdas,phis = diffusion_map(X,5)



fig, axes = plt.subplots(6, 1)
ax1, ax2, ax3, ax4,ax5,ax6 = axes 
ax1.plot(t,X)
ax1.set_title('Dataset : signal X')
k = 0
for phi in phis :
    k += 1
    
    axes[k].plot(t,phi)
    axes[k].set_title(r'$\phi_'+ str(k) + '(x_k)$ against $t_k$')

plt.show()


#%% PART 2
N = 1000

from mpl_toolkits.mplot3d import Axes3D
X,t = make_swiss_roll(n_samples=100, noise=0.0, random_state=None)

### Diffusion Map analysis
lambdas,phis = diffusion_map(X,10)

k = 0
#%%
fig = plt.figure()

ax1 = fig.add_subplot(4,2,1)
ax2 = fig.add_subplot(4,2,2)
ax3 = fig.add_subplot(4,2,3)
ax4 = fig.add_subplot(4,2,4)

ax5 = fig.add_subplot(4,2,5)
ax6 = fig.add_subplot(4,2,6)
ax7 = fig.add_subplot(4,2,7)
ax8 = fig.add_subplot(4,2,8)

axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]

for k in range(8) :

    axes[k].plot(phis[1],phis[2+k])
    axes[k].set_title(r'$\phi_{'+ str(2+k) + '}$ against $\phi_1$')

plt.subplots_adjust(hspace=0.5)
plt.show()
#%%
#more points for a better visualization.
X,t = make_swiss_roll(n_samples=10000, noise=0.0, random_state=None)
pca = PCA(n_components=3)
principalComponents = pca.fit_transform(X)


fig = plt.figure(figsize = (10,40))

ax1 = fig.add_subplot(411, projection='3d')
ax1.set_title('Swiss roll data set')
ax1.scatter(xs = X[:,0],ys = X[:,1],zs = X[:,2],c = t)


ax2 = fig.add_subplot(412, projection='3d')
ax2.scatter(t,principalComponents[:,0],c= t,zdir = 'z')
#ax2.set_ylim(-40,-30)
#ax2.set_xlim(20,30)
ax2.set_title('PCA 1')

ax3 = fig.add_subplot(413, projection='3d')
ax3.scatter(t,principalComponents[:,1],c= t,zdir = 'z')
ax3.set_title('PCA 2')

ax4 = fig.add_subplot(414, projection='3d')
ax4.scatter(t,principalComponents[:,2],c= t,zdir = 'z')

ax4.set_title('PCA 3')

plt.show()

#%%
t = np.arange(1000)
X = []
file = open(glob.glob('data_DMAP_PCA_vadere.txt')[-1], "r")
for line in file:
    l_arr = line.split()
    for i in range(len(l_arr)):
        l_arr[i] = float(l_arr[i])
    X.append(l_arr)

X = np.array(X)

lambdas,phis = diffusion_map(X,20)
plt.figure(figsize = (18,9))

plt.subplot(311)
plt.title(r'$X$')
plt.plot(X)


plt.subplot(312)
plt.title('10 eighenfunctions')
plt.plot(phis[:10])



plt.subplot(313)
plt.title('20 eighenfunctions')
plt.plot(phis)



plt.show()

