# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:16:17 2017

@author: andys

Electron Energy spectrum and analysis of VSim plasma simulation
"""

import matplotlib as mpl
mpl.use('Agg') 

from matplotlib import pyplot as mplt
import numpy as np
import h5py

from matplotlib import ticker as mtick

from scipy import stats


ScalarFormatter = mtick.ScalarFormatter

mplt.rcParams['font.family'] = 'DejaVu Sans'
mplt.rcParams['mathtext.fontset'] = 'custom'
mplt.rcParams['font.sans-serif'] = "DejaVu Sans"
mplt.rcParams['mathtext.cal'] = 'DejaVu Sans'
mplt.rcParams['mathtext.it'] = 'DejaVu Sans:italic'
mplt.rcParams['mathtext.rm'] = 'DejaVu Sans'
mplt.rcParams['text.usetex'] = False
hfont = {'fontname':'Courier'}
mplt.rcParams['font.size'] = 12
mplt.rcParams['figure.figsize'] = (7, 4)

qE = 1.6021766208e-19


pathToData     = "//lustre//scratch//x_suthera//space30//"
figFolder       ="Images//"
prefix         = "spaceScanConf30"
speciesList      = ["HElecLaser", "HeElecLaser"] #Name of electron species
dumpNumbers    = np.arange(35, 100 + 1) # range of dump numbers
collisionDump  = 40 #dump where beam reaches laser focus

timeStep = 1.92153e-13 - 9.60665e-14  #temporal spacing between two dumps

timeRange      =(dumpNumbers-collisionDump)*100 # dump number range converted into time

xFOCUS = 1.0e-3
zSHIFT = 150.0e-6 #for every tens unit in label, add 50microns 

dumpmin         = np.amin(dumpNumbers)

hdf5_file_name =  "%s%s_" % (pathToData, prefix)


gas = "Helium"
#gas = "Hydrogen"


class elecDump:
    """Create object for assigning electron attributes"""
    
    def __init__(self, hdf5_file_name, dumpNumber, species):
        self.dumpSpecies            = species
        self.dumpNumber             = dumpNumber
        self.path                   = hdf5_file_name + str(species) + "_" + str(dumpNumber) + ".h5"
        self.X      = 0
        self.Y      = 0
        self.Z      = 0         
        self.PX     = 0
        self.PY     = 0
        self.PZ     = 0
        self.Weight = 0
        self.E      = 0
        
        self.numPtclsInMacro = 0
        
    def loadDump(self) :
        if h5py.is_hdf5(self.path) == False or self.path.find(".h5") == -1:
                print("   (!) No .h5 file found: ")
                print(self.path)
                print(" loading skipped")
        else:
            f = h5py.File(self.path, 'r')
            fData = np.array(f[self.dumpSpecies], dtype=np.float32)
            
            self.X      = fData[:,0]
            self.Y      = fData[:,1]
            self.Z      = fData[:,2]         
            self.PX     = fData[:,3]
            self.PY     = fData[:,4]
            self.PZ     = fData[:,5]
            self.Weight = fData[:,7] 
  
            gammaCol              = np.sqrt((self.PX**2+self.PY**2+self.PZ**2)/(299792458.0**2))
            self.E  = 0.511*(np.sqrt(1+gammaCol**2)-1)*1e6
            self.EX = 0.511*(np.sqrt(1+(self.PX/299792458.)**2-1))*1e6
            self.EY = 0.511*(np.sqrt(1+(self.PZ/299792458.)**2-1))*1e6   
            self.EZ = 0.511*(np.sqrt(1+(self.PY/299792458.)**2-1))*1e6  
            self.numPtclsInMacro = int(round(f[self.dumpSpecies].attrs["numPtclsInMacro"]))
            
            f.close()
            print(str(self.dumpSpecies)+ "_" + str(self.dumpNumber) + " successfully loaded ")
            
    def columnCut(self, radius) :
        pos = np.sqrt((self.X-xFOCUS)**2 + (self.Z-zSHIFT)**2)
        print str(len(pos[pos<radius])) + " " + self.dumpSpecies + " macroparticles removed"
        if len(pos[pos<radius]) > 0:
            self.E = self.E[pos>radius]
            self.EX = self.EX[pos>radius]
            self.EY = self.EY[pos>radius]
            self.EZ = self.EZ[pos>radius]
            self.Weight = self.Weight[pos>radius]
            self.X = self.X[pos>radius]
            self.Y = self.Y[pos>radius]
            self.Z = self.Z[pos>radius]
        else:
            return
            
    def totalCharge(self):
        if isinstance(self.Weight, int):
            return 0
        else:
            return sum(self.Weight)*self.numPtclsInMacro*qE

    def totalEnergy(self):
        if isinstance(self.Weight, int):
            return 0
        else:
            return sum(np.multiply(self.Weight, self.E))*self.numPtclsInMacro  
    
        
def calculateYield(energy,charge,gas):
    #Gives output in nC
    c0 = 299792458
    density = 6.5e22
    if gas == "Helium":
        a1 = 0.745
        a2 = 0.6174
        I  = 24.6
    elif gas == "Hydrogen":
        a1 = 0.695
        a2 = 1.5668
        I  = 15.4
    else:
        print " gas not recognised "
        return
            
        
    energy[energy<I] = 0
            
    gamma = (energy*1.60218e-19)/(9.11e-31*(3e8)**2)+1;
    beta = (1-(1/gamma**2))**(0.5);
    funcB = 2*I/0.511e6/beta**2*(0.511e6*beta**2/2/I-1)
            
    xsect = 1.872e-24*a1/(beta**2)*funcB*(np.log(7.515e4*a2*beta**2*gamma**2)-beta**2)
    
    return xsect*beta*c0*density*(charge*1e9)
        

    
def moving_average(a, n=3):
    moving_aves = []
    if n%2 == 0:
        raise Exception(" n must be odd ")
    else:
        nside=(n-1)/2
        for i, x in enumerate(a):
            if nside-i>=0:
                moving_ave = (sum(a[0:i+nside+1])/(len(a[0:i+nside+1])))
                moving_aves.append(moving_ave) 
            elif i>nside:
                moving_ave = (sum(a[i-nside:i+nside+1])/n)
                moving_aves.append(moving_ave) 
            elif i+nside >= len(a):
                moving_ave = (sum(a[(i-nside):])/(len(a[(i-nside):])))
                moving_aves.append(moving_ave) 
            else: 
                raise Exception()
    return moving_aves

    
class ScalarFormatterForceFormat(ScalarFormatter):
    def _set_format(self, vmin, vmax):
        self.format = "%1.1f"
        
def histPlot(bins, data, instaYield, timestep, title, cutdata=False):
    fig, ax = mplt.subplots()
    ar = ax.fill_between(bins, data*1e9, color='#ff7575', label='$\mathrm{r<w_0}$' )
    ax.set_xlabel('$E\mathrm{_{kin}}$ (eV)')
    ax.set_ylabel('$Q$ $\mathrm{(nC\hspace{0.4} 10eV^{-1})}$')
    ax.set_xscale('log')
    #ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0) )
    ymft = ScalarFormatterForceFormat()
    ymft.set_powerlimits((0,0))
    ax.yaxis.set_major_formatter(ymft)
    
    

    axRight = ax.twinx()
    axRight.plot(bins[:len(instaYield)],instaYield, color='k', label="Impact Ionization Yield")
    axRight.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axRight.set_ylabel('$R$ $\mathrm{(nC\hspace{0.4} s^{-1}\hspace{0.4} 10eV^{-1})}$')   
    axRight.locator_params(nbins=5, axis='y')
    
    ymft = ScalarFormatterForceFormat()
    ymft.set_powerlimits((0,0))
    axRight.yaxis.set_major_formatter(ymft)
    
    ax.locator_params(nbins=5, axis='y')  
    ax.spines['left'].set_color('red')
    ax.yaxis.label.set_color('red')
    ax.tick_params(axis='y', colors='red')
    ax.yaxis.get_offset_text().set_color('red')
    ax.set_title(r'$\Delta t\mathrm{_{kick}} \approx %s $fs' %(timestep))
    
    if not (isinstance(cutdata, bool) and cutdata == False):
        ar = ax.fill_between(bins, cutdata*1e9, color='#ff2B2B', label='$\mathrm{r\geq w_0}$')
        
    ax.legend(fontsize=9)
    
    mplt.savefig(pathToData + figFolder + prefix + "Hist_" + title + ".png", format = "png", dpi = 300, bbox_inches='tight')
    mplt.close(fig)

runCharge=np.zeros(len(dumpNumbers))
runEnergy=np.zeros(len(dumpNumbers))   
runHCharge=np.zeros(len(dumpNumbers))
runHeCharge=np.zeros(len(dumpNumbers))
runHEnergy=np.zeros(len(dumpNumbers))
runHeEnergy=np.zeros(len(dumpNumbers))
runCharge=np.zeros(len(dumpNumbers))
runEnergy=np.zeros(len(dumpNumbers))
runHeYield=np.zeros(len(dumpNumbers))
runHYield=np.zeros(len(dumpNumbers))
runYield=np.zeros(len(dumpNumbers))
for i in dumpNumbers:  
     

    Htorch = elecDump(hdf5_file_name, i, speciesList[0])
    Htorch.loadDump()
    Hetorch = elecDump(hdf5_file_name, i, speciesList[1])
    Hetorch.loadDump()
    
    Hhistdata, histbins  = np.histogram(Htorch.E, bins=int(1e5/10), range=(0, 1e5), weights=(Htorch.Weight*Htorch.numPtclsInMacro*qE))
    Hehistdata, histbins  = np.histogram(Hetorch.E, bins=int(1e5/10), range=(0, 1e5), weights=(Hetorch.Weight*Hetorch.numPtclsInMacro*qE))
    
    Htorch.columnCut(38e-6)
    Hetorch.columnCut(38e-6)
    

    HCharge = Htorch.totalCharge()
    print(" Hydrogen Electron Charge = " + str(HCharge*1e9) + "nC")
    

    HeCharge = Hetorch.totalCharge()
    print(" Helium Electron Charge = " + str(HeCharge*1e9) + "nC")
    
    Charge = np.add(HCharge,HeCharge)
    print(" Total Electron Charge = " + str(Charge*1e9) + "nC")
    
    HEnergy = Htorch.totalEnergy()
    print(" Total  Hydrogen Electron KineticEnergy = " + str(HEnergy) + "eV")
    
    HeEnergy = Hetorch.totalEnergy()
    print(" Total Helium Electron Kinetic Energy = " + str(HeEnergy) + "eV")
    
    Energy = np.add(HEnergy, HeEnergy)
    print(" Total Electron Kinetic Energy = " + str(Energy) + "eV")
    
    runHCharge[i-dumpmin]=HCharge
    runHeCharge[i-dumpmin]=HeCharge
    runHEnergy[i-dumpmin]=HEnergy
    runHeEnergy[i-dumpmin]=HeEnergy
    runCharge[i-dumpmin]=Charge
    runEnergy[i-dumpmin]=Energy
    

    
    cutHhistdata, histbins  = np.histogram(Htorch.E, bins=int(1e5/10), range=(0, 1e5), weights=(Htorch.Weight*Htorch.numPtclsInMacro*qE))
    cutHehistdata, histbins = np.histogram(Hetorch.E, bins=int(1e5/10), range=(0, 1e5), weights=(Hetorch.Weight*Hetorch.numPtclsInMacro*qE))
    histbins = (np.delete(histbins,len(histbins)-1))-5

    histdata = np.add(Hhistdata, Hehistdata)
    cuthistdata = np.add(cutHhistdata, cutHehistdata)
    HinstantYield = np.nan_to_num(calculateYield(histbins, cutHhistdata, gas))
    HeinstantYield = np.nan_to_num(calculateYield(histbins, cutHehistdata, gas))
    instantYield = np.nan_to_num(calculateYield(histbins, cuthistdata, gas))
    
    runHYield[i-dumpmin]=sum(HinstantYield)
    runYield[i-dumpmin]=sum(instantYield)
    runHeYield[i-dumpmin]=sum(HeinstantYield)
    
    Hmoving_aves = moving_average(HinstantYield, n=9)
    Hemoving_aves = moving_average(HeinstantYield, n=9)
    moving_aves = moving_average(instantYield, n=9)
    
    
    histPlot(histbins,Hhistdata,Hmoving_aves,(i-dumpmin)*100, "H_" + str(i), cutHhistdata)
    histPlot(histbins,Hehistdata,Hemoving_aves,(i-dumpmin)*100, "He_" + str(i), cutHehistdata)
    histPlot(histbins,histdata,moving_aves,(i-dumpmin)*100, "All_" + str(i), cuthistdata)
        

    print(" Dump Analysis Complete! ")
    print("\n")
    
             
fig, (ax1, ax2, ax3) = mplt.subplots(3, 1, sharex = True, figsize = (7,6))
ax1.plot(timeRange, runHCharge*1e9, label='H2')
ax1.plot(timeRange, runHeCharge*1e9, label='He')
ax1.plot(timeRange, runCharge*1e9, label='Both')
ax1.set_ylabel('$Q\mathrm{_{kick} (nC)}$')
ax1.set_title("Total Charge")
ax1.legend(fontsize=9)
ax2.plot(timeRange, runHEnergy, label='H2')
ax2.plot(timeRange, runHeEnergy, label='He')
ax2.plot(timeRange, runEnergy, label='Both')
ax2.set_title("Total Kinetic Energy")
ax2.set_ylabel('$E\mathrm{_{kin} (eV)}$')
ax3.plot(timeRange, runHYield, label='H')
ax3.plot(timeRange, runHeYield, label='He')
ax3.plot(timeRange, runYield, label='Both')
ax3.set_ylabel('$R$ $\mathrm{(nC\hspace{0.4} s^{-1})}$')
ax3.set_xlabel('$t\mathrm{_{sim} (fs)}$')
mplt.savefig(pathToData + figFolder + prefix + "_Totals.png", format = "png", dpi = 300, bbox_inches='tight')
mplt.close(fig)

maxE = np.amax(runEnergy)
imaxE = np.argmax(runEnergy)
print("Maximum kinetic energy of cut electrons =" + str(maxE) + "eV, occuring in dump " + str(imaxE + collisionDump) + "($t\mathrm{_{kick}} = $" + str((imaxE)*100) + "fs)")
                       
a = np.column_stack((timeRange, runHCharge, runHeCharge, runCharge, runHEnergy, runHeEnergy, runEnergy, runHYield, runHeYield, runYield))
np.savetxt(pathToData + figFolder + prefix  + "_specSummary.txt", a, delimiter='    ')

def round_to_1(x):
    return round(x, -int(np.floor(np.log10(abs(x))))) 
    
cumHYield = np.cumsum(runHYield)*timeStep*1e3
Hslope = stats.linregress(timeRange*1e-3, cumHYield)
print("Hydrogen linear fit slope = " + str("{:.4e}".format(Hslope[0])) + " pC/ps")

cumHeYield = np.cumsum(runHeYield)*timeStep*1e3
Heslope = stats.linregress(timeRange*1e-3, cumHeYield)
print("Helium linear fit slope = " + str("{:.4e}".format(Heslope[0])) + " pC/ps")

cumYield = np.cumsum(runYield)*timeStep*1e3
slope = stats.linregress(timeRange*1e-3, cumYield)
print("Hydrogen + Helium linear fit slope = " + str("{:.4e}".format(slope[0])) + " pC/ps")

        
lineX = np.linspace(min(timeRange*1e-3), max(timeRange*1e-3), 10)
    
fig, (ax1, ax2, ax3) = mplt.subplots(3, 1, sharex = True, figsize = (7,6))            
ax1.plot(timeRange*1e-3, cumHYield, "blue", label='H2')
ax1.plot(lineX, Hslope[1] + Hslope[0]*lineX, "blue", ls = "--", label = "y = " + str("{:.4e}".format(Hslope[0])) + "x + " + str("{:.4e}".format(Hslope[1])))
ax1.legend(loc=2, fontsize=9)
ax1.set_ylabel('$Q\mathrm{_{impact}}$ $\mathrm{(ps)}$')

ax2.plot(timeRange*1e-3, cumHeYield, "green", label='He')
ax2.plot(lineX, Heslope[1] + Heslope[0]*lineX, "green", ls = "--", label = "y = " + str("{:.4e}".format(Heslope[0])) + "x + " + str("{:.4e}".format(Heslope[1])))
ax2.legend(loc=2, fontsize=9)
ax2.set_ylabel('$Q\mathrm{_{impact}}$ $\mathrm{(pC)}$')

ax3.plot(timeRange*1e-3, cumYield, "red", label='Both')
ax3.plot(lineX, slope[1] + slope[0]*lineX, "red", ls = "--", label = "y = " + str("{:.4e}".format(slope[0])) + "x + " + str("{:.4e}".format(slope[1])))
ax3.legend(loc=2, fontsize=9)
ax3.set_ylabel('$Q\mathrm{_{impact}}$ $\mathrm{(pC)}$')
ax3.set_xlabel('$t\mathrm{_{sim}}$ $\mathrm{(ps)}$')
mplt.savefig(pathToData + figFolder + prefix + "_YieldFits.png", format = "png", dpi = 300, bbox_inches='tight')
mplt.close(fig)