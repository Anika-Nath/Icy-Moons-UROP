# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:08:05 2022
@author: Anika Nath
"""
import numpy as np
import xarray as xr
import glob
import matplotlib.pyplot as plt

threshold_z = -1000

fn = glob.glob("C:/Users/Anika XPS13/1st UROP/run*/icy_moon_long_channel_particles_sim12.nc")

ds = xr.open_mfdataset(fn, decode_times=False)

Omega_Enceladus = ds.attrs['rotation_rate']  # Rotation rate [1/rad]
rotation_period_Enceladus = 2*np.pi / Omega_Enceladus # [s]

def compute_y_displacement_with_y_bounds(ds, y_min, y_max, threshold_z=-1000):
    particles = ds.particle_id.values
    time = ds.time.values

    y = ds.y.values
    z = ds.z.values
    y_initial = ds['y'][0, :]
    
    indices_to_keep = (y_min <= y_initial) & (y_initial <= y_max)
    
    z = z[:, indices_to_keep]
    y = y[:, indices_to_keep]
    y_initial = y_initial[indices_to_keep]
    
    is_z_gt_threshold = (z > threshold_z)
    particles_cross_threshold = np.any(is_z_gt_threshold, axis=0)

    n_particles = y.shape[1]
    
    y_final = np.array([y[particles_cross_threshold[n], n] for n in range(n_particles)])
    
    z_particles_that_cross_threshold = z[:, particles_cross_threshold]

    time_particles_cross_threshold = np.argmax(z_particles_that_cross_threshold > threshold_z, axis=0)
    
    particles = particles[particles_cross_threshold]
    times = time[time_particles_cross_threshold]/rotation_period_Enceladus

    return [y_final - y_initial, times]

interval=300
km=1000

fig, ax = plt.subplots(1,1, figsize=(6,5))
for i, j in zip(range(-400000, 400000, interval * km), range(100, 330, 100)):
    if j == 200:
        interval = 200
    result = compute_y_displacement_with_y_bounds(ds, i, i + interval * km)
    '''if j >= 301:
        plt.subplot("%i" % (j + 10))
    else:
        plt.subplot("%i" % j)'''
    y_displacement_middle = result[0]
    times = result[1]
    
    ax.hist(times)
    ax.set_title('Transit Times for Simulation 12')
    ax.set_xlabel('Transit time (rot. periods)')
    ax.set_ylabel('Number of particles')
    fig.savefig('transit_hist_sim12_w_bounds.png', bbox_inches='tight', dpi=150)
