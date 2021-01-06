#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

# Quiero resolver la ecuacion diferencial psi'' = M*psi, donde psi es un vector 
# que contiene en cada componente el desplazamiento de cada masa en función del
# tiempo, medido respecto a la posicion de equilibrio, y donde M es una matriz
# de 2x2 que contiene los términos de interacción entre las masas.
#
# Por simplicidad consideremos el caso de dos partículas de igual masa (m)
# unidas por resortes con la misma constante elástica (k). Los resortes están
# fijos a dos soportes en los extremos (i.e., extremos fijos)
#
# |                                     |
# |_/\_/\_[MASA 1]_/\_/\_[MASA 2]_/\_/\_|
# |                                     |
#         |-> psi1       |-> psi2
#

k = 1.0         # en mks: N/M
m = 1.0         # en mks: kg

# La matriz M será:
#
# M = [ -2k/m,   k/m
#         k/m, -2k/m ]

#grado_acoplamiento = 0.01
grado_acoplamiento = 1
M = np.matrix( ((-2.0*k/m, grado_acoplamiento*k/m), (grado_acoplamiento*k/m, -2.0*k/m)) )


# para el caso de dos pendulos acoplados
ma = 1
mb = 2
k  = 1
g  = 10
L  = 1

M  = np.matrix( (( -g/L-k/ma , k/ma), (k/mb, -g/L-k/mb)) )


# n_masas = len(M)

# La solución para este sistema es psi = v*e^(i(wt+theta)), donde v es un
# vector y w y theta son escalares. Es decir, proponemos que todas las masas
# oscilan *a la misma frecuencia y en fase*, y que las únicas diferencias entre
# las masas vendrán del vector v. A esto lo llamamos solucion de modos normales.
# Al proponer esta solucion se obtiene un problema de autovalores y autovectores
# donde la matriz es M y los autovalores son iguales a -w^2. Definamos:
#
# u = vector de autovalores
# v = matriz de autovectores (cada columna = 1 autovector*)

# Ojo! En realidad v contiene "autoversores", es decir los autovectores con
# norma 1. Referencia:
# https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.linalg.eig.html
u, v = np.linalg.eig(M)         

# Calculemos la frecuencia angular para cada modo.  Recordemos que la misma es
# w = sqrt(-u) (es decir los autovalores del problema deben ser < 0)
w = np.sqrt(-u)

# Presentemos en pantalla los resultados
for i in range(2):
    print("Modo " + str(i+1) + ": w=" + str(w[i]) + "; v=[" + str(v[0,i]) + ", " + str(v[1,i]) + "]")

# La solucion para nuestro sistema, hasta ahora, es
#
#       psi(t) = C_1*v_1*exp(i*(w_1*t + theta_1)) + C_2*v_2*exp(i*(w_2*t + theta_2))
#
# donde C_1, C_2, theta_1 y theta_2 son parametros definidos al plantear las
# condiciones iniciales. Nótese que se trata de 4 escalares reales. (Recordar
# que v_1 y v_2 son los autovectores con norma 1). Sin embargo, podemos
# reescribir la ecuación para transformarlos en 2 números complejos:
#
#       psi(t) = C_1*exp(i*theta_1)*v_1*exp(i*w_1*t) + C_2*exp(i*theta_2)*v_2*exp(i*w_2*t)
#
# es decir:
#
#       psi(t) = z_1*v_1*exp(i*w_1*t) + z_2*v_2*exp(i*w_2*t)
#
# con:
#
#       z_1 = C_1*exp(i*theta_1)
#       z_2 = C_2*exp(i*theta_2)
#
# Evaluando en t=0, obtenemos el siguiente sistema para resolver las C.I.:
#
#       psi(0)       =       z_1*v_1 +         z_2*v_2
#       psi_punto(0) = i*w_1*z_1*v_1 + i*w_2^2*z_2*v_2
#
# donde para que tenga sentido la igualdad hay que tomar parte real de las
# expresiones complejas.

# Planteemos entonces las condiciones iniciales para nuestro sistema. Probemos
# diferentes condiciones:

# Una única masa apartada del equilibrio
x0 = np.array((1,1))
v0 = np.array((0,0))

# Ambas masas apartadas en la misma cantidad (fase)
#x0 = np.array((1,1))
#v0 = np.array((0,0))

# Ambas masas apartadas en la misma cantidad pero sentidos opuestos (contrafase)
#x0 = np.array((1,-1))
#v0 = np.array((0,0))

# Tambien podemos probar condiciones partiendo del equilibrio con perturbaciones
# en la velocidad, o bien condiciones combinadas sobre x y v.


# Defino un vector z complejo con 2 elementos para calcular los parametros que
# dependen de las condiciones iniciales. Inicializo el vector en cero ya que
# completaré sus valores a continuacion:
z  = np.zeros(2, dtype="complex128")
z2 = np.zeros(2, dtype="complex128")

# Si los autovectores son ortogonales, obtenemos, haciendo álgebra a partir de
# las C.I., el siguiente resultado:
#
#                   z_i = x0*v_i + j*v0*v_i / w_i
#
# donde j es la unidad imaginaria (para no confundir con el subindice i de los
# modos)

