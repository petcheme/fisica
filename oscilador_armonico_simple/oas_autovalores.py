# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
Autovalores para un oscilador armonico simple amortiguado

"""

""" 1. parametros """

# parametros del sistema

m    = 2.           # masa
k    = 1 / 8e-6     # constante elastica

# coeficiente de disipacion variable
b_min    = 100      # disipacion minima, no puede ser 0
b_max    = 1500     # disipacion maxima
n_puntos = 10000    # cantidad de samples, debe ser entero

b = np.linspace(b_min, b_max, n_puntos)


""" 2. solucion """

#-- parametros derivados
gamma = b / m               # constante de amortiguamiento por unidad de masa
tau   = 2. / gamma          # tiempo caracteristico de decaimiento exponencial
w0    = np.sqrt(k/m)        # frecuencia angular natural del sistema, es decir,
                            # la frecuencia en ausencia de disipacion o fuerzas
                            # externas (aka frecuencia de resonancia)

f0 = w0 / 2. / np.pi        # frecuencia natural del sistema, np.pi es la
                            # representacion en punto flotante de la constante
                            # pi provista por la biblioteca numpy 


w = np.sqrt(k/m - tau**(-2) + 0*1j)
         
# recordar: 
# si w es real . . . . . . . . . . regimen sub-amortiguado
# si w es complejo puro. . . . . . regimen sobre-amortiguado
# si w es nulo . . . . . . . . . . regimen critico



# constantes de tiempo del sistema, cuando el sistema es sobreamortiguado, son
# valores reales, por lo que las exponenciales se convierten en terminos que
# decaen. cuando el sistema es subamortiguado, son valores con parte compleja
# no nula, por lo que las exponenciales se comportan como osciladores
# amortiguados.
lambda1  =  1j*w-1/tau
lambda2  = -1j*w-1/tau

""" 3. graficos """

# --- grafico 1

# muestro la parte real y compleja de omega en funcion de la disipacion
# este grafico me permite obtener el limite entre sub- y sobre-amortiguado
# ademas, dentro del regimen sub-amortiguado me permite comparar la frecuencia
# de oscilacion del sistema con la frecuencia de resonancia (w0) (faltaria
# agregar ese valor como referencia)

fig1, ax1 = plt.subplots(nrows=2, ncols=2)
fig1.set_size_inches(9, 6)

ax1[0,0].plot(b, np.real(w), label = 'Re(w)')
ax1[0,0].plot(b, np.imag(w), label = 'Im(w)')

ax1[0,0].set(ylabel = '$\omega$ [$s^{-1}$]')
ax1[0,0].legend()

# --- grafico 2

# muestro la parte imaginaria de lambda 1 y 2
ax1[0,1].plot(b, np.imag(lambda1), label = 'Im(lambda1)')
ax1[0,1].plot(b, np.imag(lambda2), label = 'Im(lambda2)')

ax1[0,1].legend()

# --- grafico 3

# muestro la constante de decaimiento tau, la cual nos da la tasa de perdida
# de energia en el regimen sub-amortiguado
ax1[1,0].plot(b, tau, linewidth = 1, label = 'tau')
ax1[1,0].set(xlabel = 'b [Ns/m]', ylabel = 'tau [s]')
ax1[1,0].legend()

# --- grafico 4

# muestro 1 sobre la parte real de lambda 1, dentro del regimen subamortiguado
# ambos valores corresponden a tau. en el regimen sobreamortiguado, ambas
# constantes de tiempo se bifurcan, dando lugar a un decaimiento lento y uno
# rapido

ax1[1,1].plot(b, -1/ np.real(lambda1), label = '1 / Re(lambda1) rapido')
ax1[1,1].plot(b, -1/ np.real(lambda2), label = '1 / Re(lambda2) lento')
ax1[1,1].plot(b, tau, '--', linewidth = 1, label = 'tau')                     # agrego como referencia tau

ax1[1,1].legend()
ax1[1,1].set(xlabel = 'b [Ns/m]')

# plt.legend()
plt.show()
