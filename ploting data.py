# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:08:05 2022

@author: Anika Nath
"""
import matplotlib.pyplot as plt
import netCDF4 as nc

fn = 'C:/Users/Anika Nath/MIT/1st UROP/icy_moon_long_channel_particles.nc'
ds = nc.Dataset(fn)

particle_id = ds['particle_id'][:]
num_particles = len(particle_id)

time = ds['time'][:]
#x = ds['x'][:, i]
#y = ds['x'][:]


#plt.ylim(-19750, -19650)

for i in range(num_particles):
    if i <= 16020:
        continue
    z = ds['z'][:, i]
    plt.plot(time, z)
    plt.title('Z Position of Particle %i Over Time' % i)
    plt.xlabel('Time (days)')
    plt.ylabel('Z (meters)')
    plt.savefig('Z Position of Particle %i Over Time.png' % i, bbox_inches='tight')
    plt.show()