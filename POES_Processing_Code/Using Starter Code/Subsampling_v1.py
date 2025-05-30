import numpy as np
import netCDF4
import glob
import os
import re

sat = 'n15'
input_dir = ''

path = os.path.expanduser(input_dir)
ifiles_00 = sorted(glob.glob(os.path.join(path, "POES_combinedSpectrum_"+sat+"_00_*.nc")))

for in range(0, len(ifiles_00)):

    # Searches file path for the date and saves it to a string array for the output filename

    filepath = file_00_path
    pattern = r"\d{8}"  # match number format
    result = re.search(pattern, filepath)  # search pattern
    
    if result:
        Filename_start_index = result.start()  # match start index
        filename_for_output = file_00_path[Filename_start_index:Filename_start_index+8]
    else:
        print("Filename Issue")


    read code for each netcdf file

    sub sampling logic 

    useful_time = rtime*60.  # 60 minutes in an hour ( 0 - 1440)

    ii = 0 
    kk = 1

    for in range (0, 1440):
      if useful_time[itime] ge ii and lt kk:

         temp_array = eocounts_corrected[]

        if np.size(temp_array) lt 1 
            median = -99 #flag value
            mean = -99 #flag value

        median = count rates over each minutes
        mean = count rates each minutes

      ii = ii + 1
      kk = kk + 1


    
