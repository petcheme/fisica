#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:52:59 2020

@author: petcheme
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

""" 1. Parametros y definicion de funciones """
c1 = 1              # velocidad de propagacion medio 1
c2 = 3              # velocidad de propagacion medio 2
L  = 1              # longitud completa de la cuerda
alpha = .2          # fracción de la cuerda donde se encuentra la interface

L1 = alpha*L        # longitud del lado izquierdo
L2 = L - L1         # longitud del lado derecho

# valores de k2 que voy a probar
k2_prueba = np.linspace(start=0, stop=50, num=2000)

epsilon = 1e-1      # parametro de comparacion para buscar candidatos

max_candidatos = 20 # parametro para controlar la cantidad de casos que voy a resolver

# defino las funciones de la ecuación que debo resolver:
#
#           f1(k2) = f2(k2)

def f1(k2,L2):
    return np.tan(k2*L2)
    
def f2(k2,L1,c1,c2):
    return -c1 / c2 *np.tan(c2/c1 *k2*L1)

# ecuacion del problema: f1(k2) - f2(k2) = 0
def my_func(k2,L1,L2,c1,c2):
    return f1(k2,L2) - f2(k2,L1,c1,c2)

# version tomando valor absoluto
def my_func_abs(k2,L1,L2,c1,c2):
    return np.abs(f1(k2,L2) - f2(k2,L1,c1,c2))


""" 2. Mi primer objetivo es encontrar valores candidatos """

# evaluo las funciones y las guardo para no volver a evaluarlas
f1_valores = f1(k2_prueba, L2)
f2_valores = f2(k2_prueba, L1, c1,c2)
dif_abs    = np.abs(f1_valores - f2_valores)

comparacion = np.where(dif_abs < epsilon)[0]


# según el valor de epsilon tomado, puedo tener candidatos consecutivos, los agrupo
def agrupar_consecutivos(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

comparacion_grupos = agrupar_consecutivos(comparacion)

# ahora me quedo con un valor de k2 por cada grupo
k2_candidatos = np.zeros(len(comparacion_grupos))
for i in np.arange(0, len(comparacion_grupos)):
    k2_candidatos[i] = k2_prueba[comparacion_grupos[i][0]]


# abro la figura y los ejes
fig_prueba = plt.figure()
ax_prueba  = plt.axes()

# grafico f1 y f2, uso scatter para que las asíntotas verticales no me embarren la gráfica
my_alpha = 1   # \_ parametros para mejorar la visualizacion
my_ylim  = 5    # /
ax_prueba.scatter(k2_prueba, f1_valores, label='f1', s=5, alpha=my_alpha)
ax_prueba.scatter(k2_prueba, f2_valores, label='f2', s=5, alpha=my_alpha)
ax_prueba.scatter(k2_prueba[comparacion], f2_valores[comparacion], label='candidatos', s=50)
ax_prueba.set_xlabel('k2')
ax_prueba.set_ylabel('f')
ax_prueba.legend()

plt.title('Ajustar \'epsilon\' o la cantidad de valores de k2 hasta que la cantidad de candidatos coincida con\nlas intersecciones que muestra el gráfico')
plt.ylim(-my_ylim, my_ylim)

""" 3. Ahora que tengo mis candidatos, refino los valores """

for i in np.arange(0, np.min((len(comparacion_grupos), max_candidatos))):

    print('Candidato ' + str(i+1) + ': ')
    
    # resuelvo el problema
    resultado = scipy.optimize.minimize(fun=my_func_abs, x0=k2_candidatos[i], args=(L1,L2,c1,c2), method='Nelder-Mead')
    delta = np.abs(k2_candidatos[i] - resultado.x[0])
    
    # salida en pantalla
    print(resultado)
    print('Optimización: ' + '{:f}'.format(k2_candidatos[i]) + ' -> ' + '{:f}'.format(resultado.x[0]))
    print('Diferencia: ' + '{:f}'.format(delta))

    # gráfico
    fig_candidato = plt.figure()
    ax_candidato  = plt.axes()

    beta = 10
    k2_rango = np.linspace(start= min(k2_candidatos[i], resultado.x[0]) - beta*delta, \
                            stop = max(k2_candidatos[i], resultado.x[0]) + beta*delta, \
                            num = 1000)
    
    ax_candidato.scatter(k2_rango, f1(k2_rango, L2),      label='f1', s=5)
    ax_candidato.scatter(k2_rango, f2(k2_rango,L1,c1,c2), label='f2', s=5)
    ax_candidato.axvline(k2_candidatos[i])
    ax_candidato.axvline(resultado.x[0])
    
    
    ax_candidato.set_xlabel('k2')
    ax_candidato.set_ylabel('f')
    ax_prueba.legend()
    
    plt.title('Candidato ' + str(i+1))
    # plt.ylim(-my_ylim, my_ylim)
    plt.show()

    
    print('')
    

