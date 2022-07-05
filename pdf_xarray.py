# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:08:05 2022

@author: Anika Nath
"""
import numpy as np
import xarray as xr
import glob
import matplotlib.pyplot as plt

Omega_Enceladus = 5.3e-5  # Rotation rate [1/rad]
rotation_period_Enceladus = 2*np.pi / Omega_Enceladus # [s]
threshold_z = -1000
ymax, ymin = 100000, -100000 # in meters

fn = glob.glob("/net/fs08/d0/bire/mitgcm/enceladus_oceananigans/enceladus_expt16/run*/icy_moon_long_channel_particles.nc")

ds = xr.open_mfdataset(fn, decode_times=False)

particles = ds.particle_id.values
time = ds.time.values

z = ds.z.values
y = ds.y.values

is_initial_y_in_range = (y[0,:] < ymax) & (y[0,:] > ymin)
is_z_gt_threshold = (z > threshold_z)
particles_cross_threshold_and_in_range = np.any(is_z_gt_threshold & is_initial_y_in_range, axis=0)

z_particles_that_cross_threshold = z[:, particles_cross_threshold_and_in_range]

time_particles_cross_threshold_and_in_range = np.argmax(z_particles_that_cross_threshold > threshold_z, axis=0)

particles = particles[particles_cross_threshold_and_in_range]
times = time[time_particles_cross_threshold_and_in_range]/rotation_period_Enceladus

fig, ax = plt.subplots(1,1, figsize=(6,5))
ax.hist(times)
ax.set_xlabel('Transit time (rot. periods)')
ax.set_ylabel('Number of particles')
fig.savefig('transit_hist.png', bbox_inches='tight', dpi=150)
