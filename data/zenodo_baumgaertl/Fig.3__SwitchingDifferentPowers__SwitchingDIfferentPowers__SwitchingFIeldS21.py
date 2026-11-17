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
fig_width = 5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width*2,fig_width]
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
g = -35
while g  < 5:
    
    g = g+5

    Power = '%sdBm' %(g)

    #==============================================================================
    # define the Sparameter and its component
    #==============================================================================
    SParam='S21'; #choose S-parameter
    Component = "MAG" #choose component
    FieldMin = -10
    FieldMax = 40
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
    
    
    os.chdir(Power)
    
    
    #==============================================================================
    # Magentic field (start field and increment)
    #==============================================================================
    field = np.genfromtxt("measurement.txt", skip_header= 2, dtype = str)[:,1]
    field = np.char.replace(field, ";","")
    magField = np.zeros((len(field)))
    for i in range(len(field)):
        magField[i] = float(field[i])
        
    with open('set_vna.txt') as f:
        lines = f.readlines()[7]
        lines=lines.replace("power level:","")
        lines=lines.replace(";","")
        PowerLevel=int(lines)
    with open('set_vna.txt') as f:    
        lines = f.readlines()[2]
        lines=lines.replace("start frequency: ","")
        lines=lines.replace(";","")
        FreqStart=float64(lines)
    with open('set_vna.txt') as f:    
        lines = f.readlines()[3]
        lines=lines.replace("stop frequency: ","")
        lines=lines.replace(";","")
        FreqEnd=float64(lines)
        
        
    magstep=magField[5]-magField[4]
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
    
    #AvMeasDataA = np.mean(MeasDataA,axis=1)
    #MeasDataASub = MeasDataA - AvMeasDataA[:,np.newaxis] 
    
    
    RefDataA = RefDataA["Data"][:,:]
    RefDataB = RefDataB["Data"][:,:]
    Freq = Freq["Data"]
    Freq = Freq[:,0]
    
    #subtract the data with reference value
    DeltaMeasDataA = MeasDataA - RefDataA
    DeltaMeasDataB = MeasDataB - RefDataB
    #DeltaMeasDataA = MeasDataA 
    #DeltaMeasDataB = MeasDataB 
    DeltaAmplitude = np.sqrt(DeltaMeasDataA **2 + DeltaMeasDataB **2)
    Amplitude=np.sqrt(MeasDataA **2 + MeasDataB **2)
    
    NumMeas = np.size(MeasDataA,1)
    
    ProcessData = MeasDataC
    NumMeas = np.size(MeasDataA,1)
    NumFreq = len(Freq)
    
    ProcessDataNeighbor = np.zeros((len(Freq), NumMeas-1))
    for i in range(NumMeas-1):
        ProcessDataNeighbor[:,i] = ProcessData[:, i+1] - ProcessData[:, i]
    
    
    
    ProcessData2=MeasDataA
    
    
    ProcessDataNeighborReal = np.zeros((len(Freq), NumMeas-1))
    for i in range(NumMeas-1):
        ProcessDataNeighborReal[:,i] = ProcessData2[:, i+1] - ProcessData2[:, i]
    
    
    
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
    
    
    os.chdir('..')
    
    #DeltaMeasDataA = Signal.real
    #DeltaMeasDataA = signal.detrend(DeltaMeasDataA,axis=0, type='constant')
    #DeltaMeasDataA = signal.detrend(DeltaMeasDataA, type='constant',axis=1)
    ##ref=np.mean(DeltaMeasDataA)
    ##DeltaMeasDataA=DeltaMeasDataA-ref
    #DeltaMeasDataB = Signal.imag
    #for i in range(len(DeltaMeasDataB[1,:])):
    #    DeltaMeasDataB[:,i] =DeltaMeasDataB[:, i] - np.mean(DeltaMeasDataB[:, i][DeltaMeasDataB[:, i] < 0.0])
    #DeltaMeasDataB = signal.detrend(DeltaMeasDataB, type='constant',axis=1)
    ##negavg = np.mean(DeltaMeasDataB[DeltaMeasDataB < 0.0])
    ##DeltaMeasDataB=DeltaMeasDataB+negavg
    #DeltaAmplitude = np.sqrt(DeltaMeasDataB**2+DeltaMeasDataA**2)
    #ProcessData = DeltaAmplitude
    
    
    
    
    
    
    
    
    index111 = np.where(magField==FieldMin)
    index222 = np.where(magField==FieldMax)
    ##index11=index111[0]  #in number occurs two times
    ##index22=index222[0]
    #
    index11=index111[0]  
    index22=index222[0]
    index1=index11[0]  
    index2=index22[0]
    
    lll=len(magField)
    #magField=np.insert(magField,lll,magField[lll-1]+magstep)
    #if FieldMin<=0:
    #    magField +=magstep/2
    #else:
    #    magField -=magstep/2
    
    #
    #pp = PdfPages('f%s_%smT_%smT.jpg'% (SParam,FieldMin, FieldMax))
    
    DataType = 'REAL (ab. sub)'
    
    DataIm = MeasDataA
    DataAv = np.median(DataIm,axis=1)
    Data = DataIm - DataAv[:,np.newaxis] 
    
    
    
    DataIm2 = MeasDataB
    DataAv2 = np.median(DataIm2,axis=1)
    Data2 = DataIm2 - DataAv2[:,np.newaxis] 
    
    #Data=DataIm
    
    
    #Data= Data-
    
     
    time   = Freq*1e-9
    
    Xin = Data[:,0].size
    Xpad = 40002
    
    Xpad=Xin
    
    Yin = Data[0,:].size
    Ypad = 600
    
    Ypad=Yin
    
    cut_low = 5
    cut_high = 80
    #2/(delta f)=2*s/vg or maybe s/vg
    W = np.fft.fftfreq(Xpad, d=time[1]-time[0])
    
    Wx = np.fft.fftfreq(Ypad, d=2)
    #print(WX)
    cut_lowX= 0.0075
    
      
        
    if SParam == 'S11': 
        z_min, z_max=-0.01,0.01
    if SParam == 'S21':
         z_min, z_max=-0.00005,0.00005
    #plt.clf()
    
