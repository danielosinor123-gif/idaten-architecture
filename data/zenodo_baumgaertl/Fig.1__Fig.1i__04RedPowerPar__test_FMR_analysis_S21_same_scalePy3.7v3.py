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

#mpl.rcParams['xtick.major.size'] = 1.5
#mpl.rcParams['xtick.major.width'] = 0.5
#mpl.rcParams['xtick.minor.size'] = 2
#mpl.rcParams['xtick.minor.width'] = 0.5
#mpl.rcParams['ytick.major.size'] = 1.5
#mpl.rcParams['ytick.major.width'] = 0.5
#mpl.rcParams['ytick.minor.size'] = 1.5
#mpl.rcParams['ytick.minor.width'] = 0.5
#mpl.rcParams['pdf.fonttype'] = 42
#font = {'size'   : 9}
#mpl.rc('font', **font)
#mpl.rc('font', family='sans-serif') 
#mpl.rc('font', serif='Arial') 
#matplotlib.rc('text', usetex='false') 

#st=1
#fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
#inches_per_pt = 1.0/72.27               # Convert pt to inch
#golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
#fig_width = 6.69 # width in inches #6.69 two column single 3.37
#fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
#fig_size =  [fig_width,fig_height]
#params = {'axes.labelsize': 9*st,   #'backend': 'eps',
#          'legend.fontsize': 9*st,
#          'xtick.labelsize': 9*st,
#          'ytick.labelsize': 9*st,
#          'text.usetex': False,
#          'figure.figsize': fig_size}
#plt.rcParams.update(params)




#==============================================================================
# define the Sparameter and its component
#==============================================================================
SParam='S12'; #choose S-parameter
Component = "MAG" #choose component
FieldMin = 30
FieldMax = -40
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
magField=np.insert(magField,lll,magField[lll-1]+magstep)
if FieldMin<=0:
    magField +=magstep/2
else:
    magField -=magstep/2

#
pp = PdfPages('f_%s_%smT_%smT.pdf'% (SParam,FieldMin, FieldMax))

    
def function_plot(Data,FieldMin, FieldMax, DataType):   
#    fig = plt.figure()
#    Data=signal.detrend(Data, type='constant',axis=0)
#    Data=signal.detrend(Data, type='constant',axis=1)

#    ref=np.mean(Data[200:,index1:index2])
#    Data=Data-ref
#    DataCopy= copy.deepcopy(Data)

#    z_min, z_max = -np.abs(DataCopy[:,index1:index2]).max()*0.005, np.abs(DataCopy[:,index1:index2]).max()*0.005#
    if SParam == 'S11': 
        z_min, z_max=-0.003,0.003
    if SParam == 'S21':
         z_min, z_max=-0.0005,0.0005
         
    if SParam == 'S12':
         z_min, z_max=-0.005,0.005    
    if SParam == 'S22': 
        z_min, z_max=-0.003,0.003        
    plt.clf()
    plt.pcolormesh(magField[index1:index2+1], Freq*1e-9, Data[:,index1:index2+1],cmap='seismic', vmin=z_min, vmax=z_max,rasterized=True)
  
#    plt.pcolormesh(magField, Freq*1e-9, Data,cmap='seismic', vmin=z_min, vmax=z_max,rasterized=True)

    plt.title('%s %s %s dBm' % (SParam, DataType,PowerLevel))
    plt.xlabel('B (mT)')
    plt.ylabel('Frequency (GHz)')
#plt.set_xlim(-90,90)
    plt.xlim(FieldMin-magstep/2, FieldMax+magstep/2)
#    plt.xlim(-95, 95)
    plt.ylim(FreqStart*1e-9,FreqEnd*1e-9)
    ax = plt.subplot()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
    plt.colorbar()
    pp.savefig(dpi=600)
    plt.close()
#plt.savefig('%s.eps' % (identifier_long))
#plt.savefig('tem3p.pdf', dpi=300)
function_plot(DeltaMeasDataA,FieldMin, FieldMax, 'REAL')
function_plot(DeltaMeasDataB,FieldMin, FieldMax, 'IMAG')
function_plot(DeltaAmplitude,FieldMin, FieldMax, 'MAG')
function_plot(ProcessDataNeighborReal,FieldMin, FieldMax, 'REAL - Next neighbour subtraction')
function_plot(ProcessDataNeighbor,FieldMin, FieldMax, 'MAG - Next neighbour subtraction')
plt.show()   
pp.close()

