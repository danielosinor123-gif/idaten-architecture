# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:11:42 2020

@author: bamgaert
"""

import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
import shutil

import os

StartFreq = 1.0
EndFreq=  13.0
Step = 0.25

#os.chdir('RefFileMeas') 
VNAFile = open('PathFile.txt',"w+")
#os.chdir('..')  


while StartFreq <= EndFreq: 
    newpath = str(round(StartFreq,2))
    VNAFile.write("FoldertoAdd"+"\\"+newpath+"\\"+"Pre"+"\\"+"\n")
    VNAFile.write("FoldertoAdd"+"\\"+newpath+"\\"+"Meas"+"\\"+"\n")
#    if not os.path.exists(newpath):
#        os.makedirs(newpath)
  
    shutil.copytree('RefFileMeas\Add',newpath)
    os.chdir(newpath)
    
    for i in range(-25,7,1):
#        Folder="5to9Ghz/"
        Power="%sdBm/"%i
        Power1="%sdBm"%i
        if not os.path.exists(Power):
            os.makedirs(Power)
#        print(Date)
            
            
#        shutil.copy('\\sti1files.epfl.ch\lmgn\bamgaert\VNA\20200227_KB-BE2-11-23\Switching10mT\RefFileMeas\calibration.txt', '\\sti1files.epfl.ch\lmgn\bamgaert\VNA\20200227_KB-BE2-11-23\Switching10mT\newpath\power')
#        shutil.copy('\sti1files.epfl.ch\lmgn\bamgaert\VNA\20200227_KB-BE2-11-23\Switching10mT\RefFileMeas\measurement.txt', '\\sti1files.epfl.ch\lmgn\bamgaert\VNA\20200227_KB-BE2-11-23\Switching10mT\newpath\power')
        shutil.copy('..\RefFileMeas\set_vna.txt', Power)
        shutil.copy('..\RefFileMeas\calibration.txt', Power)
        shutil.copy('..\RefFileMeas\measurement.txt', Power)
        
        VNAFile.write("FoldertoAdd"+"\\"+newpath+"\\"+Power1+"\\"+"\n")
        VNAFile.write("FoldertoAdd"+"\\"+newpath+"\\"+"Meas"+"\\"+"\n")
#        save(Power+'set_vna.txt', VNAFile)
#        VNAFile.write(Power+'set_vna.txt') 
        
        File="set_vna"
        
        name = "%s%s.txt" %(Power,File)
        
        
        #pattern =  "start frequency: 2.5e9;"
        #
        #subst  =  "start frequency: 1.5e9;"
        
        pattern =  "start frequency: 1.5e9;"
        pattern1 =  "stop frequency: 2e9;"
        pattern2 = "power level: -15;"
        
        subst  =  "start frequency: %se9;"%str(round(StartFreq,2 ))
        subst1  =  "stop frequency: %se9;"%str(round(StartFreq+Step,2))
        subst2  =  "power level: %s;"%str(int(i))
        
        fin = open(name, "rt")
        data = fin.read()
        data = data.replace(pattern,subst)
        data = data.replace(pattern1,subst1)
        data = data.replace(pattern2,subst2)
        fin.close()
        
        fin = open(name, "wt")
        fin.write(data)
        fin.close()
    os.chdir('..')   
    VNAFile.write("FoldertoAdd"+"\\"+newpath+"\\"+"After"+"\\"+"\n")
    StartFreq  =  StartFreq + Step




VNAFile.close()




