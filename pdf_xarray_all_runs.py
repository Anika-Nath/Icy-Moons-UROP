# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:08:05 2022

@author: Anika Nath
"""
import numpy as np
import xarray as xr
import glob
import matplotlib.pyplot as plt
import string

threshold_z = -1000

# # the following ymin and ymax gives us three ranges: -400km to -100km, -100km to 100km, and 100km to 400km
ymins, ymaxs = [-400000, -100000, 100000], [-100000, 100000, 400000] # in meters
colors = ['k', 'r', 'b']

expt_names = ["15", "17", "21", "14", "18", "20", "13_2", "16", "19", "13_diff", "16_diff", "19_diff"]

fns = []
for name in expt_names:
    fn = glob.glob("/net/fs08/d0/bire/mitgcm/enceladus_oceananigans/enceladus_expt" + name + "/run*/icy_moon_long_channel_particles.nc")
    fns.append(fn)

fig, ax = plt.subplots(4,3, figsize=(12,10))

eq_means = []
sh_means = []
nh_means = []
meanarrays = [sh_means, eq_means, nh_means]

eq_std = []
sh_std = []
nh_std = []
stdevarrays = [sh_std, eq_std, nh_std]

rostararray = []

markers = ['$\\boxplus$', '$\\oplus$', '$\\otimes$',  '$+$', '$\\dagger$', '$\\times$', '$\\circ$', '$\\triangleleft$', '$\\triangleright$', '$\\bullet$', '$\\blacktriangleleft$', '$\\blacktriangleright$']

itermarker = iter(markers)
iterlabel = iter(string.ascii_lowercase)

for i, (axc, fn) in enumerate(zip(ax.ravel(), fns)):
    print(i)
    ds = xr.open_mfdataset(fn, decode_times=False)
    rostararray.append(ds.attrs['natural_rossby_number'])
    rotation_period = ds.attrs['rotation_period']

    particles = ds.particle_id.values
    time = ds.time.values
    z = ds.z.values

    # # We first find only particles that cross the threshold and ignore all the other particles

    is_z_gt_threshold = (z > threshold_z)
    particles_cross_threshold = np.any(is_z_gt_threshold, axis=0)
    z = z[:, particles_cross_threshold]
    y = ds.y[:, particles_cross_threshold].values
    particles = particles[particles_cross_threshold]

    for ymin, ymax, c, meanarray, stdarray in zip(ymins, ymaxs, colors, meanarrays, stdevarrays):
        is_initial_y_in_range = (y[0,:] < ymax) & (y[0,:] > ymin)

        z_particles_that_cross_threshold = z[:, is_initial_y_in_range]

        time_particles_cross_threshold_and_in_range = np.argmax(z_particles_that_cross_threshold > threshold_z, axis=0)

        particles_in_range = particles[is_initial_y_in_range]
        times_in_range = time[time_particles_cross_threshold_and_in_range]/rotation_period
        mean_transit_time = np.mean(times_in_range)
        std_transit_time = np.std(times_in_range)
        first_quartile, median_transit_time, third_quartile = np.percentile(times_in_range,[25,50,75])
        print(mean_transit_time, std_transit_time, median_transit_time, first_quartile, third_quartile)
        meanarray.append(mean_transit_time)
        stdarray.append(std_transit_time)

        axc.hist(times_in_range, histtype='step', label=f'{ymin/1000} to {ymax/1000}km', color=c, linewidth=2)
        axc.axvline(x=mean_transit_time, color=c, linestyle='-', linewidth=2)
        axc.axvline(x=median_transit_time, color=c, linestyle='--', linewidth=2)
    axc.set_title('(' + next(iterlabel) + ') ' + next(itermarker))

    ds.close()


for axc in ax[-1,:]:
    axc.set_xlabel('Transit time (rot. periods)')
for axc in ax[:,0]:
    axc.set_ylabel('Number of particles')
ax[0,0].legend()
fig.tight_layout()
fig.savefig(f'transit_hist_all_expts.png', bbox_inches='tight', dpi=150)

std_mul = 1

fig, axs = plt.subplots(2,1, figsize=(5,6), sharex=True)
ax = axs[0]
for eqmn, eqstd, ro, marker in zip(eq_means, eq_std, rostararray, markers):
    # ax.plot(ro, eqmn, color='k', marker=marker)
    # ax.vlines(x=ro, ymin=eqmn-std_mul*eqstd, ymax=eqmn+std_mul*eqstd, color='k', linewidth=1)
    ax.errorbar(ro, eqmn, yerr=std_mul*eqstd, color='k', marker=marker)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel(r'Mean transit time (rot. periods)')
ax.set_title('Eq. partilces')
ax.grid()

ax = axs[1]
for nhmn, nhstd, ro, marker in zip(nh_means, nh_std, rostararray, markers):
    # ax.plot(ro, nhmn, color='r', marker=marker)
    # ax.vlines(x=ro, ymin=nhmn-std_mul*nhstd, ymax=nhmn+std_mul*nhstd, color='r', linewidth=1)
    ax.errorbar(ro, nhmn, yerr=std_mul*nhstd, color='r', marker=marker)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$Ro^{\ast}$')
ax.set_ylabel(r'Mean transit time (rot. periods)')
ax.grid()
ax.set_title('Polar partilces')
fig.savefig(f'rostar_vs_meantransit.png', bbox_inches='tight', dpi=150)

