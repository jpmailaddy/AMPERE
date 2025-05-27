#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:41:26 2025


@author: jmpettit
"""

def netcdf_writer(relative_times_filtered, flag_and_time_array, ratio_00_over_90, counts_00_filtered, counts_90_filtered, filename_for_output):

    from netCDF4 import Dataset
    
    
    POES_Flagged_file = Dataset(filename_for_output+".nc4", 'w', format='NETCDF4')
    POES_Flagged_file.description = 'Flagged MEPED data'
                            
    
    
    # Dimensions of the file
    
    POES_Flagged_file.createDimension('rtime', None)
    POES_Flagged_file.createDimension('detector', 2)
    
    # create variables
    
    rtime = POES_Flagged_file.createVariable('rtime', 'f8', ('rtime'))
    rtime.long_name = "universal time (in decimal hour)"
    
    ratio = POES_Flagged_file.createVariable('ratio', 'f8', ('rtime'))
    ratio.long_name = "Ratio of the 0 and 90 degree detectors"
    
    zero = POES_Flagged_file.createVariable('00_Counts', 'f8', ('rtime'))
    zero.long_name = "Filtered 0 degree count rates"

    ninety = POES_Flagged_file.createVariable('90_Counts', 'f8', ('rtime'))
    ninety.long_name = "Filtered 90 degree count rates"
    
    flagged_array = POES_Flagged_file.createVariable('Flagged', 'f8', ('rtime', 'detector'))
    flagged_array.long_name = "Flagged array with time stamp"


    # fill variables

    rtime[:] = relative_times_filtered
    ratio[:] = ratio_00_over_90
    zero[:] = counts_00_filtered
    ninety[:] = counts_90_filtered
    flagged_array[:, :] = flag_and_time_array
    
    POES_Flagged_file.close