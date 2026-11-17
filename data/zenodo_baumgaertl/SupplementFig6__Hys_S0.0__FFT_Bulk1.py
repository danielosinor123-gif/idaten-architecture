from __future__ import division, print_function

import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import copy
import csv
from math import pow
from numpy import ma
import matplotlib.colors as colors
from numpy import genfromtxt
from scipy.fftpack import rfft, irfft, fftfreq
import pandas as pd

for FieldVal in range(16):
    
    Filname = str(FieldVal*2+2).zfill(2)+'mT.out'
    Filname2 = str(FieldVal*2+2).zfill(2)
    os.chdir(Filname)
    
    
    X=np.array([])
    num=1199
    
    toskip = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,204800+28,204800+29]
    Ref = pd.read_csv('m_x_yrange0-25_000000.ovf',delimiter=",",skiprows=toskip)
    #Ref = Ref[100:,0]
    Ref = Ref.to_numpy()
    #
    dat1 = pd.read_csv('m_x_yrange0-25_000000.ovf',delimiter=",",skiprows=toskip)
    dat1 = dat1.to_numpy()
    #datx1=dat1[0:20,600:8192-600]
    mx1=dat1-Ref
    mx1 = mx1.reshape(25,8192)
    mx1=mx1[np.newaxis,...]
    
    for i in range(num):
    #    datx = np.loadtxt('m_x'+str(i).zfill(6)+'.ovf').reshape(32,8192)
        datx = pd.read_csv('m_x_yrange0-25_'+str(i).zfill(6)+'.ovf',delimiter=",",skiprows=toskip)
        datx = datx.to_numpy()
    #    datx=datx.reshape(32,8192)
        mx=datx-Ref
        mx=mx.reshape(25,8192)
    
        mx1 = np.vstack((mx1,mx[np.newaxis,...]))
    #    
    
    

    np.save('mxImported.npy', mx1)
    
    # mx1 = np.load("mxImported.npy")
    mx1[:,20:26,:]=mx1[:,20:26,:]*(800/140)
    # mx1[:,20:30,:] = mx1[:,20:30,:]*800/140.0
    
    
    #plt.imshow(mx1[1000,:,:], aspect = "auto")
    
    
    
    f_s = 1/10e-3   #sampling rate in GHz
    
    from scipy import fftpack
    # mx1 = mx1[:,:,5496:6296]
    # mx1 = mx1[:,:,1896:2696]
    # mx1 = mx1[:,:,3096:5096]
    
    X = fftpack.fft(mx1,axis=0)
    freqs = fftpack.fftfreq(len(mx1[:,0,0])) * f_s
    
    #Xabs = np.abs(X[:,:,4096-1000 : 4096+1000])
    Xabs = np.abs(X)
    
    
    Xav = np.average(Xabs[:,:,3096:5096], axis=(1,2))
    fig, ax = plt.subplots()
    Layer= 'Sat S= 0'
    #ax.stem(freqs, Xav )
    ax.plot(freqs, Xav)
    ax.set_title(Layer)
    np.savetxt('Frequency%s.txt'%Layer, freqs )
    np.savetxt('Amplitudes%s.txt'%Layer, Xav )
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('FFT Amplitude')
    #ax.set_xlim(0, f_s / 2)
    #ax.set_ylim(0, 1.3)
    ax.set_xlim(0, 15)
    plt.savefig('%s_Mid.png'%Layer,dpi=600)
    plt.close()
    np.savetxt( "FFT_mid.txt" , Xav )
    #ax.set_ylim(-5, 110)
    
    
    XavR = np.average(Xabs[:,:,5496:6296], axis=(1,2))
    fig, ax = plt.subplots()
    Layer= 'Sat S= 0'
    #ax.stem(freqs, Xav )
    ax.plot(freqs, XavR)
    ax.set_title(Layer)
    np.savetxt('Frequency%s.txt'%Layer, freqs )
    np.savetxt('Amplitudes%s.txt'%Layer, Xav )
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('FFT Amplitude')
    #ax.set_xlim(0, f_s / 2)
    #ax.set_ylim(0, 1.3)
    ax.set_xlim(0, 15)
    plt.savefig('%s_Right.png'%Layer,dpi=600)
    plt.close()
    np.savetxt( "FFT_right.txt", XavR )
    
    XavL = np.average(Xabs[:,:,1896:2696], axis=(1,2))
    fig, ax = plt.subplots()
    Layer= 'Sat S= 0'
    #ax.stem(freqs, Xav )
    ax.plot(freqs, XavL)
    ax.set_title(Layer)
    np.savetxt('Frequency%s.txt'%Layer, freqs )
    # np.savetxt('Amplitudes%s.txt'%Layer, Xav )
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('FFT Amplitude')
    #ax.set_xlim(0, f_s / 2)
    #ax.set_ylim(0, 1.3)
    ax.set_xlim(0, 15)
    plt.savefig('%s_Left.png'%Layer,dpi=600)
    plt.close()
    np.savetxt( "FFT_right.txt", XavL)

    
    ##
    #
