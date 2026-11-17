import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
#from scipy.optimize import leastsq
#from scipy.optimize import curve_fit
import copy
import matplotlib.ticker as ticker

mpl.rcParams['xtick.major.size'] = 3
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.size'] = 1.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.size'] = 3
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.size'] = 1.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['pdf.fonttype'] = 42
font = {'size'   : 9}
mpl.rc('font', **font)
mpl.rc('font', family='sans-serif') 
#matplotlib.rc('text', usetex='false') 
mpl.rcParams['font.sans-serif'] = 'Arial'
# Then, "ALWAYS use sans-serif fonts"
mpl.rcParams['font.family'] = "sans-serif"

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 6.69 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
#fig_size =  [fig_width*3,fig_height*2]
# fig_size =  [13,6.75]
# fig_size =  [6,2]
fig_size =  [3,2]
# fig_size =  [2,2]
params = {'axes.labelsize': 9*st,    #'backend': 'eps',
#          'text.fontsize': 9*st,
          'legend.fontsize': 9*st,
          'xtick.labelsize': 9*st,
          'ytick.labelsize': 9*st,
          'text.usetex': False,
          'figure.figsize': fig_size}
plt.rcParams.update(params)
"""
@author: swatanab
"""



#==============================================================================
# define the Sparameter and its component
#==============================================================================

Component = "MAG" #choose component
FieldMin = -30
FieldMax = 40

scale=0.1
stepmult=2

StartFieled=14
points=1





SParam='S21'; #choose S-parameter
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

#==============================================================================
# Magentic field (start field and increment)
#==============================================================================
field = np.genfromtxt("measurement.txt", skip_header= 2, dtype = str)[:,1]
field = np.char.replace(field, ";","")
magField = np.zeros((len(field)))
for i in range(len(field)):
    magField[i] = float(field[i])
#
#magField = magField[::-1]#flip the field direction

#==============================================================================
# S-parameter 
#==============================================================================
#load measurement MAT file
MeasDataA = scipy.io.loadmat(MeasFolder + NameDataA +".mat");
MeasDataB = scipy.io.loadmat(MeasFolder + NameDataB +".mat");
MeasDataC = scipy.io.loadmat(MeasFolder + NameDataC +".mat");
Freq = scipy.io.loadmat(MeasFolder + NameFreq +".mat");
RefDataA = scipy.io.loadmat(RefFolder + NameDataA +".mat");
RefDataB = scipy.io.loadmat(RefFolder + NameDataB +".mat");
RefDataC = scipy.io.loadmat(RefFolder + NameDataC +".mat");
#extract values from key of "Data" in MAT file
#flip the data with regard to magnetic field
#MeasDataA = MeasDataA["Data"][:,::-1]
#MeasDataB = MeasDataB["Data"][:,::-1]
#RefDataA = RefDataA["Data"][:,::-1]
#RefDataB = RefDataB["Data"][:,::-1]
#extract values from key of "Data" in MAT file
#flip the data with regard to magnetic field
MeasDataA = MeasDataA["Data"][:,:]
MeasDataB = MeasDataB["Data"][:,:]
MeasDataC = MeasDataC["Data"][:,:]
RefDataA = RefDataA["Data"][:,:]
RefDataB = RefDataB["Data"][:,:]
RefDataC = RefDataC["Data"][:,:]
Freq = Freq["Data"]
Freq = Freq[:,0]




AvMeasDataA = np.mean(MeasDataA,axis=1)
AvMeasDataC = np.mean(MeasDataC,axis=1)



MMeasDataA = np.median(MeasDataA,axis=1)
MMeasDataC = np.median(MeasDataC,axis=1)
#subtract the data with reference value
DeltaMeasDataA = MeasDataA - RefDataA
DeltaMeasDataB = MeasDataB - RefDataB
DeltaMeasDataC = MeasDataC - RefDataC


MedMeasDataA = MeasDataA - MMeasDataA[:,np.newaxis] 
MedMeasDataC = MeasDataC - MMeasDataC[:,np.newaxis] 

#DeltaMeasDataA = MeasDataA 
#DeltaMeasDataB = MeasDataB 
DeltaAmplitude = np.sqrt(DeltaMeasDataA **2 + DeltaMeasDataB **2)
Amplitude=np.sqrt(MeasDataA **2 + MeasDataB **2)
RawAbsorbtion=1-Amplitude

NumMeas = np.size(MeasDataA,1)

ProcessData = MeasDataC
NumMeas = np.size(MeasDataA,1)
NumFreq = len(Freq)

ProcessDataNeighbor = np.zeros((len(Freq), NumMeas-1))
for i in range(NumMeas-1):
    ProcessDataNeighbor[:,i] = ProcessData[:, i+1] - ProcessData[:, i]



ProcessData2=MeasDataA
ProcessData3=MeasDataB

ProcessDataNeighborReal = np.zeros((len(Freq), NumMeas-1))
for i in range(NumMeas-1):
    ProcessDataNeighborReal[:,i] = ProcessData2[:, i+1] - ProcessData2[:, i]


