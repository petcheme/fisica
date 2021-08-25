#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:52:59 2020

@author: petcheme
"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import scipy.optimize

""" 1. Parametros y definicion de funciones """
c1 = 3.             # velocidad de propagacion medio 1
c2 = 1.             # velocidad de propagacion medio 2
L  = 1.             # longitud completa de la cuerda
alpha = 3. / 4.          # fracción de la cuerda donde se encuentra la interface

L1 = alpha*L        # longitud del lado izquierdo
L2 = L - L1         # longitud del lado derecho

# valores de k2 que voy a probar
k2_prueba = np.linspace(start=0, stop=160, num=20000)

epsilon = 1e-1      # parametro de comparacion para buscar candidatos

max_candidatos  = 8 # parametro para controlar la cantidad de casos que voy a resolver
plot_candidatos = False

# defino las funciones de la ecuación que debo resolver:
#
#           f1(k2) = f2(k2)

def f1(k2,L2):
    return np.tan(k2*L2)
    
def f2(k2,L1,c1,c2):
    return -c1 / float(c2) *np.tan(c2/c1 *k2*L1)

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
my_ylim  = 2.5    # /
ax_prueba.scatter(k2_prueba, f1_valores, label='f1', s=5, alpha=my_alpha)
ax_prueba.scatter(k2_prueba, f2_valores, label='f2', s=5, alpha=my_alpha)
ax_prueba.scatter(k2_prueba[comparacion], f2_valores[comparacion], label='candidatos', s=50)
ax_prueba.set_xlabel('k2')
ax_prueba.set_ylabel('f')
ax_prueba.legend()

plt.title('Ajustar \'epsilon\' o la cantidad de valores de k2 hasta que la cantidad de candidatos coincida con\nlas intersecciones que muestra el gráfico')
plt.xlim(0, max(k2_prueba))
plt.ylim(-my_ylim, my_ylim)

""" 3. Ahora que tengo mis candidatos, refino los valores """
cuantos_candidatos = np.min((len(comparacion_grupos), max_candidatos))
k2_finales = np.zeros(cuantos_candidatos)
for i in np.arange(0, cuantos_candidatos):

    print('Candidato ' + str(i+1) + ': ')
    
    # resuelvo el problema
    resultado = scipy.optimize.minimize(fun=my_func_abs, x0=k2_candidatos[i], args=(L1,L2,c1,c2), tol = 1e-20) #, method='Nelder-Mead')
    delta = np.abs(k2_candidatos[i] - resultado.x[0])
    
    k2_finales[i] = resultado.x[0]
    
    # salida en pantalla
    print(resultado)
    print('Optimización: ' + '{:f}'.format(k2_candidatos[i]) + ' -> ' + '{:f}'.format(resultado.x[0]))
    print('Diferencia: ' + '{:f}'.format(delta))
    print('')

    # gráfico
    if (plot_candidatos):
        fig_candidato = plt.figure()
        ax_candidato  = plt.axes()
    
        beta = 10
        k2_rango = np.linspace(start = min(k2_candidatos[i], resultado.x[0]) - beta*delta, \
                               stop  = max(k2_candidatos[i], resultado.x[0]) + beta*delta, \
                               num   = 1000)
        
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


# parametros para los graficos
samples_x = 1000
eje_x = np.linspace(-L1,  L2, num = samples_x)      # \_ armo el eje x para cada tramo
x1    = eje_x[eje_x < 0]                        # |
x2    = eje_x[eje_x >= 0]                       # /

cuantos_modos = 8
plot_derivada = False


# graficos
cuantos_modos = min(cuantos_modos, max_candidatos-1, k2_finales.size-1)

my_colormap   = iter(cm.rainbow(np.linspace(0,1,cuantos_modos)))

fig_modos, ax_modos = plt.subplots()
if (plot_derivada):
    fig_deriv, ax_deriv = plt.subplots(nrows= cuantos_modos)

lista_modos = np.zeros([cuantos_modos, samples_x])

