#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:50:06 2020

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt

""" matrix definitions """

def rot(x=0):   # rotation matrix
    return np.array( ((np.cos(x), -np.sin(x)),
                      (np.sin(x),  np.cos(x))) )
    
def lp(x=0):    # linear polarizer
    return np.matmul(rot(x), 
           np.matmul(np.array( ((1, 0), (0, 0)) ),
                     rot(-x)))
    
def qw(x=0):    # quarter-wave plate
    return np.matmul(rot(x), 
           np.matmul(np.array( ((1, 0), (0, 1j)) ),
                     rot(-x)))

def hw(x=0):    # half-wave plate
    return np.matmul(rot(x), 
           np.matmul(np.array( ((1, 0), (0, -1)) ),
                     rot(-x)))

""" demo """

alpha = np.pi/12
theta = np.pi/3
phi   = theta - alpha

# quarter-wave plate applied to elliptical state

# half-axes and coordinate system are coincident 
J0     = np.array(((2),(1j)), ndmin=2).T / np.sqrt(5)
J1     = np.matmul(hw(theta - alpha), J0)

# half-axes with inclination alpha
J0_rot = np.matmul(rot(alpha), J0)
J1_rot = np.matmul(hw(theta), J0_rot)


""" graphics """

# first plot: electric field trajectory in polarization plane

fig, ax = plt.subplots(ncols=2)

# oscillatory factor
phases  = np.linspace(start=0,stop=np.pi*2,num=200)     # full cycle
osc_exp = np.exp(1j*phases)

# plots and settings
ax[0].plot(np.real(osc_exp*J0[0]),
           np.real(osc_exp*J0[1]), label='J0')

ax[0].plot(np.real(osc_exp*J1[0]),
           np.real(osc_exp*J1[1]), label='J1')

ax[0].set_xlim((-2,2))
ax[0].set_ylim((-2,2))
ax[0].legend()

ax[1].plot(np.real(osc_exp*J0_rot[0]),
           np.real(osc_exp*J0_rot[1]), label='J0_rot')

ax[1].plot(np.real(osc_exp*J1_rot[0]),
           np.real(osc_exp*J1_rot[1]), label='J1_rot')

ax[1].set_xlim((-2,2))
ax[1].set_ylim((-2,2))
ax[1].legend()

# hard-coded axis size
figw =6.56
figh =3
ax[0].figure.set_size_inches(figw, figh)
bbox = ax[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
width, height = bbox.width, bbox.height
width *= fig.dpi
height *= fig.dpi

# references
ax[0].axvline(0,color='lightgray')
ax[0].axhline(0,color='lightgray')
ax[1].axvline(0,color='lightgray')
ax[1].axhline(0,color='lightgray')

xx = np.linspace(-2,2, num=200)
yy = xx*np.tan(alpha)
ax[1].plot(xx,yy,color='lightgray')
# ax[0].axline((0,0), slope=np.tan(alpha))

xx = np.linspace(-2,2, num=200)
yy = -xx/np.tan(alpha)
ax[1].plot(xx,yy,color='lightgray')
# ax[0].axline((0,0), slope=-1/np.tan(alpha))


# second plot: jones vectors in complex plane

fig2, ax2 = plt.subplots(ncols=2)

ax2[0].plot((0, np.real(J0[0]) [0]),
            (0, np.imag(J0[0]) [0]), color='royalblue')
ax2[0].plot((0, np.real(J0[1]) [0]),
            (0, np.imag(J0[1]) [0]), color='royalblue', linestyle='--')

ax2[0].plot((0, -np.real(J1[0]) [0]),
            (0, -np.imag(J1[0]) [0]), color='orange')
ax2[0].plot((0, -np.real(J1[1]) [0]),
            (0, -np.imag(J1[1]) [0]), color='orange', linestyle='--')

ax2[1].plot((0, np.real(J0_rot[0]) [0]),
            (0, np.imag(J0_rot[0]) [0]), color='royalblue')
ax2[1].plot((0, np.real(J0_rot[1]) [0]),
            (0, np.imag(J0_rot[1]) [0]), color='royalblue', linestyle='--')

ax2[1].plot((0, np.real(J1_rot[0]) [0]),
            (0, np.imag(J1_rot[0]) [0]), color='orange')
ax2[1].plot((0, np.real(J1_rot[1]) [0]),
            (0, np.imag(J1_rot[1]) [0]), color='orange', linestyle='--')
            




