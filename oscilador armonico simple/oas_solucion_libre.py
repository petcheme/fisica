# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
Solucion de un oscilador armonico simple, con amortiguacion y libre

- Determinamos si el regimen de la solucion (sub, sobre, o critico).
- Calculamos frecuencia y tiempos caracteristicos del sistema.
- Mostramos la solucion para condiciones iniciales x(t=0) v(t=0).
- Si los parametros se introducen en unidades mks, los resultados tambien seran
  mks.
"""

""" 1. parametros """

# parametros del sistema, el formato interno es punto flotante salvo indicacion contraria
# el simbolo = es un operador que significa asignacion

# oscilador sub-amortiguado con disipación despreciable
m    = 2.           # masa
k    = 1 / 8e-6     # constante elastica
b    = .2           # coeficiente de disipacion
Fext = 400.         # amplitud de la fuerza externa (no implementado)

# condiciones iniciales
x0   = 1.           # posicion
v0   = 0.           # velocidad

# parametros del grafico
t_min    = 0.       # tiempo minimo
t_max    = .8       # tiempo maximo
n_puntos = 10000    # cantidad de samples, debe ser entero


# a continuación hay cambios en los parametros pensados para mostrar los diferentes
# regimenes del oscilador. comentar y descomentar para activarlos.

# oscilador sub-amortiguado con disipación
# b     = 20.
# t_max = 0.5

# oscilador sub-amortiguado con disipacion fuerte
# b     = 200.
# t_max = .2

# oscilador sub-amortiguado cerca del limite critico
# b     = 700.
# t_max = .05

# oscilador sub-amortiguado muy cerca del limite critico
# b     = 950.
# t_max = .05

# oscilador critico
# b     = 1000.
# t_max = .025

# oscilador sobreamortiguado
# b     = 2000.
# t_max = .05

# oscilador con inercia despreciable (estilo circuito RC)
# m = 1e-10
# t_max = .5e-5



""" 2. solucion """

#-- parametros derivados

# si bien inicialmente damos tres parametros para caracterizar al sistema, la
# dinamica depende de solo dos: la disipacion por unidad de masa (gamma) y la
# constante elastica por unidad de masa (la frecuencia natural al cuadrado)

gamma = b / m               # constante de amortiguamiento por unidad de masa
tau   = 2. / gamma          # tiempo caracteristico de decaimiento exponencial
w0    = np.sqrt(k/m)        # frecuencia angular natural del sistema, es decir,
                            # la frecuencia en ausencia de disipacion o fuerzas
                            # externas (aka frecuencia de resonancia)

f0 = w0 / 2. / np.pi        # frecuencia natural del sistema, np.pi es la
                            # representacion en punto flotante de la constante
                            # pi provista por la biblioteca numpy 


# voy a definir la frecuencia angular en presencia de la disipacion como un
# numero complejo, de este modo puedo emplear una unica expresion para los
# regimenes sobre- y sub-amortiguados (para el critico no es asi ya que en este
# regimen interviene un limite, por lo que debo emplear la expresion resultante
# de tomar dicho limite) (todas las operaciones que vamos a realizar son 
# numericas, no simbolicas; es decir, si se presenta una division por cero, el
# programa no es capaz de determinar el limite, sino que genera un error al
# querer calcular una operacion no definida)

# para escribir la frecuencia angular w en presencia de disipacion, voy a
# definir w como un numero complejo, esto me permite manejar en un unico
# parametro los distintos regimenes de la oscilacion
    
# para lograr esto, sumo parte compleja nula dentro de la raiz; esto hace que
# la funcion sqrt acepte argumentos negativos y devuelva un complejo 
w = np.sqrt(k/m - tau**(-2) + 0*1j)         # la unidad imaginaria se escribe 1j
                                            # el operador potencia se escribe **
                                            
# luego (esto lo usaremos más adelante): 
# si w es real . . . . . . . . . . regimen sub-amortiguado
# si w es complejo puro. . . . . . regimen sobre-amortiguado
# si w es nulo . . . . . . . . . . regimen critico

# la clave de esto es que tanto las funciones trignometricas como las
# exponenciales se pueden extender para aceptar argumentos complejos

# obtengo la frecuencia de oscilacion para el caso sub-amortiguado
if (np.imag(w) == 0) & (np.real(w) != 0):
    f = np.real(w) / 2 / np.pi

# constantes de tiempo del sistema, cuando el sistema es sobreamortiguado, son
# valores reales, por lo que las exponenciales se convierten en terminos que
# decaen. cuando el sistema es subamortiguado, son valores con parte compleja
# no nula, por lo que las exponenciales se comportan como osciladores
# amortiguados.
lambda1  =  1j*w-1/tau
lambda2  = -1j*w-1/tau


#-- solucion homogenea

# coeficientes definidos por las c.i.
A = x0 
B = v0 + x0 / tau

# defino el eje del tiempo, es un vector que contiene todos los puntos del
# tiempo en que deseo evaluar 
eje_t = np.linspace(t_min, t_max, num=n_puntos)

# ademas calculo la frecuencia de sampleo del grafico, debo tenerla en cuenta
# para evitar subsampleo
fs = n_puntos / (t_max - t_min)   

# calculo x vs t

# separo el regimen critico de los otros dos, esto es porque la expresion para
# este regimen se obtiene de tomar el limite en que w -> 0. nuestro codigo
# trabaja de manera numerica, no simbolica, por lo que debo poner a mano la
# expresion correspondiente:
#
#   lim cuando w -> 0 de sin(w*t)/w = t
#   
# para hacer esto empleo una bifuracion del codigo (bloque if-else) y el
# operador comparacion, dado por el simbolo ==
if w == 0:                                  # critico

    eje_x = np.exp(-eje_t / tau)*(A + B*eje_t)

else:                                       # sub- o sobre-

    # expresion con senos y cosenos modulados por una exponencial, esta
    # expresion puede ser problematica en el regimen sobreamortiguado ya que 
    # los senos y cosenos se transforman en exponenciales que pueden diverger
    # mas alla del limite superior para la representacion de punto flotante
    # del sistema
    # eje_x = np.exp(-eje_t / tau)*(A*np.cos(w*eje_t) + B*np.sin(w*eje_t)/w)
    
    # esta forma alternativa, empleando unicamente exponenciales, previene ese
    # problema, ya que las exponenciales son todas decrecientes (chequear los
    # parametros lambda 1 y 2)
    eje_x = 0.5* ((A + B/1j/w)*np.exp(lambda1*eje_t) + (A - B/1j/w)*np.exp(lambda2*eje_t))

    # al final de todo tomo parte real, ya que los complejos son solo una
    # herramienta de calculo
    eje_x = np.real(eje_x)


""" 3. salida en pantalla """

# graficomos la solucion


# creo la figura y los ejes
fig, ejes1 = plt.subplots()
# grafico x(t)
ejes1.plot(eje_t, eje_x, label = 'x(t)')
# grafico solucion particular                   
ejes1.plot(np.array([t_min, t_max]), np.array([0, 0]), '--k', linewidth=1, label ='x eq.')

# a continuacion grafico algunas cosas mas, dependiendo del regimen
# ademas, imprimo en pantalla info util del oscilador

if (np.imag(w) == 0) & (np.real(w) != 0): # regimen sub-amortiguado
    
    print('El regimen del sistema es sub-amortiguado.')
    # %.2g indica un numero de punto flotante con dos cifras significativas
    print('El tiempo caracteristico de decaimiento es %.2g'      % (tau))
    # %.2f indica un numero de punto flotante con dos cifras decimales
    print('La frecuencia natural es %.2f (periodo = %.2g)'       % (f0, 1/f0))
    print('La frecuencia de oscilacion es %.2f (periodo = %.2g)' % (f, 1/f))
    
    # cuantifico la distancia al regimen critico
    print('La diferencia respecto a la frecuencia natural es -%.2g por ciento'
          % ((1 - f/f0)*100))
    print('Un ciclo de oscilación equivale a %.2g tiempos caracteristicos de decaimiento'
          % (1 / f / tau))

    if 1 / f / tau < 5:
        # muestro la envolvente si el sistema no esta tan cerca del regimen critico
        ejes1.plot(eje_t, -np.exp(-eje_t/tau), '--r', linewidth=1)
        ejes1.plot(eje_t,  np.exp(-eje_t/tau), '--r', linewidth=1)
    else:
        ejes1.plot(eje_t, np.exp(-eje_t/tau) *(A + B*eje_t), '--', linewidth=1, label='sol. crit.' )
    
elif (np.imag(w) != 0) & (np.real(w) == 0): # regimen sobre-amortiguado
    
    print('El regimen del sistema es sobre-amortiguado.')
    print('El tiempo caracteristico de decaimiento critico es %.2g' % (tau))

    print('El tiempo de decaimiento minimo (rapido) es %.2g' % np.real(1/lambda1))

    print('El tiempo de decaimiento maximo (lento) es %.2g' % np.real(1/lambda2))

    # ejes1.plot(eje_t, np.real(np.exp(-eje_t / tau)*(A*np.cos(w*eje_t)   )), label='cos')    # contribucion coseno hiperbolico
    # ejes1.plot(eje_t, np.real(np.exp(-eje_t / tau)*(B*np.sin(w*eje_t)/w )), label='sin')    # contribucion seno hiperbolico

    ejes1.plot(eje_t, np.exp(-eje_t/tau) *(A + B*eje_t), '--', linewidth=1, label='sol. crit.' )
    
    ejes1.plot(eje_t, 0.5*np.real(np.exp(-eje_t *(1 / tau + 1j*w ))*( A + B / 1j)), '--', label='lenta') 
    ejes1.plot(eje_t, 0.5*np.real(np.exp(-eje_t *(1 / tau - 1j*w ))*( A - B / 1j)), '--', label='rapida')
    
else: # regimen critico
    print('El regimen del sistema es critico.')
    print('El tiempo caracteristico de decaimiento es %.2g' % (tau))

    
    
# nombres de los ejes
plt.xlabel('t [mks]')
plt.ylabel('x(t) [mks]')

# muestro la leyenda
ejes1.legend()

# muestro el grafico
plt.show()


# agrego el grafico de la velocidad en funcion del tiempo pero como no quiero
# derivar la expresion simbolica, uso una derivada numerica
fig, ejes2 = plt.subplots()
# grafico v(t)

eje_v      = fs * np.concatenate(( np.array([v0]), np.diff(eje_x) ))
eje_v_crit = fs * np.concatenate(( np.array([v0]), np.diff(np.exp(-eje_t / tau)*(A + B*eje_t)) ))

ejes2.plot(eje_t, eje_v, label = 'v(t)')
ejes2.plot(eje_t, eje_v_crit, '--', label = 'sol. crit.')

ejes2.legend()

plt.xlabel('t [mks]')
plt.ylabel('v(t) [mks]')
plt.show()


