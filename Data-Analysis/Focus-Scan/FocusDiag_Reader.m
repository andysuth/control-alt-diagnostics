
clear
close all hidden

%% Constants
qE=1.60217657e-19; %electron charge in Coulomb
c0=299792458; %m/s
Epsilon0= 8.854e-12;
ElectronMass=9.10938291e-31;
ElectronMasseV=0.510999; %MeV
kB=1.3806488e-23;
torrToPa=133.322368;
In2mm=25.4;
rmstogauss=sqrt(8*log(2));

%% set default plotting
set(groot, 'defaultAxesTickLabelInterpreter','latex');
set(groot, 'defaultLegendInterpreter','latex');
set(groot, 'defaultGraphplotInterpreter','latex');
set(groot, 'defaultTextInterpreter','latex');
set(groot, 'defaultAxesYGrid','on')
set(groot, 'defaultAxesXGrid','on')
set(groot, 'defaultAxesBox','on')
set(groot, 'defaultAxesYMinorTick','on')
set(groot, 'defaultAxesXMinorTick','on')
set(groot, 'defaultAxesYMinorGrid','on','defaultAxesYMinorGridMode','manual')
set(groot, 'defaultAxesXMinorGrid','on','defaultAxesXMinorGridMode','manual')

%% Define directory

pathToDir = 'L:\EXPDATA\2025\2502\250207\FocusDiag\Morning\';
flist = dir([pathToDir, '*.tiff']);
calibration = 0.93;

stepSettings = [];
backgroundFiles = [];
maskFlag = 1;
threshold =[5 100];

plotFirst = 1;

%% Extract unique step settings and background files
[uniqueStepSettings, numericStepSettings, backgroundFiles] = extract_step_settings(pathToDir);

%% Load background data
bgData = load_background(pathToDir, backgroundFiles);

%% Display results and check
disp('Unique step settings:');
disp(uniqueStepSettings);

disp('Background files found:');
disp(backgroundFiles);

userResponse = input('Continue? (y/n): ', 's');

if lower(userResponse) ~= 'y'
    disp('Exiting script.');
    return;
end
disp('Beginning analysis...');


%% Start analysis

if ~exist('calibration','var') || ~isempty(calibration)
    calibration = 1;
    units = 'px';
else
    units = '/mu m';
end

for i=1:length(uniqueStepSettings)
    stepList=dir(string(join([pathToDir,'*',uniqueStepSettings(i),'*.tiff'],'')));
    for j=1:length(stepList)
        
        cam = Tiff([pathToDir, stepList(j).name]);
        camData = double(read(cam))-bgData;
       
        if maskFlag == 1
            threshmask = max(camData,[],'all')*threshold./100;
            camData(camData<threshmask(1))=threshmask(1);
            camData(camData>threshmask(2))=threshmask(2);
            camData=camData-threshmask(1);
             camData(camData<0) = 0;
        end
        
        SE = strel('cube',3);
        focImg = imopen(camData, SE); %filter noise
        
        x = 1:size(camData,1);
        y=1:size(camData,2);
        [X, Y] = meshgrid(y,x);
        
        %calculation of the center via the filtered data
        foc_centerx(j) = (sum(X.*focImg)/sum(focImg));
        foc_centery(j) = (sum(Y.*focImg)/sum(focImg));
      
        %calculation of the second momentum
        foc_widthx(j) = sqrt(sum(focImg.^2.*(X-foc_centerx(j)).^2)/sum(focImg.^2)); %rms widths calculated from 2nd moments of image
        foc_widthy(j) = sqrt(sum(focImg.^2.*(Y-foc_centery(j)).^2)/sum(focImg.^2)); %rms widths calculated from 2nd moments of image
               
        if plotFirst == 1 && j == 1
            figure(1)
            set(gcf,'Position',[1 49 1920 955])
            subplot(ceil(length(uniqueStepSettings)/5),5, i)
            hold on
            
            imagesc(y, x, focImg) % Plot image
            title(uniqueStepSettings(i))
            
            % Ellipse parameters
            theta = linspace(0, 2*pi, 100); % Angle for ellipse
            ellipseX = foc_widthx(j) * cos(theta) + foc_centery(j);
            ellipseY = foc_widthy(j) * sin(theta) + foc_centerx(j);
            
            % Plot ellipse
            plot(ellipseY, ellipseX, 'r', 'LineWidth', 1);
            
            axis tight
            axis image
            colorbar
        end
        
    end
    
    CenterX(i) = mean(foc_centerx); CenterSX(i) = std(foc_centerx);
    CenterY(i) = mean(foc_centery);  CenterSY(i) = std(foc_centery);
    
    WidthX(i) = mean(foc_widthx)*rmstogauss; WidthSX(i) = std(foc_widthx)*rmstogauss;
    WidthY(i) = mean(foc_widthy)*rmstogauss;  WidthSY(i) = std(foc_widthy)*rmstogauss;
    
        
