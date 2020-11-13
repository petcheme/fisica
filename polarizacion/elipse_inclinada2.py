#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 10:36:26 2020

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt

# defino una matriz cuyos semiejes coinciden con los ejes de coordenadas
# Sa   = 10
# Sb   = 5
Sa   = 2.8
Sb   = 10.8
fase = np.pi/2      # cambiar el signo segun el sentido de giro deseado (horario o antihorario)

# armo un vector columna con la parte vectorial del campo eléctrico
E = np.array((Sa, Sb*np.exp(1j*fase)), ndmin=2).T

# voy a rotar la elipse un ángulo alpha
# alpha = 0.4
alpha = 0.5*np.arctan(-4/3*np.cos(np.pi/2-np.arctan(4/3)))

# para eso empleo la tradicional matriz de rotacion en R^2
R = np.array(((np.cos(alpha), -np.sin(alpha)),
              (np.sin(alpha), np.cos(alpha))))

# obtengo el estado rotado aplicando la matriz al vector
E_rot = np.matmul(R, E)

# Obtengo las amplitudes Ax y Ay del estado rotado
Ax = np.abs(E_rot[0])
Ay = np.abs(E_rot[1])
# Obtengo el desfasaje entre dichas componentes
epsilon = np.angle(E_rot[1]) - np.angle(E_rot[0])

# obtengo alpha mediante la formula del hecht
tan2a = 2*Ax*Ay/(Ax**2 - Ay**2)*np.cos(epsilon)
alpha_hecht = 0.5*np.arctan(tan2a)

# uso la otra formula
tan2a = 2*Ax*Ay/(Ax**2 + Ay**2)*np.cos(epsilon)
alpha_3 = 0.5*np.arctan(tan2a)

# -- graficos
fig, ax = plt.subplots()

# para graficar, voy a definir un vector que exprese una oscilación completa
# (es decir de tamaño 2pi) mediante una exponencial compleja
oscilacion = np.exp(-1j*np.linspace(0, 2*np.pi, 200))               # el signo menos se debe a que el tiempo va como exp(-1j*omega*t)

# grafico mi elipse original (sin rotar)
ax.plot(np.real(Sa*oscilacion), np.real(Sb*oscilacion*np.exp(1j*fase)))

# grafico la elipse rotada
ax.plot(np.real(Ax*oscilacion), np.real(Ay*oscilacion*np.exp(1j*epsilon)))

# para estar seguros, agrego los semiejes a la elipse rotada
ax.plot((0,Sa*np.cos(alpha)), (0,Sa*np.sin(alpha)))
ax.plot((0,Sb*np.cos(alpha + np.pi/2)), (0,Sb*np.sin(alpha +np.pi/2)))

# para estar mas seguros, agrego un arco de circulo que indica el ángulo de rotacion
radio = 2
angulo = np.linspace(min(0, alpha_hecht), max(0,alpha_hecht), 200)
ax.plot(radio*np.cos(angulo), radio*np.sin(angulo))

# además agrego los ejes de referencia
plt.plot((-Ax, Ax),(0,0),color='lightgray',linestyle='--')
plt.plot((0,0),(-Ay, Ay),color='lightgray',linestyle='--')

# por último, agrego la caja que enmarca a la elipse rotada
plt.plot((-Ax,Ax,Ax,-Ax,-Ax),(-Ay,-Ay,Ay,Ay,-Ay))

