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


fn = glob.glob("/net/fs08/d0/bire/mitgcm/enceladus_oceananigans/enceladus_expt16/run*/icy_moon_long_channel_particles.nc")

ds = xr.open_mfdataset(fn, decode_times=False)

particles = ds.particle_id.values
time = ds.time.values

z = ds.z.values
y = ds.y.values

is_z_gt_threshold = (z > threshold_z)

# the following ymin and ymax gives us three ranges: -400km to -100km, -100km to 100km, and 100km to 400km
ymins, ymaxs = [-400000, -100000, 100000], [-100000, 100000, 400000] # in meters

colors = ['k', 'r', 'b']

fig, ax = plt.subplots(1,1, figsize=(6,5))

for ymin, ymax, c in zip(ymins, ymaxs, colors):
    is_initial_y_in_range = (y[0,:] < ymax) & (y[0,:] > ymin)
    particles_cross_threshold_and_in_range = np.any(is_z_gt_threshold & is_initial_y_in_range, axis=0)

    z_particles_that_cross_threshold = z[:, particles_cross_threshold_and_in_range]

    time_particles_cross_threshold_and_in_range = np.argmax(z_particles_that_cross_threshold > threshold_z, axis=0)

    particles_in_range = particles[particles_cross_threshold_and_in_range]
    times_in_range = time[time_particles_cross_threshold_and_in_range]/rotation_period_Enceladus
    mean_transit_time = np.mean(times_in_range)
    median_transit_time = np.median(times_in_range)

    ax.hist(times_in_range, histtype='step', label=f'{ymin/1000} to {ymax/1000}km', color=c, linewidth=2)
    ax.axvline(x=mean_transit_time, color=c, linestyle='-', linewidth=2)
    ax.axvline(x=median_transit_time, color=c, linestyle='--', linewidth=2)

ax.set_xlabel('Transit time (rot. periods)')
ax.set_ylabel('Number of particles')
ax.legend()
fig.savefig(f'transit_hist.png', bbox_inches='tight', dpi=150)