#

    XavT = np.average(Xabs[:,:,1896:6296], axis=(1,2))
    fig, ax = plt.subplots()
    Layer= 'Sat S= 0'
    #ax.stem(freqs, Xav )
    ax.plot(freqs, XavT)
    ax.set_title(Layer)
    np.savetxt('Frequency%s.txt'%Layer, freqs )
    # np.savetxt('Amplitudes%s.txt'%Layer, Xav )
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('FFT Amplitude')
    #ax.set_xlim(0, f_s / 2)
    #ax.set_ylim(0, 1.3)
    ax.set_xlim(0, 15)
    plt.savefig('%s_Tot.png'%Layer,dpi=600)
    plt.close()
    np.savetxt( "FFT_tot.txt", XavT)
    os.chdir('..')
    np.savetxt( "%smT_FFT_mid.txt" %Filname2, Xav )
    np.savetxt( "%smT_FFT_right.txt"%Filname2, XavR )
    np.savetxt( "%smT_FFT_left.txt"%Filname2, XavL)
    np.savetxt( "%smT_FFT_tot.txt"%Filname2, XavT)
    





































#
#

#2D FFT
#TopLayers1=mx1[:,:,0:2400]
#
##TopLayers1=mx1[:,:,2550:6992-2550]
##TopLayers=np.average(TopLayers1,axis=1)
#
#f = np.fft.fftn(TopLayers1)
##f=f[:,19,:]
#f=np.average(f,axis=1)
#
#          
#fshift = np.fft.fftshift(f)
##fshift=f
#FT_Pic=np.abs(fshift)
#
#
#nX=len(FT_Pic[0,:])
#SamplinglengthX=5e-9   #10 nm
#Xff=np.arange(nX)/(nX*SamplinglengthX)*np.pi*2*1e-6
#
#n = FT_Pic[0,:].size
#Xfreq = sorted(np.fft.fftfreq(n, d=SamplinglengthX)*np.pi*2*1e-6)
#stepX=(Xfreq[1]-Xfreq[0])/2
#Xfreq-=stepX
#
#nY=len(FT_Pic[:,0])
#SamplinglengthY=10e-12*1e9   #10 nm
#Yff=np.arange(nY)/(nY*SamplinglengthY)
#
#nY = FT_Pic[:,0].size
#Yfreq = sorted(np.fft.fftfreq(nY, d=SamplinglengthY))
##Yfreq=Yfreq*1e9
#
#x,y = np.meshgrid(Xfreq,Yfreq)
#
#plt.pcolormesh(x,y,FT_Pic, vmin=0,vmax=0.5,rasterized="True")
#plt.xlim(0,100)
#plt.ylim(0,20)
###plt.plot(Yff,FT_Pic[:,0])
##plt.xlim(0,75)
#
#plt.xlabel("Wavevector (rad/um)")
#plt.ylabel("Frequency (GHz)")
#
#
#plt.tight_layout()
#plt.savefig('FFT_MiddelGrating.






#
#time   = np.linspace(0,10e-12*num,num+1)
#signal = mx1[:,:,:]
##cut_signal = mx1[:,0,0]
#W = np.fft.fftfreq(num+1, 10e-12)
#f_signal = np.fft.fft(signal,axis=0)
#
#f_signalav=np.abs(f_signal)
#f_signalav=np.average(f_signalav,axis=1)
#f_signalav=np.average(f_signalav,axis=1)
#
#cut_low = 9.1e9
#cut_high = 9.3e9
## If our original signal time was in seconds, this is now in Hz    
#cut_f_signal = f_signal.copy()
#cut_f_signal[ np.logical_and(W < cut_low, W > -cut_low),:,:] = 0
#cut_f_signal[(W>cut_high),:,:] = 0
#cut_f_signal[(W<-cut_high),:,:] = 0
##cut_f_signal[(W<4e9),:,:] = 0
##cut_f_signal[(W>5e9),:,:] = 0
#cut_signal = np.fft.ifft(cut_f_signal,axis=0)
#
#
##plt.plot(mz1[600,12,:])#
#plt.plot(cut_signal[650,19,:])
#
#


#
#
#Data = mx1[:,:,:]
##plt.imshow(mx1[620,:,:],aspect=100)
#
#
#time   = np.linspace(0,10e-12*num,num+1)
#
#Xin = Data[:,0,0].size
##Xpad = 40002
#
#Xpad=Xin
#
#Yin = Data[0,0,:].size
##Ypad = 600
#
#Ypad=Yin
#
#
#cut_low = 15.0e9
#cut_high =15.2e9
##2/(delta f)=2*s/vg or maybe s/vg
#W = np.fft.fftfreq(Xpad, d=time[1]-time[0])
#
#Wx = np.fft.fftfreq(Ypad, d=0.005)*2*np.pi
##print(WX)
#cut_lowX= 50
#cut_highX= 75
#
# 
#    
#
#f_signal = np.fft.fft2(Data,s=(Xpad,Ypad),axes=(0,2))
#cut_f_signal = f_signal.copy()
#cut_f_signal[ np.logical_and(W < cut_low, W > -cut_low),:,:] = 0
#cut_f_signal[(W>cut_high),:,:] = 0
#cut_f_signal[(W<-cut_high),:,:] = 0
#cut_f_signal[:, :, np.logical_and(Wx < cut_lowX, Wx > -cut_lowX )] = 0
#cut_f_signal[:,:,(Wx>cut_highX)] = 0
#cut_f_signal[:,:,(Wx<-cut_highX)] = 0
#
#DataFilt1 = np.fft.ifft2(cut_f_signal,axes=(0,2))
#DataFilt = DataFilt1.real
##plt.plot(DataFilt[700,19,:])
##
##
##
#plt.imshow(DataFilt[720,:,:],aspect=100)
#
#
#
#
#
#
#
#