#    f_signal = np.fft.fft2(Data,s=(Xpad,Ypad))
#    cut_f_signal = f_signal.copy()
#    cut_f_signal[ np.logical_and(W < cut_low, W > -cut_low),:] = 0
#    cut_f_signal[(W>cut_high),:] = 0
#    cut_f_signal[(W<-cut_high),:] = 0
#    cut_f_signal[:, np.logical_and(Wx < cut_lowX, Wx > -cut_lowX )] = 0
#    
#    DataFilt11 = np.fft.ifft2(cut_f_signal)
#    DataFilt1 = DataFilt11.real
#    
#    
#    f_signal2 = np.fft.fft2(Data2,s=(Xpad,Ypad))
#    cut_f_signal2 = f_signal2.copy()
#    cut_f_signal2[ np.logical_and(W < cut_low, W > -cut_low),:] = 0
#    cut_f_signal2[(W>cut_high),:] = 0
#    cut_f_signal2[(W<-cut_high),:] = 0
#    cut_f_signal2[:, np.logical_and(Wx < cut_lowX, Wx > -cut_lowX )] = 0
#    
#    DataFilt12 = np.fft.ifft2(cut_f_signal2)
#    DataFilt2 = DataFilt12.real
#    
#    
#    DataFilt=np.sqrt(DataFilt1**2+DataFilt2**2)
    
    
    
    
    DataMag = np.sqrt(Data**2+Data2**2)
    
    #indmin = np.argmin(np.abs(Freq-14e9))
    #DataMag[indmin:,:]=DataFilt[indmin:,:]*10
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    
    z_max=0.00015
    
    #plt.pcolormesh(magField[index1:index2+2], Freq*1e-9, DataMag[0:Xin,index1:index2+2],cmap='Greys', vmin=0, vmax=z_max,rasterized=False)
    #magField1=np.arange(-10.5,41,1)*1.07
    magField1=np.arange(-10.5,41,1)
    magField1r=np.arange(-10.0,40.5,1)
    FieldReF= np.arange(40,-0.5,-1) 
    Mode1 = np.array([9.42,9.39,9.35,9.32,9.28,9.25,9.22,9.18,9.15,9.11,9.08,9.05,9.01,8.98,8.94,8.91,8.88,8.84,8.8,8.76,8.72,8.69,8.65,8.61,8.57,8.52,8.47,8.43,8.38,8.35,8.28,8.21,8.13,8,7.89,7.79,7.64,7.54,7.43,7.34,7.27])
    #magField1=np.arange(91,-92,-2)
    FieldUp= np.arange(1,26.5,1)
    ModeUp = np.array([8.51,8.51,8.62,8.71,8.84,8.92,8.99,9.05,9.11,9.14,9.2,9.25,9.28,9.32,9.35,9.38,9.41,9.45,9.48,9.51,9.54,9.57,9.6,9.63,9.66,9.69])
    
    
    
    
    
    ax1.pcolormesh(magField1, Freq*1e-9, DataMag,cmap='Greys', vmin=0, vmax=z_max,rasterized=True)  
