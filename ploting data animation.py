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
#% matplotlib qt

Omega_Europa = 2.1e-5  # Rotation rate [1/rad]
rotation_period_Europa = 2*pi / Omega_Europa  # [s]

f = 'C:/Users/Anika Nath/MIT/1st UROP/Particle 0 y-position vs. z-position.gif'
fn = 'C:/Users/Anika Nath/MIT/1st UROP/icy_moon_long_channel_particles.nc'
ds = nc.Dataset(fn)

particle_id = ds['particle_id'][:]
num_particles = len(particle_id)


#x = ds['x'][:, i]
#y = ds['x'][:]

x1,y1,y2,y3 = [], [], [], []


#plt.ylim(-19750, -19650)]

for i in range(1):
    y = ds['y'][:, i]
    z = ds['z'][:, i]
        
    fig, axes = plt.subplots(nrows = 1, ncols = 1, figsize = (15,5))
    #axes.set_ylim(-20, -16.800)
    #axes.set_xlim(277.220, 278)
    plt.style.use("ggplot")
    x1,y1 = [], []
    
    def animate(n):
        x1.append((y[n]/1000))
        y1.append((z[n]/1000))    
        axes.plot(x1, y1, color="red")
        
        t = ds['time'][n] / rotation_period_Europa
        axes.set_title(f'Icy moon particle trajectory: t = {t:.1f} rotation periods')
        # axes.set_title('Y-position vs. z-position of a particle in the ocean of a generic icy moon over 2.7 billion seconds (about 2604 years)')
    
    axes.set_xlabel('Y (km)')
    axes.set_ylabel('Z (km)')
    anim = FuncAnimation(fig, animate, frames=range(300), interval=30)
    
    #anim.title('Particle 0 y-position vs. z-position')
    #anim.xlabel('Y (meters')
    #anim.ylabel('Z (meters)')
    
    writergif = animation.PillowWriter(fps=3) 
    anim.save (f, writer=writergif)
    
    plt.show()