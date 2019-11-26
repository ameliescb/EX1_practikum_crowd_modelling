"""
================
Lorenz Attractor
================

This is an example of plotting Edward Lorenz's 1963 `"Deterministic Nonperiodic
Flow"`_ in a 3-dimensional space using mplot3d.

.. _"Deterministic Nonperiodic Flow":
   http://journals.ametsoc.org/doi/abs/10.1175/1520-0469%281963%29020%3C0130%3ADNF%3E2.0.CO%3B2

.. note::
   Because this is a simple non-linear ODE, it would be more easily done using
   SciPy's ODE solver, but this approach depends only upon NumPy.
"""

import numpy as np
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


def lorenz(x, y, z, s=10, r=28, b=2.667):
    '''
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    '''
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


dt = 0.01
num_steps = 10000

# Need one more for the initial values
xs = np.empty(num_steps + 1)
ys = np.empty(num_steps + 1)
zs = np.empty(num_steps + 1)

# Set initial values
xs[0], ys[0], zs[0] = (10, 10, 10)

# Step through "time", calculating the partial derivatives at the current point
# and using them to estimate the next point
for i in range(num_steps):
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i]) #, r=0.5
    xs[i + 1] = xs[i] + (x_dot * dt)
    ys[i + 1] = ys[i] + (y_dot * dt)
    zs[i + 1] = zs[i] + (z_dot * dt)

# Need one more for the initial values
xl = np.empty(num_steps + 1)
yl = np.empty(num_steps + 1)
zl = np.empty(num_steps + 1)

# Set initial values
xl[0], yl[0], zl[0] = (10, 10, 10) #+10**(-8)

# Step through "time", calculating the partial derivatives at the current point
# and using them to estimate the next point
for i in range(num_steps):
    x_dot, y_dot, z_dot = lorenz(xl[i], yl[i], zl[i], r=0.5) #, r=0.5
    xl[i + 1] = xl[i] + (x_dot * dt)
    yl[i + 1] = yl[i] + (y_dot * dt)
    zl[i + 1] = zl[i] + (z_dot * dt)

keep_iterating = True
j = 0
while j < (num_steps + 1) and keep_iterating:
  trajectory_difference = xl[j] - xs[j]
  if trajectory_difference > 1:
    print("Difference between trajectories were greater than 1 in this step:")
    print(j)
    keep_iterating = False
  j += 1

# Plot
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(xs, ys, zs, lw=0.5, color="red")
ax.plot(xl, yl, zl, lw=0.5, color="green")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")

plt.show()


def bifurcation_diagram(seed, n_skip, n_iter, step=0.0001, r_min=0, r_max=0):
    print("Starting with x0 seed {0}, skip plotting first {1} iterations, then plot next {2} iterations.".format(seed, n_skip, n_iter));
    # Array of r values, the x axis of the bifurcation plot
    R = []
    # Array of x_t values, the y axis of the bifurcation plot
    X = []
    Y = []
    Z = []
    
    dt = 0.01
    # Create the r values to loop. For each r value we will plot n_iter points
    r_range = np.linspace(r_min, r_max, int(1/step))

    for r in r_range:
        x = seed
        y = seed
        z = seed
        # For each r, iterate the logistic function and collect datapoint if n_skip iterations have occurred
        for i in range(n_iter+n_skip+1):
            if i >= n_skip:
                R.append(r)
                X.append(x)
                Y.append(y)
                Z.append(z)
                
            x_dot, y_dot, z_dot = lorenz(x, y, z, r=r) #, r=0.5
            x += x_dot*dt
            y += y_dot*dt
            z += z_dot*dt
            #x = logistic_eq(r,x)
    # Plot the data    
    plt.figure()
    plt.plot(R, X, ls='', marker=',', color="blue")
    plt.xlim(r_min, r_max)
    plt.xlabel('r')
    plt.ylabel('X')    
    plt.figure()
    plt.plot(R, Y, ls='', marker=',', color="red")
    plt.xlim(r_min, r_max)
    plt.xlabel('r')
    plt.ylabel('Y')    
    plt.figure()
    plt.plot(R, Z, ls='', marker=',', color="green")
    plt.xlim(r_min, r_max)
    plt.xlabel('r')
    plt.ylabel('Z')
    plt.show()


# In[ ]:

#bifurcation_diagram(1, 0, 10000, r_min=0.5, r_max=28)