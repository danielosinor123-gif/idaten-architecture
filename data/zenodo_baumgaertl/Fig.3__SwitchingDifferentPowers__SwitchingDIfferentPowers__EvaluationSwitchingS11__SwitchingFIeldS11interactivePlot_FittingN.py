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
mpl.rc('font', serif='Arial') 
mpl.rc('text', usetex='false') 

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width*3,fig_width]
#fig_size =  [7,8]
params = {'axes.labelsize': 9*st,   #'backend': 'eps',
          'legend.fontsize': 9*st,
          'xtick.labelsize': 9*st,
          'ytick.labelsize': 9*st,
          'text.usetex': False,
          'figure.figsize': fig_size}
plt.rcParams.update(params)
#
#def create_window():
#    win = ImageDialog(edit=False, toolbar=True, wintitle="Cross sections test",
#                      options=dict(show_xsection=True, show_ysection=True,
#                                   show_itemlist=True))
#    win.resize(1600, 1200)
#    return win



import os

g = -25
x1 = 10
x2 = 22
Power = '%sdBm' %(g)

#==============================================================================
# define the Sparameter and its component
#==============================================================================
SParam='S11'; #choose S-parameter
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


os.chdir('..')
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
    FreqStart=float(lines)
with open('set_vna.txt') as f:    
    lines = f.readlines()[3]
    lines=lines.replace("stop frequency: ","")
    lines=lines.replace(";","")
    FreqEnd=float(lines)
    
    
magstep=magField[5]-magField[4]
#
Address = FolderName + "\\MEAS\\" + SParam + "\\"
file_name_listReal = glob.glob(Address+'*REAL*')
file_name_listImag = glob.glob(Address+'*IMAG*')
file_name_listMLIN = glob.glob(Address+'*MLIN*')
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


MeasDataC = np.loadtxt(file_name_listMLIN[0])
for file_name in file_name_listMLIN[1:]:
     MeasDataC = np.vstack((MeasDataC, np.loadtxt(file_name)))
#     MeasDataA = np.append(MeasDataA, np.loadtxt(file_name))
MeasDataC1a = copy.deepcopy(np.swapaxes(MeasDataC,0,1))


file_name_listFreq = glob.glob(Address+'*freq*')
Freq = np.loadtxt(file_name_listFreq[0])




DataAv = np.median(MeasDataA1a,axis=1)
DataAv2 = np.median(MeasDataB1a,axis=1)











#subtract the data with reference value
DeltaMeasDataA = MeasDataA1a - DataAv[:,np.newaxis] 
DeltaMeasDataB = MeasDataB1a - DataAv2[:,np.newaxis] 


os.chdir('..')
os.chdir('EvaluationSwitchingS11')







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


DataType = 'REAL (ab. sub)'


    




DataMag = np.sqrt(DeltaMeasDataA**2+DeltaMeasDataB**2)

fig, (ax1, ax2) = plt.subplots(1, 2)


z_max=0.005*2

#plt.pcolormesh(magField[index1:index2+2], Freq*1e-9, DataMag[0:Xin,index1:index2+2],cmap='Greys', vmin=0, vmax=z_max,rasterized=False)
#magField1=np.arange(-10.5,41,1)*1.07
magField1=np.arange(-10.5,41,1)
magField1r=np.arange(-10.0,40.5,1)
FieldReF= np.arange(40,2.5,-1) 
Mode1= np.array([11.61,	11.59,	11.57,	11.55,	11.52,	11.5,	11.48,	11.46,	11.42,	11.39,	11.36,	11.34,	11.31,	11.29,	11.25,	11.21,	11.18,	11.16,	11.13,	11.1,	11.06,11.02,	10.99,	10.96,	10.94,	10.91,	10.86,	10.83,	10.8,	10.77,	10.74,	10.72,	10.68,10.64,	10.61,	10.55,	10.49,	10.45])

#Mode1 = np.array([9.42,9.39,9.35,9.32,9.28,9.25,9.22,9.18,9.15,9.11,9.08,9.05,9.01,8.98,8.94,8.91,8.88,8.84,8.8,8.76,8.72,8.69,8.65,8.61,8.57,8.52,8.47,8.43,8.38,8.35,8.28,8.21,8.13,8,7.89,7.79,7.64,7.54,7.43,7.34,7.27])-0.04
#magField1=np.arange(91,-92,-2)
FieldUp= np.arange(0,23.5,1)
# ModeUp = np.array([8.51,8.51,8.62,8.71,8.84,8.92,8.99,9.05,9.11,9.14,9.2,9.25,9.28,9.32,9.35,9.38,9.41,9.45,9.48,9.51,9.54,9.57,9.6,9.63,9.66,9.69])-0.03

