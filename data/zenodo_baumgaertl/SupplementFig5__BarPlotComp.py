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
mpl.rc('font', serif='Arial') 
mpl.rc('text', usetex='false') 

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 3.37 # width in inches #6.69 two column single 3.37
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
Step = 0.25
values = np.loadtxt('PhaseDiagram.txt')

S11v = np.loadtxt('PhaseDiagramS11VNA14mT.txt')
S11v[1,:] = 1/S11v[1,:]


def Con(dB):
    return 10**(dB/10)



man = copy.deepcopy(values[2,:])
man = np.nan_to_num(man, copy=True, nan=7)

scaling = np.min(Con(man))/ np.min(S11v[1,:])

print(scaling)

S11v[1,:]  = (S11v[1,:])*scaling





#plt.facecolor('xkcd:salmon')
#plt.rcParams['axes.facecolor'] = 'xkcd:salmon'
plt.rcParams['axes.facecolor'] = 'snow'
plt.bar(values[0,:]+0.5*Step,Con(man)-Con(-35),width=0.25,bottom=Con(-35),color = 'dimgray')
plt.bar(S11v[0,:]+0.5*Step,S11v[1,:],width=0.1,color =  'orange')
#plt.hlines(y=Con(-15),xmin=1,xmax=13.25)

#plt.ylim
#plt.fill_between(values[0,:]+0.5*Step,Con(values[2,:]),color="red")
#plt.bar(values[0,:]+0.5*Step,values[1,:]-6, width=0.24, label= "CPW1")
#plt.legend(loc=1)
#set_major_locator(ticker.MultipleLocator(5))

plt.ylim(Con(-25),Con(6))
plt.yscale('log')
plt.xlim(1,13.25)

plt.xlabel('Frequency(GHz)')
plt.ylabel('P_crit (mW)')
plt.tight_layout()
plt.savefig("Comparison.pdf",dpi=500)