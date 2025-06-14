#FILTERING FOR ALL CHANNELS AND STORING RESULTS FOR LATER ACCESS

import numpy as np
import netCDF4
import glob
import os
import re
import sys
import matplotlib.pyplot as plt


np.set_printoptions(threshold=sys.maxsize)


path = os.path.expanduser("~/Documents/POES_Data_S3")

ifiles_00 = sorted(glob.glob(os.path.join(path, "POES_combinedSpectrum_m02_00_*.nc")))
ifiles_90 = sorted(glob.glob(os.path.join(path, "POES_combinedSpectrum_m02_90_*.nc")))

if not ifiles_00 or not ifiles_90:
    print("Error: No NetCDF files found. Check path and patterns.")
    print(f"Path searched: {path}")
    exit()

if len(ifiles_00) != len(ifiles_90):
    print(f"Warning: Mismatch in file counts: {len(ifiles_00)} (00deg) vs {len(ifiles_90)} (90deg).")
    print("Processing pairs based on sorted order. Ensure files correspond correctly.")

# --- Dictionary to store processed flag_and_time_arrays ---
processed_data_arrays = {}

for i, (file_00_path, file_90_path) in enumerate(zip(ifiles_00, ifiles_90), start=1):
    print(f"Processing File Pair {i}:")
    print(f"  00-degree file: {os.path.basename(file_00_path)}")
    print(f"  90-degree file: {os.path.basename(file_90_path)}")


    # Searches file path for the date and saves it to a string array for the output filename

    filepath = file_00_path
    pattern = r"\d{8}"  # match phone number format
    
    result = re.search(pattern, filepath)  # search pattern
    
    if result:
        Filename_start_index = result.start()  # match start index
        filename_for_output = file_00_path[Filename_start_index:Filename_start_index+8]
    else:
        print("Filename Issue")

    try:
        with netCDF4.Dataset(file_00_path) as d0, netCDF4.Dataset(file_90_path) as d9:
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

    if EOcounts_corrected00.ndim == 1:
        num_channels = 1
    elif EOcounts_corrected00.ndim > 1:
        num_channels = EOcounts_corrected00.shape[1]
        if EOcounts_corrected90.ndim <= 1 or EOcounts_corrected90.shape[1] != num_channels:
            print(f"  Error: Mismatch in number of channels or dimensions between 00-deg and 90-deg files for pair {i}.")
            print(f"  00-deg shape: {EOcounts_corrected00.shape}, 90-deg shape: {EOcounts_corrected90.shape}")
            print("-" * 40)
            continue
    else:
        print(f"  Error: Unexpected dimensions for EOcounts_corrected in 00-deg file for pair {i}. Shape: {EOcounts_corrected00.shape}")
        print("-" * 40)
        continue

    lshell_index = np.where(lshell > 5)

    if not np.any(lshell_index):
        print(f"  File Pair {i}: No data points found with L > 5 (applies to all channels).")
        print("-" * 40)
        continue

    new_rtime = rtime[lshell_index]
    
    new_lshell = lshell[lshell_index]


    if new_rtime.size == 0:
        print(f"  File Pair {i}: No data points remain after L > 5 filtering for time alignment (applies to all channels). Skipping.")
        print("-" * 40)
        continue


                        
    all_counts_00_filtered = []  # Initialize an empty list
    all_counts_90_filtered = []
    
    all_flagfilter = []

    for channel_idx in range(num_channels):
        print(f"\n  --- Processing Energy Channel {channel_idx} ---")

        if num_channels == 1 and EOcounts_corrected00.ndim == 1:
            current_counts_00 = EOcounts_corrected00
            current_counts_90 = EOcounts_corrected90
        else:
            current_counts_00 = EOcounts_corrected00[:, channel_idx]
            current_counts_90 = EOcounts_corrected90[:, channel_idx]
        
        counts_00_filtered = current_counts_00[lshell_index]
        counts_90_filtered = current_counts_90[lshell_index]
       
        all_counts_00_filtered.append(counts_00_filtered)
        all_counts_90_filtered.append(counts_90_filtered)

        
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio_00_over_90 = counts_00_filtered/counts_90_filtered
            event_flags = (ratio_00_over_90 > 2).astype(int)
        if event_flags.size > 0 and new_rtime.size > 0 and event_flags.size == new_rtime.size:
            timeflag = np.column_stack((event_flags, new_rtime))
            # --- Store the array instead of printing it fully ---
            processed_data_arrays[(i, channel_idx)] = timeflag
            print(f"    Data for Channel {channel_idx} (Pair {i}) processed and stored.")
        else:
            print(f"    Skipping Channel {channel_idx} for File Pair {i} due to empty or mismatched arrays after filtering.")
            print(f"    event_flags size: {event_flags.size}, relative_times_filtered size: {new_rtime.size}")
            continue # Skip to the next channel if data is problematic for stacking
        
        all_flagfilter.append(event_flags)

        num_condition_met = np.sum(event_flags)
        print(f"    Number of instances for Channel {channel_idx} where 00deg_counts / 90deg_counts > 2 (L > 5): {num_condition_met}")
        print(f"    Total data points for Channel {channel_idx} after L > 5 filtering: {len(event_flags)}")


        from netcdf_writer import netcdf_writer
        netcdf_writer(new_rtime, timeflag, ratio_00_over_90, counts_00_filtered, counts_90_filtered, filename_for_output)

    EOcounts_sorted00 = np.vstack(all_counts_00_filtered).T
    EOcounts_sorted90 = np.vstack(all_counts_90_filtered).T
    flagger = np.vstack(all_flagfilter).T      
    
    flagfilter1 = np.where(flagger[:,0] < 1)
    flagfilter2 = np.where(flagger[:,1] < 1)
    flagfilter3 = np.where(flagger[:,2] < 1)
    flagfilter4 = np.where(flagger[:,3] < 1)

    
    rtimefilter1 = rtime[flagfilter1]
    rtimefilter2 = rtime[flagfilter2]
    rtimefilter3 = rtime[flagfilter3]
    rtimefilter4 = rtime[flagfilter4]

    lshell1_filtered = new_lshell[flagfilter1]
    lshell2_filtered = new_lshell[flagfilter2]
    lshell3_filtered = new_lshell[flagfilter3]
    lshell4_filtered = new_lshell[flagfilter4]
    
