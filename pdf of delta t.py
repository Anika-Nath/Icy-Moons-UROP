# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:08:05 2022

@author: Anika Nath
"""
import matplotlib.pyplot as plt
import netCDF4 as nc
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from math import pi
import numpy as np
#% matplotlib qt

Omega_Europa = 2.1e-5  # Rotation rate [1/rad]
rotation_period_Europa = 2*pi / Omega_Europa  # [s]

f = 'C:/Users/Anika XPS13/1st UROP/Particle 0 y-position vs. z-position.gif'
fn = 'C:/Users/Anika XPS13/1st UROP/icy_moon_long_channel_particles.nc'
ds = nc.Dataset(fn)

particle_id = ds['particle_id'][:]
num_particles = len(particle_id)

def transit_time(particle_num, threshold_z=-1000):
    z = ds['z'][:, particle_num]
    
    return ds['time'][np.argmax(z > threshold_z)]
'''
    for i in range(len(z)):
        if z[i] > threshold_z:
            return ds['time'][i]
    return None
'''

'''
def compute_transit_times(ds, threshold_z=-100):
    z = ds['z'][:, :]
    y_array = ds['y'][:, :]
    y_initial = ds['y'][0, :]
    max_y = max(y_initial)
    min_y = min(y_initial)
    group_interval = (max_y - min_y)/3
    num_groups = (max_y - min_y)/group_interval
    7 3 9 4 2 11 0 y-value to split - sample data
    group_interval=4
    num_groups=
    should be 0 2 3 group 1   4 7 groupp 2    9 11 group 3
    
    use to ffigure algorithm
    y_displacement = []
    for i in range(num_particles):
        y_displacement.append(y_array[i, num_particles] - y_array[i, 0])
    print(np.shape(y))
    print(y)
    
    threshold_indices = np.argmax(z > threshold_z, axis=0)
    transit_times = y_displacement[threshold_indices]
    return transit_times
'''

def compute_transit_times(ds, threshold_z=-1000):
    t = ds['time'][:]
    z = ds['z'][:, :]
    
    threshold_indices = np.argmax(z > threshold_z, axis=0)
    transit_times = t[threshold_indices]
    return transit_times

def compute_transit_times_with_y_bounds(ds, y_min, y_max, threshold_z=-1000):
    t = ds['time']
    z = ds['z'][:, :]
    y_initial = ds['y'][0, :]
    print(y_min, y_max, y_initial)

    indices_to_keep = (y_min <= y_initial) & (y_initial <= y_max)
    '''count = 0
    for i in indices_to_keep:
        if i:
            count += 1
    print('c', count)'''
    z = z[:, indices_to_keep]
    
    threshold_indices = np.argmax(z > threshold_z, axis=0)
    transit_times = t[threshold_indices]
    return transit_times

# transit_times = [float(transit_time(n)) for n in range(60)]
transit_times = compute_transit_times(ds)
transit_times_in_rp = transit_times / rotation_period_Europa

plt.hist(transit_times_in_rp, bins=50, density=True)
plt.xlabel("transit time (rotation periods)")
plt.ylabel("Probability density")
plt.savefig("transit_time_probability_distribution.png", dpi=300)

km = 1000
y_min = int(min(ds['y'][0, :]))
y_max = int(max(ds['y'][0, :]))
print(y_min, y_max)
for i, j in zip(range(-400, 400, 50), range(111, 1000, 10)):
    transit_times_middle = compute_transit_times_with_y_bounds(ds, i*km, (i + 50)*km) / rotation_period_Europa
    print("%i" % (j + 10))
    '''if j >= 201:
        plt.subplot("%i" % (j + 10))
    else:
        plt.subplot("%i" % j)'''
    plt.subplot(311)
    plt.hist(transit_times_middle, bins=75, density=True)
    plt.title("from y = %i km" % i)
    plt.xlabel("transit time (rotation periods)")
    plt.savefig("testing_transit_times -400 to 400.png", dpi=300)
    #plt.savefig("testing_transit_times%i.png" %i, dpi=300)
    

'''
transit_times_top = compute_transit_times_with_y_bounds(ds, -300*km, -250*km) / rotation_period_Europa


plt.subplot("122")
plt.hist(transit_times_top, bins=75, density=True)
plt.title("300 km < y < 350 km")
plt.xlabel("transit time (rotation periods)")

plt.savefig("testing_transit_times.png", dpi=300)'''
