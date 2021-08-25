# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 13:51:42 2021

@author: petcheme
"""

import matplotlib.pyplot as plt
import numpy as np

# coeficientes de fresnel

ni = 1.
nt = 1.5
tita_i = np.linspace(start = 0, stop = np.pi/2, num=1000)


tita_t = np.arcsin(ni/nt*np.sin(tita_i))


# los coefs son las ecs. 4.34, 4.35, 4.40 y 4.41 del hecht
r_perp = (ni*np.cos(tita_i) - nt*np.cos(tita_t)) / \
         (ni*np.cos(tita_i) + nt*np.cos(tita_t))            # hecht 4.34
r_para = (nt*np.cos(tita_i) - ni*np.cos(tita_t)) / \
         (ni*np.cos(tita_t) + nt*np.cos(tita_i))            # hecht 4.40

         

plot(tita_i/np.pi*180, r_para)      # es la que se puede anular
plot(tita_i/np.pi*180, r_perp)
plot(tita_i/np.pi*180, tita_i*0)

