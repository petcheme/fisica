clear variables
close all


% Estos parametros describen la ecuacion del sistema:
%
%    m*x'' = -k*x - b*x' + F0*cos(w_ext*t)
%
par.m     = 1;      % masa, kg
par.k     = 1;      % constante elástica, N m^-1
par.b     = 1;      % coeficiente disipativo, N s m^-1 = kg m s^-2 s m^-1 = kg s^-1
par.w_ext = .8;      % frecuencia angular de la fuerza externa, Hz
par.F0    = 1;      % amplitud de la fuerza externa, N

par.tau_ext = 2*pi/par.w_ext;   % como referencia obtenemos el período de la f. ext

% Poniendo todos m, k, y w_ext iguales a 1 obtenemos muy fácilmente el régimen 
% de resonancia del sistema.

% Estos parametros permiten simplificar la ecuacion del sistema (simplemente
% ganamos un coeficiente 1 en el término de derivada segunda):
%
%   x'' + gamma*x' + w0^2*x = a0*cos(w_ext*t)
%
% Para esto, todos los parámetros se normalizan según la masa. Pasamos de 5
% parámetros a 4. (La frecuencia de la fuerza externa no se ve modificada, dado
% que está dentro de un coseno).
par.w0_sq = par.k  / par.m;     % frecuencia angular natural del sistema en
                                % ausencia de disipación, elevada al cuadrado
par.gamma = par.b  / par.m;
par.a0    = par.F0 / par.m;

% Escribimos la solución analítica en función del tiempo. Primero definimos los
% puntos del tiempo donde la evaluaremos:
t_min     = 0;               % Por claridad escribimos los tiempos inicial,
t_max     = 2*par.tau_ext;   % final (dado por dos períodos de f. ext),
N_samples = 100000;          % y la cantidad de samples temporales.
% 1000 samples entre 0 y 2*tau_ext segundos, equiespaciadas (frec. de sampleo = 1000 / 2*tau_ext))
t = linspace(t_min, t_max, N_samples);

% Luego definimos los coeficientes para la solución particular (omitimos la
% homogénea ya que solo existe durante un período de tiempo finito).

aux = (par.w0_sq - par.w_ext^2)^2 + par.gamma^2 * par.w_ext^2; % este factor es
                                % común a las amplitudes A y B, lo escribimos
                                % una sola vez para trabajar menos y tener menos
                                % chance de cometer errores.
A = par.gamma*par.w_ext*par.a0 / aux;
B = (par.w0_sq - par.w_ext^2) * par.a0 / aux;

% Luego escribimos la solución particular, su velocidad y aceleración. Acá vemos
% por primera vez una de las características principales de MatLab/Octave. t es
% un vector, y MatLab/Octave permite evaluar la solución para todos los puntos
% del tiempo en una sola línea de código. (Internamente realiza la evaluación
% para cada punto).
xp =            A*sin(par.w_ext*t) + B*cos(par.w_ext*t);        % x_p(t)
vp = par.w_ext*(A*cos(par.w_ext*t) - B*sin(par.w_ext*t));       % v_p(t)
ap = -xp*par.w_ext^2;                                           % a_p(t)

% Luego escribimos las fuerzas involucradas
F_res = -par.k*xp;                  % Fuerza elástica vs. t
F_dis = -par.b*vp;                  % Fuerza disipativa vs. t
F_ext = par.F0*cos(par.w_ext*t);    % Fuerza externa vs. t

% Graficamos todo lo que obtuvimos hasta ahora

figure
    subplot(4,1,1)
        plot(t, xp)
        ylabel('x_p(t) [m]')
    subplot(4,1,2)
        plot(t, vp)
        ylabel('v_p(t) [m/s]')
    subplot(4,1,3)
        plot(t, ap)
        ylabel('a_p(t) [m/s^2]')
    subplot(4,1,4)
        hold all
        plot(t, F_res)
        plot(t, F_dis)
        plot(t, F_ext)
        ylabel('Fuerzas [N]')
        legend('Elástica', 'Disipativa', 'Externa')
        xlabel('Tiempo (s)')
        box on

