%%

% 04-oct-2017

clear variables
close all

clc

% parametros del sistema

L  = .005;	% momento angular
m  = 1;     % masa
k  = 1;     % cte elástica
l0 = 1;     % long de reposo


% parametros para el grafico

n_pts = 1000;
min_r = 1e-3;
max_r = 1e1;

%r = linspace(      min_r,        max_r,  n_pts);
r = logspace(log10(min_r), log10(max_r), n_pts);         % <- preferimos espaciado logaritmico


% calculo de los potenciales

pot_elastico = 1/2*k*(r - l0).^2;
pot_angular  = L^2 / 2 / m ./ r.^2;

pot_efectivo = pot_angular + pot_elastico;


% graficos

color_palette = [ 213,  94,   0 ;
                  204, 121, 167 ;
                    0, 114, 178 ; 
                  240, 228,  66 ;
                    0, 158, 115 ;
                  150, 150, 150 ] / 255;

figure
    hold all

    x_pos = 2.01e-3;
    y_pos = 4;
    
    plot(r, pot_elastico, ...
         'linewidth', 2, 'color', color_palette(1,:) )

    for n = 0:2:6
        plot(r, pot_angular*10^n + pot_elastico, ...
             'linewidth', 2, 'color', color_palette(3,:) )
        
        plot(r, pot_angular*10^n, 'color', color_palette(6,:))
        
        text(x_pos*10^(n/2), y_pos, sprintf('L = %.2g', L*10^(n/2)))
    end

    % repito el plot para que el trazo resalte
    plot(r, pot_elastico, ...
         'linewidth', 3, 'color', color_palette(1,:) )
    
    legend('U_{k}', 'U_{ef}', 'U_{L}', 'Location', 'BestOutside')

    xlabel('Distancia radial')
    ylabel('Energia')
    
    title('Masa unida a una fuerza elástica central')
    
    set(gca, 'XScale', 'log')
    ylim([ 0 5 ])

    set(gcf, 'Position', [ 500 500 1000 500 ])
    
        
