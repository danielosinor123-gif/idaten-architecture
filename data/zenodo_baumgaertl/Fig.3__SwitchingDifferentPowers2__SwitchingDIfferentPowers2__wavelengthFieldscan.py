import numpy  as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
import os
from scipy.fftpack import rfft, irfft, fftfreq,fft,rfftfreq,ifft
from matplotlib import gridspec
from scipy.optimize import curve_fit
#plt.rcParams['animation.ffmpeg_path'] = 'C:/ffmpeg/bin/ffmpeg'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
font = {'size'   : 9}
mpl.rc('font', **font)
# Say, "the default sans-serif font is COMIC SANS"
mpl.rcParams['font.sans-serif'] = "Arial"
# Then, "ALWAYS use sans-serif fonts"
mpl.rcParams['font.family'] = "sans-serif"
#matplotlib.rc('text', usetex='false') 
st=1
fig_width_pt = 246.0*st  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = 6.69*1.5 # width in inches #6.69 two column single 3.37
fig_height = fig_width*golden_mean    # height in inches #2.7 ohne titel
#fig_size =  [fig_width*0.2,fig_height*1]
fig_size =  [fig_width/1.5,fig_height]
params = {'axes.labelsize': 9*st,    #'backend': 'eps',
          'legend.fontsize': 9*st,
          'xtick.labelsize': 9*st,
          'ytick.labelsize': 9*st,
          'text.usetex': False,
          'figure.figsize': fig_size}
plt.rcParams.update(params)



Folder="200515/"
Date="MPI_200515"
File="063"
#File="040"



xminR = 39
xmaxR = 25
step = 1 

Fieldlist = np.arange(xmaxR,xminR,1)
ToPlot = 28

FieldVal = np.argmin(np.abs(Fieldlist - ToPlot))
# FieldVal = 10

scal = 0.030*2

os.chdir('..')
os.chdir('..')   

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
    del(Bild)
    return Normbild,N

info=np.genfromtxt("%s%s%s.txt" %(Folder,Date,File))

Frequency=info[0]
Field=info[1]
MagicNumber=int(info[2])
Power=info[3]
dX=info[4]
dY=info[5]


    
Pic,N=BBXimport(MagicNumber,'%s%s%s.bbx' %(Folder,Date,File))
Pic = np.swapaxes(Pic,1,0)
Pic=np.flip(Pic,axis=0)
Pic= Pic[:,1:,:]
Pic= Pic[:,FieldVal:int(FieldVal+1),:]


static=np.loadtxt("%s%s%s_a.xim" %(Folder,Date,File))
static=np.flip(static,axis=0)
static=np.flip(static,axis=1)    #new to match plot ptogram
static = static[:,1:]
static = static[:,FieldVal:int(FieldVal+1)]

#
avPicT=np.mean(np.mean(Pic[:,:,:],axis=0),axis=0)
for i in range(0,N):
        Pic[:,:,i]= Pic[:,:,i]-avPicT[i]

os.chdir('Plots')
os.chdir('4.21GHz')  


f_signal = fft(Pic,axis=2)
cut_f_signal = f_signal.copy()
# In general: i=1 and i=N are +1/T and -1?T
cut_f_signal[:,:,:] = 0
cut_f_signal[:,:,1] = f_signal[:,:,1]
cut_f_signal[:,:,N-1] = f_signal[:,:,N-1]
FFT_Pic = ifft(cut_f_signal).real




#xmin, xmax, ymin, ymax = np.amin(static[:,0]), np.amax(static[:,0]), np.amin(static[0,:]), np.amax(static[0,:])
xmin=0
ymin=0
lengthY=len(static[:,0])
xmax=len(static[0,:])*dX
ymax=len(static[:,0])*dY
extent = xmin, xmax, ymin, ymax

#fig = plt.figure(frameon=False)
#plt.title('%s Ghz, %s mT, %s mV'%(Frequency, Field,Power))
#plt.title(' %s mT'%(Field))
#plt.title('Static')
#
x=np.arange(0,len(Pic[:,0,0])*dY,dY)
#for i in range(N):
#plt.plot(x,np.mean(FFT_Pic[:,:,1],axis=1))






#ims = []
#for i in range(N):    
##    im = plt.imshow(Pic[:,:,i], cmap="viridis", animated=True, alpha=0.6,extent =extent,aspect="auto")
#    im = plt.plot(x,np.mean(FFT_Pic[:,:,i],axis=1))
##    im = plt.imshow(FFT_Pic[:,:,i], cmap="Greys", animated=True,vmin=-0.025, vmax=0.025,interpolation= 'Nearest', alpha=1,extent =extent, aspect ="auto")
#    ims.append([im])



