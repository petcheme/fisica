%%

clear variables
close all

clc


% parametros de entrada
T   = 1;        % N
mu1 = 1;        % kg/m
mu2 = 2;        % kg/m

L    = 1;       % longitud de la cuerda, m
alfa = .2;      % punto de union, adim


% parametros derivados
c1 = sqrt(T/mu1);
c2 = sqrt(T/mu2);
g  = sqrt(mu2/mu1);                 % c1 / c2


% ecuacion trascendental para hallar los k permitidos
k1_eje = linspace(0, 15, 10000);
f1 = tan(k1_eje*g*L*(alfa-1));
f2 = g*tan(k1_eje*alfa*L);

figure
%     subplot(2,1,1)
        hold all
        plot(k1_eje, f1, '.')
        plot(k1_eje, f2, '.')
        ylim([-20, 20])
        
        xlabel('k_1')
        ylabel('f_i(k_1)')
        legend('f1', 'f2', 'Location', 'SouthEast')

% version alternativa
%     subplot(2,1,2)
%         hold all
%         plot(k1_eje, g*f1 ./ f2, '.')
%         plot([ k1_eje(1), k1_eje(end) ], g*[1,1], 'k-')
%         ylim([ -2*g, 2*g])
% 
%         xlabel('k_1')
%         ylabel('f_i(k_1)')
%         legend('f1 / f2', 'g', 'Location', 'SouthEast')


% determino valores posibles de k1 y muestro la solución

% para mu2 = 2:
% k1 = 2.247;            % modo 1
k1 = 4.601;             % modo 2

% para mu2 = 10:
% k1 = 1.014;             % modo 1
% k1 = 2.106;             % modo 2



k2 = k1*g;

omega = c1*k1;          % \_ son lo mismo
%omega = c2*k2;         % /


eje_x = linspace(0, L, 1000);
eje_t = linspace(0, 10*2*pi/omega, 5000);

onda_total = zeros(size(eje_x));
idx1 = eje_x <= alfa*L;
idx2 = not(idx1);

figure
hold all

A = 1;
B = A*sin(k1*alfa*L) / sin(k2*L*(alfa-1));

for i = 1:length(eje_t)

    % muestro la onda en las dos partes de la cuerda
    onda_total(idx1) = A*sin(k1*eje_x(idx1))*cos(omega*eje_t(i));
    onda_total(idx2) = B*sin(k2*(eje_x(idx2) - L))*cos(omega*eje_t(i));
    
    plot(eje_x(idx1), onda_total(idx1), 'linewidth', 2)
    plot(eje_x(idx2), onda_total(idx2), 'linewidth', 2)

    % muestro la continuacion de la solucion en cada tramo a lo largo del
    % oootro tramo
    onda_total(idx1) = B*sin(k2*(eje_x(idx1) - L))*cos(omega*eje_t(i));
    onda_total(idx2) = A*sin(k1*eje_x(idx2))*cos(omega*eje_t(i));
    
    plot(eje_x(idx1), onda_total(idx1), '--', 'linewidth', 2, 'color', [ 0.850, 0.325, 0.098 ])
    plot(eje_x(idx2), onda_total(idx2), '--', 'linewidth', 2, 'color', [ 0, 0.447, 0.741 ])
    
    
    [ val, pos ] = max(abs(onda_total));
    plot(eje_x(pos), onda_total(pos), 'xk')
    
    xlabel('x')
    ylabel('Psi')
    ylim([-1,1])
    pause(.01)
    cla
    
end






