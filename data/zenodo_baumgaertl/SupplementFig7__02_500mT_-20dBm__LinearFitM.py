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
    return slope*x

Field = np.array([500,480,460,440,420,400,380,360,340,320,300,280,260])
#-10 to -4 
Freq1 =np.array([8.27,	7.743,	7.232,	6.712,	6.189,	5.684,	5.178,	4.695,	4.223,	3.783,	3.337,2.824,	2.29])
FWHM1 = np.array([40.21,	40.028,	38.609,	45.347,	43.114,37.312,	38.373,	34.455,	31.865,	29.705,	26.783,	25.354,	25.795])*1e-3

def Kittel(Field,Ms, gamma):
    return gamma*(Field-Ms)*1e-3


#def Kittel(Field, gamma):
#    return gamma*(Field-182)*1e3

#plt.scatter(Freq1, FWHM1)
#
popt1, pcov = curve_fit(Kittel, Field, Freq1)
plt.plot(Field,Kittel(Field,*popt1),color= "green")
print(popt1)
# 
#plt.xlabel("Resonance Frequency (GHz)")
#plt.ylabel("FWHM (GHz)")
#plt.savefig("Fitt.jpg", dpi = 600)#plt.scatter(Freq1, FWHM1)
#

plt.scatter(Field, Freq1)
plt.xlabel("Field (mT)" )
plt.ylabel("Freq (GHz)" )