import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import copy
import matplotlib.ticker as ticker
import glob

import os.path as osp, numpy as np

from guiqwt.plot import ImageDialog
from guiqwt.builder import make

mpl.rcParams['xtick.major.size'] = 1.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.size'] = 2
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.size'] = 1.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.size'] = 1.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['pdf.fonttype'] = 42
font = {'size'   : 9}
mpl.rc('font', **font)
mpl.rc('font', family='sans-serif') 
mpl.rc('font', serif='Arial') 
mpl.rc('text', usetex='false') 

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width*3,fig_width]
#fig_size =  [7,8]
params = {'axes.labelsize': 9*st,   #'backend': 'eps',
          'legend.fontsize': 9*st,
          'xtick.labelsize': 9*st,
          'ytick.labelsize': 9*st,
          'text.usetex': False,
          'figure.figsize': fig_size}
plt.rcParams.update(params)
#

import os



Startpower = -30
Endpower = 5
Step = 1

Power1 = np.arange(Startpower,Endpower+0.5*Step,Step)
Power1.astype(int)
values = np.zeros((6,len(Power1)))
valuesErr = np.zeros((5,len(Power1)))
#
#values = np.zeros((3,len(freq)))
#
#
#y = 0
a=0
for g in Power1: 

# g = l
    
    Power = '%sdBm' %(int(g))
    
    #==============================================================================
    # define the Sparameter and its component
    #==============================================================================
    SParam='S11'; #choose S-parameter
    Component = "MAG" #choose component
    FieldMin = -10
    FieldMax = 40
    #==============================================================================
    # define the folder for FMR analysis
    #==============================================================================
    #FolderName = "20161012_CoFeB_600s_FMR_UCPWB2_10Mto16G_1600p_1st" #specify up to before \store; no backslash!
    
    
    FolderName = "measurement"
    Object='SW_161111_26491_100'
    MeasFolder = FolderName +  "\store\MEAS\\" + SParam + "\\"
    RefFolder = FolderName +  "\store\REF\\" + SParam + "\\"
    
    NameDataA = "REAL";
    NameDataB = "IMAG";
    NameDataC = "MLIN";
    NameFreq = "freq";
    
    os.chdir('..')
    os.chdir(Power)
    
    #==============================================================================
    # Magentic field (start field and increment)
    #==============================================================================
    field = np.genfromtxt("measurement.txt", skip_header= 2, dtype = str)[:,1]
    field = np.char.replace(field, ";","")
    magField = np.zeros((len(field)))
    for i in range(len(field)):
        magField[i] = float(field[i])
        
    with open('set_vna.txt') as f:
        lines = f.readlines()[7]
        lines=lines.replace("power level:","")
        lines=lines.replace(";","")
        PowerLevel=int(lines)
    with open('set_vna.txt') as f:    
        lines = f.readlines()[2]
        lines=lines.replace("start frequency: ","")
        lines=lines.replace(";","")
        FreqStart=float(lines)
    with open('set_vna.txt') as f:    
        lines = f.readlines()[3]
        lines=lines.replace("stop frequency: ","")
        lines=lines.replace(";","")
        FreqEnd=float(lines)
        
        
    magstep=magField[5]-magField[4]
    #
    Address = FolderName + "\\MEAS\\" + SParam + "\\"
    file_name_listReal = glob.glob(Address+'*REAL*')
    file_name_listImag = glob.glob(Address+'*IMAG*')
    file_name_listMLIN = glob.glob(Address+'*MLIN*')
    #
    MeasDataA = np.loadtxt(file_name_listReal[0])
    for file_name in file_name_listReal[1:]:
         MeasDataA = np.vstack((MeasDataA, np.loadtxt(file_name)))
    #     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
    MeasDataA1a = copy.deepcopy(np.swapaxes(MeasDataA,0,1))
    
    MeasDataB = np.loadtxt(file_name_listImag[0])
    for file_name in file_name_listImag[1:]:
         MeasDataB = np.vstack((MeasDataB, np.loadtxt(file_name)))
    #     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
    MeasDataB1a = copy.deepcopy(np.swapaxes(MeasDataB,0,1))
    
    
    MeasDataC = np.loadtxt(file_name_listMLIN[0])
    for file_name in file_name_listMLIN[1:]:
         MeasDataC = np.vstack((MeasDataC, np.loadtxt(file_name)))
    #     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
    MeasDataC1a = copy.deepcopy(np.swapaxes(MeasDataC,0,1))
    
    
    file_name_listFreq = glob.glob(Address+'*freq*')
    Freq = np.loadtxt(file_name_listFreq[0])
    
    
    DataAv = np.median(MeasDataA1a,axis=1)
    DataAv2 = np.median(MeasDataB1a,axis=1)
    # DataAv = np.min(MeasDataA1a,axis=1)
    # DataAv2 = np.min(MeasDataB1a,axis=1)
    
    #subtract the data with reference value
    DeltaMeasDataA = MeasDataA1a - DataAv[:,np.newaxis] 
    DeltaMeasDataB = MeasDataB1a - DataAv2[:,np.newaxis] 
    
    
    os.chdir('..')
    os.chdir('EvaluationNonLinearity')
    
     
    DataMag = np.sqrt(DeltaMeasDataA**2+DeltaMeasDataB**2)


    fig, (ax1, ax2) = plt.subplots(1, 2)
    z_max=0.025
    magField1=np.arange(-10.5,41,1)
    ax1.pcolormesh(magField1, Freq*1e-9, DataMag,cmap='Greys', vmin=0, vmax=z_max,rasterized=True)  
    ax2.plot(DataMag[:,0],Freq*1e-9)
    
    def fit(x, Off, Cent, FWHM, Amp):     
        FWHM  = FWHM/1e3
        return Amp*(1/np.pi)*0.5*FWHM/((x-Cent)**2+(0.5*FWHM)**2)+Off
    
    popt, pcov = curve_fit(fit, Freq*1e-9, DataMag[:,0], p0=[0,1.71,80,0.01])
    perr = np.sqrt(np.diag(pcov))
    valuesErr[0,a] = perr[0]
    valuesErr[1,a] = perr[1]
    valuesErr[2,a] = perr[2]
    valuesErr[3,a] = perr[3]
    valuesErr[4,a] = (2*1e3/np.pi)*np.sqrt((perr[3]/popt[2])**2+((perr[2]*popt[3])/popt[2]**2)**2)
    
    plt.plot(fit(Freq*1e-9,*popt), Freq*1e-9)
    # plt.plot(fit(Freq*1e-9,*[0,1.71,100,0.04]), Freq*1e-9)
    Amplitude = popt[3]*2/(np.pi*popt[2]/1e3)
    print(str(Amplitude)+str('+/-')+ str(valuesErr[4,a]))
    values[0,a] = g
    values[1,a] = popt[0]
    values[2,a] = popt[1]
    values[3,a] = popt[2]
    values[4,a] = popt[3]
    values[5,a] = Amplitude
    
    
    a=a+1


# ax2.plot(DataMag[:,3],Freq*1e-9)
# ax2.plot(DataMag[:,20],Freq*1e-9)
#        plt.pcolormesh(magField, Freq*1e-9, Data,cmap='seismic', vmin=z_min, vmax=z_max,rasterized=True)

#        
# 
# ax1.set_xlim(-0.5, 40.5)

# ax1.set_ylim(7,12.5)

# fig.tight_layout()
    plt.savefig('%s_MagGreyS11.jpg'% (Power),dpi=600)
    plt.close()
    
    
np.savetxt('AMplitudesS11.txt', values)
np.savetxt('AMplitudesS11Err.txt', valuesErr)
plt.errorbar(values[0,:], values[5,:], yerr=valuesErr[4,:])

# #np.savetxt('Mode1_%s.txt'% Power, Uvalues.T)
# #plt.close()

    
    