for i in range(2):
    z[i] = np.dot(x0, v[:,i]) + 1j*np.dot(v0, v[:,i])/w[i]      # <- notese que la unidad imaginaria se escribe como 1j

# Si no son ortogonales, obtenemos:
#   
#           z_i = sumatoria{ v_inversa_ki*x0_i + j*v_inversa_ki*v0_i / w_i }
#

v_inv = np.linalg.inv(v)
v_inv_X_x0 = np.dot(v_inv, x0)      # inversa de v aplicada a x0
v_inv_X_v0 = np.dot(v_inv, v0)      # inversa de v aplicada a v0

for i in range(2):
    z[i] = v_inv_X_x0[0,i] + 1j*v_inv_X_v0[0,i]/w[i]

print(z)
#print(z2)

# Grafiquemos la solucion para cada masa
n_tau = 20

# El tiempo va desde 0 hasta n_tau veces el periodo del modo fundamental.
tiempo = np.linspace(0, n_tau*2*np.pi/np.min(w), 1000)

psi   = np.zeros((2,len(tiempo)), dtype="complex128")
veloc = np.zeros((2,len(tiempo)), dtype="complex128")

for i in range(2):                          # ciclo sobre masas
    for j in range(2):                      # ciclo sobre modos normales
        psi[i,:]   =   psi[i,:] +         z[j]*v[i,j]*np.exp(1j*w[j]*tiempo)
        veloc[i,:] = veloc[i,:] + 1j*w[j]*z[j]*v[i,j]*np.exp(1j*w[j]*tiempo)

# Ahora calculemos la solucion del sistema en la base de modos normales. Para
# esto uso a la inversa de la matriz de autoversores para aplicar una
# transformacion lineal a la solucion en las coordenadas de masas.

v_inversa = np.linalg.inv(v)

psi_modos   = np.zeros((2, len(tiempo)), dtype="complex128")
veloc_modos = np.zeros((2, len(tiempo)), dtype="complex128")

# Lo que hago aqui es aplicar la transformacion instante a instante, por eso mi
# loop realiza tantas iteraciones como la longitud del vector tiempo. Notar que
# la transformacion tambien vale para la velocidad, transformo de la velocidad
# de las coordenadas de cada masa a la "velocidad" de cada coordenada modal.
for i in range(len(tiempo)):
    psi_modos[:,i]   = np.dot(v_inversa, psi[:,i])
    veloc_modos[:,i] = np.dot(v_inversa, veloc[:,i])


# Ahora vamos a graficar todo lo que estuvimos calculando...

grafico_coordenadas_flag    = True
grafico_parametros_ci       = True

# Ordeno los graficos en bloques para mayor claridad

if grafico_coordenadas_flag:

    # Defino estas variables para armar los subplots para poder modificar la
    # estructura del grafico con mas comodidad
    subplot_nrows = 3
    subplot_ncols = 4

    subplot_counter = 1

    plt.figure()

    # -------- FILA SUPERIOR: posicion --------


    #plt.subplot(441)
    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(psi[0,:]))
    plt.title("Masa 1")
    plt.ylabel("Posicion")
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1
    #if np.abs(z[0]) and np.abs(z[1]):
    #    plt.plot(tiempo, ???)                   # Quiero plotear la envolvente de la masa 1

    #plt.subplot(442)
    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(psi[1,:]))
    plt.title("Masa 2")
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1
    #if np.abs(z[0]) and np.abs(z[1]):
    #    plt.plot(tiempo, ???)                   # Quiero plotear la envolvente de la masa 2

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(psi_modos[0,:]))
    plt.title("Modo 1")
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(psi_modos[1,:]))
    plt.title("Modo 2")
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1


    # -------- FILA MEDIA: velocidad --------

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(veloc[0,:]))
    plt.ylabel("Velocidad")
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(veloc[1,:]))
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(veloc_modos[0,:]))
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, np.real(veloc_modos[1,:]))
    my_axes.axes.xaxis.set_ticklabels([])
    subplot_counter = subplot_counter + 1

    print(subplot_counter)

    # -------- FILA INFERIOR: energia cinetica --------

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, m/2*np.square(np.real(veloc[0,:])))
    plt.xlabel("Tiempo")
    plt.ylabel("E. Cinetica")
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, m/2*np.square(np.real(veloc[1,:])))
    plt.xlabel("Tiempo")
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, m/2*np.square(np.real(veloc_modos[0,:])))
    plt.xlabel("Tiempo")
    subplot_counter = subplot_counter + 1

    my_axes = plt.subplot(subplot_nrows, subplot_ncols, subplot_counter)
    plt.plot(tiempo, m/2*np.square(np.real(veloc_modos[1,:])))
    plt.xlabel("Tiempo")
    subplot_counter = subplot_counter + 1

    plt.show(block=False)


if grafico_parametros_ci:

    plt.figure()

    plt.plot((-10, 10), (0,0), color="grey")
    plt.plot((0,0), (-10,10),  color="grey")
    plt.scatter(z[0].real, z[0].imag, color="red")
    plt.scatter(z[1].real, z[1].imag, color="orange")
    plt.title('¿Como son z1 (rojo) y z2 (naranja)?')
    plt.xlabel('Eje real')
    plt.ylabel('Eje complejo')

    plt.show(block=False)

#plt.close()

