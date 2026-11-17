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
#mpl.rc('font', serif='Arial') 
#mpl.rc('text', usetex='false') 


#plt.rcParams['mathtext.fontset'] = 'custom'
#plt.rcParams['mathtext.it'] = 'Arial:italic'
#plt.rcParams['mathtext.rm'] = 'Arial'
mpl.rcParams['font.sans-serif'] = 'Arial'
# Then, "ALWAYS use sans-serif fonts"
mpl.rcParams['font.family'] = "sans-serif"

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 4.5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width,fig_height*0.8]
#fig_size =  [7,8]
params = {'axes.labelsize': 9*st,   #'backend': 'eps',
          'legend.fontsize': 9*st,
          'xtick.labelsize': 9*st,
          'ytick.labelsize': 9*st,
          'text.usetex': False,
          'figure.figsize': fig_size}
plt.rcParams.update(params)
def MagneticField(dbm):
     # return (10**(dbm/10))
    # return 1000*(np.sqrt(50*1e-3*10**(dbm/10)))
    return 4*np.pi*1e-7*np.sqrt(1e-3*(10**(dbm/10))/(2*50*(2.1*1e-6)**2))*1e3
#    return dbm
    
def lineafit(x,mx,off):
    return mx * x + off    
    
#
plt.close()
g = -30
val1 = np.loadtxt('%s.txt' %g)
#val= val[:,:,np.newaxis]

# while g < -9:
while g < -15:
    g=g+1
    new1 = np.loadtxt('%s.txt' %g)
    val1 = np.hstack((val1, new1))
    
# Values1 = val1.reshape((2,6,22),order='F')   
Values1 = val1.reshape((2,6,16),order='F')   
g = -30
val2 = np.loadtxt('%s_m2.txt' %g)
#val= val[:,:,np.newaxis]
# while g < -9:
while g < -15:
    g=g+1
    new2 = np.loadtxt('%s_m2.txt' %g)
    val2 = np.hstack((val2, new2))
    
# Values2 = val2.reshape((2,6,22),order='F')
Values2 = val2.reshape((2,6,16),order='F')                       
Values = (Values1+Values2)/2                       

# power = np.arange(-30, -8.5, step = 1)
power = np.arange(-30, -14.5, step = 1)

Up50 = Values[1,0,:]
Up70 = Values[1,1,:]
Up30 = Values[1,2,:]

ErrUp= np.array([Up50-Up30, Up70-Up50])
plt.errorbar(MagneticField(power), Up50, yerr= ErrUp, fmt='-o', capsize =5, label = 'HC2', color = 'orange')

popt, pcov = curve_fit(lineafit, MagneticField(power), Up50)
plt.plot(MagneticField(power),lineafit(MagneticField(power),*popt), linestyle = 'dashed')

print(popt)


Down50 = Values[1,3,:]
Down70 = Values[1,4,:]
Down30 = Values[1,5,:]


popt1, pcov1 = curve_fit(lineafit, MagneticField(power), Down50)
print(popt1)
plt.plot(MagneticField(power),lineafit(MagneticField(power),*popt1), linestyle = 'dashed')

ErrDown= np.array([Down50-Down30, Down70-Down50])
plt.errorbar(MagneticField(power), Down50, yerr= ErrDown, fmt='-o', capsize =5, label = 'HC1', color = 'blue')

Field = MagneticField(power)*1000 #microTesla


# plt.xlabel('Voltage_rms (mV)')
plt.xlabel('h-rf (mT)')
# plt.xlabel('Power (mW)')
plt.ylabel('Field (mT)')#plt.scatter(power, Values[1,3,:])
# plt.xscale("log")
plt.legend()

plt.show()
plt.tight_layout()

plt.savefig('SwitchingFieldsFitting.pdf', dpi=600)