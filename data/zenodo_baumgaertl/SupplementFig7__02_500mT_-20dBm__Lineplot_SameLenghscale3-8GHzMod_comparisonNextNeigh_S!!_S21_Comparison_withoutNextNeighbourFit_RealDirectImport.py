import numpy as np
import scipy.io
import matplotlib.pyplot as plt
#from scipy import signal
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import copy
import matplotlib.ticker as ticker
#import guiqwt
import glob

Component = "MAG" #choose component
FieldMin = 500
FieldMax = -500

scale=0.05
stepmult=2


#
#
##==============================================================================
## define the Sparameter and its component
##==============================================================================
#SParam='S11'; #choose S-parameter
#Component = "MAG" #choose component
#FieldMin = 500
#FieldMax = 80
##==============================================================================
## define the folder for FMR analysis
##==============================================================================
##FolderName = "20161012_CoFeB_600s_FMR_UCPWB2_10Mto16G_1600p_1st" #specify up to before \store; no backslash!
#FolderName = "measurement"
#Object='SW_161111_26491_100'
##MeasFolder = FolderName +  "\store\MEAS\\" + SParam + "\\"
##RefFolder = FolderName +  "\store\REF\\" + SParam + "\\"
#
#NameDataA = "REAL";
#NameDataB = "IMAG";
#NameDataC = "MLIN";
#NameFreq = "freq";
#
##==============================================================================
## Magentic field (start field and increment)
##==============================================================================
#field = np.genfromtxt("measurement.txt", skip_header= 2, dtype = str)[:,1]
#field = np.char.replace(field, ";","")
#magField = np.zeros((len(field)))
#for i in range(len(field)):
#    magField[i] = float(field[i])
#    
#
#
#
##SParam='S21'; #choose S-parameter
#Component = "MAG" #choose component
##FieldMin = -18
##FieldMax = 6
#
#
#
#Address = FolderName + "\\MEAS\\" + SParam + "\\"
#file_name_listReal = glob.glob(Address+'*REAL*')
#file_name_listImag = glob.glob(Address+'*IMAG*')
#file_name_listMLIN = glob.glob(Address+'*MLIN*')
##
#MeasDataA = np.loadtxt(file_name_listReal[0])
#for file_name in file_name_listReal[1:]:
#     MeasDataA = np.vstack((MeasDataA, np.loadtxt(file_name)))
##     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
#MeasDataA1a = copy.deepcopy(np.swapaxes(MeasDataA,0,1))
#
#MeasDataB = np.loadtxt(file_name_listImag[0])
#for file_name in file_name_listImag[1:]:
#     MeasDataB = np.vstack((MeasDataB, np.loadtxt(file_name)))
##     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
#MeasDataB1a = copy.deepcopy(np.swapaxes(MeasDataB,0,1))
#
#
#MeasDataC = np.loadtxt(file_name_listMLIN[0])
#for file_name in file_name_listMLIN[1:]:
#     MeasDataC = np.vstack((MeasDataC, np.loadtxt(file_name)))
##     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
#MeasDataC1a = copy.deepcopy(np.swapaxes(MeasDataC,0,1))
#
#
#file_name_listFreq = glob.glob(Address+'*freq*')
#Freq = np.loadtxt(file_name_listFreq[0])
#
#
#
#
#DataAv = np.median(MeasDataA1a,axis=1)
#DataAv2 = np.median(MeasDataB1a,axis=1)
#DataAv3 = np.median(MeasDataC1a,axis=1)
#
#
#
#
#
#
#
#
#
#
#
##subtract the data with reference value
#DeltaMeasDataA = MeasDataA1a - DataAv[:,np.newaxis] 
#DeltaMeasDataB = MeasDataB1a - DataAv2[:,np.newaxis] 
#DeltaMeasDataC = MeasDataC1a - DataAv3[:,np.newaxis] 
##DeltaMeasDataA = MeasDataA 
##DeltaMeasDataB = MeasDataB 
#DeltaAmplitude = np.sqrt(DeltaMeasDataA **2 + DeltaMeasDataB **2)
##Amplitude=np.sqrt(MeasDataA **2 + MeasDataB **2)
#
#NumMeas = np.size(MeasDataA1a,1)
#
#ProcessData = MeasDataC1a
##NumMeas = np.size(MeasDataA,1)
#NumFreq = len(Freq)
#
#ProcessDataNeighbor = np.zeros((len(Freq), NumMeas-1))
#for i in range(NumMeas-1):
#    ProcessDataNeighbor[:,i] = ProcessData[:, i+1] - ProcessData[:, i]
#
#
#
#ProcessData2=MeasDataA1a
#
#
#ProcessDataNeighborReal = np.zeros((len(Freq), NumMeas-1))
#for i in range(NumMeas-1):
#    ProcessDataNeighborReal[:,i] = ProcessData2[:, i+1] - ProcessData2[:, i]
#
#    
#    
##MagNN=np.sqrt(ProcessDataNeighborReal**2+ProcessDataNeighborImag**2)
#
#
#
#NumMeas = np.size(MeasDataA,1)
#


##


start=0.075
stop=16

f0 = 9.5
StartFieled=260


# index111 = np.where(magField==90)
# index1=index111[0]  

indexST1 = np.where(magField==StartFieled)
indexST=indexST1[0]  

#plt.plot(Freq*1e-9,(MeasDataA[:,indexST[0]]),color='k',linewidth=0.5)

#
#plt.xlim(start,stop)
#plt.grid(True)
#plt.ylim(-0.0015*7,0.0015*7)
#plt.xlabel("Frequency (GHz)")

    
#Testdata = MeasDataA -  AvMeasDataA[:,np.newaxis]
Testdata1 = DeltaMeasDataA
Testdata2 = DeltaMeasDataB 
Testdata3 = DeltaMeasDataC 

Testdata = np.sqrt(Testdata1**2+Testdata2**2)

#Testdata = Testdata3

from guiqwt.widgets.fit import FitParam, guifit

FreqMin = 1.25
FreqMax = 10
FreqGHz= Freq*1e-9

idx = int((np.abs(FreqGHz-FreqMax)).argmin())
idxMin = int((np.abs(FreqGHz-FreqMin)).argmin())

def test():
    x = FreqGHz[idxMin:idx]

    y = Testdata[idxMin:idx,indexST[0]]
    pos111 = np.argmax(y)
    
    f0 = x[pos111]
    
#    def fit(x, params):
#        a, b, c, Phase, x0, ww = params
#        return c*10e-3*np.cos(x*2*np.pi/(b*1e-3)+Phase)*np.exp(-(x-x0)**2/(2*ww**2))+a
#    
    
    def fit(x, params):
        Off, Cent, FWHM, Amp = params
        FWHM  = FWHM/1e3
        return Amp*1e-7*(1/np.pi)*0.5*FWHM/((x-Cent)**2+(0.5*FWHM)**2)+Off
    
    
    a = FitParam("Offset", 0., -0.1, 0.1)
    b = FitParam("Frequency (MHz)", f0, 1, 50)
    c = FitParam("FWHM", 20, 0., 100)
    Phase = FitParam("Amplitude", 1000, 0., 2000)
    # x0 = FitParam("Middel", f0, FreqMin, FreqMax)
#    x0 = FitParam("Middel", ( min + max )/2. , 0., 5)
    # ww = FitParam("FWHM", 33, 0.001, 100)
    params = [a, b, c, Phase]
    values = guifit(x, y, fit, params, xlabel="f (GHz)", ylabel="Power (a.u.)")
    
    print(values)
    print([param.value for param in params])

#if __name__ == "__main__":
#    test()

test()