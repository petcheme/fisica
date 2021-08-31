# fisica
Códigos para materias de física. Por ahora, todos los códigos son para Física 2 (F) (FCEN-UBA) y la mayoría están en Python (incluyendo Jupyter Notebook). A continuación el índice de códigos disponibles.

### Oscilador armónico simple

 1. Calculadora de parámetros (notebooks):

    * La que vimos en clase ([oas_calculadora_de_parametros_2021.ipynb](oscilador_armonico_simple/oas_calculadora_de_parametros_2021.ipynb)) y una versión similar anterior ([oas_calculadora_de_parametros.ipynb](oscilador_armonico_simple/oas_calculadora_de_parametros.ipynb)).    
    * Variación de la frecuencia (compleja) en función de la disipación ([oas_autovalores.py](oscilador_armonico_simple/oas_autovalores.py), script).

    En ambos casos se muestra un uso básico de ``numpy`` (vectores y matrices) y ``matplotlib`` (gráficos).

2. Oscilador libre con disipación:

   * Solución en función del tiempo para ciertos parámetros y condiciones iniciales. Tiene en cuenta el régimen (sub, sobre, crítico) en función de los parámetros ([oas_solucion_libre.py](oscilador_armonico_simple/oas_solucion_libre.py), script).

3. Oscilador forzado:

   * Amplitudes elástica y absorbente en función de la disipación ([oas_amplitudes_forzado.py](oscilador_armonico_simple/oas_amplitudes_forzado.py), script).
   * Trabajo de las fuerzas en función del tiempo ([oas_solucion_forzado.py](oscilador_armonico_simple/oas_solucion_forzado.py), script).
   * Integración numérica de la ecuación diferencial mediante ``scipy`` ([oas_integral_numerica.py](oscilador_armonico_simple/oas_integral_numerica.py), script).

### Sistemas acoplados discretos

 1. Solución de modos normales y autovalores:

    * Un notebook que permite resolver (mediante ``numpy``) los modos normales del sistema a partir de las matrices de masa y de interacciones. También resuelve las condiciones iniciales y el régimen forzado ([sd_solucion_libre.ipynb](sistemas_discretos/sd_solucion_libre.ipynb)).
    * Ejemplo de solución simbólica mediante sympy ([problema_de_autovalores_simbolico.py](sistemas_discretos/problema_de_autovalores_simbolico.py), script).
    * Animación de los modos normales de un sistema ([pendulos_acoplados.ipynb](sistemas_discretos/pendulos_acoplados.ipynb), notebook)

 2. Ortogonalidad de modos normales

    * Comparación entre un sistema continuo y uno discreto ([comparacion_modos_discreto_vs_continuo.py](sistemas_discretos/comparacion_modos_discreto_vs_continuo.py), script)

 3. Sistemas de péndulos acoplados

    * Relación de dispersión ([relacion_de_dispersion_pendulos_acoplados.py](sistemas_discretos/relacion_de_dispersion_pendulos_acoplados.py), script).
    * Sistema forzado y animación de los regímenes reactivo y dispersivo ([pendulos_acoplados_forzados.py](sistemas_discretos/pendulos_acoplados_forzados.py), script).
