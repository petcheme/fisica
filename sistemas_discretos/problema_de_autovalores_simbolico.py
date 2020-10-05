import numpy as np
import sympy         # librería para cálculo simbólico

# a = \tilde{\omega}_0^2-\omega^2
# b = \omega_0^2-\omega^2
# c = \omega_2^2

""" 1. parametros """
a_valor = 1.2
b_valor = np.pi
c_valor = 5.

""" 2. solución simbólica """
# Defino los símbolos que usaré en mis expresiones
a, b, c = sympy.symbols('a,b,c')

# Armo mi matriz como una lista de Python
M_lista = [[a,0,c,0,0,0], \
           [0,b,0,c,0,0], \
           [c,0,a,0,c,0], \
           [0,c,0,b,0,c], \
           [0,0,c,0,a,0], \
           [0,0,0,c,0,b]]

# Mediante numpy convierto mi matriz-lista en un array 2d,
# notar que es un array de símbolos
M_array = np.array(M_lista)
    
# Ahora obtengo mi matriz simbólica usando la instrucción Matrix de sympy
M_simb = sympy.Matrix(M_lista)
# M_simb = sympy.Matrix(M_array)    # no es necesario pasar por numpy realmente...

# el determinante simbólico se obtiene a partir de la representación
# simbólica de la matriz
determinante = M_simb.det()
autovectores = M_simb.eigenvects()
autovalores  = M_simb.eigenvals()

""" 3. Salida en pantalla de resultados simbólicos """

print('La matriz es:')
print(M_array)                      # ...aunque numpy es más cómodo para mostrar la matriz en pantalla
print() # línea en blanco

print('El determinante de la matriz es:')
print(determinante)
print()


# revisar: https://stackoverflow.com/questions/43689076/how-to-find-the-eigenvalues-and-eigenvectors-of-a-matrix-with-sympy
print('Autovectores:')
print(autovectores)
print()

print('Autovalores')
print(autovalores)
print()


""" 4. evaluación de la solución simbólica """

print('Evaluación numérica de las expresiones simbólicas')

# pido 10 cifras significativas
precision = 10

# el primer paso es sustituir las variables por sus valores
# para eso necesito un diccionario que vincule símbolos y valores
diccionario_valores = {a:a_valor, b:b_valor, c:c_valor}

# el comando subs toma el diccionario y realiza las sustituciones
det_subs = determinante.subs(diccionario_valores)

# el paso final es usar evalf() para obtener el valor en punto flotante de la
# expresión sustituída
det_valor = det_subs.evalf(precision)
print('Determinante: ' + str(det_valor))
print()

# autovectores viene en formato lista
# a su vez cada autovector se compone de 
# - v[0], el autovalor
# - v[1], la multiplicidad
# - v[2], el autovector como Matrix (se debe evaluar como v[2][0])
counter = 1
for v in autovectores: 
    print('Autovector #' + str(counter))
    print('- multiplicidad: ' + str(v[1]))
    print('- autovalor: '     + str(v[0].subs(diccionario_valores).evalf(precision)))
    print('- autovector: '    + str(v[2][0].subs(diccionario_valores).evalf(precision)))

    print()
    counter += 1
    

