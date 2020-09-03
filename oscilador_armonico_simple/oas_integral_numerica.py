#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 13:01:15 2020

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, ode

# parametros

# parametros del sistema
m     = 2.              # inercia
k     = 1 / 8e-6        # elasticidad
b     = 2               # disipacion
F_ext = 0.0             # \_ amplitud y frecuencia del forzante
w_ext = 240.0           # /

# condiciones iniciales
y0 = [0.0, 0.0]         # posicion y momento iniciales

# coordenadas temporales para la solucion de la ecuación diferencial
t  = np.linspace(0, 10, 1000000)

# parametros derivados
gamma = b / m
w0    = np.sqrt(k/m)
w0_sq = k / m

# defino la derivada temporal del sistema que quiero integrar
def dy(y, t, gamma, w0, F_ext, w_ext):
    """
    El lado derecho de la ecuación diferencial: definimos coordenadas x
    (posicion) y p (momento lineal). Las ecuaciones son:
        dx / dt = p
        dv / dt = -gamma*v - w0_sq*x + F_ext(t)
    """
    x, v = y[0], y[1]
    
    dx = v
    dv = -v*gamma - x*w0**2 + F_ext*np.cos(w_ext*t)

    return [dx, dv]

y1 = odeint(dy, y0, t, args=(gamma, w0, F_ext, w_ext))


fig, ax = plt.subplots(2,1)

ax[0].plot(t, y1[:,0])
ax[1].plot(t, y1[:,1])





 



