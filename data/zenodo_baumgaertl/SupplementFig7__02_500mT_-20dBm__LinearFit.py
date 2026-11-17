import numpy as np
import scipy.io
import matplotlib.pyplot as plt
#from scipy import signal
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import copy
import matplotlib.ticker as ticker

from scipy.optimize import leastsq
from scipy.optimize import curve_fit
#import guiqwt

#def linear(x,slope, offset):
#    return slope*x+offset

def linear(x,slope, offset):
    return slope*x + offset
#-10 to -4 
    
#S21
# Freq1 =np.array([8.2750,7.7480,	7.2340,	6.7120,	6.1900,	5.6860,	5.1830,	4.7000,	4.2270,	3.7870,	3.3400,	2.8270])
# FWHM1 = np.array([20.444	,16.184,	15.217,	19.423,	21.901,	18.241,	16.775,	14.813,	13.759,	12.703,	11.524,	9.741])*1e-3
# Freq1 =np.array([6.7120,	6.1900,	5.6860,	5.1830,	4.7000,	4.2270,	3.7870,	3.3400,	2.8270])
# FWHM1 = np.array([	19.423,	21.901,	18.241,	16.775,	14.813,	13.759,	12.703,	11.524,	9.741])*1e-3

#S11
Freq1 =np.array([8.27,	7.743,	7.232,	6.712,	6.189,	5.684,	5.178,	4.695,	4.223,	3.783,	3.337,2.824,	2.29])
FWHM1 = np.array([40.21,	40.028,	38.609,	45.347,	43.114,37.312,	38.373,	34.455,	31.865,	29.705,	26.783,	25.354,	25.795])*1e-3


plt.scatter(Freq1, FWHM1)

popt1, pcov = curve_fit(linear, Freq1, FWHM1)
plt.plot(Freq1,linear(Freq1,*popt1),color= "green")
print(popt1)
 
plt.xlabel("Resonance Frequency (GHz)")
plt.ylabel("FWHM (GHz)")
plt.savefig("Fitt.jpg", dpi = 600)
plt.savefig("Fitt.pdf", dpi = 600)