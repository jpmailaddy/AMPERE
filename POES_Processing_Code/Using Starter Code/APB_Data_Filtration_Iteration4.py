#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 22:29:57 2025

@author: Home
"""

import numpy as np
import netCDF4 
import glob
import os
import sys
import matplotlib.pyplot as plt



np.set_printoptions(threshold=sys.maxsize)
ifiles00 = sorted(glob.glob(os.path.expanduser("~/Documents/POES_Data_S2/POES_combinedSpectrum_n19_00_*.nc")))
ifiles90 = sorted(glob.glob(os.path.expanduser("~/Documents/POES_Data_S2/POES_combinedSpectrum_n19_90_*.nc")))

if not ifiles00 or not ifiles90:
    print(f"Error: No NetCDF files found. Check path and patterns.")
    exit()

if len(ifiles00) != len(ifiles90):
    print(f"Warning: Mismatch in file counts: {len(ifiles00)} (00deg) vs {len(ifiles90)} (90deg).")
    print("Processing pairs based on sorted order. Ensure files correspond correctly.")

for i, (file00_path, file90_path) in enumerate(zip(ifiles00, ifiles90), start=1):
    print(f"Processing File Pair {i}:")
    print(f"  00-degree file: {os.path.basename(file00_path)}")
    print(f"  90-degree file: {os.path.basename(file90_path)}")

    try:
        with netCDF4.Dataset(file00_path) as d0, netCDF4.Dataset(file90_path) as d9:
            lshell = d0.variables['lValue'][:]
            rtime = d0.variables['rtime'][:]
           
            EOcounts_corrected00 = d0.variables['EOcounts_corrected'][:]
            EOcounts_corrected90 = d9.variables['EOcounts_corrected'][:]


    except FileNotFoundError:
        print(f"  Error: One or both files in pair {i} not found. Skipping.")
        print("-" * 40)
        continue
    except KeyError as e:
        print(f"  Error: Variable {e} not found in one of the files. Skipping pair {i}.")
        print("-" * 40)
        continue
    except Exception as e:
        print(f"  An unexpected error occurred while reading files: {e}. Skipping pair {i}.")
        print("-" * 40)
        continue

    lshell_index = np.where(lshell > 5)

    if not np.any(lshell_index):
        print(f"  File Pair {i}: No data points found with L > 5.")
        print("-" * 40)
        continue

    new_rtime = rtime[lshell_index]
    
    new_lshell = lshell[lshell_index]

    counts_00_filtered = EOcounts_corrected00[lshell_index]
    counts_90_filtered = EOcounts_corrected90[lshell_index]


    if new_rtime.size == 0:
        print(f"  File Pair {i}: No data points remain after L > 5 filtering for time alignment. Skipping.")
        print("-" * 40)
        continue

    flagger1 = (counts_00_filtered[:,0]/counts_90_filtered[:,0] > 2).astype(int)
    flagger2 = (counts_00_filtered[:,1]/counts_90_filtered[:,1] > 2).astype(int)
    flagger3 = (counts_00_filtered[:,2]/counts_90_filtered[:,2] > 2).astype(int)
    flagger4 = (counts_00_filtered[:,3]/counts_90_filtered[:,3] > 2).astype(int)

    timeflag1 = np.column_stack((flagger1, new_rtime))
    timeflag2 = np.column_stack((flagger2, new_rtime))
    timeflag3 = np.column_stack((flagger3, new_rtime))
    timeflag4 = np.column_stack((flagger4, new_rtime))

    flagfilter1 = np.where(flagger1 < 1)
    flagfilter2 = np.where(flagger2 < 1)
    flagfilter3 = np.where(flagger3 < 1)
    flagfilter4 = np.where(flagger4 < 1)


    nflag1 = flagger1[flagfilter1]
    nflag2 = flagger1[flagfilter2]
    nflag3 = flagger1[flagfilter3]
    nflag4 = flagger1[flagfilter4]
    
    rtimefilter1 = rtime[flagfilter1]
    rtimefilter2 = rtime[flagfilter2]
    rtimefilter3 = rtime[flagfilter3]
    rtimefilter4 = rtime[flagfilter4]

    lshell1_filtered = new_lshell[flagfilter1]
    lshell2_filtered = new_lshell[flagfilter2]
    lshell3_filtered = new_lshell[flagfilter3]
    lshell4_filtered = new_lshell[flagfilter4]

    print("  Flag and Time array (Flag=1 if 00deg_counts/90deg_counts > 2, for L > 5):")
    print(timeflag1)

    instances1 = np.sum(flagger1)
    instances2 = np.sum(flagger2)
    instances3 = np.sum(flagger3)
    instances4 = np.sum(flagger4)
    instances_all = np.sum(flagger1 + flagger2 + flagger3 + flagger4)    
    
    
    
    print(f"  Number of instances in R1 where 00deg_counts > 90deg_counts (L > 5): {instances1}")
    print(f"  Number of instances in R2 where 00deg_counts > 90deg_counts (L > 5): {instances2}")
    print(f"  Number of instances in R3 where 00deg_counts > 90deg_counts (L > 5): {instances3}")
    print(f"  Number of instances in R4 where 00deg_counts > 90deg_counts (L > 5): {instances4}")
    print(f"  Total number of instances where 00deg_counts > 90deg_counts (L > 5): {instances_all}")

    
    
    print(f"  Total data points after L > 5 filtering: {len(flagger1)}")

    
    print("-" * 40)
    
#==================================Filtered Plots================================
    
    plt.scatter(lshell1_filtered,counts_00_filtered[flagfilter1,0],s=2,label = "E1 - $00°$")
    plt.scatter(lshell2_filtered,counts_00_filtered[flagfilter2,1],s=2,label = "E2 - $00°$")
    plt.scatter(lshell3_filtered,counts_00_filtered[flagfilter3,2],s=2,label = "E3 - $00°$")
    plt.scatter(lshell4_filtered,counts_00_filtered[flagfilter4,3],s=2,label = "E4 - $00°$")
    
    plt.title('EOcounts vs Lshell (Filtered)')
    plt.minorticks_on()
    plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
    plt.grid(which='minor',linestyle='--',alpha=0.5)
    plt.xlabel('LShell')
    plt.ylabel('EOCounts')
    plt.legend()
    plt.show()
    
    plt.scatter(lshell1_filtered,counts_90_filtered[flagfilter1,0],s=2,label = "E1 - $90°$")
    plt.scatter(lshell2_filtered,counts_90_filtered[flagfilter2,1],s=2,label = "E2 - $90°$")
    plt.scatter(lshell3_filtered,counts_90_filtered[flagfilter3,2],s=2,label = "E3 - $90°$")
    plt.scatter(lshell4_filtered,counts_90_filtered[flagfilter4,3],s=2,label = "E4 - $90°$")
    
    plt.title('EOcounts vs Lshell (Filtered)')
    plt.minorticks_on()
    plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
    plt.grid(which='minor',linestyle='--',alpha=0.5)
    plt.xlabel('LShell')
    plt.ylabel('EOCounts')
    plt.legend()
    plt.show()    

print("Processing complete.")