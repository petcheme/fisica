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
wext = 200      # frecuencia fuerza externa

n_ciclos = 10
t_min    = 0
t_max    = 2 * np.pi / wext * n_ciclos        # 10 ciclos exactos de oscilacion
n_puntos = n_ciclos*100                       # cuantos samples por ciclo


""" 2. solucion particular """

#-- parametros derivados
a0    = Fext / m                # aceleracion del forzante
gamma = b / m                   # disipacion por unidad de masa
w0_sq = k / m                   # constante elastica por unidad de masa

dif_w_sq    = w0_sq - wext**2 
denominador = dif_w_sq**2 + (wext*gamma)**2

A = a0 * (dif_w_sq)   / denominador
B = a0 * wext * gamma / denominador 

""" --- 3. graficos """

eje_t = np.linspace(t_min, t_max, n_puntos)
eje_x = A*np.cos(wext*eje_t) + B*np.sin(wext*eje_t)

ejes = plt.subplot(3,1,1)

ejes.plot(eje_t, Fext*np.cos(wext*eje_t), label='Fext')
plt.legend()

ejes2 = plt.subplot(3,1,2)
ejes2.plot(eje_t, eje_x, label = 'x(t)')

plt.legend()
plt.show()

