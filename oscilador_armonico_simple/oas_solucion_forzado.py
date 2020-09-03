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
wext = 25      # frecuencia fuerza externa

n_ciclos = 3
t_min    = 0
t_max    = 2 * np.pi / wext * n_ciclos      # de este modo, t_max corresponde a la cantidad
                                            # especificada de ciclos de oscilacion
n_puntos = n_ciclos*10000                   # cuantos samples por ciclo


""" 2. solucion particular """

#-- parametros derivados
a0    = Fext / m                # aceleracion del forzante
gamma = b / m                   # disipacion por unidad de masa
w0_sq = k / m                   # constante elastica por unidad de masa (es la
                                # frecuencia natural al cuadrado)

# uso variables auxiliares para escribir las amplitudes de la solucion
# particular, de este modo evito repetir formulas y cometer errores
dif_w_sq    = w0_sq - wext**2 
denominador = dif_w_sq**2 + (wext*gamma)**2

A = a0 * (dif_w_sq)   / denominador
B = a0 * wext * gamma / denominador 

#-- solucion
t  = np.linspace(t_min, t_max, n_puntos)                # tiempo
xp =   A*np.cos(wext*t) + B*np.sin(wext*t)              # posicion
vp = (-A*np.sin(wext*t) + B*np.cos(wext*t))*wext        # velocidad
ap = -xp*wext**2                                        # aceleracion

# fuerzas presentes
F_res = -k*xp                                           # Fuerza elástica vs. t
F_dis = -b*vp                                           # Fuerza disipativa vs. t
F_ext = Fext*np.cos(wext*t)                             # Fuerza externa vs. t

# trabajo de las fuerzas (diferenciales)
d_xp   = np.concatenate(( np.array([0]), np.diff(xp) )) # diferencial para la posicion, chequear que sea chico
dW_res = F_res * d_xp                                   # \
dW_dis = F_dis * d_xp                                   # |_ diferenciales para cada fuerza
dW_ext = F_ext * d_xp                                   # /  

# trabajo acumulado por cada fuerza
W_res = np.cumsum(dW_res)
W_dis = np.cumsum(dW_dis)
W_ext = np.cumsum(dW_ext)

""" --- 3. graficos """


fig1, ax1 = plt.subplots(3, 1)
fig1.set_size_inches(6, 9)

ax1[0].plot(t, F_ext, label='Fext')
ax1[0].set(ylabel='$F_{ext}$ [mks]', xticklabels = [])

ax1[1].plot(t, xp, label = 'x_p(t)')
ax1[1].set(ylabel='$x_p$ [mks]', xticklabels = [])

ax1[2].plot(t, vp, label = 'v_p(t)')
ax1[2].set(xlabel = '$t$ [mks]', ylabel = '$v_p$ [mks]')

fig1.show()


fig2, ax2 = plt.subplots(4, 1)
fig2.set_size_inches(6, 8)

ax2[0].plot(t, F_res)
ax2[0].plot(t, F_dis)
ax2[0].plot(t, F_ext)
ax2[0].set(ylabel='$F$ [mks]', xticklabels = [])

ax2[1].plot(t, dW_res, label='res')
ax2[1].plot(t, dW_dis, label='dis')
ax2[1].plot(t, dW_ext, label='ext')
ax2[1].set(ylabel='$dW$ [mks]', xticklabels = [])

ax2[2].plot(t, W_res)
ax2[2].plot(t, W_dis)
ax2[2].plot(t, W_ext)
ax2[2].set(ylabel='$W$ [mks]', xticklabels = [])

ax2[3].plot(t, W_ext + W_dis, color='firebrick', label='ext+dis')
ax2[3].set(ylabel='$W$ [mks]',xlabel='$t$ [mks]')

fig2.legend()
fig2.show()

