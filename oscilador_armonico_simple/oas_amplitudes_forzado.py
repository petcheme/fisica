# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
Amplitudes para la solucion particular de un oscilador armonico simple
amortiguado, forzado por una fuerza armonica simple

"""

""" 1. parametros """

# parametros del sistema


m = 2.          # masa
k = 1 / 8e-6    # constante elastica
b = 20          # coef disipacion

Fext = 1        # amplitud fuerza externa

n_puntos = 1000
wext = np.linspace(100, 400, n_puntos)




""" 2. solucion """

#-- parametros derivados
a0    = Fext / m                # aceleracion del forzante
gamma = b / m                   # disipacion por unidad de masa
w0_sq = k / m                   # constante elastica por unidad de masa

dif_w_sq    = w0_sq - wext**2 
denominador = dif_w_sq**2 + (wext*gamma)**2

A = a0 * (dif_w_sq)   / denominador
B = a0 * wext * gamma / denominador 

# --- grafico 1

fig, ejes = plt.subplots()

ejes.plot(wext, A, label = 'A, en fase, elastica')
ejes.plot(wext, B, label = 'B, en cuadratura, absorbente')
plt.xlabel('b (Ns/m)')
plt.ylabel('Amplitud (m)')

plt.legend()
plt.show()

# fig, ejes2 = plt.subplots()

# ejes2.plot(wext, B / A, label = 'B / A')

# plt.legend()
# plt.show()



