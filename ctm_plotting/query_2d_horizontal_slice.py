#!/usr/bin/env python
#
#  query_2d_horizontal_slice.py
#

from pyctm import init_ctm, check_inbounds_values, test_plot, write_csv_output

### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
import argparse

## query the model along a horizontal slice at fixed depth
#  - inputs: start longitude and latitude, end longitude and latitude, slice depth; optional plotting
#  - returns: DataFrame with temperature at these points; optional figure
def query_2D_horizontal_slice(lat_start, lon_start, lat_end, lon_end, z_slice, modelname, modelpath, plot = False):
    
    # initialize dataset
    xdata = init_ctm(modelname, modelpath)

    # Boyd (2019) model does not start at the surface (depth = 0 meter). Here I have to extrapolate to get the surface temperature.
    if modelname == 'Boyd_2019':
        surface = np.insert(xdata['depth[m]'].values, 0, 0)
        xdata = xdata.interp({'depth[m]': surface}, method = 'linear', kwargs = {'fill_value': 'extrapolate'})

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon_start, lon_end], 
                                  "latitude[°]": [lat_start, lat_end], 
                                  "depth[m]": [z_slice]})
    
    # Define longitude and latitude arrays for the slice sample
    lon_range = np.abs(lon_end - lon_start)
    lat_range = np.abs(lat_end - lat_start)

    # Spaing in degree
    space_deg = np.sqrt((lon_range * lat_range) / 10000)

    nlon = int(np.ceil(lon_range / space_deg) + 1) 
    nlat = int(np.ceil(lat_range / space_deg) + 1)
    
    lon_vals = np.linspace(lon_start, lon_end, nlon)
    lat_vals = np.linspace(lat_start, lat_end, nlat)

    # sample the horizontal slice at fixed depth
    xi = xdata.interp({"longitude[°]": lon_vals, "latitude[°]": lat_vals, "depth[m]": z_slice})

    # define dataframe to return
    df = xi.to_dataframe().reset_index()
    df = df[["longitude[°]", "latitude[°]", "depth[m]", "temperature[°C]"]]

    # return
    if plot: # optional plot
        fig = test_plot(xi, "2D_horizontal")
        return df, fig
    else:
        return df

# Make a function to allow batch mode
def call_func():
    
    par = argparse.ArgumentParser()
    par.add_argument('--lat_start', type = float, required = True)    # Add argument of starting latitude (°)
    par.add_argument('--lon_start', type = float, required = True)    # Add argument of starting longitude (°)
    par.add_argument('--lat_end', type = float, required = True)      # Add argument of ending latitude (°)
    par.add_argument('--lon_end', type = float, required = True)      # Add argument of ending longitude (°)
    par.add_argument('--z', type = float, required = True)            # Add arugment of depth (m)
    par.add_argument('--modelname', type = str, required = True)      # Add argument of model name: Lee_2025 or Shinevar_2018
    par.add_argument('--modelpath', type = str, required = True)      # Add argument of input model path
    par.add_argument('--outpath', type = str, required = True)        # Add argument of output file path and file name
    
    args = par.parse_args()                                           # Extract arguments
    
    # Call the function
    df = query_2D_horizontal_slice(
         args.lat_start,
         args.lon_start,
         args.lat_end,
         args.lon_end,
         args.z,
         args.modelname,
         args.modelpath)

    df.drop(columns = ['depth[m]'], inplace = True)

    # Rename columns
    rename = {'longitude[°]': '# Lon',
              'latitude[°]': 'Lat',
              'temperature[°C]': 'Temperature(°C)'}
    
    df = df.rename(columns = rename)

    tmp = args.outpath[:]
    final_outpath = tmp.replace('data','data_final')
    write_csv_output(df, final_outpath, '2D_horizontal', args.modelname, z = args.z)    

    # Add dummy columns
    df[['dummy1', 'dummy2']] = np.nan

    # Call the function to write the output csv file
    write_csv_output(df, args.outpath, '2D_horizontal', args.modelname, z = args.z)    

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    # Call the query function
    call_func()
