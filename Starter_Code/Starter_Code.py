# Code to get everyone started

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import netCDF4
import glob

ifiles = glob.glob("C:/Directory_where_files_exist/*.nc")

for itime in range(0, 10):

    file2read = netCDF4.Dataset(ifiles[itime]),'r')

    var = file2read.variables['MLT']
    MLT = np.array(var)
    var = file2read.variables['lValue']
    lshell = np.array(var)
    var = file2read.variables['EOcounts_corrected']
    EOcounts = np.array(var)

plt.plot(EOcounts[150, :])
    
