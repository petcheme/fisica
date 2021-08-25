# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 18:13:54 2021

@author: petcheme
"""

import numpy as np
import matplotlib.pyplot as plt

g = 10
l = 1
m = 2
K = 10

ka_values = np.linspace(0, np.pi, num=100000)

fig, ax = plt.subplots()
ax.plot(ka_values, np.sqrt(g/l + 4*K/m*np.sin(ka_values/2)**2))
ax.plot(ka_values, np.sqrt(g/l + 2*K/m*(1 + np.cosh(ka_values))))
ax.plot(ka_values, np.sqrt(g/l + 2*K/m*(1 - np.cosh(ka_values))))

ax.plot([0, np.pi], [np.sqrt(g/l), np.sqrt(g/l)], '--', color='grey' )
ax.plot([0, np.pi], [np.sqrt(g/l+ 4*k/m), np.sqrt(g/l + 4*k/m)], '--', color='grey' )

ax.annotate('\sqrt{g/l}', (np.pi-.5, .1+np.sqrt(g/l)))
ax.annotate('\sqrt{g/l + 4K/m}', (np.pi-.8, .1+np.sqrt(g/l + 4*K/m)))

ax.set_xticks(ticks= [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels(labels= ['0', 'pi/4', 'pi/2', '3pi/4', 'pi'])

ax.set_xlabel('ka')
ax.set_ylabel('omega')

