# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:29:13 2021

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt


g  = 10.
l1 = .108
l2 = 1.
L  = 1.
c  = 1.                

A0 = 1.
omega_ext = 9.3 #3.5
tau_ext   = 2.*np.pi / omega_ext

# relacion de dispersion
eje_k = np.linspace(0, 10, num=1000)
fig, ax = plt.subplots()
ax.plot(eje_k, np.sqrt(g / l1 + c**2 *eje_k**2))
ax.plot(eje_k, np.sqrt(g / l1 - c**2 *eje_k**2))
ax.plot(eje_k, np.sqrt(g / l2 + c**2 *eje_k**2))
ax.plot(eje_k, np.sqrt(g / l2 - c**2 *eje_k**2))
ax.plot(eje_k, omega_ext + eje_k*0)

# ejes de posicion y de tiempo
eje_t = np.linspace(0, 3*tau_ext, num = 100)
eje_x1 = np.linspace(0, L,   num = 1000)
eje_x2 = np.linspace(L, 3*L, num = 2000)

if (l1 > l2):
    
    # hay que chequear tambien que la frecuencia externa sea menor que el
    # rango dispersivo de l2
    
    # numero de onda y atenuacion segun omega externo
    k     = np.sqrt(1/c**2 * (omega_ext**2 - g / l1))
    kappa = np.sqrt(1/c**2 * (g / l2 - omega_ext**2))
    
    # amplitudes de las soluciones
    C = A0 / (kappa/k*np.sin(k*L) + np.cos(k*L))
    B = C
    A = -C*kappa/k

    # perfiles espaciales
    A1 = A*np.sin(k*(eje_x1-L)) + B*np.cos(k*(eje_x1-L))
    A2 = C*np.exp(-kappa*(eje_x2-L))

    # figura de la solucion    
    fig2, ax2 = plt.subplots()
    ax2.plot(eje_x1, A1)
    ax2.plot(eje_x2, A2)
    
    # figura del coeficiente C en funcion del numero de onda
    fig3, ax3 = plt.subplots()
    ax3.plot(eje_k, A0 / (kappa/k*np.sin(eje_k*L) + np.cos(eje_k*L)))
    ax3.set_ylim((-10,10))
    ax3.set_xlim((9.1,9.2))

if (l1 < l2):
    
    # numero de onda y atenuacion segun omega externo
    k     = np.sqrt(1/c**2 * (omega_ext**2 - g / l2))
    kappa = np.sqrt(1/c**2 * (g / l1 - omega_ext**2))
    
    # resuelvo los coeficientes para mi solucion
    matrix = np.array(((np.exp(-kappa*L), np.exp(kappa*L),     0),
                       (               1,               1,    -1),
                       (           kappa,          -kappa, -k*1j)))
    
    vector = np.array((A0,0,0),ndmin=2).T
    
    resultado = np.matmul(np.linalg.inv(matrix), vector)
    
    B1 = resultado[0]
    B2 = resultado[1]
    C  = resultado[2]
    
    # perfiles espaciales
    A1 = B1*np.exp(kappa*(eje_x1 - L)) + B2*np.exp(-kappa*(eje_x1 - L))
    A2 = C*np.exp(1j*k*(eje_x2 - L))
    
    # figura de la solucion    
    
    fig2, ax2 = plt.subplots()

    factor_tiempo = np.exp(-1j*omega_ext*eje_t[0])
    ax2.plot(eje_x1, np.real(A1*factor_tiempo))
    ax2.plot(eje_x2, np.real(A2*factor_tiempo))
    
    factor_tiempo = np.exp(-1j*omega_ext*eje_t[5])
    ax2.plot(eje_x1, np.real(A1*factor_tiempo))
    ax2.plot(eje_x2, np.real(A2*factor_tiempo))

    factor_tiempo = np.exp(-1j*omega_ext*eje_t[10])
    ax2.plot(eje_x1, np.real(A1*factor_tiempo))
    ax2.plot(eje_x2, np.real(A2*factor_tiempo))
    