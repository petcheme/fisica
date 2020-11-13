#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 20:38:08 2020

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt

# -- parametros

# amplitudes en x e y, no son los semiejes!
Ax  = 5
Ay  = 10

# desfasaje
phi = np.arctan(4/3)
epsilon = np.pi/2 - phi

# epsilon = 2              


# -- comienzan los calculos

# cálculo del angulo de inclinacion alpha
tan2a = 2*Ax*Ay/(Ax**2 - Ay**2) * np.cos(epsilon)
alpha = 0.5*np.arctan(tan2a)

alpha_deg = alpha / np.pi *180

# matriz de rotacion: 
R = np.array(((np.cos(-alpha), -np.sin(-alpha)),
              (np.sin(-alpha), np.cos(-alpha))))

# parte vectorial del campo eléctrico
E0 = np.array((Ax, Ay*np.exp(1j*epsilon)),ndmin=2).T

# elimino la inclinación de la elipse aplicando una rotacion en -alpha:
E0_rot = np.matmul(R, E0)

# resultados
semieje_a = np.abs(E0_rot[0])
semieje_b = np.abs(E0_rot[1])
np.angle(E0_rot[0])
np.angle(E0_rot[1])

np.angle(E0_rot[1]) - np.angle(E0_rot[0])


# -- graficos

# vamos a graficar la elipse
# MUY IMPORTANTE: acomodar a mano la escala para asegurar una correcta visualización
# - que ángulos rectos se vean como ángulos rectos
# - ídem círculos
fig, ax = plt.subplots()

rotacion = np.exp(1j*np.linspace(0,np.pi*2,200))
ax.plot(Ax*np.real(rotacion),
        Ay*np.real(rotacion*np.exp(1j*epsilon)))

rr = 2
angulos = np.linspace(min(0,alpha),max(alpha,0),200)
ax.plot(rr*np.cos(angulos), rr*np.sin(angulos))

ax.plot((0,semieje_a*np.cos(alpha)),
        (0,semieje_a*np.sin(alpha)))

ax.plot((0,semieje_b*np.cos(alpha + np.pi/2)),
        (0,semieje_b*np.sin(alpha + np.pi/2)))

ax.plot((-Ax,Ax),(0,0),linestyle='--',color='lightgray')
ax.plot((0,0),(-Ay,Ay),linestyle='--',color='lightgray')

ax.set_title(alpha_deg)
