%%

clear variables
close all

clc

% lamina de cuarto de onda fija aplicada a estado eliptico rotado

figure
    set(gcf, 'Position', [ 1000, 400, 400, 400 ])

    % defino estado elíptico
    Ex = 2;
    Ey = 1;
    J0  = [ Ex; 1i*Ey ];

    % lamina de cuarto de onda
    L = [ 1, 0  ;
          0, 1i ];
    
    for tita = linspace(0, 2*pi, 101) % pi/4

        % matriz de rotacion:
        R = [ cos(tita), -sin(tita) ;
              sin(tita),  cos(tita) ];
        
        % aplico lámina de cuarto de onda al estado rotado
        J1 = R * J0;            % estado rotado
        J2 = L * J1;            % estado final

        % resultado analitico
        %J3 = [  Ex*cos(tita) - 1i*Ey*sin(tita) ;
        %       -Ey*cos(tita) + 1i*Ex*sin(tita) ];
        
        % obtengo la trayectoria del campo electrico en el plano
        % transversal
        angulos = -linspace(0, 2*pi, 1000);
        E1_plot = real(J1 * exp(1i*angulos));
        E2_plot = real(J2 * exp(1i*angulos));

        % ploteo
        clf
        hold all
        plot(E1_plot(1,:), E1_plot(2,:))
        plot(E2_plot(1,:), E2_plot(2,:))

        xlim([-2, 2]*1.5)
        ylim([-2, 2]*1.5)
        title(sprintf('tita = %.2f pi', tita/pi))

        legend('J1', 'J2')
        set(gca, 'Position', [.1 .1 .8 .8 ])

        % diferencia de fase entre componentes para el estado resultante
        diff(angle(J2))
        atan2(Ex*sin(tita), -Ey*cos(tita)) - atan2(-Ey*sin(tita), Ex*cos(tita))   % <- usamos atan2 ya que atan nos da un resultado entre -pi/2 y pi/2 (cubre solo media vuelta en el círculo) 
        
        % diff(angle(J3))
        
        pause(.1)
    end
    