ModeUp = np.array([10.34	,10.34,	10.37,	10.42,	10.45,	10.49,	10.52,	10.55,	10.57,	10.59,	10.6,	10.61,	10.62,	10.63,	10.64,	10.66,	10.68,	10.69,	10.75,	10.81,	10.82,	10.83, 10.84, 10.85])

FieldNoise = np.arange(5,40.5,1)
ModeNoise= np.ones(FieldNoise.shape)*7.5

ax1.pcolormesh(magField1, Freq*1e-9, DataMag,cmap='Greys', vmin=0, vmax=z_max,rasterized=True)  
#        plt.pcolormesh(magField, Freq*1e-9, Data,cmap='seismic', vmin=z_min, vmax=z_max,rasterized=True)


ax1.scatter(FieldUp, ModeUp, s=80, facecolors='none', edgecolors='blue')
ax1.plot(FieldUp, ModeUp+0.175,color= 'blue',linestyle ='dashed')
ax1.plot(FieldUp, ModeUp-0.175,color= 'blue',linestyle ='dashed')


ax1.scatter(FieldReF,Mode1, s=80, facecolors='none', edgecolors='orange')    
ax1.plot(FieldReF,Mode1+0.25,color= 'orange',linestyle ='dashed')
ax1.plot(FieldReF,Mode1-0.25,color= 'orange',linestyle ='dashed')





ax1.scatter(FieldNoise, ModeNoise, s=80, facecolors='none', edgecolors='grey')
ax1.plot(FieldNoise,ModeNoise+0.25,color= 'grey',linestyle ='dashed')
ax1.plot(FieldNoise, ModeNoise-0.25,color= 'grey',linestyle ='dashed')



ax1.set_title('%s %s %s dBm' % (SParam, DataType,PowerLevel))
ax1.set_xlabel('B (mT)')
ax1.set_ylabel('Frequency (GHz)')



Tvalues = np.zeros((2,len(Mode1)))
for i in range(len(Mode1)):
    index1 = np.argmin(np.abs(Freq - (Mode1[i]-0.25)*1e9))
    index2 = np.argmin(np.abs(Freq - (Mode1[i]+0.25)*1e9))
    FieldIndex = np.argmin(np.abs(magField1r - FieldReF[i]))
    Mode1Sum=np.mean(DataMag[index1:index2,FieldIndex],axis=0)
    Tvalues[0,i] = FieldReF[i]
    Tvalues[1,i] = Mode1Sum
    
    
Uvalues = np.zeros((2,len(ModeUp)))
for i in range(len(ModeUp)):
    index1u = np.argmin(np.abs(Freq - (ModeUp[i]-0.175)*1e9))
    index2u = np.argmin(np.abs(Freq - (ModeUp[i]+0.175)*1e9))
    FieldIndexU = np.argmin(np.abs(magField1r - FieldUp[i]))
    Mode1SumU=np.mean(DataMag[index1u:index2u,FieldIndexU],axis=0)
    Uvalues[0,i] = FieldUp[i]
    Uvalues[1,i] = Mode1SumU
    
    
Nvalues = np.zeros((2,len(ModeNoise)))
for i in range(len(ModeNoise)):
    index1un = np.argmin(np.abs(Freq - (ModeNoise[i]-0.25)*1e9))
    index2un = np.argmin(np.abs(Freq - (ModeNoise[i]+0.25)*1e9))
    FieldIndexUn = np.argmin(np.abs(magField1r - FieldNoise[i]))
    Mode1SumUn=np.mean(DataMag[index1un:index2un,FieldIndexUn],axis=0)
    Nvalues[0,i] = FieldNoise[i]
    Nvalues[1,i] = Mode1SumUn    
    
    
    
    
#        
ax2.plot(Tvalues[0,:],Tvalues[1,:], color= 'orange')    
ax2.scatter(Tvalues[0,:],Tvalues[1,:], color= 'orange')  
ax2.plot(Uvalues[0,:],Uvalues[1,:], color= 'blue')  
ax2.scatter(Uvalues[0,:],Uvalues[1,:], color= 'blue')  
ax2.scatter(Nvalues[0,:],Nvalues[1,:], color= 'grey')  


def linear(x):
    return np.mean(x)

# Offset

Xx1 = np.argmin(np.abs(FieldNoise - x1))
Xx2 = np.argmin(np.abs(FieldNoise - x2))
Offset = linear(Nvalues[1,Xx1:Xx2+1])
plt.hlines(y=Offset, xmin= x1, xmax = x2, linestyle = 'dashed', colors='k')


# Maximum mode2
#x1m = 36
#x2m = 40
#Xx1m = np.argmin(np.abs(FieldReF - x1m))
#Xx2m = np.argmin(np.abs(FieldReF - x2m))
#Offsetm = linear(Tvalues[1,Xx2m:Xx1m])
#ax2.hlines(y=Offsetm, xmin= x1m, xmax = x2m, linestyle = 'dashed', colors='k')


