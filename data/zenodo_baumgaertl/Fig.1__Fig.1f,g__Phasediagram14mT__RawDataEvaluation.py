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
# EndFreq=  1.25
Step = 0.25

 #StartFreq = 1.75
 #EndFreq=  6
 #Step = 10.25

freq = np.arange(StartFreq,EndFreq+0.5*Step,Step)

Values = np.zeros((2,7,len(freq)))
Mode1com = np.zeros((33, len(freq)))
Mode3com = np.zeros((33, len(freq)))
y = 0
while StartFreq <= EndFreq: 
     newpath = str(round(StartFreq,2))
     os.chdir(newpath)


     Folder1 = 'After'
     Folder2 = 'Meas'
    
     SParam='S21'; #choose S-parameter
     Component = "MAG" #choose component

    
    
    
     FolderName = "measurement"
    
    
     os.chdir(Folder1)
    

     Address = FolderName + "\\MEAS\\" + SParam + "\\"
     file_name_listReal = glob.glob(Address+'*REAL*')
     file_name_listImag = glob.glob(Address+'*IMAG*')
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
    
    
    
     DataAv = np.median(MeasDataA1a,axis=1)
     DataAv2 = np.median(MeasDataB1a,axis=1)
    
    
    
    
     os.chdir('..')
     os.chdir(Folder2)
    
     Address = FolderName + "\\MEAS\\" + SParam + "\\"
     file_name_listReal = glob.glob(Address+'*REAL*')
     file_name_listImag = glob.glob(Address+'*IMAG*')
     #
     MeasDataA = np.loadtxt(file_name_listReal[0])
     for file_name in file_name_listReal[1:]:
           MeasDataA = np.vstack((MeasDataA, np.loadtxt(file_name)))
     #     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
     MeasDataA = np.swapaxes(MeasDataA,0,1)
    
     MeasDataB = np.loadtxt(file_name_listImag[0])
     for file_name in file_name_listImag[1:]:
           MeasDataB = np.vstack((MeasDataB, np.loadtxt(file_name)))
     #     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
     MeasDataB = np.swapaxes(MeasDataB,0,1)
    
    
     file_name_listFreq = glob.glob(Address+'*freq*')
     Freq = np.loadtxt(file_name_listFreq[0])
     os.chdir('..')
    
    
     DataType = 'REAL (ab. sub)'
    
     Data = MeasDataA
    
     Data = Data - DataAv[:,np.newaxis] 
    
    
    
     Data2  = MeasDataB
    
     Data2 = Data2  - DataAv2[:,np.newaxis] 

     DataMag = np.sqrt(Data**2+Data2**2)
     DataFilt = DataMag
    
    
 #    fig, ax1 = plt.subplots(1,1)
    
     z_max=0.00025
    
     magField1=np.arange(-26,6.1,1)

 #    plt.pcolormesh(magField1, Freq*1e-9, DataFilt ,cmap='Greys', rasterized=True)


     indexX1 = np.argmin(np.abs(Freq - 8.3*1e9))
     indexX2 = np.argmin(np.abs(Freq - 8.7*1e9))
     Mode1=np.sum(DataFilt[indexX1:indexX2,:],axis=0)
     Mode1com[:,y] = Mode1
 #    plt.scatter(magField1,Mode1)

    
     indexX3a = np.argmin(np.abs(Freq - 9.1*1e9))
     indexX3b = np.argmin(np.abs(Freq - 9.5*1e9))
     Mode3=np.sum(DataFilt[indexX3a:indexX3b,:],axis=0)
     Mode3com[:,y] = Mode3
 #    plt.scatter(magField1,Mode3)
    
     m1low = 0.003266782650440199
     m1high = 0.014507043801769783
    
     m3low = 0.0034872665208233416
     m3high = 0.008983068247055297
    



     FiftyPC = 0.5*(m1high-m1low)+m1low
     SeventyPC = 0.7*(m1high-m1low)+m1low
     ThirtyPC = 0.3*(m1high-m1low)+m1low
    
    
     def Hrise(Boundary):
         i=1
         while Mode1[i] < Boundary:
             i = i+1
             if i == len(magField1):
                 break
         if i< len(magField1):
             return (Boundary-Mode1[(i-1)])/(Mode1[i]-Mode1[(i-1)])+magField1[(i-1)]
         else:
             return np.nan
    
    

     Values[0,0,y] = FiftyPC
     Values[0,1,y] = SeventyPC
     Values[0,2,y] = ThirtyPC
    
     Values[1,0,y] = HFiftyPC = Hrise(FiftyPC)
     Values[1,1,y] = HSeventyPC = Hrise(SeventyPC)
     Values[1,2,y] = HThirtyPC = Hrise(ThirtyPC)
    
    
    
     FiftyPCD = 0.5*(m3high-m3low)+m3low
     SeventyPCD = 0.7*(m3high-m3low)+m3low
     ThirtyPCD = 0.3*(m3high-m3low)+m3low
    
    
     def Hfall(Boundary):
         i=1
         while Mode3[i] > Boundary:
             i = i+1 
             if i == len(magField1):
                 break
         if i< len(magField1):
             return (Boundary-Mode3[i-1])/(Mode3[i]-Mode3[(i-1)])+magField1[(i-1)]
         else:
             return np.nan
    
        
     Values[0,3,y] = FiftyPCD
     Values[0,4,y] = SeventyPCD
     Values[0,5,y] = ThirtyPCD
     #
     Values[1,3,y] = HFiftyPCfall = Hfall(FiftyPCD)
     Values[1,4,y] = HSeventyPCfall = Hfall(SeventyPCD)
     Values[1,5,y] = HThirtyPCfall = Hfall(ThirtyPCD)


        
     Values[0,6,y]=StartFreq
     Values[1,6,y]=StartFreq 

            
     os.chdir('..')

     StartFreq  =  StartFreq + Step        
     y = y+1
    
np.save('PhaseDiagramN.npy', Values)
np.save('SumFull1.npy', Mode1com)
np.save('SumFull2.npy', Mode3com)



###
#Plot
###



Mode3com = np.load('SumFull2.npy')
Mode1com = np.load('SumFull1.npy')
Values = np.load('PhaseDiagramN.npy')



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
np.savetxt('S21Power.txt', Up50*1000) 
np.savetxt('S21Power70%.txt', Up70*1000) 
np.savetxt('S21Power30%.txt', Up30*1000) 
np.savetxt('S11Power.txt', Down50*1000) 
np.savetxt('S11Power30%.txt', Down30*1000) 
np.savetxt('S11Power70%.txt', Down70*1000) 

plt.xlim(StartFreq,EndFreq+1.0*Step)
# plt.xlim(StartFreq,3.25)
plt.yscale('log')
plt.ylim(Con(-25), Con(6))
plt.xlabel('Frequency(GHz)')
plt.ylabel('P_crit (mW)')
plt.tight_layout()














