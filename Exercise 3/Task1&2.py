# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:45:48 2019

@author: amelie
"""


import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as manimation
from scipy.integrate import odeint
import scipy
from numpy import linalg as LA
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#%% ########################TASK 1 ############################

alpha = 0.1 #set the alpha value that you want

def A_alpha(alpha) : 
    A = np.array([[alpha,alpha],[-0.25,0]])
    w,v = LA.eig(A)
    return(A,w)

#example
A, lambdas = A_alpha(alpha) #get A_{alpha} and its eighenvalues
L1, L2 = lambdas[0], lambdas[1]
print(L1,L2)

def d_phi_alpha(t,x) : 
    res = A @ x
    return(res)


#visualisation
nx, ny = (55, 55)
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)
X,Y = np.meshgrid(x, y)
fig = plt.figure(figsize=(9, 9))
gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])


#########################Alpha = 0.1 ############################# 
#speed d_phi(x)
U = A[0][0]*X + A[0][1] * Y
V = A[1][0]*X + A[1][1] * Y

#  Varying density along a streamline
ax0 = fig.add_subplot(gs[0, 0])

# first point
seed_points = np.array([[0], [ 0]])

ax0.streamplot(X, Y, U, V, color='k',density = 2, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)
ax0.streamplot(X, Y, U, V, color='r', linewidth=2,start_points=seed_points.T)


ax0.set_title(r'$\alpha$ = ' + str(alpha)+ r', $\lambda_1$ = ' +str(np.round_(L1, decimals=2))
            + r', $\lambda_2$ = ' + str(np.round_(L2, decimals=2)))


#########################Alpha = 0.5 ############################# 
alpha = 0.5 #set the alpha value that you want
A, lambdas = A_alpha(alpha) #get A_{alpha} and its eighenvalues
L1, L2 = lambdas[0], lambdas[1]

#speed d_phi(x)
U = A[0][0]*X + A[0][1] * Y
V = A[1][0]*X + A[1][1] * Y

#  Varying density along a streamline
ax1 = fig.add_subplot(gs[0, 1])

# first point
seed_points = np.array([[0], [ 0]])

ax1.streamplot(X, Y, U, V, color='k',density = 2, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)
ax1.streamplot(X, Y, U, V, color='r', linewidth=2,start_points=seed_points.T)


ax1.set_title(r'$\alpha$ = ' + str(alpha)+ r', $\lambda_1$ = ' +str(np.round_(L1, decimals=2))
            + r', $\lambda_2$ = ' + str(np.round_(L2, decimals=2)))


#########################Alpha = 2 ############################# 
alpha = 2 #set the alpha value that you want
A, lambdas = A_alpha(alpha) #get A_{alpha} and its eighenvalues
L1, L2 = lambdas[0], lambdas[1]

#speed d_phi(x)
U = A[0][0]*X + A[0][1] * Y
V = A[1][0]*X + A[1][1] * Y

#  Varying density along a streamline
ax2 = fig.add_subplot(gs[1, 0])

# first point
seed_points = np.array([[0], [ 0]])

ax2.streamplot(X, Y, U, V, color='k',density = 2, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)
ax2.streamplot(X, Y, U, V, color='b', linewidth=2,start_points=seed_points.T)


ax2.set_title(r'$\alpha$ = ' + str(alpha)+ r', $\lambda_1$ = ' +str(np.round_(L1, decimals=2))
            + r', $\lambda_2$ = ' + str(np.round_(L2, decimals=2)))

######################### Alpha = 10 ############################# 

alpha = 10 #set the alpha value that you want
A, lambdas = A_alpha(alpha) #get A_{alpha} and its eighenvalues
L1, L2 = lambdas[0], lambdas[1]

#speed d_phi(x)
U = A[0][0]*X + A[0][1] * Y
V = A[1][0]*X + A[1][1] * Y

#  Varying density along a streamline
ax3 = fig.add_subplot(gs[1, 1])

# first point
seed_points = np.array([[0], [ 0]])

ax3.streamplot(X, Y, U, V, color='k',density = 2, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)
ax3.streamplot(X, Y, U, V, color='b', linewidth=2,start_points=seed_points.T)


ax3.set_title(r'$\alpha$ = ' + str(alpha)+ r', $\lambda_1$ = ' +str(np.round_(L1, decimals=2))
            + r', $\lambda_2$ = ' + str(np.round_(L2, decimals=2)))


plt.show()

#%% ########################## TASK 2 ##################################""

###############First equation


def dxdt(t,x) : 
    return(alpha - x**(2))
    
#getting the roots of the polynom to get the diagram
alphas = np.linspace(-1,1,10000)

alph_real= []
alph_imag= []
roots_real = []
roots_imag = []

for alpha in alphas : 
    coeff = [-1,0, alpha]
    roots = np.roots(coeff)
    
    if roots[0].imag == 0 and roots[1].imag == 0 :
        roots_real.append(roots)
        alph_real.append(alpha)
    
    else : 
        roots_imag.append(roots)
        alph_imag.append(alpha)
    
roots_real = np.array(roots_real)
roots_imag = np.array(roots_imag)


plt.plot(alph_real,roots_real[:,0],label = "steady state", color = 'b')
plt.plot(alph_real,roots_real[:,1], color = 'b')

plt.plot(alph_imag,roots_imag[:,0],color = 'c',label = "no steady state", linestyle="--")
plt.plot(alph_imag,roots_imag[:,1],color = 'c',linestyle="--")

plt.xlabel(r'$\alpha$')
plt.legend()
plt.title(r'Bifurcation diagramm, $ \dot{x} = \alpha - x^{2}$'  )
plt.show()
#%%

########### Second equation 
#getting the roots of the polynom to get the diagram
alphas = np.linspace(-1,3,10000)

alph_real= []
alph_imag= []
roots_real = []
roots_imag = []

for alpha in alphas : 
    coeff = [-2,0, alpha-2]
    roots = np.roots(coeff)
    roots = roots.tolist()
    
    if roots[0].imag == 0 and roots[1].imag == 0 :
        roots_real.append(roots)
        alph_real.append(alpha)
    
    else : 
        roots_imag.append(roots)
        alph_imag.append(alpha)
    
roots_real = np.array(roots_real)
roots_imag = np.array(roots_imag)

plt.plot(alph_real,roots_real[:,0],label = "steady state", color = 'b')
plt.plot(alph_real,roots_real[:,1], color = 'b')

plt.plot(alph_imag,roots_imag[:,0],color = 'c',label = "no steady state", linestyle="--")
plt.plot(alph_imag,roots_imag[:,1],color = 'c',linestyle="--")

plt.xlabel(r'$\alpha$')
plt.legend()
plt.title(r'Bifurcation diagramm, $ \dot{x} = \alpha - 2x^{2}-2$')
plt.show()

#%%
#Topological equivalence : phase portraits
#alpha = 1 

#visualisation
X = np.linspace(-10,10,100)
fig = plt.figure()
gs = gridspec.GridSpec(nrows=1, ncols=2)

ax1 = fig.add_subplot(gs[0,0])
VX1 = 1 - X**(2)
ax1.plot(VX1,X)
ax1.set_title(r'$ \dot{x} = \alpha - x^{2}$, $\alpha$ = 1')

ax2 = fig.add_subplot(gs[0,1])
VX2 = -2 * X**(2) - 1
ax2.plot(VX2,X)
ax2.set_title(r'$ \dot{x} = \alpha - 2x^{2}-2$, $\alpha$ = 1')

plt.show()

#%%
#alpha = -1

#visualisation
X = np.linspace(-10,10,100)
fig = plt.figure()
gs = gridspec.GridSpec(nrows=1, ncols=2)

ax1 = fig.add_subplot(gs[0,0])
VX1 = -X**(2) - 1
ax1.plot(VX1,X)
ax1.set_title(r'$ \dot{x} = \alpha - x^{2}$, $\alpha$ = 1')

ax2 = fig.add_subplot(gs[0,1])
VX2 = -2 * X**(2) - 3
ax2.plot(VX2,X)
ax2.set_title(r'$ \dot{x} = \alpha - 2x^{2}-2$, $\alpha$ = 1')

plt.show()
