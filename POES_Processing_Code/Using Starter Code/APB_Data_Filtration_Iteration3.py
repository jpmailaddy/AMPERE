#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:29:20 2025

@author: Home
"""


import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import glob




np.set_printoptions(threshold=sys.maxsize)
ifiles00 = sorted(glob.glob(os.path.expanduser("~/Documents/POES_Data_S3/POES_combinedSpectrum_m02_00_*.nc")))
ifiles90 = sorted(glob.glob(os.path.expanduser("~/Documents/POES_Data_S3/POES_combinedSpectrum_m02_90_*.nc")))


for itime in range(0, len(ifiles00)):

#======================================EOCounts==================================
    
    file2read00 = netCDF4.Dataset(ifiles00[itime],'r')
    lshell00 = np.array(file2read00.variables['lValue'])
    time00 = np.array(file2read00.variables['rtime'])
    EOcounts_corrected00 = np.array(file2read00.variables['EOcounts_corrected'])
    
    file2read90 = netCDF4.Dataset(ifiles90[itime],'r')
    lshell90 = np.array(file2read90.variables['lValue'])
    time90 = np.array(file2read90.variables['rtime'])    
    EOcounts_corrected90 = np.array(file2read90.variables['EOcounts_corrected'])

#=======================================LShells==================================
    
    lshell_index00 = np.where(lshell00>5)
    lshell_index00 = np.array(lshell_index00)
    
    lshell_index90 = np.where(lshell90>5)
    lshell_index90 = np.array(lshell_index90)
    time00_s = (time00)*3600
    time90_s = (time90)*3600    

#==================================LShell Index Sort=============================

    new_lshell00 = lshell00[lshell_index00]
    new_lshell90 = lshell90[lshell_index90]

    new_time_array00 = time00_s[lshell_index00]
    new_time_array90 = time90_s[lshell_index90]
    nta00c = (new_time_array00 - new_time_array00[0,0])


    new_EOcounts_array00 = np.array(EOcounts_corrected00[lshell_index00])
    new_EOcounts_array90 = np.array(EOcounts_corrected90[lshell_index90])

#==============================EOcount Void Data Sort============================

    how_many_less_than1 = np.where(new_EOcounts_array00[0,:,0]/new_EOcounts_array90[0,:,0] < 2)
    how_many_less_than2 = np.where(new_EOcounts_array00[0,:,1]/new_EOcounts_array90[0,:,1] < 2)
    how_many_less_than3 = np.where(new_EOcounts_array00[0,:,2]/new_EOcounts_array90[0,:,2] < 2)
    how_many_less_than4 = np.where(new_EOcounts_array00[0,:,3]/new_EOcounts_array90[0,:,3] < 2)
   
    hmlt1 = np.array(how_many_less_than1)
    hmlt2 = np.array(how_many_less_than2)
    hmlt3 = np.array(how_many_less_than3)
    hmlt4 = np.array(how_many_less_than4)

    EOcounts1_filtered00 = new_EOcounts_array00[0,hmlt1[:],0]
    EOcounts2_filtered00 = new_EOcounts_array00[0,hmlt2[:],1]
    EOcounts3_filtered00 = new_EOcounts_array00[0,hmlt3[:],2]
    EOcounts4_filtered00 = new_EOcounts_array00[0,hmlt4[:],3]


    EOcounts1_filtered90 = new_EOcounts_array90[0,hmlt1[:],0]
    EOcounts2_filtered90 = new_EOcounts_array90[0,hmlt2[:],1]
    EOcounts3_filtered90 = new_EOcounts_array90[0,hmlt3[:],2]
    EOcounts4_filtered90 = new_EOcounts_array90[0,hmlt4[:],3]
    
    lshell1_filtered00 = new_lshell00[0,hmlt1[:]]
    lshell2_filtered00 = new_lshell00[0,hmlt2[:]]
    lshell3_filtered00 = new_lshell00[0,hmlt3[:]]
    lshell4_filtered00 = new_lshell00[0,hmlt4[:]]

    lshell1_filtered90 = new_lshell90[0,hmlt1[:]]
    lshell2_filtered90 = new_lshell90[0,hmlt2[:]]
    lshell3_filtered90 = new_lshell90[0,hmlt3[:]]
    lshell4_filtered90 = new_lshell90[0,hmlt4[:]]

#=======================================Plots====================================

plt.scatter(new_lshell00,new_EOcounts_array00[0,:,0],s=2,label = "E1 - $00°$")
plt.scatter(new_lshell00,new_EOcounts_array00[0,:,1],s=2,label = "E2 - $00°$")
plt.scatter(new_lshell00,new_EOcounts_array00[0,:,2],s=2,label = "E3 - $00°$")
plt.scatter(new_lshell00,new_EOcounts_array00[0,:,3],s=2,label = "E4 - $00°$")

plt.title('EOcounts vs Lshell (Corrected)')
plt.minorticks_on()
plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
plt.grid(which='minor',linestyle='--',alpha=0.5)
plt.xlabel('LShell')
plt.ylabel('EOCounts')
plt.legend()
plt.show()

plt.scatter(new_lshell90,new_EOcounts_array90[0,:,0],s=2,label = "E1 - $90°$")
plt.scatter(new_lshell90,new_EOcounts_array90[0,:,1],s=2,label = "E2 - $90°$")
plt.scatter(new_lshell90,new_EOcounts_array90[0,:,2],s=2,label = "E3 - $90°$")
plt.scatter(new_lshell90,new_EOcounts_array90[0,:,3],s=2,label = "E4 - $90°$")

plt.title('EOcounts vs Lshell (Corrected)')
plt.minorticks_on()
plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
plt.grid(which='minor',linestyle='--',alpha=0.5)
plt.xlabel('LShell')
plt.ylabel('EOCounts')
plt.legend()
plt.show()

#==================================Filtered Plots================================

plt.scatter(lshell1_filtered00,EOcounts1_filtered00,s=2,label = "E1 - $00°$")
plt.scatter(lshell2_filtered00,EOcounts2_filtered00,s=2,label = "E2 - $00°$")
plt.scatter(lshell3_filtered00,EOcounts3_filtered00,s=2,label = "E3 - $00°$")
plt.scatter(lshell4_filtered00,EOcounts4_filtered00,s=2,label = "E4 - $00°$")

plt.title('EOcounts vs Lshell (Filtered)')
plt.minorticks_on()
plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
plt.grid(which='minor',linestyle='--',alpha=0.5)
plt.xlabel('LShell')
plt.ylabel('EOCounts')
plt.legend()
plt.show()

plt.scatter(lshell1_filtered90,EOcounts1_filtered90,s=2,label = "E1 - $90°$")
plt.scatter(lshell2_filtered90,EOcounts2_filtered90,s=2,label = "E2 - $90°$")
plt.scatter(lshell3_filtered90,EOcounts3_filtered90,s=2,label = "E3 - $90°$")
plt.scatter(lshell4_filtered90,EOcounts4_filtered90,s=2,label = "E4 - $90°$")

plt.title('EOcounts vs Lshell (Filtered)')
plt.minorticks_on()
plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
plt.grid(which='minor',linestyle='--',alpha=0.5)
plt.xlabel('LShell')
plt.ylabel('EOCounts')
plt.legend()
plt.show()
