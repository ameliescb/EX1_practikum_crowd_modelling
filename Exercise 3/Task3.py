#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:24:11 2019

@author: mayau
"""
import cmath
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as manimation
from scipy.integrate import odeint
import scipy
from numpy import linalg as LA
#from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits import mplot3d
from scipy.optimize import fsolve

#%% Task 3 -1

#visualisation
nx, ny = (500, 500)
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)
X,Y = np.meshgrid(x, y)
fig = plt.figure(figsize=(9, 27))
gs = gridspec.GridSpec(nrows=3, ncols=1, height_ratios=[2, 2, 2])





alpha = -1 #set the alpha value that you want

#########################Alpha = 0.1 ############################# 
#speed d_phi(x)
U = -X*(X**2 + Y**2)**2 + alpha*X - Y
V = -Y*(X**2 + Y**2)**2 + X + alpha*Y

#  Varying density along a streamline
ax0 = fig.add_subplot(gs[0, 0])

ax0.streamplot(X, Y, U, V, color='k',density = 1, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)

ax0.set_title(r'$\alpha$ = ' + str(alpha))





alpha = 0 #set the alpha value that you want

#speed d_phi(x)
U = -X*(X**2 + Y**2)**2 + alpha*X - Y
V = -Y*(X**2 + Y**2)**2 + X + alpha*Y

#  Varying density along a streamline
ax1 = fig.add_subplot(gs[1, 0])

ax1.streamplot(X, Y, U, V, color='k',density = 1, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)

ax1.set_title(r'$\alpha$ = ' + str(alpha))





alpha = 1 #set the alpha value that you want

#speed d_phi(x)
U = -X*(X**2 + Y**2)**2 + alpha*X - Y
V = -Y*(X**2 + Y**2)**2 + X + alpha*Y

#  Varying density along a streamline
ax2 = fig.add_subplot(gs[2, 0])

ax2.streamplot(X, Y, U, V, color='k',density = 1, maxlength=0.2,
               arrowstyle='->', arrowsize=1,linewidth=0.5)

ax2.set_title(r'$\alpha$ = ' + str(alpha))





#%% Task 3 -2


def dpdt(p, t):
    alpha = 1
    return p*(alpha-p**2)

def dOdt(O, t):
    return 0.2

x0, y0 = (0.5, 0)

p0, O0 = cmath.polar(x0 + 1j*y0)

t = np.linspace(0, 500, 10000)
O = odeint(dOdt, O0, t)
p = odeint(dpdt, p0, t)

x = [cmath.rect(p[i], O[i]) for i in range (10000)]
x1 = np.array([x1.real for x1 in x])
x2 = np.array([x2.imag for x2 in x])

fig = plt.figure(figsize = [10,4])
ax1 = fig.add_subplot(121)#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:58:00 2019

@author: mayau
"""
ax1.title.set_text('Init: '+ str([x0,y0]))
ax1.plot(x1, x2)
#plt.title('initial point: ' [x0,y0])


x0, y0 = (2, 0)

p0, O0 = cmath.polar(x0 + 1j*y0)

t = np.linspace(0, 500, 10000)
O = odeint(dOdt, O0, t)
p = odeint(dpdt, p0, t)

x = [cmath.rect(p[i], O[i]) for i in range (10000)]
x1 = np.array([x1.real for x1 in x])
x2 = np.array([x2.imag for x2 in x])

ax2 = fig.add_subplot(122)
ax2.title.set_text('Init: '+ str([x0,y0]))
ax2.plot(x1, x2)
#plt.title('initial point: ' [x0,y0])
#%% Task 3

n = 100

alpha1 = [-1 + 2*i/n for i in range(n)]
alpha2 = [-1 + 2*i/n for i in range(n)]
x = []

alpha12 = []
alpha22 = []
alpha13 = []
alpha23 = []
x2 = []
x3 = []

for al1 in alpha1:
    for al2 in alpha2:
        roots = np.roots([-1, 0, al2, al1])
        x.append(roots[0].real)
        if len (roots) > 1:
            alpha12.append(al1)
            alpha22.append(al2)
            x2.append(roots[1].real)
        if len (roots) > 2:
            alpha13.append(al1)
            alpha23.append(al2)
            x3.append(roots[2].real)
        
alpha1 = [-1 + 2*int(i/n)/n for i in range(n**2)]
for j in range(n-1):
    alpha2 = alpha2 + [-1 + 2*i/n for i in range(n)]
    
ax = plt.figure(figsize=(15, 15))     
ax = plt.axes(projection='3d')
ax.scatter3D(alpha1, alpha2, x, )
ax.scatter3D(alpha12, alpha22, x2)
ax.scatter3D(alpha13, alpha23, x3)


ax.view_init(80, 90)
#plt.draw()