ProcessDataNeighborImag = np.zeros((len(Freq), NumMeas-1))
for i in range(NumMeas-1):
    ProcessDataNeighborImag[:,i] = ProcessData3[:, i+1] - ProcessData3[:, i]
    
    
MagNN=np.sqrt(ProcessDataNeighborReal**2+ProcessDataNeighborImag**2)


#Delay=0.0062 #in meter  0.0062
#
#phi=2*np.pi*np.fabs(Freq)*Delay/299792458
#chi=DeltaMeasDataA-1j*DeltaMeasDataB
#angle = np.angle(chi)
#Amp = np.abs(chi)
#Signal = Amp*np.exp((angle+phi[:,None])*1j)
#
#test=angle+phi[:,None]
#plotSparamete = Signal.real
#plotSparamete = Signal.imag
NumMeas = np.size(MeasDataA,1)


start=1
stop=16




index111 = np.where(magField==90)
index1=index111[0]  

indexST1 = np.where(magField==StartFieled)
indexST=indexST1[0]  

#plt.plot(Freq*1e-9,MeasDataA[:,0]-(np.average(MeasDataA[:,1:],axis=1)))

#offset=0.00075
#i=0
#for i in range(1):
##    plt.plot(time,cut_signal[i,:]+i*offset-cut_signal[0,:], label='%s GHz'%(round(i*0.1+4,2)))
##    plt.plot(Freq*1e-9,MeasDataA[:,indexST+i]-MeasDataA[:,index1[0]]+i*offset,linewidth=1,label='%s mT'%(round(40-i*2)))
##    plt.plot(Freq*1e-9,MeasDataA[:,indexST[0]+i]-MeasDataA[:,index1[0]]+i*offset,linewidth=1.5,label='%s mT'%(round(8-i*2)))
#    plt.plot(Freq*1e-9,ProcessDataNeighborReal[:,indexST[0]+i]+1*offset,linewidth=1.5,label='BE2-01 %s mT'%(round(10-i*2)))
##    plt.yscale('symlog')
##    plt.plot(time,cut_signal[i,:]+i*offset, label='%s GHz'%(round(i*0.1+4,2)))
#    plt.xlim(start,stop)
#    plt.grid(True)
#    plt.ylim(-0.0015,0.0015)
#    plt.xlabel("Frequency (GHz)")
#    plt.legend(loc="left bottom")

offset=0.00075*3
offset = 0
i=0
CC=['b','g','r','c','m','y','k','b']
# for i in range(points):

    
    
    
#     if SParam == 'S11':
#         plt.plot(Freq*1e-9,MedMeasDataC[:,indexST[0]]+i*offset-4*offset,linewidth=1.5,color='tab:gray',linestyle='--')
    
#         plt.plot(Freq*1e-9,MedMeasDataA[:,indexST[0]]+i*offset-4*offset,linewidth=1.5,label='%s mT'%(round(StartFieled-i*2*stepmult)))
#         plt.legend(loc="left bottom")
#         plt.title('Scale: %s' %scale)
    
#     if SParam == 'S21':    
# #       plt.plot(Freq*1e-9,scale*2*(MeasDataA[:,indexST[0]+stepmult*i]-AvMeasDataA)+i*offset-4*offset,color='k',linewidth=0.5)
#       plt.plot(Freq*1e-9,(MedMeasDataA[:,indexST[0]])+i*offset-4*offset,color='k',linewidth=0.5)
    
    

#     plt.xlim(start,stop)
#     plt.grid(True)
#     # plt.ylim(-0.0015*7,0.0015*7)
#     plt.xlabel("Frequency (GHz)")
# #    plt.legend(loc="left bottom")
    





SParam='S11'; #choose S-parameter
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

#==============================================================================
# Magentic field (start field and increment)
#==============================================================================
field = np.genfromtxt("measurement.txt", skip_header= 2, dtype = str)[:,1]
field = np.char.replace(field, ";","")
magField = np.zeros((len(field)))
for i in range(len(field)):
    magField[i] = float(field[i])
#
#magField = magField[::-1]#flip the field direction

#==============================================================================
# S-parameter 
#==============================================================================
#load measurement MAT file
MeasDataA = scipy.io.loadmat(MeasFolder + NameDataA +".mat");
MeasDataB = scipy.io.loadmat(MeasFolder + NameDataB +".mat");
MeasDataC = scipy.io.loadmat(MeasFolder + NameDataC +".mat");
Freq = scipy.io.loadmat(MeasFolder + NameFreq +".mat");
RefDataA = scipy.io.loadmat(RefFolder + NameDataA +".mat");
RefDataB = scipy.io.loadmat(RefFolder + NameDataB +".mat");
RefDataC = scipy.io.loadmat(RefFolder + NameDataC +".mat");


MeasDataA = MeasDataA["Data"][:,:]
MeasDataB = MeasDataB["Data"][:,:]
MeasDataC = MeasDataC["Data"][:,:]
RefDataA = RefDataA["Data"][:,:]
RefDataB = RefDataB["Data"][:,:]
RefDataC = RefDataC["Data"][:,:]
Freq = Freq["Data"]
Freq = Freq[:,0]

