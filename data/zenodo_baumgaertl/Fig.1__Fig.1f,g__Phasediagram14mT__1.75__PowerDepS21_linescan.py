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
mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams['font.family'] = "sans-serif"

st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
fig_size =  [fig_width*0.7,fig_width*0.5]
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


Folder1 = 'After'
Folder2 = 'Meas'

#==============================================================================
# define the Sparameter and its component
#==============================================================================
SParam='S21'; #choose S-parameter
Component = "MAG" #choose component
#FieldMin = -18
#FieldMax = 6



FolderName = "measurement"

MeasFolder = FolderName +  "\store\MEAS\\" + SParam + "\\"
RefFolder = FolderName +  "\store\REF\\" + SParam + "\\"

NameDataA = "REAL";
NameDataB = "IMAG";
NameDataC = "MLIN";
NameFreq = "freq";


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

# DataMag = np.sqrt(Data**2 + Data2 **2)


 
# time   = Freq*1e-9
# Xin = Data[:,0].size
# Xpad = 40002

# Xpad=Xin

# Yin = Data[0,:].size
# Ypad = 600

# Ypad=Yin

# cut_low = 5
# cut_high = 80
# #2/(delta f)=2*s/vg or maybe s/vg
# W = np.fft.fftfreq(Xpad, d=time[1]-time[0])

# #Wx = np.fft.fftfreq(Ypad, d=2)
# #print(WX)
# #cut_lowX= 0.0075

  


# f_signal = np.fft.fft2(Data,s=(Xpad,Ypad))
# cut_f_signal = f_signal.copy()
# cut_f_signal[ np.logical_and(W < cut_low, W > -cut_low),:] = 0
# cut_f_signal[(W>cut_high),:] = 0
# cut_f_signal[(W<-cut_high),:] = 0
# #cut_f_signal[:, np.logical_and(Wx < cut_lowX, Wx > -cut_lowX )] = 0

# DataFilt11 = np.fft.ifft2(cut_f_signal)
# DataFilt1 = DataFilt11.real


# f_signal2 = np.fft.fft2(Data2,s=(Xpad,Ypad))
# cut_f_signal2 = f_signal2.copy()
# cut_f_signal2[ np.logical_and(W < cut_low, W > -cut_low),:] = 0
# cut_f_signal2[(W>cut_high),:] = 0
# cut_f_signal2[(W<-cut_high),:] = 0
# #cut_f_signal2[:, np.logical_and(Wx < cut_lowX, Wx > -cut_lowX )] = 0

# DataFilt12 = np.fft.ifft2(cut_f_signal2)
# DataFilt2 = DataFilt12.real
# DataFilt=np.sqrt(DataFilt1**2+DataFilt2**2)


DataMag = np.sqrt(Data**2+Data2**2)

DataFilt = DataMag

fig, ax1 = plt.subplots(1,1)

z_max=0.0005

#start value  +1 
magField1=np.arange(-26,6.1,1)


#plt.pcolormesh(magField1, Freq*1e-9, DataFilt ,cmap='Greys', rasterized=True)





indexX1 = np.argmin(np.abs(Freq - 8.3*1e9))
indexX2 = np.argmin(np.abs(Freq - 8.7*1e9))
Mode1=np.sum(DataFilt[indexX1:indexX2,:],axis=0)
plt.scatter(magField1,Mode1)
plt.plot(magField1,Mode1)


m1low = np.average(Mode1[np.argmin(np.abs(magField1 + 26 )) : np.argmin(np.abs(magField1 + 15 ))])
print(m1low)
plt.hlines(y= m1low , xmin= -26, xmax= -15 , linestyle = 'dashed', color='k')

m1high = np.average(Mode1[np.argmin(np.abs(magField1 + 11 )) : np.argmin(np.abs(magField1 -6 ))])
print(m1high)
plt.hlines(y= m1high , xmin= -11, xmax= 6 , linestyle = 'dashed', color='k')
# plt.xlim(-25.5,6.5)


# indexX12 = np.argmin(np.abs(Freq - 10.20*1e9))
# indexX22 = np.argmin(np.abs(Freq - 10.55*1e9))
# Mode2=np.sum(DataFilt[indexX12:indexX22,:],axis=0)
# plt.scatter(magField1,Mode2)


indexX3a = np.argmin(np.abs(Freq - 9.1*1e9))
indexX3b = np.argmin(np.abs(Freq - 9.5*1e9))
Mode3=np.sum(DataFilt[indexX3a:indexX3b,:],axis=0)
plt.scatter(magField1,Mode3)
plt.plot(magField1,Mode3)

m3high = np.average(Mode3[np.argmin(np.abs(magField1 + 26 )) : np.argmin(np.abs(magField1 + 20 ))])
print(m3high)
plt.hlines(y= m3high , xmin= -26, xmax= -20 , linestyle = 'dashed', color='k')

m3low = np.average(Mode3[np.argmin(np.abs(magField1 + 15 )) : np.argmin(np.abs(magField1 -6 ))])
print(m3low)
plt.hlines(y= m3low , xmin= -15, xmax= 6 , linestyle = 'dashed', color='k')


# print(np.average(Mode3[0:7]))
# print(np.average(Mode1[-10:]))
Boundary1 = 0.0141436319594531
Boundary3 = 0.008533746078828224

cut1 = 0.5
cut2 = 0.5

i=0
while Mode3[i] > Boundary3*cut1 :
#while Mode3[i] > 0.005 :
    i=i+1
    if i == len(magField1):
        break
print(magField1[i]-0.5)

b= 0
while Mode1[b] < Boundary1*cut2:
    b=b+1
    if b == len(magField1):
        break
    
if b< len(magField1):
    print(magField1[b]-0.5)
else:
    print(np.nan)