# Code to get everyone started

import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import glob

ifiles_00 = glob.glob("E:/POES_Data/No_Noise_Floor/Level_1_MPE/NOAA15/POES_combinedSpectrum_n15_00_*.nc")
ifiles_90 = glob.glob("E:/POES_Data/No_Noise_Floor/Level_1_MPE/NOAA15/POES_combinedSpectrum_n15_90_*.nc")

for itime in range(0, 10):
          
    file2read = netCDF4.Dataset(ifiles_00[itime],'r')
    
    var = file2read.variables['MLT'] # var can be 'Theta', 'S', 'V', 'U' etc..
    MLT = np.array(var)
    var = file2read.variables['lValue']
    lshell = np.array(var)
    var = file2read.variables['EOcounts_corrected']
    EOcounts_corrected = np.array(var)
   
    
    file2read90 = netCDF4.Dataset(ifiles_90[itime],'r')

    var = file2read90.variables['EOcounts_corrected']
    EOcounts_corrected90 = np.array(var)

    lshell_index = np.where(lshell > 5)
    lshell_index = np.array(lshell_index)
    new_electron_count_array = EOcounts_corrected[lshell_index[0,:], 0]
    new_electron_count_array90 = EOcounts_corrected90[lshell_index[0,:], 0]
    
    # This counts how many times the 90 degree counts are less than 00 degree counts at lshell > 5 
    how_many_less_than = np.where(new_electron_count_array90/new_electron_count_array < 1)
