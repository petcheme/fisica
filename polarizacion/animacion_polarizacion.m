%%

% F2Q 1c 2018

clear variables
close all

clc

t_max     = 100;
z_max     = 10;
n_samples = 1000;

t = linspace(0, t_max, n_samples);
z = linspace(0, 4*pi, 60);


k=1;
omega=1;

figure

    for i = 1:n_samples

        E_x = cos(k*z - omega*t(i));
        E_y = sin(k*z - omega*t(i));

        subplot(1,2, 1 )
            hold all
        
            % vamos a redefinir
            % z -> x        % eje de propagacion
            % x -> y
            % y -> z
            
            plot3(z, E_x, E_y)
            plot3(z, zeros(size(z)), zeros(size(z)), 'r')

            for j = 1:2:60
                plot3(z(j)*[ 1, 1 ]', [ 0, E_x(j) ]', [ 0, E_y(j) ]', 'Color', 1 - [ 1 1 1 ]*j/60)
            end

            title(sprintf('t=%.1f (sample %d)', t(i), i))
            xlabel('z')
            ylabel('x')
            zlabel('y')

        view(50, 20)    % azimuth, elevation
        
        subplot(1,2, 2)
            hold all
        
            plot3(E_x, E_y, z)
            plot3(zeros(size(z)), zeros(size(z)), z, 'r')

            for j = 1:60
                plot3([ 0, E_x(j) ]', [ 0, E_y(j) ]', z(j)*[ 1, 1 ]', 'Color', 1 - [ 1 1 1 ]*j/60)
            end

            title('vista observador')
            xlabel('x')
            ylabel('y')
            zlabel('z')

            view(0, 90)    % azimuth, elevation        
        
        pause(0.1)
    
        subplot(1,2,1)
            cla
        subplot(1,2,2)
            cla
            

    end



