# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:50:12 2021

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt

# parametros
n_modos = 10
n_masas = 10
L = 1.

# chequeos
n_modos = min(n_masas, n_modos)

# aca empieza la cosa
fig, ax = plt.subplots(nrows = n_modos, ncols = 3)

eje_x = np.linspace(0, L, num=1000)
eje_n = np.linspace(1, n_masas, n_masas)

# fijo-fijo
a = L / (n_masas+1)
for modo in np.arange(start=0, stop=n_modos, step=1):

    k = (modo+1)*np.pi/L
    ax[modo][0].plot(eje_x, np.sin(k*eje_x))
    ax[modo][0].scatter(eje_n*a, np.sin(k*a*eje_n))

ax[0][0].set_title('Fijo-fijo')

# fijo-libre    
a = L / (n_masas+0.5)
for modo in np.arange(start=0, stop=n_modos, step=1):

    k = (modo+0.5)*np.pi/L
    ax[modo][1].plot(eje_x, np.sin(k*eje_x))
    ax[modo][1].scatter(eje_n*a, np.sin(k*a*eje_n))
    
ax[0][1].set_title('Fijo-libre')
    
# libre-libre    
a = L / n_masas
for modo in np.arange(start=0, stop=n_modos, step=1):

    k = modo*np.pi/L
    ax[modo][2].plot(eje_x, np.cos(k*eje_x))
    #ax[modo][2].scatter((eje_n - 0.5)*a, np.cos(k*(eje_n - 0.5)*a))
    
    kp = modo*np.pi/a/n_masas
    ax[modo][2].scatter((eje_n - 0.5)*a, np.cos(kp*(eje_n - 0.5)*a))
    
    # comparacion con matriz de autovectores
    # obtenida previamente mediante linalg.eig
#    autovector = A[:,modo]
#    autovector = autovector / autovector[0] * np.cos(kp*(1 - 0.5)*a)
#    ax[modo][2].scatter((eje_n - 0.5)*a, autovector)
    
ax[0][2].set_title('Libre-libre')