#==================================Filtered Plots================================
    
    plt.scatter(lshell1_filtered,EOcounts_sorted00[flagfilter1,0],s=2,label = "E1 - $00°$")
    plt.scatter(lshell2_filtered,EOcounts_sorted00[flagfilter2,1],s=2,label = "E2 - $00°$")
    plt.scatter(lshell3_filtered,EOcounts_sorted00[flagfilter3,2],s=2,label = "E3 - $00°$")
    plt.scatter(lshell4_filtered,EOcounts_sorted00[flagfilter4,3],s=2,label = "E4 - $00°$")
    
    plt.title('EOcounts vs Lshell (Filtered)')
    plt.minorticks_on()
    plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
    plt.grid(which='minor',linestyle='--',alpha=0.5)
    plt.xlabel('LShell')
    plt.ylabel('EOCounts')
    plt.legend()
    plt.show()
    
    plt.scatter(lshell1_filtered,EOcounts_sorted90[flagfilter1,0],s=2,label = "E1 - $90°$")
    plt.scatter(lshell2_filtered,EOcounts_sorted90[flagfilter2,1],s=2,label = "E2 - $90°$")
    plt.scatter(lshell3_filtered,EOcounts_sorted90[flagfilter3,2],s=2,label = "E3 - $90°$")
    plt.scatter(lshell4_filtered,EOcounts_sorted90[flagfilter4,3],s=2,label = "E4 - $90°$")
    
    plt.title('EOcounts vs Lshell (Filtered)')
    plt.minorticks_on()
    plt.grid(which='major',linestyle='-',alpha=0.8)   # add a grid to the major ticks
    plt.grid(which='minor',linestyle='--',alpha=0.5)
    plt.xlabel('LShell')
    plt.ylabel('EOCounts')
    plt.legend()
    plt.show()                   
        
    print("-" * 40)

print("Processing complete.")

print("\n" + "="*50)
print("ACCESSING STORED DATA EXAMPLE")
print("="*50)

example_pair_to_access = 1
example_channel_to_access = 0
data_key = (example_pair_to_access, example_channel_to_access)

if data_key in processed_data_arrays:
    print(f"\nAccessing stored data for File Pair {example_pair_to_access}, Channel {example_channel_to_access}:")
    retrieved_array = processed_data_arrays[data_key]
    print(f"  Array shape: {retrieved_array.shape}")
    print(f"  First 5 rows of the array:\n{retrieved_array[:5, :]}")
    
else:
    print(f"\nNo data found or stored for File Pair {example_pair_to_access}, Channel {example_channel_to_access}.")
    print("This could be due to an error during its processing, or no data points meeting the criteria.")

print("\nAvailable keys in processed_data_arrays:")
if processed_data_arrays:
    for key in processed_data_arrays.keys():
        print(f"  {key} -> array shape: {processed_data_arrays[key].shape}")
else:
    print("  No data was stored.")