end
WidthX = WidthX*calibration;
Widthy = WidthY*calibration;
WidthSX = WidthSX*calibration;
WidthSY = WidthSY*calibration;


%% Fit Laser Focus Profile to Beam Width Data

% Laser focus profile equation: w(x) = w0 * sqrt(1 + ((x - x0)/zR)^2)
laserFocusEqn = @(p, x) p(1) * sqrt(1 + ((x - p(2)) / p(3)).^2);

% Initial guesses for fitting parameters:
% p(1) = minimum beam waist w0 (approx min width),
% p(2) = focus position x0 (middle of range),
% p(3) = Rayleigh range zR (estimated as 1/4 of step range).
initParams = [min(WidthX), mean(numericStepSettings), range(numericStepSettings) / 4];

% Fit for WidthX
pX = lsqcurvefit(laserFocusEqn, initParams, numericStepSettings, WidthX');

% Fit for WidthY
pY = lsqcurvefit(laserFocusEqn, initParams, numericStepSettings, WidthY');

% Generate fitted curves
xFit = linspace(min(numericStepSettings), max(numericStepSettings), 1000); % Generate a smooth x range for plotting
WidthX_fit = laserFocusEqn(pX, xFit); % Calculate the fit values for each x
WidthY_fit = laserFocusEqn(pY, xFit);

% Focus position (minimum waist)
focusX = pX(2);
focusY = pY(2);


%% Plot Results
figure()
hold on
errorbar(numericStepSettings, WidthX, WidthSX, WidthSX, 'o', 'MarkerFaceColor', 'b', 'DisplayName', 'WidthX Data');
errorbar(numericStepSettings, WidthY, WidthSY, WidthSY, 'o', 'MarkerFaceColor', 'r', 'DisplayName', 'WidthY Data');

plot(xFit, WidthX_fit, 'b-', 'LineWidth', 2, 'DisplayName', 'Laser Focus Fit X');
plot(xFit, WidthY_fit, 'r-', 'LineWidth', 2, 'DisplayName', 'Laser Focus Fit Y');

% Mark estimated focus positions
xline(focusX, '--b', ['Focus X: ', num2str(focusX, '%.2f')], 'LabelHorizontalAlignment', 'left');
xline(focusY, '--r', ['Focus Y: ', num2str(focusY, '%.2f')], 'LabelHorizontalAlignment', 'left');

% Mark estimated w0
yline(pX(1), '--b', ['Spot X: ', num2str(pX(1), '%.2f')], 'LabelHorizontalAlignment', 'left');
yline(pY(1), '--r', ['Spot Y: ', num2str(pY(1), '%.2f')], 'LabelHorizontalAlignment', 'left');

set(gcf,'Position', [260 261 1352 634])
xlabel('Step Setting ($\mathrm{\mu}$m)');
ylabel('Beam Width ($\mathrm{\mu}$m)');
legend();
title('Laser Focus Fit to Beam Width Data');
grid on
hold off

%% Calculate a0 and plot scaling

Area = pX(1)*pY(1)*pi*1e-8;
Energy = linspace(0,2,100);
Duration = 35e-15;

Intensity = Energy./Area./Duration;

EField = sqrt(Intensity.*1e4.*2/c0/Epsilon0);
a0 = qE*EField*800e-9/ElectronMass/(2*pi*c0)/c0;

figure()
plot(Energy,a0)
xlabel('Energy (J)')
ylabel('$a_0$')
title('a0 Scaling for calculated spot size')
set(gca,'FontSize',14)