Amplitude = np.sqrt(MeasDataA **2 + MeasDataB **2)

AvMeasDataA = np.mean(MeasDataA,axis=1)
AvMeasDataC = np.mean(MeasDataC,axis=1)


MMeasDataA = np.median(MeasDataA,axis=1)
MMeasDataB = np.median(MeasDataB,axis=1)
MMeasDataC = np.median(MeasDataC,axis=1)
#subtract the data with reference value
DeltaMeasDataA = MeasDataA - RefDataA
DeltaMeasDataB = MeasDataB - RefDataB
DeltaMeasDataC = MeasDataC - RefDataC


MedMeasDataA = MeasDataA - MMeasDataA[:,np.newaxis] 
MedMeasDataB = MeasDataB - MMeasDataB[:,np.newaxis] 
MedMeasDataC = MeasDataC - MMeasDataC[:,np.newaxis] 


MedAmplitude = np.sqrt(MedMeasDataA **2 + MedMeasDataB **2)



DeltaAmplitude = np.sqrt(DeltaMeasDataA **2 + DeltaMeasDataB **2)

NumMeas = np.size(MeasDataA,1)


start=1
stop=16


index111 = np.where(magField==90)
index1=index111[0]  

indexST1 = np.where(magField==StartFieled)
indexST=indexST1[0]  


offset=0.00075*3
offset = 0
i=0
CC=['b','g','r','c','m','y','k','b']
# for i in range(points):
    
    
#     if SParam == 'S21':

#        plt.plot(Freq*1e-9,scale*0.3*MeasDataC[:,indexST[0]+stepmult*i]+i*offset-4*offset,linewidth=1.25,color='tab:grey',linestyle='--')
#        plt.plot(Freq*1e-9,scale*0.3*MagNN[:,indexST[0]+stepmult*i]+i*offset-4*offset,linewidth=1.25,'y--')
#        plt.plot(Freq*1e-9,scale*0.3*MagNN[:,indexST[0]+stepmult*i]+i*offset-4*offset,linewidth=1.0,label='%s mT'%(round(StartFieled-i*2*stepmult))) 

# plt.plot(Freq*1e-9,signal.wiener(Amplitude[:,indexST[0]],mysize =3)+i*offset-4*offset,linewidth=1.5,color='k', label = "-30 dBm")
plt.plot(Freq*1e-9,signal.wiener(MedAmplitude[:,indexST[0]],mysize =3)+i*offset-4*offset,linewidth=1.5,color='k', label = "-30 dBm")

Frequency = Freq*1e-9
SignalExp = signal.wiener(MedAmplitude[:,indexST[0]],mysize =3)

# plt.plot(Freq*1e-9,(MedAmplitude[:,indexST[0]])+i*offset-4*offset,linewidth=1.5,color='k', label = "-30 dBm")
# plt.plot(Freq*1e-9,signal.wiener(MedMeasDataC[:,indexST[0]]*-1,mysize =3)+i*offset-4*offset,linewidth=1.5,color='b', label = "-30 dBm")

np.savetxt("14mT_-30dBm_Mag_nFLT.txt", (Freq, MedAmplitude[:,indexST[0]]))
# plt.plot(Freq*1e-9,(MedMeasDataB[:,indexST[0]])+i*offset-4*offset,linewidth=1.0,label='%s mT'%(round(StartFieled-i*2*stepmult)))  
# plt.plot(Freq*1e-9,(MedMeasDataA[:,indexST[0]])+i*offset-4*offset,linewidth=1.0) 
#        plt.plot(Freq*1e-9,scale*0.3*(DeltaAmplitude[:,indexST[0]+stepmult*i])+i*offset-4*offset,linewidth=1.0,label='%s mT'%(round(StartFieled-i*2*stepmult)))  
#        plt.plot(Freq*1e-9,scale*0.3*MeasDataA[:,indexST[0]+stepmult*i]+i*offset-4*offset,linewidth=1.0,label='%s mT'%(round(StartFieled-i*2*stepmult)))
plt.legend(loc="left bottom")
# plt.title('Scale: %s' %scale)

#    if SParam == 'S21':    
#       plt.plot(Freq*1e-9,scale*2*MedMeasDataA[:,indexST[0]+stepmult*i]+i*offset-4*offset,color='k',linewidth=0.5)


plt.xlim(start,stop)
# plt.grid(True)
#    plt.ylim(-0.0015*7,0.0015*7)
# plt.ylim(-0.05,0.05)
plt.yscale("log")
plt.xlabel("Frequency (GHz)")
#    plt.legend(loc="left bottom")


plt.xlim(1,13.25)
# plt.xlim(1,3.25)
plt.tight_layout()
# plt.savefig("AmpRealLineplotsRange%s_%s.jpg"%(StartFieled,scale),dpi=600)
# plt.savefig("S21AmpRealLineplotsRange%s_%s.pdf"%(StartFieled,scale),dpi=600)
#plt.clf()
#plt.close()