#Data=DeltaMeasDataB
##Data=DeltaAmplitude
#
##Data=signal.detrend(Data, type='constant',axis=0)
##Data=signal.detrend(Data, type='constant',axis=1)
#cut1=-20
##cut2=20
##cut3=-20
#ind1 = np.where(magField==cut1)
##ind2 = np.where(magField==cut2)
##ind3 = np.where(magField==cut3)
#ind1=ind1[0]
##ind2=ind2[0]
##ind3=ind3[0]
##DataCopy= copy.deepcopy(Data)
#z_min, z_max = -np.abs(Data[300:,index1:index2]).max(), np.abs(Data[200:,index1:index2]).max()#
#fig = plt.figure() 
#gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 
#ax0 = plt.subplot(gs[0])
#fig.suptitle('IMAG S11')
#ax0.set_xlabel('B (mT)')
#ax0.set_ylabel('Frequency (GHz)')
#ax0.pcolormesh(magField[index1:index2+1], Freq/1e9, Data[:,index1:index2+1],cmap='Greys', vmin=z_min, vmax=z_max, rasterized=True)
#ax0.set_ylim(3,10)
#ax0.set_xlim(FieldMin,FieldMax)
#ax0.axvline(x=cut1, linestyle='--', color='r')
#
##ax0.axvline(x=cut2, linestyle='--', color='b')
##ax0.axvline(x=cut3, linestyle='--', color='g')
#def lorentz(x,w,x0,z,y):
#    return y*(w**2/((x-x0)**2+w**2))-z
#    
#def gauss_function(x, a, x0, sigma, z):
#    return a*np.exp(-(x-x0)**2/(2*sigma**2))-z
##
##def lorentz(x,w,x0,z):
##    return  w/ (1.0 + (x / x0 - 1.0)**4 * z**2)
#
##p0 = np.array([-2.0, -4.0, 6.8], dtype=np.double) #Initial guess
#popt, pcov =  curve_fit(gauss_function, Freq[500:700]/1e9, Data[500:700,ind1[0]]*1e4, p0= [20, 6.28, 0.19,2])
##FMWHM=2.3548*sigma
#ax1 = plt.subplot(gs[1])
#ax1.plot(Data[:,ind1[0]]*1e4, Freq/1e9,color='r', label='%s mT'%(cut1))
#ax1.plot(gauss_function(Freq[500:700]/1e9,popt[0],popt[1],popt[2],popt[3]),Freq[500:700]/1e9, 'b--', linewidth=3, label='Gauss Fit')
#
##ax1.plot(Data[:,ind2[0]]*1e4, Freq/1e9,color='b', label='%s mT'%(cut2))
##ax1.plot(Data[:,ind3[0]]*1e4, Freq/1e9,color='g', label='%s mT'%(cut3))
#ax1.legend(loc='upper right')
#ax1.set_xlabel('IMAG(a11) (arb. units)')
##ax1.set_xlim([-2,2])
#ax1.set_ylim(3,10)
#plt.tight_layout()
#plt.savefig('new_lineplot%s_%smT_%smT_phasedelay%sIMAG.pdf'% (SParam,FieldMin, FieldMax,Delay))
    
    
    
#==============================================================================
# GUI interface for Sparameter plot
#==============================================================================
#name of the qui plot interface
#identifier = SParam + " parameter" + Component
## component shown in Gui plot interface
#if Component == "REAL":
#    plotSparamete = DeltaMeasDataA
#elif Component == "IMAG":
#    plotSparamete = DeltaMeasDataB
#elif Component == "MAG":
#    plotSparamete = DeltaAmplitude
#
#
#from guiqwt.builder import make
#def imshow(win, x, y, data, yreverse=False, title=None):
#    image = make.xyimage(x, y, data, interpolation="nearest", title=title )
#    plot = win.get_plot()
#    plot.add_item(image)
#    plot.do_autoscale()
#    plot.replot()
#    return plot, image
#
#from guiqwt.plot import ImageDialog
#import guidata
#_app = guidata.qapplication()
#
#win = ImageDialog(edit = False, toolbar = True, wintitle=identifier, 
#              options=dict(xlabel = "Static magnetic field [mT]", ylabel = "Frequency [GHz]", zlabel=identifier, yreverse=False, lock_aspect_ratio=False))
#            
#plot,image = imshow(win, magField[::-1], Freq, plotSparamete)
#win.show()
#win.exec_()