#ani = animation.ArtistAnimation(fig, ims, interval=100)
#ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=0)
#mywriter = animation.FFMpegWriter()
##ani.save('%s_%s_%s%s.mp4'%(Frequency,Field,Date,File),writer=mywriter,dpi=300)
#plt.show()


    
#imgs = []
#for i in range(N):
##    img = plt.plot(x, np.mean(FFT_Pic[:,:,i],axis=1), 'b-o')
#    img = plt.plot(x, np.mean(FFT_Pic[:,:,i],axis=1), 'b-o')
#    imgs.append(img)
#anim = animation.ArtistAnimation(fig, imgs, interval=250)
#anim.save('result1.gif', 'imagemagick')
#plt.show()
##

#for i in range(N+1):
#    plt.plot(x, np.flip(np.mean(FFT_Pic[:,:,i%N],axis=1))+i*0.02, 'b-o',markersize=3)
##    plt.plot(x, np.flip(np.mean(Pic[:,:,i%N],axis=1))+i*0.02, 'b-o',markersize=3)
#    plt.hlines(xmin=0,xmax=2.5,y=i*0.02,colors='k', linestyles='dashed')
#    plt.annotate('%s/7T'%(i), (-0.205,i*0.02),fontsize='10')


av=np.mean(FFT_Pic[:,:,:],axis=1)
#
#av1=av[:,0]
#phase1 = np.arcsin(av1)
##plt.plot(x,av1)
#plt.plot(x,phase1)






#av=av[80:160,:]
#x=x[0:80]


#Man1
#A=0 
#B=80



##Man2
A=-285
B=-1

A=-400
B=-310



# A=0
# B=30



#A=130
#B=238


av=av[A:B,:]
x = np.flip(x)
x=x[A:B]
x = np.flip(x)


av2=av**2
#av2=np.abs(av)
amplitude= np.mean(av2,axis=1)




fig = plt.figure()
gs = gridspec.GridSpec(9, 3)
gs.update(wspace=0.0, hspace=0.00)
#ax1 = fig.add_subplot(gs[0,:])
ax1 = plt.subplot(gs[0,:])

ax1.plot(x, np.flip(np.mean(static[A:B,:],axis=1)), 'k',markersize=3)
#ax1.plot(x, np.flip(amplitude), 'k',markersize=3)



ax1.set_ylabel('static')
ax1.set_yticks([], [])


def SinFit(x,wavelength, PhaseOff,Amp):
    return Amp*np.sin(x*np.pi*2/wavelength + PhaseOff)

popt=np.zeros((7,3))
errorwavelength = np.zeros((7))
for i in range(7):
##    popt[i,:], pcov = curve_fit(cosin,xdata,data[:,i], p0=[0.5,200,2700], bounds=((-np.inf, 10, 20), (np.inf, np.inf, np.inf)))   #, maxfev=50000)  
#    popt[i,:], pcov = curve_fit(SinFit,x,av[:,i], p0=[0.1,1.351+i*np.pi*2/8,0.006], maxfev=50000)
    popt[i,:], pcov = curve_fit(SinFit,x,av[:,i], p0=[0.199,2.351+i*np.pi*2/8,0.006], maxfev=50000)
    errorwavelength[i] = np.sqrt(np.diag(pcov))[0]



#ax2 = plt.subplot(gs[1,:],sharex=ax1)
#
#ax2.set_ylabel('Power')
#ax2.set_yticks([], [])
#ax2.plot(x, np.flip(amplitude), 'k',markersize=3)


#ax2 = fig.add_subplot(gs[1:,:],sharex=ax1)
ax3 = plt.subplot(gs[1:,:],sharex=ax1)
    
for i in range(7):
    ax3.plot(x, 1.75*np.flip(av[:,i])+i*scal, 'b-o',markersize=6)
    ax3.plot(x, 1.75*np.flip(SinFit(x,*popt[i,:]))+i*scal, 'g-')
    

print(np.average(popt[:,0]))  
print(np.std(popt[:,0]))
print(np.average(errorwavelength)) 
#    plt.plot(x, np.flip(np.mean(Pic[:,:,i%N],axis=1))+i*0.02, 'b-o',markersize=3)
#    ax3.hlines(xmin=0,xmax=1.0,y=i*0.030,colors='k', linestyles='dashed')
#    ax3.annotate('%s/7T'%(i+1), (-0.15,i*0.015),fontsize='10')
        
plt.setp(ax1.get_xticklabels(), visible=False)

ax3.set_xlabel('y (um))')
ax3.set_yticks([], [])
ax3.set_ylabel('Amplitude (arb. units)')
#plt.xlim(-0.175,2.5)
#
#plt.subplots_adjust(hspace=-1)
#gcf().subplots_adjust(hspace=-10)
#fig.tight_layout()
plt.savefig('RReportnTime_FFT%s_%sn%s%s.pdf'%(Frequency,Field,Date,File),dpi=150)
#


#plt.plot(x, np.flip(np.mean(static[:,:],axis=1))+i*0.02, 'k',markersize=3)
#plt.ylabel('Transmission')
#plt.xlabel('y (um))')



#xx=np.linspace(0,2.5, num=10000)
#plt.plot(xx, np.sin(2*np.pi*xx/0.1),'k')