Offsetm = np.max(Tvalues[1,:])
Xx1m = np.argmax(Tvalues[1,:])
x1m = Tvalues[0,Xx1m]

#ax2.hlines(y=OffsetD, xmin= 0, xmax = 10, linestyle = 'dashed', colors='k')
ax2.annotate('Max', xy = (x1m, Offsetm), xycoords='data', xytext=(-50, 0), textcoords='offset points',
            arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')




#
#ax2.hlines(y=0.5*(Offsetm-Offset)+Offset, xmin= x2+2, xmax = x1m, linestyle = 'dashed', colors='yellow')
#ax2.hlines(y=0.3*(Offsetm-Offset)+Offset, xmin= x2+2, xmax = x1m, linestyle = 'dashed', colors='yellow')
#ax2.hlines(y=0.7*(Offsetm-Offset)+Offset, xmin= x2+2, xmax = x1m, linestyle = 'dashed', colors='yellow')


ax2.hlines(y=0.5*(Offsetm-Offset)+Offset, xmin=5, xmax = x1m, linestyle = 'dashed', colors='yellow')
ax2.hlines(y=0.3*(Offsetm-Offset)+Offset, xmin= 5, xmax = x1m, linestyle = 'dashed', colors='yellow')
ax2.hlines(y=0.7*(Offsetm-Offset)+Offset, xmin= 5, xmax = x1m, linestyle = 'dashed', colors='yellow')


FiftyPC = 0.5*(Offsetm-Offset)+Offset
SeventyPC = 0.7*(Offsetm-Offset)+Offset
ThirtyPC = 0.3*(Offsetm-Offset)+Offset

ax2.annotate('50%', (x2, FiftyPC))
ax2.annotate('70%', (x2, SeventyPC))
ax2.annotate('30%', (x2, ThirtyPC))


#def Hrise(Boundary):
#    BoundaryIndex = np.argmin(np.abs(Tvalues[1,:] - Boundary))
#    if Tvalues[1,BoundaryIndex] < Boundary:
#        print('a')
#        return (Boundary-Tvalues[1,BoundaryIndex])/(Tvalues[1,BoundaryIndex-1]-Tvalues[1,BoundaryIndex])+Tvalues[0,BoundaryIndex]
#    if Tvalues[1,BoundaryIndex] > Boundary:
#        print('b')
#        return -(Boundary-Tvalues[1,BoundaryIndex])/(Tvalues[1,BoundaryIndex+1]-Tvalues[1,BoundaryIndex])+Tvalues[0,BoundaryIndex]
#  
  
#def helpfunction(i,startI,Boundary):
#    if i > startI:
#        return (Boundary-Tvalues[1,-(i-1)])/(Tvalues[1,-i]-Tvalues[1,-(i-1)])+Tvalues[0,-(i-1)]
#    else:
#        return np.nan
     
     
def Hrise(Boundary):
    i = np.argmin(np.flip(Tvalues[1,:]))+1
#    print(i)
    startI = copy.deepcopy(i)
    
    while Tvalues[1,-i] < Boundary:
        i = i+1
        
#    return helpfunction(i, startI,Boundary)
    if i > startI:
        return (Boundary-Tvalues[1,-(i-1)])/(Tvalues[1,-i]-Tvalues[1,-(i-1)])+Tvalues[0,-(i-1)]
    else:
        return np.nan
        


Values = np.zeros((2,6))
Values[0,0] = FiftyPC
Values[0,1] = SeventyPC
Values[0,2] = ThirtyPC

Values[1,0] = HFiftyPC = Hrise(FiftyPC)
Values[1,1] = HSeventyPC = Hrise(SeventyPC)
Values[1,2] = HThirtyPC = Hrise(ThirtyPC)

if HFiftyPC is not np.nan:
    ax2.annotate('%s'%round(HFiftyPC,3), xy = (HFiftyPC,FiftyPC), xycoords='data', xytext=(50, -20), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')
#
print('Rise50 percent: %s'%HFiftyPC)

if HSeventyPC is not np.nan:
    ax2.annotate('%s'%round(HSeventyPC,3), xy = (HSeventyPC,SeventyPC), xycoords='data', xytext=(50, -20), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')
#
print('Rise70 percent: %s'%HSeventyPC)


if HThirtyPC is not np.nan:
    ax2.annotate('%s'%round(HThirtyPC,3), xy = (HThirtyPC,ThirtyPC), xycoords='data', xytext=(50, -20), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')
#
print('Rise30 percent: %s'%HThirtyPC)
#
print('Fall')

 # Maximum mode1
 #y1m = 1
 #y2m = 10
 #Yy1m = np.argmin(np.abs(FieldReF - y1m))
 #Yy2m = np.argmin(np.abs(FieldReF - y2m))
 #Offsetm = linear(Tvalues[1,Yy1m:Yy2m])

OffsetD = np.max(Uvalues[1,:])
Yy1m = np.argmax(Uvalues[1,:])
y1m = Uvalues[0,Yy1m]

 #ax2.hlines(y=OffsetD, xmin= 0, xmax = 10, linestyle = 'dashed', colors='k')
ax2.annotate('Max', xy = (y1m, OffsetD), xycoords='data', xytext=(-50, 0), textcoords='offset points',
            arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')


FiftyPCD = 0.5*(OffsetD-Offset)+Offset
SeventyPCD = 0.7*(OffsetD-Offset)+Offset
ThirtyPCD = 0.3*(OffsetD-Offset)+Offset
ax2.hlines(y=FiftyPCD, xmin= y1m, xmax = y1m+5, linestyle = 'dashed', colors='yellow')
ax2.hlines(y=SeventyPCD, xmin= y1m, xmax = y1m+5, linestyle = 'dashed', colors='yellow')
ax2.hlines(y=ThirtyPCD, xmin= y1m, xmax = y1m+5, linestyle = 'dashed', colors='yellow')
 #

 #
ax2.annotate('50%', (y1m, FiftyPCD))
ax2.annotate('70%', (y1m, SeventyPCD))
ax2.annotate('30%', (y1m, ThirtyPCD))

 #
 #def Hfall(Boundary):
 #    BoundaryIndex = np.argmin(np.abs(Uvalues[1,:] - Boundary))
 #    if Uvalues[1,BoundaryIndex] < Boundary:
 #        print('a')
 #        return -(Boundary-Uvalues[1,BoundaryIndex])/(Uvalues[1,BoundaryIndex-1]-Uvalues[1,BoundaryIndex])+Uvalues[0,BoundaryIndex]
 #    if Uvalues[1,BoundaryIndex] > Boundary:
 #        print('b')
 #        return (Boundary-Uvalues[1,BoundaryIndex])/(Uvalues[1,BoundaryIndex+1]-Uvalues[1,BoundaryIndex])+Uvalues[0,BoundaryIndex]
    
    
def Hfall(Boundary):
    i=1+ Yy1m
    bond = np.argmin(Uvalues[1,:])
    while Uvalues[1, i] > Boundary:
        i = i+1 
    if i < bond:
        return (Boundary-Uvalues[1,i-1])/(Uvalues[1,i]-Uvalues[1,(i-1)])+Uvalues[0,(i-1)]
    else:
        return np.nan
    
Values[0,3] = FiftyPCD
Values[0,4] = SeventyPCD
Values[0,5] = ThirtyPCD
 #
Values[1,3] = HFiftyPCfall = Hfall(FiftyPCD)
Values[1,4] = HSeventyPCfall = Hfall(SeventyPCD)
Values[1,5] = HThirtyPCfall = Hfall(ThirtyPCD)

#Values[0,3] = np.nan
#Values[0,4] = np.nan
#Values[0,5] = np.nan
##
#Values[1,3] = np.nan
#Values[1,4] = np.nan
#Values[1,5] = np.nan

# #
if HFiftyPCfall is not np.nan:
    ax2.annotate('%s'%round(HFiftyPCfall,3), xy = (HFiftyPCfall,FiftyPCD), xycoords='data', xytext=(-20, -20), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')
 #
print('Fall50 percent: %s'%HFiftyPCfall)

if HSeventyPCfall is not np.nan: #
    ax2.annotate('%s'%round(HSeventyPCfall,3), xy = (HSeventyPCfall,SeventyPCD), xycoords='data', xytext=(-20, -20), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')

print('Fall70 percent: %s'%HSeventyPCfall)

if HThirtyPCfall is not np.nan:
    ax2.annotate('%s'%round(HThirtyPCfall,3), xy = (HThirtyPCfall,ThirtyPCD), xycoords='data', xytext=(-20, -20), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.002, width = 1, headwidth = 5), horizontalalignment='right', verticalalignment='bottom')

print('Fall30 percent: %s'%HThirtyPCfall)






#        
# 
ax1.set_xlim(-0.5, 40.5)

ax1.set_ylim(7,12.5)

# fig.tight_layout()
# plt.savefig('%s_MagGrey%s_%smT_%smT_median.jpg'% (Power,SParam,FieldMin, FieldMax),dpi=600)
# plt.savefig('%s_MagGrey%s_%smT_%smT_median.pdf'% (Power,SParam,FieldMin, FieldMax),dpi=600)
# # np.savetxt('%s.txt'% g, Values)
# # np.savetxt('Mode1_%s.txt'% Power, Uvalues.T)
# #plt.close()

    
    

