# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 14:11:43 2018

@author: KorbinianLocal
"""

import numpy  as np
import scipy
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import cm
import matplotlib as mpl
from scipy.optimize import curve_fit
from scipy.fftpack import rfft, irfft, fftfreq,fft,ifft,fft2,ifft2
import os
import scipy.signal
#from scipy import ndimag

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
font = {'size'   : 9}
mpl.rc('font', **font)
# Say, "the default sans-serif font is COMIC SANS"
mpl.rcParams['font.sans-serif'] = "Arial"
# Then, "ALWAYS use sans-serif fonts"
mpl.rcParams['font.family'] = "sans-serif"


st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 15 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean   # height in inches #2.7 ohne titel
fig_size =  [fig_width,fig_height*1.25]
params = {'axes.labelsize': 9,    #'backend': 'eps',
          'legend.fontsize': 9,
          'xtick.labelsize': 9,
          'ytick.labelsize': 9,
          'text.usetex': False,
          'figure.figsize': fig_size,
          'figure.autolayout': True}
plt.rcParams.update(params)




#import matplotlib
plt.rcParams['animation.ffmpeg_path'] = 'C:/ffmpeg/bin/ffmpeg'
#matplotlib.use('Qt5Agg')

#Folder="181212/"
#Folder="181212/"
#Date="MPI_181212"
#File="074"
Folder="200515/"
Date="MPI_200515"
File="063"
#Field=10

os.chdir('..')
os.chdir('..')

info=np.genfromtxt("%s%s%s.txt" %(Folder,Date,File))

Frequency=info[0]
Field=info[1]
MagicNumber=int(info[2])

Power=info[3]
dX=info[4]
dY=info[5]

# Field values:
xminR = 39
xmaxR = 25
step = 1 
    
xmin = xminR + step/2
xmax = xmaxR - step/2

#
# MagicNumber = 22
#Frequency=1.57
#
#MagicNumber=22
#Power=120
#dX=0.1
#dY=0.1



def complex_array_to_rgb(X, Y, theme='dark', rmax=None):
    '''Takes an array of complex number and converts it to an array of [r, g, b],
    where phase gives hue and saturaton/value are given by the absolute value.
    Especially for use with imshow for complex plots.'''
    absmax = rmax or np.abs(X).max()
    Z = np.zeros(X.shape + (3,), dtype='float')
    Z[..., 0] = Y / (2 * np.pi) % 1
    if theme == 'light':
        Z[..., 1] = np.clip(np.abs(X) / absmax, 0, 1)
        Z[..., 2] = 1
    elif theme == 'dark':
        Z[..., 1] = 1
        Z[..., 2] = np.clip(np.abs(X) / absmax*10, 0, 1)
    Z = mpl.colors.hsv_to_rgb(Z)
    return Z



def BBXimport(M, path):
    with open(path, 'rb') as f:
        a=np.fromfile(f, dtype='>u4')
    N=a[0]
    Y=a[2]
    X=a[1]
    Bild=np.zeros([Y,X,N])
    for k in range(0,N):
        for i in range(0,Y):
            for j in range(0,X):
                Bild[i,j,k*M%N]=a[3+i+Y*j+Y*X*k]
    Normbild=np.zeros(np.shape(Bild))
    S=np.mean(Bild,axis=2)
    for i in range(0,N):
        Normbild[:,:,i]=np.flip(Bild[:,:,i]/S, axis=0)-1
        # Normbild[:,:,i]=np.flip(Bild[:,:,i], axis=0)
    del(Bild)
    return Normbild,N
    
Pic,N=BBXimport(MagicNumber,'%s%s%s.bbx' %(Folder,Date,File))
Pic = np.swapaxes(Pic,1,0)
Pic=np.flip(Pic,axis=0)
Pic= Pic[:,1:,:]

static=np.loadtxt("%s%s%s_a.xim" %(Folder,Date,File))
static=np.flip(static,axis=0)
static=np.flip(static,axis=1)    #new to match plot ptogram
static = static[:,1:]
# xmin=0
ymin=0
lengthY=len(static[:,0])
# xmax=len(static[0,:])*dX
ymax=len(static[:,0])*dY
extent = xmin, xmax, ymin, ymax

extentT =  ymin, ymax, xmin, xmax
#


avPicT=np.mean(np.mean(Pic[:,:,:],axis=0),axis=0)
for i in range(0,N):
        Pic[:,:,i]= Pic[:,:,i]-avPicT[i]
        
        




os.chdir('Plots')
os.chdir('4.21GHz')       


f_signal = fft(Pic,axis=2)

# If our original signal time was in seconds, this is now in Hz    

cut_f_signal = f_signal.copy()
# In general: i=1 and i=N are +1/T and -1?T
cut_f_signal[:,:,:] = 0
#cut_f_signal[:,:,1] = 0
#cut_f_signal[:,:,2] = 0
#cut_f_signal[:,:,3] = 0
#cut_f_signal[:,:,4] = 0
#cut_f_signal[:,:,5] = 0
##cut_f_signal[:,:,6] = 0
cut_f_signal[:,:,1] = f_signal[:,:,1]
cut_f_signal[:,:,N-1] = f_signal[:,:,N-1]


meantest=np.abs(cut_f_signal[:,:,1]+cut_f_signal[:,:,N-1])


x=np.arange(0,len(static[:,0])*dX,dX)


FFT_Pic = ifft(cut_f_signal).real

def rot90(data):
    return np.flip((data).T,axis=1)


vmin1 = -(np.abs([FFT_Pic[:,:,0].min(), FFT_Pic[:,:,0].max()])).max()
vmax1 = -vmin1

vmin2 = 0
vmax2 = np.abs((cut_f_signal[:,:,1])).max()

fig, axs = plt.subplots(4, 1)
#fig.suptitle("Title for whole figure", fontsize=16)
#plt.imshow(Amplitude, cmap="Greys",extent =extent,aspect="auto")
#plt.title('%s Ghz, %s mT, %s mV'%(Frequency, Field,Power))
#axs[0].title.set_text('%s mT'%(Field))
axs[0].set_title("%s GHz, Field %s mT to %s mT"%(Frequency,xminR, xmaxR))
#plt.imshow(static*-1, cmap="gist_yarg",extent =extent,aspect="auto")
axs[0].imshow(rot90(static*-1), cmap="gist_yarg",extent =extentT,aspect="auto")


#axs[1].set_title("Snapshot")
#axs[1].imshow(rot90(Pic[:,:,0]), cmap="Greys",extent =extentT,aspect="auto")

axs[1].set_title("Snapshot (FFT filtered)")
axs[1].imshow(rot90(FFT_Pic[:,:,0]), cmap="Greys",vmin=vmin1,vmax=vmax1 ,extent =extentT,aspect="auto")

axs[2].set_title("Amplitude (FFT filtered)")
axs[2].imshow(rot90(np.abs((cut_f_signal[:,:,N-1]))), cmap="Greys",vmin=0,vmax=vmax2,extent =extentT,aspect="auto")
axs[0].set_ylabel('Field (mT)')
axs[1].set_ylabel('Field (mT)')
axs[2].set_ylabel('Field (mT)')
axs[3].set_ylabel('Field (mT)')
#axs[2].imshow(rot90(np.abs((meantest))), cmap="Greys",vmin=0,vmax=vmax2,extent =extentT,aspect="auto")
#axs[2].imshow(rot90(np.abs((meantest))), cmap="Greys",vmin=0,vmax=vmax2,extent =extentT,aspect="auto")


axs[3].set_title("Phase")
axs[3].imshow(rot90(np.mean(FFT_Pic[:,:,:],axis=2)), cmap="hsv",extent =extentT,aspect="auto")


##axs[4].plot(x,np.flip(np.mean(static,axis=1)/np.mean(static,axis=1).max()),label='static')
#f_signalStatic = fft2(static)
#cut_f_signalStatic = f_signalStatic.copy()
#le=len(static[:,1])
##cut_f_signalStatic[int(480/495*le):,:] = 0
##cut_f_signalStatic[0:int(le/2+5),:] = 0
#staticFFT = ifft2(cut_f_signalStatic).real
#staticFFT=staticFFT/staticFFT.max()
#
#minStatic=staticFFT.min()
#maxStatic=staticFFT.max()
#img=staticFFT#
##hist, bin_edges = np.histogram(img, bins=60)
##bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
#
#binary_img = img > -0.1
##axs[4].imshow(rot90(binary_img*-1), cmap="gist_yarg",extent = (ymin, ymax, -1, 1), aspect="auto")
##staticFFT[-92:,:]=+1
#staticFFT[-60:,:]=+1
#staticFFT[0:74,:]=+1
#
#

#####Test k filtered
#f1 = np.fft.fft2(FFT_Pic [:,:,:],s=(10000,100),axes=(0,1))   
#f=np.sum(np.abs(f1[:,:,:]),axis=2) 
#fshift = np.fft.fftshift(f)
##    
##Method 3 
##    f_signal = fft(Pic,axis=2)
##    cut_f_signal = f_signal.copy()
### In general: i=1 and i=N are +1/T and -1?T
##    cut_f_signal[:,:,:] = 0
##    cut_f_signal[:,:,1] = f_signal[:,:,1]
##    cut_f_signal[:,:,N-1] = f_signal[:,:,N-1]
##    TimeFFT = ifft(cut_f_signal).real    
##    
##    f1 = np.fft.fft2(TimeFFT[:,:,:]/40,s=(10000,100),axes=(0,1))   
##    f=np.sum(np.abs(f1[:,:,:]),axis=2) 
##    fshift = np.fft.fftshift(f)       
##    
#
# #................   
#
#FT_Pic=np.abs(fshift)
#
#
#nX=len(FT_Pic[0,:])
#SamplinglengthX=dX*1e-6   #10 nm
#Xff=np.arange(nX)/(nX*SamplinglengthX)*np.pi*2*1e-6
#
#n = FT_Pic[0,:].size
#Xfreq = sorted(np.fft.fftfreq(n, d=SamplinglengthX)*np.pi*2*1e-6)
#stepX=(Xfreq[1]-Xfreq[0])/2
#Xfreq-=stepX
#
#nY=len(FT_Pic[:,0])
#SamplinglengthY=dY*1e-6   #10 nm
#Yff=np.arange(nY)/(nY*SamplinglengthY)*np.pi*2*1e-6
#
#nY = FT_Pic[:,0].size
#Yfreq = sorted(np.fft.fftfreq(nY, d=SamplinglengthY)*np.pi*2*1e-6)
#
#x,y = np.meshgrid(Xfreq,Yfreq)
#
##plt.pcolormesh(x,y,FT_Pic)
###plt.xlim(-25,25)
##plt.ylim(0,100)
###plt.plot(Yff,FT_Pic[:,0])
##plt.xlim(0,40)
##plt.xlabel("kx (rad/um)")
##plt.ylabel("ky (rad/um)")
#
#
#kx=np.average(FT_Pic,axis=1)*24/40
##    kx[(y[:,0]<62.8*0.85)] = 0
##    kx[(y[:,0]>62.8*1.15)] = 0
#
#kx[(y[:,0]<15.7*0.8)] = 0
#kx[(y[:,0]>15.7*1.2)] = 0
#
#
#
#
#
#





##staticFFT[0:44,:]=+1
##axs[4].imshow(rot90(staticFFT*-1), cmap="gist_yarg",extent = (ymin, ymax,0, 1),vmin=-0.2,vmax=0.9, aspect="auto")
##axs[4].imshow(rot90(staticFFT*-1), cmap="gist_yarg",extent = (ymin, ymax,0, 1), aspect="auto")
#
#axs[4].imshow(rot90(static*-1), cmap="gist_yarg",extent =extentT,aspect="auto")
#
#axs[4].plot(x,((np.flip(np.mean(np.abs((cut_f_signal[:,:,1])),axis=1)/np.mean(np.abs((cut_f_signal[:,:,1])),axis=1).max()))),color='orange',label='FFT Amplitude')
#
#np.mean(np.abs(cut_f_signal[:,:,1]),axis=1)
#
#axs[4].plot(x,((np.flip(np.mean(np.abs((cut_f_signal[:,:,1])),axis=1)/np.mean(np.abs((cut_f_signal[:,:,1])),axis=1).max()))),color='orange',label='FFT Amplitude mean')
#axs[4].set_xlim(ymin,ymax)
#axs[4].legend(loc=1)
#





fig.tight_layout()
plt.savefig('FIeldscan%sGHz%s%s.jpg'%(Frequency,Date,File),dpi=150)






