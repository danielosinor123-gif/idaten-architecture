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

mpl.rcParams['xtick.major.size'] = 3
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.size'] = 2
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.size'] = 3
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.size'] = 1.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['pdf.fonttype'] = 42
font = {'size'   : 9}
mpl.rc('font', **font)
mpl.rc('font', family='sans-serif') 
mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams['font.family'] = "sans-serif"

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 3.37*1.5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width*0.5,fig_height*0.6]
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

StartFreq = 1.0
EndFreq=  13.0
# EndFreq=  3.0
Step = 0.25



def Con(dB):
    return 10**(dB/10)
    # return np.log10(10**(dB/10))

FreqMesh = np.arange(StartFreq,EndFreq+1.5*Step,Step)
magMesh = np.arange(-26.5,6.6,1)

magMesh = Con(magMesh)


X,Y = np.meshgrid(FreqMesh, magMesh)

Mode3com = np.load('SumFull2.npy')
Mode1com = np.load('SumFull1.npy')
Values = np.load('PhaseDiagramN.npy')
# plt.imshow(Mode3com)

Up50 = Con(Values[1,0,:])
Up70 = Con(Values[1,1,:])
Up30 = Con(Values[1,2,:])

ErrUp= np.array([Up50-Up30, Up70-Up50])
# plt.errorbar(PowerMW(power), Up50, yerr= ErrUp, fmt='-o', capsize =5, label = 'HC2', color = 'orange')




Down50 = Con(Values[1,3,:])
Down70 = Con(Values[1,4,:])
Down30 = Con(Values[1,5,:])

ErrDown= np.array([Down50-Down30, Down70-Down50])



im =plt.pcolormesh(X,Y ,Mode3com)
plt.colorbar(im)
plt.errorbar(Values[1,6,:]+Step/2, Down50, yerr= ErrDown, fmt='-o', capsize =2.5,  color = 'k',linestyle = "None", markersize=2, elinewidth=0.5)


np.savetxt('S21fieldlist.txt', Values[1,6,:]) 
np.savetxt('S21Power.txt', Up50) 
np.savetxt('S21Power70%.txt', Up70) 
np.savetxt('S21Power30%.txt', Up30) 
np.savetxt('S11Power.txt', Down50) 
np.savetxt('S11Power30%.txt', Down30) 
np.savetxt('S11Power70%.txt', Down70) 

plt.xlim(StartFreq,EndFreq+1.0*Step)
# plt.xlim(StartFreq,3.25)
plt.yscale('log')
plt.ylim(Con(-25), Con(6))
plt.xlabel('Frequency(GHz)')
plt.ylabel('P_crit (mW)')
plt.tight_layout()
# plt.savefig("CPW2_14mTPhaseDia.pdf",dpi=400)

