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

#from guiqwt.plot import ImageDialog
#from guiqwt.builder import make

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
fig_width = 7 # width in inches #6.69 two column single 3.37
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
def PowerMW(dbm):
    # return np.sqrt(10**(dbm/10))
    return (10**(dbm/10))
    
def lineafit(x,mx,off):
    return mx * x + off    

def sqrtfit(x,mx,off):
    return mx * np.sqrt(x) + off   
    
#
plt.close()
g = -30
val = np.loadtxt('%s.txt' %g)
#val= val[:,:,np.newaxis]
while g < 5:
    g=g+1
    new = np.loadtxt('%s.txt' %g)
    val = np.hstack((val, new))
    
Values = val.reshape((2,6,36),order='F')    

power = np.arange(-30, 5.5, step = 1)

Up50 = Values[1,0,:]
Up70 = Values[1,1,:]
Up30 = Values[1,2,:]

ErrUp= np.array([Up50-Up30, Up70-Up50])
plt.errorbar(PowerMW(power), Up50, yerr= ErrUp, fmt='-o', capsize =5, label = 'HC2', color = 'orange')

popt, pcov = curve_fit(lineafit, PowerMW(power[0:20]), Up50[0:20])
plt.plot(PowerMW(power[0:20]),lineafit(PowerMW(power[0:20]),*popt),color= "red", label =" linear fit")

popt1, pcov = curve_fit(sqrtfit, PowerMW(power[0:20]), Up50[0:20])
plt.plot(PowerMW(power[0:20]),sqrtfit(PowerMW(power[0:20]),*popt1),color= "green", label =" sqrt(Power)")

plt.xlim(PowerMW(power[0]), PowerMW(power[22]))



# Down50 = Values[1,3,:]
# Down70 = Values[1,4,:]
# Down30 = Values[1,5,:]

# ErrDown= np.array([Down50-Down30, Down70-Down50])
# plt.errorbar(PowerMW(power), Down50, yerr= ErrDown, fmt='-o', capsize =5, label = 'HC1', color = 'blue')

# # popt2, pcov = curve_fit(sqrtfit, PowerMW(power[0:14]), Down50[0:14])
# # plt.plot(PowerMW(power[0:14]),sqrtfit(PowerMW(power[0:14]),*popt2), linestyle = 'dashed', label =" sqrt(Power)")
plt.xscale("log")






# g = -25
# val = np.loadtxt('%s_7.5to12.5GHz.txt' %g)
# #val= val[:,:,np.newaxis]
# while g < 5:
#     g=g+5
#     new = np.loadtxt('%s_7.5to12.5GHz.txt' %g)
#     val = np.hstack((val, new))
    
# Values = val.reshape((2,6,7),order='F')    

# power = np.arange(-25, 5.5, step = 5)

# Up50 = Values[1,0,:]
# Up70 = Values[1,1,:]
# Up30 = Values[1,2,:]

# ErrUp= np.array([Up50-Up30, Up70-Up50])
# plt.errorbar(PowerMW(power), Up50, yerr= ErrUp, fmt='--', capsize =3, label = 'HC2 7.5 Ghz', color = 'orange')

# Down50 = Values[1,3,:]
# Down70 = Values[1,4,:]
# Down30 = Values[1,5,:]

# ErrDown= np.array([Down50-Down30, Down70-Down50])
# plt.errorbar(PowerMW(power), Down50, yerr= ErrDown, fmt='--', capsize =3, label = 'HC1 7.5 Ghz', color = 'blue')


# g = -25
# val = np.loadtxt('%sold.txt' %g)
# #val= val[:,:,np.newaxis]
# while g < -5:
#     g=g+5
#     new = np.loadtxt('%sold.txt' %g)
#     val = np.hstack((val, new))
    
# Values = val.reshape((2,6,5),order='F')    

# power = np.arange(-25, -4.5, step = 5)

# Up50 = Values[1,0,:]
# Up70 = Values[1,1,:]
# Up30 = Values[1,2,:]

# ErrUp= np.array([Up50-Up30, Up70-Up50])
# # plt.errorbar(PowerMW(power), Up50, yerr= ErrUp, fmt='--', capsize =3, label = 'HC2 old', color = 'orange')
# plt.scatter(PowerMW(power), Up50,  label = 'HC2 old', color = 'k')

# Down50 = Values[1,3,:]
# Down70 = Values[1,4,:]
# Down30 = Values[1,5,:]

# ErrDown= np.array([Down50-Down30, Down70-Down50])
# # plt.errorbar(PowerMW(power), Down50, yerr= ErrDown, fmt='--', capsize =3, label = 'HC1 old', color = 'blue')
# plt.scatter(PowerMW(power), Down50,  label = 'HC1 old', color = 'g')









#plt.scatter(power, Up70)
#plt.scatter(power, Up30)

# plt.xlabel('sqrt(V)')
plt.xlabel('Power (mW)')
plt.ylabel('Field (mT)')#plt.scatter(power, Values[1,3,:])

plt.legend()
plt.show()
plt.tight_layout()
# plt.savefig('sqrtVoltageSwitchingFields.png', dpi=600)
# plt.savefig('-10dBmmWSwitchingFields.png', dpi=600)
plt.savefig('FitSqrtSwitchingFields.png', dpi=600)