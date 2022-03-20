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

f = 'C:/Users/Anika Nath/MIT/1st UROP/Particle 0 y-position vs. z-position.gif'
fn = 'C:/Users/Anika Nath/MIT/1st UROP/icy_moon_long_channel_particles.nc'
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
    return None'''

def compute_transit_times(ds, threshold_z=-1000):
    z = ds['z'][:, :]
    t = ds['time'][:]
    
    threshold_indices = np.argmax(z > threshold_z, axis=0)
    transit_times = t[threshold_indices]
    return transit_times

# transit_times = [float(transit_time(n)) for n in range(60)]
transit_times = compute_transit_times(ds)
transit_times_in_rp = transit_times / rotation_period_Europa

plt.hist(transit_times_in_rp, bins=50, density=True)
plt.xlabel("Rotation periods")
plt.ylabel("Probability density")
plt.savefig("transit_time_probability_distribution.png")
