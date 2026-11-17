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


FieldVal = 1
Filname2 = str(FieldVal*2).zfill(2)
Frequency = np.loadtxt("Frequency.txt")


# np.savetxt( "%smT_FFT_mid.txt" %Filname2, Xav )
# np.savetxt( "%smT_FFT_right.txt"%Filname2, XavR )
# np.savetxt( "%smT_FFT_left.txt"%Filname2, XavL)

dat = np.fft.fftshift(np.loadtxt("%smT_FFT_right.txt"%Filname2))

for FieldVal in range(11):
    Filname2 = str(FieldVal*2+4).zfill(2)
    dat1 = np.fft.fftshift(np.loadtxt("%smT_FFT_right.txt"%Filname2))

    #    datx = np.loadtxt('m_x'+str(i).zfill(6)+'.ovf').reshape(32,8192)
    dat = np.vstack((dat,dat1[np.newaxis,...]))


# plt.imshow(dat, aspect= 'auto')

z = dat
x = np.fft.fftshift(Frequency)
dx = (x[1]- x[0])*0.5
x= x -dx
# y = np.arange(2,18.1,2)
y = np.arange(1,25.1,2)


# plt.plot(Frequency, dat[1,:])



fig, ax = plt.subplots()
cmap = ax.pcolormesh(y,x, np.swapaxes(z,0,1), cmap = "Greys", vmin= 0 ,vmax = 0.05)
plt.ylim(0,15)
fig.colorbar(cmap)
plt.show()
plt.title("S21")
plt.savefig("ePropagationRight_S1.0.png", dpi=600)
plt.close()




FieldVal = 1
Filname2 = str(FieldVal*2).zfill(2)
Frequency = np.loadtxt("Frequency.txt")


# np.savetxt( "%smT_FFT_mid.txt" %Filname2, Xav )
# np.savetxt( "%smT_FFT_right.txt"%Filname2, XavR )
# np.savetxt( "%smT_FFT_left.txt"%Filname2, XavL)

dat = np.fft.fftshift(np.loadtxt("%smT_FFT_mid.txt"%Filname2))

for FieldVal in range(11):
    Filname2 = str(FieldVal*2+4).zfill(2)
    dat1 = np.fft.fftshift(np.loadtxt("%smT_FFT_mid.txt"%Filname2))

    #    datx = np.loadtxt('m_x'+str(i).zfill(6)+'.ovf').reshape(32,8192)
    dat = np.vstack((dat,dat1[np.newaxis,...]))


# plt.imshow(dat, aspect= 'auto')

z = dat
x = np.fft.fftshift(Frequency)
dx = (x[1]- x[0])*0.5
x= x -dx
# y = np.arange(2,18.1,2)
# y = np.arange(1,19.1,2)


# plt.plot(Frequency, dat[1,:])



fig, ax = plt.subplots()
cmap = ax.pcolormesh(y,x, np.swapaxes(z,0,1), cmap = "Greys", vmin= 0 ,vmax = 0.2)
plt.ylim(0,15)
fig.colorbar(cmap)
plt.show()
plt.title("S11")
plt.savefig("ePropagationMid_S1.0.png", dpi=600)
plt.close()



FieldVal = 1
Filname2 = str(FieldVal*2).zfill(2)
Frequency = np.loadtxt("Frequency.txt")


# np.savetxt( "%smT_FFT_mid.txt" %Filname2, Xav )
# np.savetxt( "%smT_FFT_right.txt"%Filname2, XavR )
# np.savetxt( "%smT_FFT_left.txt"%Filname2, XavL)

dat = np.fft.fftshift(np.loadtxt("%smT_FFT_tot.txt"%Filname2))

for FieldVal in range(11):
    Filname2 = str(FieldVal*2+4).zfill(2)
    dat1 = np.fft.fftshift(np.loadtxt("%smT_FFT_tot.txt"%Filname2))

    #    datx = np.loadtxt('m_x'+str(i).zfill(6)+'.ovf').reshape(32,8192)
    dat = np.vstack((dat,dat1[np.newaxis,...]))


# plt.imshow(dat, aspect= 'auto')

z = dat
x = np.fft.fftshift(Frequency)
dx = (x[1]- x[0])*0.5
x= x -dx
# y = np.arange(2,18.1,2)
# y = np.arange(1,19.1,2)


# plt.plot(Frequency, dat[1,:])



fig, ax = plt.subplots()
cmap = ax.pcolormesh(y,x, np.swapaxes(z,0,1), cmap = "Greys", vmin= 0 ,vmax = 0.1)
plt.ylim(0,15)
fig.colorbar(cmap)
plt.show()
plt.title("Sat S=1")
plt.savefig("ePropagationTot_S1.0.png", dpi=600)
plt.savefig("ePropagationTot_S1.0.pdf", dpi=600)
# plt.close()













