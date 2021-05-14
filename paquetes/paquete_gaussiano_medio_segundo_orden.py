# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:15:53 2021

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



# parametros
k0      = 50.
delta_k = 10.

# estos parametros deben completarse tras considerar una determinada relación
# de dispersion, en función de k0 y delta_k
vf = 10.
vg = 10.
ag = .10     # aceleracion de grupo?

# periodo de la portadora
lambda0 = 2*np.pi/k0
omega0  = vf*k0
tau0    = 2*np.pi/omega0


# ejes de coordenadas
n_samples_x = 10000
n_samples_t = 2000

eje_x = np.linspace(-0*lambda0, 100*lambda0, n_samples_x)
eje_t = np.linspace( 0.,  500*tau0, n_samples_t)

tiempo = eje_t[0]

# obtengo la solucion
def solucion(que_frame):

    tiempo = eje_t[que_frame]
    
    aux = -ag*tiempo + 1j / 4 / delta_k**2
    
    coef       = np.sqrt(1j*np.pi / aux)
    portadora  = np.exp(1j*k0*(eje_x - vf*tiempo)  )
    envolvente = np.exp(- 1j*(eje_x - vg*tiempo)**2 / 4 / aux)
    psi = np.real(coef*envolvente*portadora) # np.real(coef*portadora*envolvente)

    return psi

# fig
fig0, ax0 = plt.subplots()
aux  = -ag*eje_t + 1j / 4 / delta_k**2
coef = np.sqrt(1j*np.pi / aux)
ax0.plot(eje_t, np.real(coef))

# armo la figura
fig, ax = plt.subplots()

line_plot, = ax.plot(eje_x, 0*solucion(0))
limite_y = 50
ax.set_ylim([-limite_y, limite_y])

def update_plot(que_frame):

    y = solucion(que_frame)
    line_plot.set_ydata(y)

    ax.set_title('frame={:.0f}'.format(que_frame))
   

ani = animation.FuncAnimation(fig, update_plot, frames=range(n_samples_t),
                              interval=100, repeat=False)

plt.show()