#        plt.pcolormesh(magField, Freq*1e-9, Data,cmap='seismic', vmin=z_min, vmax=z_max,rasterized=True)
    

    ax1.scatter(FieldUp, ModeUp, s=80, facecolors='none', edgecolors='blue')
    ax1.plot(FieldUp, ModeUp+0.175,color= 'blue',linestyle ='dashed')
    ax1.plot(FieldUp, ModeUp-0.175,color= 'blue',linestyle ='dashed')
    
    
    ax1.scatter(FieldReF,Mode1, s=80, facecolors='none', edgecolors='orange')    
    ax1.plot(FieldReF,Mode1+0.175,color= 'orange',linestyle ='dashed')
    ax1.plot(FieldReF,Mode1-0.175,color= 'orange',linestyle ='dashed')
    ax1.set_title('%s %s %s dBm' % (SParam, DataType,PowerLevel))
    ax1.set_xlabel('B (mT)')
    ax1.set_ylabel('Frequency (GHz)')
    
    
    
    Tvalues = np.zeros((2,len(Mode1)))
    for i in range(len(Mode1)):
        index1 = np.argmin(np.abs(Freq - (Mode1[i]-0.175)*1e9))
        index2 = np.argmin(np.abs(Freq - (Mode1[i]+0.175)*1e9))
        FieldIndex = np.argmin(np.abs(magField1r - FieldReF[i]))
        Mode1Sum=np.sum(DataMag[index1:index2,FieldIndex],axis=0)
        Tvalues[0,i] = FieldReF[i]
        Tvalues[1,i] = Mode1Sum
        
        
    Uvalues = np.zeros((2,len(ModeUp)))
    for i in range(len(ModeUp)):
        index1u = np.argmin(np.abs(Freq - (ModeUp[i]-0.175)*1e9))
        index2u = np.argmin(np.abs(Freq - (ModeUp[i]+0.175)*1e9))
        FieldIndexU = np.argmin(np.abs(magField1r - FieldUp[i]))
        Mode1SumU=np.sum(DataMag[index1u:index2u,FieldIndexU],axis=0)
        Uvalues[0,i] = FieldUp[i]
        Uvalues[1,i] = Mode1SumU
        
        
        
#        
    ax2.plot(Tvalues[0,:],Tvalues[1,:], color= 'orange')    
    ax2.plot(Uvalues[0,:],Uvalues[1,:], color= 'blue')  
#        
#        
##    indexX2 = np.argmin(np.abs(Freq - 8.65*1e9))
##    Mode1=np.sum(DataFilt[indexX1:indexX2,:],axis=0)
##    
#    
##    #plt.set_xlim(-92,92)
##    #    plt.xlim(FieldMin-magstep/2, FieldMax+magstep/2)
##    #plt.xlim(FieldMax, FieldMin)
###    ax1.set_xlim(-10.5, 40.5)
    ax1.set_xlim(-0.5, 40.5)
###    ax1.set_ylim(FreqStart*1e-9,12.5)
    ax1.set_ylim(7,12.5)
#    #ax = plt.subplot()
##    #ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
##    #ax1.colorbar()
##    #    pp.savefig(dpi=1200)
##    #plt.show()
    fig.tight_layout()
    plt.savefig('SwitchingField%s_MagGrey%s_%smT_%smT_median.jpg'% (Power,SParam,FieldMin, FieldMax),dpi=600)
    np.savetxt('Mode2_%s.txt'% Power, Tvalues.T)
    np.savetxt('Mode1_%s.txt'% Power, Uvalues.T)
    plt.close()
##        
     
