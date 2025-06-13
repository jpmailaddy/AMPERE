import numpy as np
import netCDF4
import glob
import os
import re

sat = 'n15'
input_dir = 'C:/Users/username/Desktop/POES_Files/'
detector = '00'

path = os.path.expanduser(input_dir)
ifiles_00 = sorted(glob.glob(os.path.join(path, "POES_combinedSpectrum_"+sat+detector+".nc")))

for iday in range(0, len(ifiles_00)):

    # Searches file path for the date and saves it to a string array for the output filename

    filepath = file_00_path
    pattern = r"\d{8}"  # match number format
    result = re.search(pattern, filepath)  # search pattern
    
    if result:
        Filename_start_index = result.start()  # match start index
        filename_for_output = file_00_path[Filename_start_index:Filename_start_index+8]
    else:
        print("Filename Issue")


  #  read code for each netcdf file

    sub sampling logic 

    useful_time = rtime*60.  # 60 minutes in an hour (0 - 1440)  rtime (0-24)

    ii = 0   # first minute
    kk = 1   # second minute

    eocounts_corrected[4, 5400]    # 5400 --> rtime  useful_time array [5400] --> 0 -1440

    for itime in range (0, len(rtime)):
        sub_sample_index = where(useful_time ge ii and useful_time lt kk)

        temp_array = eocounts_corrected[:, sub_sample_index]  # -> [4, 3] 

        if np.size(temp_array) lt 1 
            median = -999 #flag value
            mean = -999 #flag value
        else:
            for k in range(0, 4)
                median_counts = np.median(temp_array[k, :]
                mean_counts = np.mean(temp_array[k, :]

      # Concantenate mean_couunts, median_counts into a total array

        if itime eq 0:
            median_counts_total = median_counts
            mean_counts_total = mean_counts
        if itime ne 0:
            median_counts_total = [[median_counts_total], [median_counts]]  
            mean_counts_total = [[mean_counts_total], [mean_counts]]  
            
        ii = ii + 1 # increase first minute
        kk = kk + 1 # increase second minute

    # Netcdf output code that saves the median_counts_total, mean_counts_total, lshell?, mlt?, geographic?
    
        filename_for_output = netcdf_file
    
