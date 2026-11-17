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
# import matplotlib.ticker as plticker
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
fig_width = 4 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width,fig_height]
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
    
# def fit(x, Off, Cent, FWHM, Amp):     
#     FWHM  = FWHM/1e3
#     return Amp*(1/np.pi)*0.5*FWHM/((x-Cent)**2+(0.5*FWHM)**2)+Off

def Voltage(dbm):
      return np.sqrt(50*(10**(dbm/10)*1e-3))

S11a = np.loadtxt('AMplitudesS11.txt') 
S11aErr =   np.loadtxt('AMplitudesS11Err.txt') 

S11b = np.loadtxt('AMplitudesS11b.txt') 
S11bErr =   np.loadtxt('AMplitudesS11Errb.txt') 

# fig, (ax1, ax2,ax3, ax4, ax5) = plt.subplots(5, 1)
# ax1.scatter(S11a[0,:], S11a[5,:])
# ax1.scatter(S11b[0,:], S11b[5,:])
# ax1.set_ylabel('Amplitude')
# ax5.scatter(S11a[0,:], S11a[5,:]*Voltage(S11a[0,:]))
# ax5.scatter(S11b[0,:], S11b[5,:]*Voltage(S11a[0,:]))
# ax5.set_ylabel('Amplitude* Voltagr')

# ax2.errorbar(S11a[0,:], S11a[2,:], yerr=S11aErr[1,:])
# ax2.errorbar(S11b[0,:], S11b[2,:], yerr=S11bErr[1,:])
# ax2.set_ylabel('f_res(GHz)')
# ax3.scatter(S11a[0,:], S11a[3,:])
# ax3.scatter(S11b[0,:], S11b[3,:])
# ax3.set_ylabel('FWHM (MHz)')
# ax4.scatter(S11a[0,:], S11a[4,:])
# ax4.scatter(S11b[0,:], S11b[4,:])
# ax4.set_xlabel('Power (dBm)')
# ax4.set_ylabel('Sum Gauss')
# def PowerMW(dbm):
#       return (10**(dbm/10))
#     # indexx = np.searchsorted(S11a[0,:], int(dbm))
#     # return 1000*(np.sqrt(50*1e-3*10**(dbm/10)))
#     # return 1000*((50*1e-3*10**(dbm/10)))
#     # return 1000*((50*1e-3*10**(dbm/10)))*S11a[4,:]
#     # return 1000*(np.sqrt(50*1e-3*10**(dbm/10)))*np.sqrt(S11a[4,:])
    


# def ResonaceShif(power,wres,Proportionality):
#     Voltage = PowerMW(power)
#     return wres+Proportionality*Voltage**2
# #
# popt, pt = curve_fit(ResonaceShif, S11a[0,:], S11a[2,:])

# #ax2.plot(S11a[0,:], ResonaceShif(S11a[0,:],*popt))
# #plt.errorbar(PowerMW(S11a[0,:]),S11a[2,:],yerr=S11aErr[1,:])
# #plt.xscale('log')
# #plt.ylabel("F_res (GHz)")
# #plt.xlabel('Power (mW)')
# plt.tight_layout()
# plt.savefig('2Nonlinearity.pdf')

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Power (dBm)')
ax1.set_ylabel('f-res', color=color)
ax1.errorbar(S11a[0,:], S11a[2,:],yerr=S11aErr[1,:], color=color, capsize=2)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('FWHM', color=color)  # we already handled the x-label with ax1
ax2.errorbar(S11a[0,:], S11a[3,:]*1e-3,yerr=S11aErr[2,:]*1e-3, color=color,  capsize=2)
ax2.tick_params(axis='y', labelcolor=color)
loc = ticker.MultipleLocator(base=5.0) # this locator puts ticks at regular intervals
ax2.xaxis.set_major_locator(loc)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
plt.savefig("S11_nonlinearity.pdf",dpi=600)