for modo in np.arange(start=1, stop=cuantos_modos+1, step=1):

    # k's
    k2 = k2_finales[modo]
    k1 = c2*k2/c1
    
    # amplitudes de senos y cosenos
    A1 = 1
    A2 = A1
    B1 = A1 / np.tan(k1*L1)
    B2 = -A2 / np.tan(k2*L2)
    
    # calculos los modos en cada subcuerda
    y1 = A1*np.cos(k1*x1) + B1*np.sin(k1*x1)
    y2 = A2*np.cos(k2*x2) + B2*np.sin(k2*x2)
    eje_y = np.concatenate((y1, y2))                # concateno
    eje_y = eje_y / np.max(abs(eje_y))              # normalizo
    
    lista_modos[modo-1,:] = eje_y
    
    # ploteo 
    my_color = next(my_colormap)
    ax_modos.plot(eje_x, eje_y, c=my_color)
    ax_modos.set_title('ccc')
    
    if (plot_derivada):
        
        ax_deriv[modo-1].plot(x1[1:], np.diff(y1) / np.diff(x1))
        ax_deriv[modo-1].plot(x2[:-1], np.diff(y2) / np.diff(x2))
        ax_deriv[modo-1].set_title('Modo: ' + str(modo) + '; k1=' + str(k1) + '; k2=' + str(k2))

# producto interno
if (False):
    producto_interno = np.zeros([cuantos_modos, cuantos_modos])
    
    for n1 in np.arange(start=0, stop=cuantos_modos, step=1):
        for n2 in np.arange(start=n1, stop=cuantos_modos, step=1):
            producto_interno[n1,n2] = sum(lista_modos[n1,:] * lista_modos[n2,:]) / (eje_x[1] - eje_x[0])
            
    plt.matshow(producto_interno)
    plt.colorbar()


# quiero comparar con el sistema discretizado

n_masas = 1000

m1 = 1.
m2 = m1*c1**2/c2**2

n1 = int(np.floor(alpha*n_masas))
n2 = n_masas - n1

vector_masas = np.zeros(n_masas)
vector_masas[0:n1] = m1
vector_masas[n1:n1+n2] = m2



M = np.diag(vector_masas)
K = np.diag(2*np.ones(n_masas)) - np.diag(np.ones(n_masas-1),-1) \
                                - np.diag(np.ones(n_masas-1),+1)
W = np.matmul(np.linalg.inv(M), K)                       
w, v = np.linalg.eig(W)

idx = np.argsort(w)
w = w[idx]
v = v[:,idx]

# Quiero ver la similitud entre autovectores del caso discreto y funciones de
# modos del caso continuo. Para esto elegi a proposito que la cantidad de
# masas del caso discreto sea la misma que la cantidad de samples del eje x del
# caso continuo
# OJO! Para el caso continuo recolectamos ciertos modos en funcion de la
# resolucion de la ecuación trascendental, pudimos haber olvidado algunos.
# Chequear eso si hay discrepancias.
que_modo = 0
fig, ax = plt.subplots()
ax.plot(v[:,que_modo] / max(v[:,que_modo]))
ax.plot(lista_modos[que_modo,:] / max(lista_modos[que_modo,:]))
ax.set_title('Modo discreto vs continuo: ' + str(que_modo))

# otra forma de verlo
# ax.plot(v[:,0], lista_modos[0,:])

# ahora quiero ver la matriz de autovectores inversa
v_inv = np.linalg.inv(v)
que_modo = 0
fig, ax = plt.subplots()
ax.scatter(range(n_masas), v_inv[que_modo,:])      # <- ahora son vectores fila!!
ax.set_title('Anti-modo ' + str(que_modo))

# comparo un modo con su "antimodo"
tabla = np.zeros([n_masas, 2])

for que_modo in np.arange(0, n_masas, step=1):
    cociente = v_inv[que_modo,:] / v[:,que_modo]
    tabla[que_modo, 0] = np.mean(cociente[0:n1])
    tabla[que_modo, 1] = np.mean(cociente[n1:n1+n2])
    
    if (False):
        fig, ax = plt.subplots()
        ax.scatter(range(n_masas), cociente) 
        ax.set_title('Comparacion modo y anti-modo ' + str(que_modo))

fig, ax = plt.subplots()
ax.plot(tabla[:,0])


