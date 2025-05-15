%% Torch Macro Designer
%
%
% Created 15 Sept 2019
% Andrew Sutherland
%
% Define global grid parameters to match those found in the prefile.
% Define shape
% Generate form and compute metrics
% export to txt format for loading to vorpal
%
close all
clear all
%% Constants
global w0 E0 tau R0 Epsilon0 qE mE

qE=1.60217657e-19; %electron charge in Coulomb
c0=299792458; %Speed of light (m s^-1)
Epsilon0= 8.854e-12; %Free space Permitivity
mE=9.10938291e-31; %electron mass(kg)
kB=1.3806488e-23; %Boltzmann constant (m^2 s^-2kg K^-1)
torrToPa=133.322368; % pressure conversion
JtoeV=6.242e+18; %Energy Conversion


density = 7e20;
p_wavelength = 200e-6; %actually skin depth

%% FLAGS

writematrix = 0; %1: Create and save VSim matrix. 0: Imaging purposes only.
restart = 0;
calc_charge = 0;

%%%%%%%
%% Global Grid Parameters
% Need a grid that represents PARTICLE positions, can be derived from
% gloabal grid and PPC numbers. Match the numbers here with the ones
% being used in the prefile.

%particles per cell
PPX = 2;
PPY = 2;
PPZ = 2;

%Macroparticle size [m]
DX = 2.e-6/PPX;
DY = 2.e-6/PPY;
DZ = 2.e-6/PPZ;
DV = DX*DY*DZ;


% Used to determine vorpal timestep
DXI = 1/(PPX*DX);
DYI = 1/(PPY*DY);
DZI = 1/(PPX*DZ);

DS = 1 / sqrt(DXI*DXI + DYI*DYI + DZI*DZI);

% grid lengths
LX = 800e-6;
LY = 1000e-6;
LZ = 1000e-6;


%%%%%%%
%% Ionization Threshold

He = 24.587387; %eV
HePlus = 54.4; %eV
H = 13.6; %eV
Rb = 4.117; %eV
Ar = 15.76;

Thresh = He;

if Thresh == H
    TL = 'H';
elseif Thresh == He
    TL = 'He';
elseif Thresh == HePlus
    TL = 'He+';
elseif Thresh == Rb
    TL = 'Rb';
else
    TL = '';
end



%%%%%%%
%% Laser Settings


%a0 = 0.04224; %dimensionless amplitude
E = 1e-3; %pulse energy (J)
tau =  60e-15; %pulse length (s)

w0 = 15.5*1e-6; %spot size [1/e^2 radius] (m)
lmbda = 0.8e-6; %Laser central wavelength (m)
angFreq = 2*pi*c0/lmbda; %Angular frequency (rad s^-1)
R0 = pi*w0^2/lmbda; %Rayleigh length (m)

E0 = sqrt(755.82*(E/tau/pi/w0^2)); %Peak electric field (V m^-1)
critE = 5.14e11*(sqrt(2)-1)*(Thresh/27.2)^(3/2); %Tunnel ionisation critical electric field


if critE < E0
    warning('Maximum electric field of laser exceeds critical levels for tunnel ionisation.')
end


label = [num2str(w0*1e6,2) 'um_' num2str(E*1e6,2) 'uJ_' num2str(tau*1e15,'%2i') 'fs_' TL];

%%%%%%%%
%% Torch Formation
% first generate cuboid subgrid big enough to fit desired shape
% with grid resolution inherited from global parameters
% Vorpal coordinate system:
%        x is direction of beam
%        z is direction of laser

if writematrix ==1
    z=linspace(-45, 45, round(90e-6/DX)+1).*1e-6;
    x=linspace(-45, 45, round(90e-6/DY)+1).*1e-6;
    y=linspace(-LY/2, LY/2, round(LY/DY)+1);
elseif calc_charge ==1
    z=linspace(-40, 40, round(2*80e-6/DX)+1).*1e-6;
    x=z;
    y=linspace(-2*R0, 2*R0, 2*200);
else
    z=linspace(-65, 65, round(4*130e-6/DX)+1).*1e-6;
    x=[0 0];
    y=linspace(-2*R0, 2*R0, 4*200);
end
%{
z=linspace(-100, 100, 300).*1e-6;
x=[0 0];
y=linspace(2500, 2500, 200).*1e-6;
%}

t = linspace(-2*tau,2*tau,10);


[X,Y,Z,T] = ndgrid(x,y,z,t); % This matrix can get heavy, be careful

%%%%%%%%
%% Ionisation Probability
%Calculate the instantatneous ionisation rate for all time and space and then
%immediatley integrate over the pulse length to get total ionisation
%rate. The rate is then transformed into a an ionisation probability
%between 0 and 1, can also be interpreted as ionisation percentage.

ADKtemp = trapz(t,WADK(X,Z,Y,T,1,Thresh),4);
ionRatio = real(1-exp(-ADKtemp));

%%%%%%%%
%% Display result
% Just to make sure it looks right, uncomment if confident


map = figure('Units','normalized','Position',[0.2 0.1 0.35 0.8]);
top = max(max(max(ionRatio)));
bottom = min(min(min(ionRatio)));


image(z.*1e6, y.*1e6, squeeze(ionRatio(round(0.5*length(x)),:,:)), 'CDataMapping','scaled')
title(['E: ' num2str(E*1e3,3) ' mJ,      w$_0$: ' num2str(w0*1e6,3) '$\mu$m,     $\tau$: ' num2str(tau.*1e15) 'fs,    ' TL])
caxis manual
caxis([bottom 1])
h = colorbar;
ylabel(h, 'Ionisation Probability','interpreter','latex')
xlabel('$$z (\mu m)$$','interpreter','latex')
ylabel('$$y (\mu m)$$','interpreter','latex')