% Ahora analizamos la energia. Calculamos primero el trabajo "instantáneo" que
% realiza cada fuerza. Usamos dos nuevas funcionalidades de Matlab/Octave.
% Primero evaluamos la fuerza en todos los puntos del tiempo excepto el último
% (ahora veremos por qué) usando la notación "(1:end-1)". Esto se lee de la
% siguiente manera: la expresión a la izquierda de ":" indica el primer elemento
% a evaluar (1), y la expresión a la derecha indica el último (end-1, esto
% quiere decir el primero antes del último elemento del vector, es decir el
% segundo contando desde atrás; end-2 es el antepenúltimo, etc.). Luego usamos
% diff(xp) para obtener el desplazamiento realizado por el sistema en cada punto
% del tiempo. El operador ".*" permite multiplicar dos vectores de iguales
% dimensiones elemento a elemento, y guardar cada resultado en un nuevo vector
% de igual tamaño a los originales. De este modo obtenemos los diferenciales
% discretos asociados a cada instante del tiempo (su precisión obviamente
% dependerá de la frecuencia de muestreo establecida).

dW_res = F_res(1:end-1) .* diff(xp);
dW_dis = F_dis(1:end-1) .* diff(xp);
dW_ext = F_ext(1:end-1) .* diff(xp);

figure
    % Ponemos como referencia la fuerza externa en un panel superior
    subplot(5,1,1)
        plot(t, F_ext)
        set(gca, 'YTickLabel', '', 'XTickLabel', '')
        ylabel('x_p(t)')

    % Aquí mostramos los diferenciales de trabajo de cada fuerza
    subplot(5,1, 2:5)
        hold all
        plot(t(1:end-1), dW_res)
        plot(t(1:end-1), dW_dis)
        plot(t(1:end-1), dW_ext)
        plot(t, zeros(size(t)), 'k--')  % linea de referencia en cero, debe ir
                                        % al final para no interferir con la
                                        % leyenda
        xlabel('Tiempo (s)')
        ylabel('dW [N m]')
        legend('Elástica', 'Disipativa', 'Externa')
        box on

% Interesantemente, vemos que la fuerza elástica realiza trabajo positivo y
% negativo alternadamente en cada medio ciclo de la fuerza externa, de modo que 
% el trabajo neto asociado en un ciclo completo es nulo. También vemos que las
% fuerzas disipativa y externa realizan trabajo opuesto en cada instante del
% tiempo. Cada una por separado realiza trabajo neto distinto de cero en un
% ciclo completo (positivo para la externa, negativo para la disipativa, como es
% de esperar*), pero en cada momento se cancelan mutuamente. Esto es
% importantísimo ya que asegura que la amplitud del sistema no diverja incluso
% en la frecuencia de resonancia (donde la transferencia de energía asociada a
% la fuerza externa es máxima).

% * Analizar qué ocurre cambiando la frecuencia de la fuerza externa

% Finalmente podemos calcular el trabajo acumulado desde el tiempo inicial hasta
% cada instante del tiempo. Para esto usamos la función cumsum, que suma todos
% los elementos de un vector y los coloca en un nuevo vector y coloca las sumas
% parciales en cada elemento del vector resultado. Ejemplo, si x = [ 1, 3, 4 ]
% obtenemos cumsum(x) = [ 1, 4, 8 ].

W_res = [ 0, cumsum(dW_res) ];      % con esta notación agregamos un 0 al principio de cada vector
W_dis = [ 0, cumsum(dW_dis) ];
W_ext = [ 0, cumsum(dW_ext) ];

figure
    hold all
    plot(t, W_res)
    plot(t, W_dis)
    plot(t, W_ext)
    plot(t, W_dis+W_ext)
    plot(t, zeros(size(t)), 'k--')  % linea de referencia en cero

    xlabel('Tiempo (s)')
    ylabel('W [N m]')
    legend('Elástica', 'Disipativa', 'Externa', 'Dis. + Ext.', 'Location', 'northwest')

    % Ademas imprimimos los valores finales de cada tabajo
    text(t(end), W_res(end), num2str(W_res(end)))
    text(t(end), W_dis(end), num2str(W_dis(end)))
    text(t(end), W_ext(end), num2str(W_ext(end)))

fprintf('Trabajo neto al final de la simulación, en J (chequear el valor de t_max):\n')
fprintf('- Elástico:    %.2f\n', W_res(end))
fprintf('- Disipativo:  %.2f\n', W_dis(end))
fprintf('- Externo:     %.2f\n', W_ext(end))
fprintf('- Dis. + Ext.: %.2f\n', W_dis(end)+W_ext(end))

fprintf('Potencia media en un ciclo (¿cuánto debe valer t_max?):\n')
fprintf('- Elástica:    %.2f\n',  W_res(end) / t_max)
fprintf('- Disipativa:  %.2f\n',  W_dis(end) / t_max)
fprintf('- Externa:     %.2f\n',  W_ext(end) / t_max)
fprintf('- Dis. + Ext.: %.2f\n', (W_dis(end)+W_ext(end)) / t_max)