set(gca,'FontSize',16,'Layer','top');
axis xy



%waitforbuttonpress %If it looks good click the plot to continue
%saveas(1,[label '.png'])
%close;

if calc_charge
    DV = (x(2)-x(1))*(y(2)-y(1))*(z(2)-z(1));
    Total_charge = sum(ionRatio,'all')*density*qE*DV
    blowout_mask_Y =  abs(y)<p_wavelength;
    blowout_mask_Z = abs(z)<p_wavelength;
    blowout_charge = sum(ionRatio(:,blowout_mask_Y, blowout_mask_Z),'all')*density*qE*DV
end



%%%%%%%%%%
%% Export into data file


mask=(ionRatio>0.001);

%Flatten matrices into column vectors converting to VSim coordinates
Z1 = X(mask);

X1 = Z(mask);
X1 = X1(abs(Z1)<LX/2);

Y1 = Y(mask);
Y1 = Y1(abs(Z1)<LX/2);

Z1 = Z1(abs(Z1)<LX/2);

%empty columns for momentum vectors

Empty = zeros(length(X1),1);
W1 = ionRatio(mask);

% Master Matrix
M = cat(2,X1,Y1,Z1,Empty,Empty,Empty,W1);




if writematrix
    fileID = fopen([label '.dat'],'w');
    fprintf(fileID,'%2.16f %22.16f %22.16f %22.8f %22.8f %22.8f %22.16f\n',M(:,:,:,:,:,:,:)');
    fclose(fileID);
end

%% Generate temporal loading profile
% Under development/testing

timestep = 0.999998 * DS / c0;
simlength = 1.4e-3;
simTime = simlength/c0;
loadTime = LY/c0;

x_focus = 800e-6;
beam_start = 500e-6;

pathlength_to_focus = x_focus - beam_start;
time_to_focus = pathlength_to_focus/c0;

Ystart = -450e-6;
startTime = Ystart/c0;

if writematrix ==1
    
    i=-1; % elaborate but correct, trust me.
    complete = 0;
    
    for j = 0:timestep:loadTime
        i=i+1;
        
        if complete ==1
            %If the data writing is complete but there are timesteps left,
            %just create empty data files
            fileID = fopen(['TorusMacroDens_' num2str(i) '.dat'],'w');
            fclose(fileID);
            
        elseif j>=startTime
                %Write plasma shape in slices
                %Each new slice corresponds to an ionization front travelling at
                %the speed of light in one timestep
                
                if startTime < 0
                    %In this case the 'laser' has started inside the
                    %simulation and so we need to account for the ionisation that
                    %happened before we started the simulation
                    
                    mask =  Y1<(Ystart);
                    % Write data to file
                    
                    fileID = fopen(['TorusMacroDens_' num2str(i-restart) '.dat'],'w');
                    fprintf(fileID,'%2.16f %22.16f %22.16f %22.8f %22.8f %22.8f %22.16f\n',M(mask,:,:,:,:,:,:)');
                    fclose(fileID);
                    
                else
                    % The laser started outside the box so start writing at the
                    % edge of the simulation
                    i=i-1;
                    Ystart = -LY/2;
                end
                
                counter = 0;                
                if Ystart<LY/2
                    for n = Ystart:timestep*c0:LY/2
                        i=i+1;
                        counter=counter+1;
                        mask = Y1>=n & Y1<(n+(timestep*c0));
                        % Write data to file

                        fileID = fopen(['TorusMacroDens_' num2str(i-restart) '.dat'],'w');
                        fprintf(fileID,'%2.16f %22.16f %22.16f %22.8f %22.8f %22.8f %22.16f\n',M(mask,:,:,:,:,:,:)');
                        fclose(fileID);
                    end
                end 
                complete = 1;
                [num2str(counter) ' .dat files written starting at timestep ' num2str(i)]
                ['Object will be loaded at ' num2str(i*timestep*1e12,4) ' ps / ' num2str(i*timestep*c0*1e3,4) ' mm']
                
        else
            %If the data is to be loaded after some delay, create leading
            %empty data files
            fileID = fopen(['TorusMacroDens_' num2str(i) '.dat'],'w');
            fclose(fileID);
        end
    end
end



%%%%%%%
%% Function Definitions

function [ out ] = Efield( x, y, z, t )
%Efield returns the value of the laser pulse for any given space or time
global E0 tau w0
out = E0.*exp(-0.5.*(t./(tau/2.355)).^2).*exp(-(x./BeamWidth(z)).^2).*exp(-(y./BeamWidth(z)).^2).*(w0^2./BeamWidth(z).^2);
end

function [ Width ] = BeamWidth( z )
%BeamWidth returns the width of a given laser pulse shape at any given
%point on the pulses path z
global w0 R0
Width = w0.*sqrt(1+(z./R0).^2);

end

function [ out ] = nn( thresh, delZ )

out = 3.69.*delZ./(thresh^0.5);

end

function [ out ] = WADK( x, y, z, t, level, thresh )
% Ionisation probability for a given laser pulse distributed in r, z

out = 1.52e15.*((4^nn(thresh,level)).*thresh./(nn(thresh,level).*gamma(2.*nn(thresh,level)))) ...
    .*(20.5.*thresh^(3/2)./(Efield(x,y,z,t).*1e-9)).^(2.*nn(thresh,level)-1) ...
    .*exp(-6.83.*thresh^(3/2)./(Efield(x,y,z,t).*1e-9));
end


